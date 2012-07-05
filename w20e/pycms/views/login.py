from pyramid.httpexceptions import HTTPFound
from pyramid.url import resource_url

from pyramid.security import remember, forget
from base import BaseView


class loginview(BaseView):

    def __init__(self, context, request):

        self.context = request.context
        self.request = request

    @property
    def can_edit(self):
        """ Until we think of something smarter... like a global tool"""

        return False

    @property
    def user(self):

        return ''

    def __call__(self):

        res = super(loginview, self).__call__()

        login_url = resource_url(self.context, self.request, 'login')
        referrer = self.request.url
        if referrer == login_url:
            referrer = self.request.registry.settings.get("pycms.logged_in_redirect", "/")
        came_from = self.request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''

        acl = self.context.root.acl

        if 'form.submitted' in self.request.params:

            login = self.request.params['login']
            password = self.request.params['password']

            try:
                if acl.users[login].challenge(password):
                    headers = remember(self.request, login)
                    return HTTPFound(location=came_from,
                                     headers=headers)
            except:
                pass
            message = 'Failed login'

        res.update({
            'message': message,
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'login': login,
            'password': password}
                   )
        return res


class logoutview(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        logout_url = resource_url(self.context, self.request, 'logout')
        referrer = self.request.url
        if referrer == logout_url:
            referrer = '/'  # never use the login form itself as came_from
        came_from = self.request.params.get('came_from', referrer)

        headers = forget(self.request)

        return HTTPFound(location=came_from,
                         headers=headers)
