from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseNotFound
from django.template import loader
 
def error(request):
    #return HttpResponseNotFound('<h1>not found</h1>')
    raise Http404("Not Found")

def index(request):
    template = loader.get_template('chatapp/index.html')
#    template = loader.get_template('base_contents.html')
    context = {
#         'login_success' : False,
#         'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))
