def slashes_to_dashes(s):
    return s.strip("/").replace("/", "-")

def url_tokens(url):
    return slashes_to_dashes(url).split("-")

