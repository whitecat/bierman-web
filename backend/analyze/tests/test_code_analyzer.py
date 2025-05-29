from django.test import TestCase
from unittest.mock import patch
import textwrap
from ..analysis.code_analyzer import CodeAnalyzer

class DummyComponent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __getitem__(self, item):
        return getattr(self, item)
    def __contains__(self, item):
        return hasattr(self, item)

class TestCodeAnalyzer(TestCase):
    @patch('analyze.analysis.code_analyzer.Component', DummyComponent)
    def test_analyze_python_class_and_function(self):
        import tempfile
        code = textwrap.dedent('''
            class MyClass:
                """This is a test class."""
                def method(self):
                    """Method docstring."""
                    pass
            def my_function():
                """Function docstring."""
                pass
        ''')
        with tempfile.NamedTemporaryFile('w+', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            analyzer = CodeAnalyzer(temp_dir=f.name.rsplit('/', 1)[0])
            components = analyzer.analyze(f.name)
        names = [c.name for c in components]
        self.assertIn('MyClass', names)
        self.assertIn('my_function', names)
        self.assertTrue(any('test class' in (c.docstring or '') for c in components))
        self.assertTrue(any('Function docstring' in (c.docstring or '') for c in components))

