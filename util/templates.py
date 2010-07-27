import os
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template import RequestContext
from django.conf import settings
from markdown2 import markdown_path

def mark_down_template(path):
    path = os.path.join(settings.USER_TEMPLATE_ROOT, path.replace(".html", ".txt"))
    try:
        return markdown_path(path)
    except IOError:
        return Http404("The page you requested (%s) cannot be found." % path)

def template_viewer(request, path):
    path = path.strip("/")
    template = ""
    if path == "":
        template = "index.html"
    else:
        if path.endswith(".html"):
            template = path
        ## Let's use html suffixes for now.
        ## else:
        ##     template = path + ".html"

    content = mark_down_template(template)

    try:
        return render_to_response(template, {'content':content},
                                  context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        if isinstance(content, Exception):
            raise content
        else:
            return render_to_response("base.html",
                                      {'content':content},
                                      context_instance=RequestContext(request))


    
