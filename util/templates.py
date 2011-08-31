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

def get_snippet(tmpl, name):
    path = os.path.join(settings.USER_TEMPLATE_ROOT,
                        tmpl.replace(".html", ""),
                        name)
    if os.path.exists(path):
        return markdown_path(path)
    else:
        return markdown_path(os.path.join(settings.USER_TEMPLATE_ROOT,
                                          "home",
                                          name))


def template_viewer(request, path):
    path = path.strip("/")
    if path == "":
        template = "home.html"
    elif path.endswith(".html"):
        template = path
    else:
        raise Http404("tcnash: not a template %s" % path)

    content = mark_down_template(template)
    sidebar = get_snippet(template, "_sidebar.txt")
    upcoming = get_snippet(template, "_upcoming.txt")

    try:
        return render_to_response(template, {'content':content,
                                             'sidebar':sidebar,
                                             'upcoming':upcoming},
                                  context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        if isinstance(content, Exception):
            raise content
        else:
            return render_to_response("base.html", {'content':content,
                                                    'sidebar':sidebar,
                                                    'upcoming':upcoming},
                                      context_instance=RequestContext(request))


    
