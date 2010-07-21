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
        return "content not found: %s" % path

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
    try:
        return render_to_response(template, {'content':mark_down_template(template)},
                                  context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404("%s does not exist" % template)
