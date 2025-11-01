import os
import re
import subprocess

MODEL_LIST_FILE = 'model_list.txt'
PILLAR_TESTS = [
    "test_pillar_01_logic.py", "test_pillar_02_instruction.py", "test_pillar_03_structural.py",
    "test_pillar_04_long_context.py", "test_pillar_05_domain_knowledge.py", "test_pillar_06_tool_use.py",
    "test_pillar_07_planning.py", "test_pillar_08_metacognition.py", "test_pillar_09_creativity.py", "test_pillar_10_math.py", "test_pillar_11_safety.py",
    "test_pillar_12_persona.py", "test_pillar_13_init.py", "test_pillar_14_multi_role.py",
    "test_pillar_15_consensus.py", "test_pillar_16_task_graph.py", "test_pillar_17_multi_agent.py",
    "test_pillar_18_workflow.py", "test_pillar_19_emergent.py", "test_pillar_20_massive_consensus.py",
    "test_pillar_21_dynamic_role_switching.py", "test_pillar_22_project_management.py",
    "test_pillar_23_parallel_task_optimization.py", "test_pillar_24_multidisciplinary_decomposition.py"
]

def parse_model_list():
    with open(MODEL_LIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    silicon_models = set()
    for line in lines:
        if line.startswith('https://api.siliconflow.cn'):
            parts = line.strip().split()
            if len(parts) == 2:
                silicon_models.add(parts[1])
    platform_models = set()
    platform_map = {
        'Together': 'together',
        'OpenRouter': 'openrouter',
        'Groq': 'groq',
        'HF': 'hf'
    }
    for line in lines:
        if '\t' in line:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                model_name = fields[1]
                platforms = fields[2].split(',')
                for plat in platforms:
                    plat = plat.strip()
                    if plat in platform_map:
                        prefix = platform_map[plat]
                        platform_models.add(f"{prefix}/{model_name}")
    all_models = set()
    all_models.update([f"siliconflow/{m}" for m in silicon_models])
    all_models.update(platform_models)
    # 也可自动轮询所有云API
    all_models.update([f"auto/{m}" for m in silicon_models.union({m.split('/',1)[1] for m in platform_models})])
    return sorted(all_models)

def run_all_tests():
    all_models = parse_model_list()
    log_dir = 'test_logs'
    for model in all_models:
        fail_log_name = f"{model.replace(':', '_').replace('/', '_')}_Allfail.log"
        fail_log_path = os.path.join(log_dir, fail_log_name)
        if os.path.exists(fail_log_path):
            print(f"[SKIP] All cloud APIs failed for {model}, skipping further tests.")
            continue
        cmd = [
            "python", "main_orchestrator.py", "--model", model, "--test"
        ] + PILLAR_TESTS
        print(f"\n===== Running tests for model: {model} =====")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Test failed for model: {model}\n{e}")
        # 检查是否刚刚生成了Allfail日志，如果有则跳过后续
        if os.path.exists(fail_log_path):
            print(f"[STOP] All cloud APIs failed for {model} after first test, skipping remaining pillars.")
            continue

def main():
    run_all_tests()

if __name__ == "__main__":
    main() 