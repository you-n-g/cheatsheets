#!/usr/bin/env python
# -*- coding:utf8 -*-

from django.template import Library, loader, Context, Node
register = Library()

@register.filter
def XXX_filter(XXX):
    return XXX

@register.simple_tag(takes_context=True)
def XXX_simple_tag(context, XXX...):
    context.update({XXX: XXX})
    return loader.get_template("XXX.html").render(Context(context, autoescape=context.autoescape))
