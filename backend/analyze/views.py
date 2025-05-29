from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import tempfile
import os
import zipfile
import shutil
import json
from .core.codebase import CodebaseExtractor
from .analysis.code_analyzer import CodeAnalyzer
from .summarization.summarizer import ComponentSummarizer
from .questions.question_generator import LLMQuestionGenerator
from .questions.question_generator import RuleBasedQuestionGenerator

def _analyze_codebase(files, temp_dir, use_llm=False, focus=None, openai_api_key=None):
    analyzer = CodeAnalyzer(temp_dir=temp_dir)
    components = []
    for file in files:
        analyzed = analyzer.analyze(file)
        components += analyzed
    summaries = ComponentSummarizer.summarize(components)
    if use_llm:
        llm_gen = LLMQuestionGenerator(openai_api_key=openai_api_key)
        questions = llm_gen.generate(summaries, focus=focus)
    else:
        questions = RuleBasedQuestionGenerator.generate(summaries, focus=focus)
    return questions

@csrf_exempt
@require_http_methods(["POST"])
def analyze_url_view(request):
    try:
        data = json.loads(request.body)
        url = data.get('url')
        use_llm = data.get('llm', False)
        focus = data.get('focus')
        if not url:
            return JsonResponse({'error': 'Missing url'}, status=400)
        extractor = CodebaseExtractor(url)
        files, temp_dir = extractor.extract()
        questions = _analyze_codebase(files, temp_dir, use_llm=use_llm, focus=focus)
        shutil.rmtree(temp_dir)
        return JsonResponse({'questions': questions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def analyze_file_view(request):
    try:
        use_llm = request.POST.get('llm', 'false').lower() == 'true'
        focus = request.POST.get('focus')
        openai_api_key = request.POST.get('openai_api_key')
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Missing file'}, status=400)
        uploaded_file = request.FILES['file']
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, uploaded_file.name)
            with open(zip_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            extractor = CodebaseExtractor(zip_path)
            files, _ = extractor.extract()
            questions = _analyze_codebase(files, temp_dir, use_llm=use_llm, focus=focus, openai_api_key=openai_api_key)
        return JsonResponse({'questions': questions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

