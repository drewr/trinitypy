from django.http import HttpResponse
from util.signup import sign_up_to_list, SignupException

def index(request):
    return HttpResponse("index!")

def subscribe(request):
    email = request.POST["email"]
    try:
        sign_up_to_list(email)
        return HttpResponse(content="{\"result\": \"success\", \"email\": \"%s\"}" % email,
                            content_type="application/json")
    except SignupException, e:
        return HttpResponse(status=500, content="{\"result\": \"error\", \"msg\": \"%s\"}" % e.message,
                            content_type="application/json")

