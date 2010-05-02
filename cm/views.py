from django.http import HttpResponse
from django.shortcuts import render_to_response
from util.signup import list_subscribers, list_lists
from util.signup import sign_up_to_list, SignupException

def index(request):
    return HttpResponse("index!")


def list(request, list_id=None):
    subs = []
    cmlist = None
    lists = list_lists()
    if list_id:
        subs = list_subscribers(list_id)
        for l in lists:
            if l['ListID'] == list_id:
                cmlist = l
    return render_to_response("cm/list.html",
                              {"lists": lists,
                               "list": cmlist,
                               "subscribers": subs,
                               "emails": map(lambda x: x['EmailAddress'], subs)})


def subscribe(request):
    email = request.POST["email"]
    try:
        sign_up_to_list(email)
        return HttpResponse(content="{\"result\": \"success\", \"email\": \"%s\"}" % email,
                            content_type="application/json")
    except SignupException, e:
        return HttpResponse(status=500, content="{\"result\": \"error\", \"msg\": \"%s\"}" % e.message,
                            content_type="application/json")

