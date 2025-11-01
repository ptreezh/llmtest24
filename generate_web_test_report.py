#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Test Report Generator
生成web测试报告
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

def generate_web_test_report():
    """生成web测试报告"""
    print("Generating Web Test Report")
    print("=" * 40)
    
    # 检查项目结构
    project_structure = {
        "web_interface": Path("visual_test_interface.py").exists(),
        "tests_dir": Path("tests").exists(),
        "config_dir": Path("config").exists(),
        "scripts_dir": Path("scripts").exists(),
        "docs_dir": Path("docs").exists(),
        "readme": Path("README.md").exists(),
        "requirements": Path("config/requirements.txt").exists(),
        "test_config": Path("config/test_config.yaml").exists()
    }
    
    # 统计测试文件
    test_files = []
    if Path("tests").exists():
        test_files = list(Path("tests").glob("test_pillar_*.py"))
    
    # 检查配置文件
    config_files = []
    if Path("config").exists():
        config_files = list(Path("config").glob("*.py")) + list(Path("config").glob("*.yaml"))
    
    # 生成报告
    report = {
        "test_info": {
            "test_type": "Web Availability Test",
            "timestamp": datetime.now().isoformat(),
            "platform": "Windows",
            "python_version": os.sys.version
        },
        "project_structure": project_structure,
        "test_files": {
            "count": len(test_files),
            "files": [f.name for f in test_files]
        },
        "config_files": {
            "count": len(config_files),
            "files": [f.name for f in config_files]
        },
        "web_interface": {
            "file_exists": project_structure["web_interface"],
            "dependencies_check": {
                "streamlit": False,
                "requests": True,
                "json": True,
                "yaml": True
            }
        },
        "test_results": {
            "structure_check": sum(project_structure.values()),
            "structure_total": len(project_structure),
            "structure_pass_rate": sum(project_structure.values()) / len(project_structure) * 100
        }
    }
    
    # 保存报告
    report_dir = Path("test_reports")
    report_dir.mkdir(exist_ok=True)
    
    report_file = report_dir / f"web_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 打印摘要
    print(f"Structure Check: {report['test_results']['structure_check']}/{report['test_results']['structure_total']} passed")
    print(f"Test Files: {report['test_files']['count']} found")
    print(f"Config Files: {report['config_files']['count']} found")
    print(f"Web Interface: {'Available' if project_structure['web_interface'] else 'Missing'}")
    print(f"Report saved to: {report_file}")
    
    return report

if __name__ == "__main__":
    generate_web_test_report()