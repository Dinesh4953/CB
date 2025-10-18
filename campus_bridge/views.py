from django.http import HttpResponse
from django.shortcuts import render
import os
def starting_page(request):
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_directory, 'index.html')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return HttpResponse(html)
    # return render(request, 'academics/index1.html')