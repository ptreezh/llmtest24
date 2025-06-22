# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from datetime import datetime
import platform
from concurrent.futures import ProcessPoolExecutor, as_completed
import glob
import re

# --- 配置 ---
MODELS_FILE = "models.txt"
if platform.system().lower().startswith('win'):
    RUNNER_SCRIPT = "run_all_tests.py"
else:
    RUNNER_SCRIPT = "run_all_tests_u.py"
RESULTS_DIR = "benchmark_results"
MAX_WORKERS = 4  # 并发进程数，可根据CPU/内存调整


def get_local_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.splitlines()
        models = set()
        for line in lines:
            if not line.strip() or line.strip().startswith('NAME'):
                continue
            parts = line.split()
            if len(parts) < 1:
                continue
            model_name = parts[0]
            models.add(model_name)
        return models
    except Exception as e:
        print(f"[WARNING] 获取本地ollama模型列表失败: {e}")
        return set()


def safe_filename(name):
    """将模型名中的所有不适合做文件名的字符替换为下划线_"""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', name)


def run_single_benchmark(model_name):
    """为单个模型执行测试套件并保存结果"""
    # 检查模型是否本地存在
    if model_name not in get_local_ollama_models():
        print(f"[SKIP] 模型 {model_name} 本地不存在，已跳过。")
        return (model_name, None)
    # 替换模型名中的所有特殊字符，确保文件名安全
    safe_model_name = safe_filename(model_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(RESULTS_DIR, f"results_{safe_model_name}_{timestamp}.txt")
    print(f"\n{'='*60}")
    print(f">>> [BENCHMARK] Testing model: {model_name}")
    print(f">>> [BENCHMARK] Output will be saved to: {output_filename}")
    print(f"{'='*60}")
    command = [sys.executable, RUNNER_SCRIPT, "--model", model_name]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"Benchmark for model: {model_name}\n")
            f.write(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*40 + "\n\n")
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\n--- STDERR ---\n")
                f.write(result.stderr)
        print(f">>> [BENCHMARK] Successfully finished testing {model_name}.")
        return (model_name, True)
    except FileNotFoundError:
        print(f"[ERROR] Script '{RUNNER_SCRIPT}' not found. Make sure it's in the same directory.")
        return (model_name, False)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] An error occurred while running tests for model '{model_name}'.")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"!!! Benchmark FAILED for model: {model_name} !!!\n")
            f.write(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*40 + "\n\n")
            f.write("--- STDOUT ---\n")
            f.write(e.stdout)
            f.write("\n\n--- STDERR ---\n")
            f.write(e.stderr)
        print(f">>> [BENCHMARK] Error log saved to {output_filename}.")
        return (model_name, False)


