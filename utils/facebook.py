import urllib
import json

from sportcourts import settings


def build_login_link(redirect_uri, host='', scope=''):
    raw_link = 'https://www.facebook.com/v2.8/dialog/oauth?client_id={appid}&state=facebook&redirect_uri={host}{redirect_uri}&response_type=code'
    if not host:
        host = settings.CURRENT_HOST
    if not redirect_uri.startswith('/'):
        redirect_uri = '/' + redirect_uri
    raw_link = raw_link.format(scope=scope, host=host, redirect_uri=redirect_uri, appid=settings.FACEBOOK['APPID'])
    return raw_link


class AuthError(Exception):
    def __init__(self, error, description, e=None):
        self.error = error
        self.description = description
        self.e = e
        super(AuthError, self).__init__(self.error, self.description)


class FacebookError(AuthError):
    def __init__(self, errordict):
        self.data = errordict
        super(FacebookError, self).__init__(errordict['error_msg'], errordict['error_code'])


def auth_code(code, redirect_uri):
    url = "https://graph.facebook.com/v2.8/oauth/access_token?client_id={}&client_secret={}&code={}&redirect_uri={}{}"
    url = url.format(settings.FACEBOOK['APPID'], settings.FACEBOOK['SECRET'], code, settings.CURRENT_HOST,
                     redirect_uri)
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        raise AuthError('Auth error', 'Unathorized', e)
    response = response.read().decode()
    response = json.loads(response)
    if 'error' in response:
        raise FacebookError(response['error'])
    return response['access_token']


def user_id(access_token):
    url = u'https://graph.facebook.com/me?access_token={}'.format(access_token)
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        raise AuthError('Auth error', 'Unathorized', e)
    response = response.read().decode()
    response = json.loads(response)
    if 'error' in response:
        raise FacebookError(response['error'])
    return response['id']


def api(token, method, **kwargs):
    params = list()
    for key in kwargs:
        if len(str(kwargs[key])) != 0:
            if isinstance(kwargs[key], list):
                params.append((key, ','.join(map(str, kwargs[key]))))
            else:
                params.append((key, str(kwargs[key])))
    if token:
        params.append(("access_token", token))
    params.append(('v', '5.27'))
    url = 'https://api.vk.com/method/{0}?{1}'.format(method, urllib.parse.urlencode(params))
    response = urllib.request.urlopen(url).read()
    response = json.loads(response.decode('utf-8'))
    if 'response' not in response:
        raise VkontakteError(response['error'])
    return response['response']
