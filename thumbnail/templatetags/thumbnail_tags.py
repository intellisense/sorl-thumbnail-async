import re

from django import template
from django.utils.encoding import smart_str
from sorl.thumbnail import default
from django.template import TemplateSyntaxError

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
from ..conf import settings
from ..utils import get_thumbnail_options_from_dict

register = template.Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')

class CustomThumbnailNode(ThumbnailNode):
    """ Extends ThumbnailNode to use thumbnail sizes from settings"""
    error_message = ('Please enter sizes defined in settings')
    def __init__(self, parser, token):
        self.parser = parser
        self.token = token
        ThumbnailNode.__init__(self, parser, token)
    
    def pre_render(self, context):
        file_ = self.file_.resolve(context)
        bits = self.token.split_contents()
        if len(bits) < 5 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)
        try:
            thumbnail_settings = get_thumbnail_options_from_dict(
                getattr(file_.instance, 'THUMBNAIL_OPTIONS_DICT', settings.OPTIONS_DICT))
            thumbnail_options = thumbnail_settings[bits[2]]
            thumbnail_options = thumbnail_options.split()
        except KeyError:
            raise TemplateSyntaxError(self.error_message)
        self.geometry = self.parser.compile_filter("'%s'" % thumbnail_options[0])
        self.options = []
        try:
            m = kw_pat.match(thumbnail_options[1])
            key = smart_str(m.group('key'))
            expr = self.parser.compile_filter('"%s"' % m.group('value'))
            self.options.append((key, expr))
        except IndexError:
            pass
        self.as_var = bits[-1]
    
    def _render(self, context):
        self.pre_render(context)
        return ThumbnailNode._render(self, context)

@register.tag
def thumbnail(parser, token):
    return CustomThumbnailNode(parser, token)
