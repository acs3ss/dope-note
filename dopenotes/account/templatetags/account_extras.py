from django import template

import re

register = template.Library()

@register.simple_tag
def watch_to_embed(format_string):
    return re.sub(r'watch\?v=', 'embed/', format_string)
