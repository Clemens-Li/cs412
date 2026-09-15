from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def quote(request):
    response_text = '''
    <html>
    <h1>Hello World!</h1>
    <html>
    '''
    return HttpResponse(response_text)