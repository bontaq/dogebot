from subprocess import call, check_output
import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect


def home(request):
    return render_to_response('index.html', RequestContext(request, {

    }))


def get_log(request):
    """Returns the last 50 lines of the main log file"""

    output = check_output(['tail', '-n', '50', 'debug.log'])
    results = str(output).split('\n')
    return HttpResponse(json.dumps({'objects': results}), content_type='application/json')
