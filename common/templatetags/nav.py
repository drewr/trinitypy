from django import template

register = template.Library()

class NavLinkNode(template.Node):
    def __init__(self, *args):
        self.link_url, self.css_class, self.link_title, self.last, self.sub = args

    def __repr__(self):
        return "<NavLinkNode>"

    def render(self, context):
        try:
            current_url = template.Variable("request.path").resolve(context)
        except template.VariableDoesNotExist:
            return "can't find request in template variables"
        import re
        mat = re.compile("^%s" % self.link_url).match(current_url)
        css_id = self.css_class
        css_class = ""
        if mat:
            css_class += " active"
        if self.sub:
            indent = "&nbsp;&nbsp;&nbsp;"
        else:
            indent = ""
        return '<a href="%s" id="nav-%s" class="%s">%s</a>' % (
            self.link_url, css_id, css_class.strip(), self.link_title.strip('"'))

def do_nav_link(parser, token, last=False, sub=False):
    bits = list(token.split_contents())
    if len(bits) == 4:
        return NavLinkNode(bits[1], bits[2], bits[3], last, sub)
    if len(bits) == 3:
        return NavLinkNode(bits[1], None, bits[2], last, sub)
    raise template.TemplateSyntaxError, "%r takes two or three arguments" % bits[0]

def nav_link(parser, token):
    return do_nav_link(parser, token)
nav_link = register.tag(nav_link)

def nav_link_last(parser, token):
    return do_nav_link(parser, token, True)
nav_link_last = register.tag(nav_link_last)

def nav_link_sub(parser, token):
    return do_nav_link(parser, token, True, sub=True)
nav_link_sub = register.tag(nav_link_sub)
