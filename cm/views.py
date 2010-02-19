from django.http import HttpResponse

def index(request):
    return HttpResponse("index!")

def subscribe(request):
    return HttpResponse(content="{\"result\": \"success\"}", content_type="application/json")

