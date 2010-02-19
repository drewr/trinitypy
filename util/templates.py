from django.shortcuts import render_to_response
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template import RequestContext

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
        return render_to_response(template, {},
                                  context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404("%s does not exist" % template)
