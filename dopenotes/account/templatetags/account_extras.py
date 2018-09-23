from django import template

import re

register = template.Library()

@register.simple_tag
def watch_to_embed(format_string):
    embed_url = re.sub(r'/(watch\?v=|watch/|v/)', '/embed/', format_string)
    embed_url = re.sub(r'/youtu\.be/', 'youtube.com/embed/', embed_url)
    embed_url = re.sub(r'&.*', '', embed_url)
    return embed_url
