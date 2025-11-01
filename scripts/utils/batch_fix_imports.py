import os
import glob

def fix_imports_in_file(filepath):
    """在指定文件中添加 sys.path 修改代码"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 检查是否已存在修复代码
    if any("sys.path.append" in line for line in lines):
        print(f"Skipping (already fixed): {filepath}")
        return

    # 找到第一个 import sys，或者在文件顶部添加
    import_sys_index = -1
    first_import_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("import sys"):
            import_sys_index = i
            break
        if first_import_index == -1 and line.strip().startswith("import "):
            first_import_index = i

    path_fix_code = [
        "import os\n",
        "# 添加项目根目录到Python路径\n",
        "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n",
        "\n"
    ]

    # 决定插入位置
    if import_sys_index != -1:
        # 在 import sys 之后插入
        lines.insert(import_sys_index + 1, path_fix_code[1])
        lines.insert(import_sys_index + 2, path_fix_code[2])
        lines.insert(import_sys_index + 3, path_fix_code[3])
        # 确保 import os 存在
        if not any(line.strip() == "import os" for line in lines):
            lines.insert(import_sys_index, "import os\n")
    else:
        # 在第一个 import 前插入
        insert_pos = first_import_index if first_import_index != -1 else 1
        if not any(line.strip() == "import sys" for line in lines):
             lines.insert(insert_pos, "import sys\n")
        lines.insert(insert_pos + 1, path_fix_code[0]) # import os
        lines.insert(insert_pos + 2, path_fix_code[1]) # comment
        lines.insert(insert_pos + 3, path_fix_code[2]) # the fix
        lines.insert(insert_pos + 4, path_fix_code[3]) # newline

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Fixed: {filepath}")


def main():
    """主函数"""
    test_files = glob.glob("tests/test_pillar_*.py")
    for filepath in test_files:
        fix_imports_in_file(filepath)
    print("\nBatch import fix complete.")

if __name__ == "__main__":
    main()
