import ast

import javalang
from kopyt import Parser

from ..models import Component


class CodeAnalyzer:
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def trim_path(self, path):
        if self.temp_dir and path.startswith(self.temp_dir):
            return path[len(self.temp_dir):].lstrip('/')
        return path

    def analyze(self, file_path):
        if file_path.endswith('.py'):
            return self._analyze_python(file_path)
        elif file_path.endswith('.java'):
            return self._analyze_java(file_path)
        elif file_path.endswith('.kt'):
            return self._analyze_kotlin(file_path)
        return []

    def _analyze_python(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=file_path)
        components = []
        parent_map = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parent_map[child] = parent
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node)
                full_name = node.name
                components.append(Component(
                    type='class',
                    name=node.name,
                    docstring=doc,
                    file=self.trim_path(file_path),
                    lineno=node.lineno,
                    full_name=full_name
                ))
            elif isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                parent_class = None
                parent = parent_map.get(node)
                while parent:
                    if isinstance(parent, ast.ClassDef):
                        parent_class = parent.name
                        break
                    parent = parent_map.get(parent)
                if parent_class:
                    full_name = f"{parent_class}.{node.name}"
                else:
                    full_name = node.name
                # Get parameter names
                params = [arg.arg for arg in node.args.args]
                components.append(Component(
                    type='function',
                    name=node.name,
                    docstring=doc,
                    file=self.trim_path(file_path),
                    lineno=node.lineno,
                    full_name=full_name,
                    parameters=params
                ))
        return components

    def _analyze_java(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        components = []
        try:
            tree = javalang.parse.parse(source)
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration):
                    components.append(Component(
                        type='class',
                        name=node.name,
                        docstring=None,
                        file=self.trim_path(file_path),
                        lineno=node.position.line if node.position else 1,
                        full_name=node.name
                    ))
                elif isinstance(node, javalang.tree.MethodDeclaration):
                    parent_class = None
                    for ancestor in path:
                        if isinstance(ancestor, javalang.tree.ClassDeclaration):
                            parent_class = ancestor.name
                            break
                    if parent_class:
                        full_name = f"{parent_class}.{node.name}"
                    else:
                        full_name = node.name

                    parameters = []
                    for param in node.parameters:
                        param_type = str(param.type.name)
                        if param.type.dimensions:
                            param_type += '[]' * len(param.type.dimensions)
                        parameters.append(f"{param_type} {param.name}")
                    components.append(Component(
                        type='function',
                        name=node.name,
                        docstring=None,
                        file=self.trim_path(file_path),
                        lineno=node.position.line if node.position else 1,
                        full_name=full_name,
                        parameters=parameters
                    ))
        except Exception:
            pass
        return components

    def _analyze_kotlin(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        components = []
        try:
            parser = Parser(source)
            kt_tree = parser.parse()
            for decl in kt_tree.declarations:
                if decl.__class__.__name__ == 'ClassDeclaration':
                    name = decl.name
                    lineno = decl.position.line if hasattr(decl, 'position') and decl.position else 1
                    components.append(Component(
                        type='class',
                        name=name,
                        docstring=None,
                        file=self.trim_path(file_path),
                        lineno=lineno,
                        full_name=name
                    ))
                    if hasattr(decl, 'body') and hasattr(decl.body, 'members'):
                        for member in decl.body.members:
                            if member.__class__.__name__ == 'FunctionDeclaration':
                                func_name = member.name
                                func_lineno = member.position.line if hasattr(member, 'position') and member.position else 1
                                parameters = []
                                if hasattr(member, 'parameters'):
                                    for param in member.parameters:
                                        param_name = getattr(param, 'name', None)
                                        param_type = getattr(param, 'type', None)
                                        if hasattr(param_type, 'name'):
                                            param_type = param_type.name
                                        parameters.append(f"{param_name}: {param_type}")
                                components.append(Component(
                                    type='function',
                                    name=func_name,
                                    docstring=None,
                                    file=self.trim_path(file_path),
                                    lineno=func_lineno,
                                    full_name=f"{name}.{func_name}",
                                    parameters=parameters
                                ))
        except Exception:
            pass
        return components
