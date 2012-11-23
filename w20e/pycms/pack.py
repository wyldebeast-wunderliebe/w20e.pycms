import ConfigParser
import sys
from paste.script import command
import cookielib, urllib2


class PackCommand(command.Command):

    max_args = 2
    min_args = 1

    usage = "pack <ini file> [login_url]"
    summary = "Pack ZODB"
    group_name = "w20e.pycms"

    parser = command.Command.standard_parser(verbose=True)

    def command(self):

        try:
            ini_file = self.args[0]

            config = ConfigParser.ConfigParser()
            config.readfp(open(ini_file))
        except:
            print "Please provide an ini file as argument"
            sys.exit(-1)

        url = None
        if len(self.args) > 1:
            url = self.args[1]

        if not url:
            host = config.get('server:main', 'host')
            port = config.get('server:main', 'port')
            url = "http://%s:%s/login" % (host, port)

        usr, pwd = config.get('app:main', "pycms.admin_user").split(":")

        cj = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url,
                              "login=%s&password=%s&form.submitted=1&came_from=/script_pack" % \
                              (usr, pwd))

        handle = urllib2.urlopen(req)

        print handle.info()

        result = handle.read()

        print result


