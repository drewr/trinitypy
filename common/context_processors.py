from django.conf import settings
from common.util import slashes_to_dashes


def url(request):
    url = request.path
    return {
        "url": url,
        "page_id": "page-%s" % slashes_to_dashes(url)
    }
