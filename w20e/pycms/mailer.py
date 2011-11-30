from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


FROM = "dokter@w20e.com"
BCC = FROM

TEXT = """
You can log in using this link... %s
"""


class Mailer(object):

    """ Mailer tool """

    def __init__(self):

        """ moi """

    def invite_user(self, request, email, key):

        """ Send invoice per email """

        mailer = get_mailer(request)

        from_addr = request.registry.settings.get('pycms.from_addr', FROM)
        bcc_addr = request.registry.settings.get('pycms.bcc_addr', BCC)

        msg = Message(subject="Invitation to join",
                      sender=from_addr,
                      bcc=bcc_addr,
                      recipients=[email],
                      html=TEXT % request.host_url.strip() + \
                      "/change_password?token=" + key)

        mailer.send(msg)
