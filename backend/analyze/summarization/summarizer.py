class ComponentSummarizer:
    @staticmethod
    def summarize(components):
        summaries = []
        for c in components:
            if c.type == 'function' and c.parameters:
                if isinstance(c.parameters, list):
                    param_str = ', '.join(str(p) for p in c.parameters)
                else:
                    param_str = str(c.parameters)
                summary = f"Function '{c.name}({param_str})' in {c.file} (line {c.lineno}): "
            else:
                summary = f"{c.type.capitalize()} '{c.name}' in {c.file} (line {c.lineno}): "
            if c.docstring:
                summary += c.docstring.split('\n')[0]
            summaries.append({
                'type': c.type,
                'name': c.name,
                'docstring': c.docstring,
                'file': c.file,
                'lineno': c.lineno,
                'parameters': c.parameters,
                'summary': summary
            })
        return summaries

    @staticmethod
    def save_to_file(summaries, filename='summaries.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for s in summaries:
                f.write(s['summary'] + '\n')
