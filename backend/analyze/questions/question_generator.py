import os
import openai
import re
import json
import random

class RuleBasedQuestionGenerator:
    @staticmethod
    def _name_with_file(c):
        if c['type'] == 'function':
            return f"{c['name']}` in `{c['file']}"
        return c['name']

    @staticmethod
    def generate(components, focus=None):
        if focus:
            filtered = [c for c in components if focus.lower() in (c['docstring'] or '').lower() or focus.lower() in c['name'].lower()]
            if filtered:
                components = filtered
        questions = []
        templates = [
            ('beginner', 'What is the purpose of the {type} `{name_updated}`?',
             'The {type} `{name}` is defined in {file} at line {lineno}. This component is responsible for implementing its declared functionality.'),
            ('intermediate', 'How does the {type} `{name_updated}` interact with other components?',
             'The {type} `{name_updated}` may interact with other classes or functions in the codebase.'),
            ('advanced', 'How could the {type} `{name_updated}` be optimized or improved?',
             'Potential optimizations for `{name_updated}` could include refactoring, improving efficiency, or enhancing documentation.')
        ]
        random.shuffle(components)
        idx = 0
        while len(questions) < 10 and components:
            c = components[idx % len(components)]
            t = templates[idx % len(templates)]
            name_with_file = RuleBasedQuestionGenerator._name_with_file(c)
            q = t[1].format(**c, name_updated=name_with_file)
            a = t[2].format(**c, name_updated=name_with_file)
            questions.append({
                'question': q,
                'answer': a,
                'difficulty': t[0],
                'component': c['name'],
                'type': c['type']
            })
            idx += 1
        return questions[:10]

class LLMQuestionGenerator:
    def __init__(self, openai_api_key=None):
        if openai_api_key is None:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError('OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass as argument.')
        self.client = openai.Client(api_key=openai_api_key)

    def generate(self, components, focus=None):
        summaries = [f"- {c['summary']}" for c in components]
        codebase_summary = '\n'.join(summaries)
        focus_str = f" Focus on the concept: {focus}." if focus else ""
        prompt = (
            f"You are an expert Python interviewer. Given the following codebase summary, generate a list of 10 technical interview questions with detailed answers."
            f"Each question should be classified as beginner, intermediate, or advanced, and should be specific to the codebase."
            f"{focus_str}\n\nCodebase summary:\n{codebase_summary}\n\n"
            "Return the result as a JSON array of objects with fields: question, answer, difficulty (beginner/intermediate/advanced)."
        )
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You are a helpful assistant."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt
                        }
                    ]
                }
            ],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2000,
            top_p=1
        )
        content = response.output[0].content[0].text.strip()
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            json_str = content
        try:
            questions = json.loads(json_str)
        except Exception:
            questions = [{
                'question': 'Failed to parse LLM response.',
                'answer': content,
                'difficulty': 'advanced'
            }]
        return questions
