from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import configparser
import sys
from paste.script import command
import http.cookiejar, urllib.request, urllib.error, urllib.parse


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

            config = configparser.ConfigParser()
            config.readfp(open(ini_file))
        except:
            print("Please provide an ini file as argument")
            sys.exit(-1)

        url = None
        if len(self.args) > 1:
            url = self.args[1]

        if not url:
            host = config.get('server:main', 'host')
            port = config.get('server:main', 'port')
            url = "http://%s:%s/login" % (host, port)

        usr, pwd = config.get('server:main', "pycms.admin_user").split(":")

        cj = http.cookiejar.CookieJar()

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

        req = urllib.request.Request(url,
                              "login=%s&password=%s&form.submitted=1&came_from=/script_pack" % \
                              (usr, pwd))

        handle = urllib.request.urlopen(req)

        print(handle.info())

        result = handle.read()

        print(result)
