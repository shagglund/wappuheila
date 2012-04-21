from django.template.context import RequestContext
from django.shortcuts import render_to_response
def render_to_request_context_response(request,template , context = {}):
    return render_to_response(template, context, context_instance=RequestContext(request))