def main():
    # 自动获取ollama模型列表并写入models.txt
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.splitlines()
        model_names = []
        model_info_list = []
        for line in lines:
            if not line.strip() or line.strip().startswith('NAME'):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            model_name = parts[0]
            size_str = parts[2].upper()
            if 'GB' in size_str:
                try:
                    size_gb = float(size_str.replace('GB','').strip())
                    if size_gb >= 1.0:
                        model_names.append(model_name)
                        model_info_list.append((model_name, size_gb))
                except:
                    continue
            elif 'MB' in size_str:
                try:
                    size_mb = float(size_str.replace('MB','').strip())
                    if size_mb >= 1024:
                        model_names.append(model_name)
                        model_info_list.append((model_name, size_mb/1024))
                except:
                    continue
        if model_names:
            with open(MODELS_FILE, 'w', encoding='utf-8') as f:
                for m in model_names:
                    f.write(m + '\n')
            print(f"[INFO] 已自动写入 {len(model_names)} 个模型到 {MODELS_FILE}")
        else:
            print("[WARNING] 未检测到任何ollama模型，models.txt未更新。")
    except Exception as e:
        print(f"[WARNING] 自动获取ollama模型列表失败: {e}")

    if not os.path.exists(RUNNER_SCRIPT):
        print(f"[ERROR] The main test script '{RUNNER_SCRIPT}' was not found.")
        print("Please make sure all original test suite files are in this directory.")
        sys.exit(1)

    if not os.path.exists(MODELS_FILE):
        print(f"[ERROR] The model list file '{MODELS_FILE}' was not found.")
        print("Please create it and add the names of the models you want to test, one per line.")
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(MODELS_FILE, 'r', encoding='utf-8') as f:
        models_to_test = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    if not models_to_test:
        print("[WARNING] No models found in 'models.txt'. Nothing to do.")
        sys.exit(0)
    print(f"--- Starting Parallel Benchmark for {len(models_to_test)} model(s) ---")
    success_count = 0
    fail_count = 0
    skip_count = 0
    results = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_model = {executor.submit(run_single_benchmark, model): model for model in models_to_test}
        for future in as_completed(future_to_model):
            model_name, result = future.result()
            results.append((model_name, result))
            if result is None:
                skip_count += 1
            elif result:
                success_count += 1
            else:
                fail_count += 1
    print(f"\n{'='*60}")
    print("--- Parallel Benchmark Suite Finished ---")
    print(f"Total models tested: {len(models_to_test)}")
    print(f"Successful runs: {success_count}")
    print(f"Failed runs: {fail_count}")
    print(f"Skipped (not found locally): {skip_count}")
    print(f"All results are saved in the '{RESULTS_DIR}' directory.")
    print(f"{'='*60}")
    # 汇总所有结果，生成HTML分析页面（与原脚本一致）
    try:
        summary_html = 'benchmark_summary.html'
        result_files = sorted(glob.glob(os.path.join(RESULTS_DIR, 'results_*.txt')))
        summary_rows = []
        for rf in result_files:
            with open(rf, 'r', encoding='utf-8') as f:
                content = f.read()
            m = re.search(r'Benchmark for model: (.+)', content)
            model_name = m.group(1) if m else os.path.basename(rf)
            m2 = re.search(r'Overall Score: ([\d\.]+)/10', content)
            score = m2.group(1) if m2 else 'N/A'
            m3 = re.search(r'Final Score & Conclusion\s*(.*?)\n?The ', content, re.DOTALL)
            conclusion = m3.group(1).strip().replace('\n',' ') if m3 else ''
            m4 = re.search(r'The (.+? model .+)', content)
            main_conclusion = m4.group(1) if m4 else ''
            summary_rows.append((model_name, score, conclusion, main_conclusion))
        with open(summary_html, 'w', encoding='utf-8') as f:
            if not summary_rows:
                f.write("""<html><body><h2>No valid benchmark results found. Please check your models and rerun the tests.</h2></body></html>""")
                print(f"[INFO] 汇总分析页面已生成: {summary_html} (无有效结果)")
                return
            f.write("""
<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Multi-Model Benchmark Summary</title>
<style>
body { font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }
h1 { text-align: center; }
table { border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 2px 8px #eee; }
th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
th { background: #f2f2f2; font-weight: bold; }
tr:nth-child(even) { background: #f9f9f9; }
tr:hover { background: #e6f7ff; }
.score { font-weight: bold; }
.conclusion { text-align: left; }
</style>
</head>
<body>
<h1>Multi-Model Benchmark Summary</h1>
<table>
<thead><tr><th>Model</th><th>Score</th><th>Conclusion</th><th>Main Conclusion</th></tr></thead>
<tbody>
""")
            for row in summary_rows:
                f.write(f"<tr><td>{row[0]}</td><td class='score'>{row[1]}</td><td class='conclusion'>{row[2]}</td><td class='conclusion'>{row[3]}</td></tr>\n")
            f.write("""
</tbody>
</table>

<!-- --- 单项排行榜和综合排行榜 --- -->
<!-- 解析每个模型的详细分项得分 -->
<!-- 读取每个模型的详细txt报告，提取各Pillar分数 -->
<h2>Per-Pillar Leaderboards</h2>
""")
            # 解析每个模型的详细分项得分
            # 读取每个模型的详细txt报告，提取各Pillar分数
            pillar_names = []
            model_scores = {}  # model_name: {pillar_idx: score, ...}
            for rf in result_files:
                with open(rf, 'r', encoding='utf-8') as f2:
                    content = f2.read()
                m = re.search(r'Benchmark for model: (.+)', content)
                model_name = m.group(1) if m else os.path.basename(rf)
                per_pillar = re.findall(r'^(\d+)\s+([\w\- &]+)\s+(\d+)/10', content, re.MULTILINE)
                if not pillar_names and per_pillar:
                    pillar_names = [p[1].strip() for p in per_pillar]
                model_scores[model_name] = {int(p[0]): int(p[2]) for p in per_pillar}
            per_pillar_ranking = []
            for idx, pname in enumerate(pillar_names, 1):
                scores = []
                for m in model_scores:
                    score = model_scores[m].get(idx, None)
                    scores.append((m, score))
                scores = [s for s in scores if s[1] is not None]
                scores.sort(key=lambda x: x[1], reverse=True)
                per_pillar_ranking.append((idx, pname, scores))
            total_scores = []
            for m in model_scores:
                s = sum([v for v in model_scores[m].values() if isinstance(v, int)])
                total_scores.append((m, s))
            total_scores.sort(key=lambda x: x[1], reverse=True)
            for idx, pname, scores in per_pillar_ranking:
                f.write(f"<h3>Pillar {idx}: {pname}</h3>\n<table><thead><tr><th>Rank</th><th>Model</th><th>Score</th></tr></thead><tbody>\n")
                for rank, (m, s) in enumerate(scores, 1):
                    color = '#d4edda' if s == 10 else ('#fff3cd' if s >= 7 else ('#f8d7da' if s <= 3 else ''))
                    f.write(f"<tr style='background:{color}'><td>{rank}</td><td>{m}</td><td><b>{s}</b></td></tr>\n")
                f.write("</tbody></table>\n")
            f.write("<h2>Overall Leaderboard</h2>\n<table><thead><tr><th>Rank</th><th>Model</th><th>Total Score</th></tr></thead><tbody>\n")
            for rank, (m, s) in enumerate(total_scores, 1):
                color = '#d4edda' if rank == 1 else ('#fff3cd' if rank == 2 else ('#d1ecf1' if rank == 3 else ''))
                f.write(f"<tr style='background:{color}'><td>{rank}</td><td>{m}</td><td><b>{s}</b></td></tr>\n")
            f.write("</tbody></table>\n")
            f.write("""
</body>
</html>
""")
        print(f"[INFO] 汇总分析页面已生成: {summary_html}")
    except Exception as e:
        print(f"[WARNING] 生成汇总HTML页面失败: {e}")

if __name__ == "__main__":
    main() 