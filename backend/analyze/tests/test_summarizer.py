from django.test import TestCase
from ..summarization.summarizer import ComponentSummarizer

class DummyComponent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestComponentSummarizer(TestCase):
    def test_summarize_class_and_function(self):
        components = [
            DummyComponent(type='class', name='MyClass', docstring='A test class.', file='foo.py', lineno=1, parameters=None),
            DummyComponent(type='function', name='my_func', docstring='A test function.', file='foo.py', lineno=5, parameters=['x', 'y']),
        ]
        summaries = ComponentSummarizer.summarize(components)
        self.assertTrue(any('MyClass' in s['summary'] for s in summaries))
        self.assertTrue(any('my_func' in s['summary'] for s in summaries))
        self.assertTrue(any('A test class.' in s['summary'] for s in summaries))
        self.assertTrue(any('A test function.' in s['summary'] for s in summaries))

    def test_save_to_file(self):
        import tempfile
        summaries = [
            {'summary': 'Class MyClass summary.'},
            {'summary': 'Function my_func summary.'}
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = f'{tmpdir}/summaries.txt'
            ComponentSummarizer.save_to_file(summaries, filename=file_path)
            with open(file_path) as f:
                content = f.read()
            self.assertIn('MyClass', content)
            self.assertIn('my_func', content)

