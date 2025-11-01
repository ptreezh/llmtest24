"""
Project Architecture Mapping Tool
Automatically scans the project structure and generates comprehensive architecture maps.
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ClassInfo:
    """Represents information about a class."""
    name: str
    file_path: str
    methods: List[str]
    base_classes: List[str]
    line_number: int

@dataclass
class FunctionInfo:
    """Represents information about a function."""
    name: str
    file_path: str
    parameters: List[str]
    line_number: int

@dataclass
class ModuleInfo:
    """Represents information about a module/file."""
    file_path: str
    classes: List[ClassInfo]
    functions: List[FunctionInfo]
    imports: List[str]

class ProjectArchitectureMapper:
    """Main class for mapping project architecture."""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.modules: Dict[str, ModuleInfo] = {}
        self.class_map: Dict[str, ClassInfo] = {}
        self.interface_map: Dict[str, Any] = {}
        
    def scan_project(self) -> None:
        """Scan the entire project and build architecture maps."""
        print(f"Scanning project at: {self.root_path}")
        
        # Walk through all Python files
        for python_file in self.root_path.rglob("*.py"):
            if self._should_skip_file(python_file):
                continue
                
            try:
                self._process_file(python_file)
            except Exception as e:
                print(f"Error processing {python_file}: {e}")
                
        # Generate interface map
        self._generate_interface_map()
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped."""
        skip_patterns = [
            "__pycache__", ".pyc", ".pyo", ".pyd", ".pyi", 
            ".egg-info", ".git", "dist", "build", ".tox",
            "venv", "env", ".env", ".virtualenv"
        ]
        
        str_path = str(file_path)
        return any(pattern in str_path for pattern in skip_patterns)
    
    def _process_file(self, file_path: Path) -> None:
        """Process a single Python file and extract its structure."""
        relative_path = file_path.relative_to(self.root_path)
        module_path = str(relative_path).replace(os.sep, ".")
        if module_path.endswith(".py"):
            module_path = module_path[:-3]
            
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError as e:
                print(f"Syntax error in {file_path}: {e}")
                return
                
        module_info = ModuleInfo(
            file_path=str(relative_path),
            classes=[],
            functions=[],
            imports=[]
        )
        
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_info.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_info.imports.append(f"{node.module}.{node.names[0].name}")
        
        # Extract classes and functions
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, file_path)
                module_info.classes.append(class_info)
                self.class_map[class_info.name] = class_info
            elif isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, file_path)
                module_info.functions.append(func_info)
                
        self.modules[module_path] = module_info
        
    def _extract_class_info(self, node: ast.ClassDef, file_path: Path) -> ClassInfo:
        """Extract information from a class definition node."""
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(ast.unparse(base))
                
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
                
        relative_path = file_path.relative_to(self.root_path)
        return ClassInfo(
            name=node.name,
            file_path=str(relative_path),
            methods=methods,
            base_classes=base_classes,
            line_number=node.lineno
        )
        
    def _extract_function_info(self, node: ast.FunctionDef, file_path: Path) -> FunctionInfo:
        """Extract information from a function definition node."""
        parameters = []
        for arg in node.args.args:
            parameters.append(arg.arg)
            
        relative_path = file_path.relative_to(self.root_path)
        return FunctionInfo(
            name=node.name,
            file_path=str(relative_path),
            parameters=parameters,
            line_number=node.lineno
        )
        
    def _generate_interface_map(self) -> None:
        """Generate a simplified interface map for easy consumption."""
        self.interface_map = {
            "classes": {},
            "functions": {},
            "modules": {}
        }
        
        # Add classes to interface map
        for class_name, class_info in self.class_map.items():
            self.interface_map["classes"][class_name] = {
                "file_path": class_info.file_path,
                "methods": class_info.methods,
                "base_classes": class_info.base_classes,
                "line_number": class_info.line_number
            }
            
        # Add functions to interface map
        for module_info in self.modules.values():
            for func_info in module_info.functions:
                self.interface_map["functions"][func_info.name] = {
                    "file_path": func_info.file_path,
                    "parameters": func_info.parameters,
                    "line_number": func_info.line_number
                }
                
        # Add modules to interface map
        for module_path, module_info in self.modules.items():
            self.interface_map["modules"][module_path] = {
                "file_path": module_info.file_path,
                "classes": [cls.name for cls in module_info.classes],
                "functions": [func.name for func in module_info.functions],
                "imports": module_info.imports
            }
            
    def save_maps(self, architecture_file: str = "architecture_map.json", 
                  interface_file: str = "interface_map.json") -> None:
        """Save the generated maps to JSON files."""
        # Save detailed architecture map
        architecture_data = {
            "project_root": str(self.root_path),
            "modules": {}
        }
        
        for module_path, module_info in self.modules.items():
            architecture_data["modules"][module_path] = {
                "file_path": module_info.file_path,
                "classes": [
                    {
                        "name": cls.name,
                        "methods": cls.methods,
                        "base_classes": cls.base_classes,
                        "line_number": cls.line_number
                    }
                    for cls in module_info.classes
                ],
                "functions": [
                    {
                        "name": func.name,
                        "parameters": func.parameters,
                        "line_number": func.line_number
                    }
                    for func in module_info.functions
                ],
                "imports": module_info.imports
            }
            
        with open(architecture_file, 'w', encoding='utf-8') as f:
            json.dump(architecture_data, f, indent=2, ensure_ascii=False)
            
        print(f"Architecture map saved to {architecture_file}")
        
        # Save simplified interface map
        with open(interface_file, 'w', encoding='utf-8') as f:
            json.dump(self.interface_map, f, indent=2, ensure_ascii=False)
            
        print(f"Interface map saved to {interface_file}")
        
    def get_class_info(self, class_name: str) -> Optional[ClassInfo]:
        """Get information about a specific class."""
        return self.class_map.get(class_name)
        
    def get_module_info(self, module_path: str) -> Optional[ModuleInfo]:
        """Get information about a specific module."""
        return self.modules.get(module_path)
        
    def find_classes_inheriting_from(self, base_class: str) -> List[ClassInfo]:
        """Find all classes that inherit from a specific base class."""
        result = []
        for class_info in self.class_map.values():
            if base_class in class_info.base_classes:
                result.append(class_info)
        return result

def main():
    """Main function to run the architecture mapper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Project Architecture Mapper')
    parser.add_argument('--root', default='.', help='Root directory to scan (default: current directory)')
    parser.add_argument('--architecture-file', default='architecture_map.json', help='Output file for detailed architecture map')
    parser.add_argument('--interface-file', default='interface_map.json', help='Output file for simplified interface map')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    mapper = ProjectArchitectureMapper(root_path=args.root)
    mapper.scan_project()
    mapper.save_maps(architecture_file=args.architecture_file, interface_file=args.interface_file)
    
    if args.verbose:
        print(f"\nArchitecture mapping complete!")
        print(f"Found {len(mapper.modules)} modules")
        print(f"Found {len(mapper.class_map)} classes")
        
        # Example: Find all classes inheriting from IndependenceTestBase
        base_classes = mapper.find_classes_inheriting_from("IndependenceTestBase")
        print(f"\nClasses inheriting from IndependenceTestBase:")
        for cls in base_classes:
            print(f"  - {cls.name} ({cls.file_path})")

if __name__ == "__main__":
    main()
