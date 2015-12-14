# coding=utf-8
from django import template
import re, random
from django.core.urlresolvers import reverse, NoReverseMatch
from utils import vkontakte

register = template.Library()

@register.simple_tag
def random_choice(*args):
    return random.choice(args)


# Определяет активный пункт меню
@register.simple_tag(takes_context=True)
def active(context, urlname):
    try:
        pattern = '^' + reverse(urlname)
    except NoReverseMatch:
        pattern = urlname
    path = context.get('request').path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.simple_tag
def vkontakte_auth_link(redirect_uri):
    return vkontakte.build_login_link(redirect_uri)


@register.simple_tag
def vkontakte_profile_link(vkuserid):
    vkuserid = str(vkuserid)
    return 'http://vk.com/' + 'id' * vkuserid.isdigit() + vkuserid