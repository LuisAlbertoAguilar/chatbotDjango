from django.shortcuts import render
from django.http import JsonResponse
from .oai_queries import get_completion

def query_view(request):
    # If POST, user prompt and chatgpt response
    if request.method == 'POST':
        # Receive user prompt
        prompt = request.POST.get('prompt')
        # Receive chatgpt response
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    # If GET, render html
    return render(request, 'query.html')
