import soundcloud
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect


# Create your views here.
def home(request):
    return render_to_response('index.html', RequestContext(request, {

    }))
