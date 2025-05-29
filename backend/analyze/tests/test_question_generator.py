from django.test import TestCase
from ..questions import question_generator

class TestRuleBasedQuestionGenerator(TestCase):
    def test_rule_based_question_generator_basic(self):
        components = [
            {'type': 'class', 'name': 'MyClass', 'docstring': 'A test class.', 'file': 'foo.py', 'lineno': 1},
            {'type': 'function', 'name': 'my_func', 'docstring': 'A test function.', 'file': 'foo.py', 'lineno': 5},
        ]
        questions = question_generator.RuleBasedQuestionGenerator.generate(components)
        self.assertTrue(len(questions) in (2, 4, 6, 10))
        self.assertTrue(any('MyClass' in q['question'] for q in questions))
        self.assertTrue(any('my_func' in q['question'] for q in questions))

    def test_rule_based_question_generator_focus(self):
        components = [
            {'type': 'class', 'name': 'MyClass', 'docstring': 'A test class.', 'file': 'foo.py', 'lineno': 1},
            {'type': 'function', 'name': 'my_func', 'docstring': 'A test function.', 'file': 'foo.py', 'lineno': 5},
        ]
        questions = question_generator.RuleBasedQuestionGenerator.generate(components, focus='my_func')
        self.assertTrue(all('my_func' in q['component'] or 'my_func' in q['question'] for q in questions))

