import ConfigParser
import sys
from paste.script import command
import cookielib, urllib2


class PackCommand(command.Command):

    max_args = 1
    min_args = 1

    usage = "pack <ini file>"
    summary = "Pack ZODB"
    group_name = "PyCMS"

    parser = command.Command.standard_parser(verbose=True)

    def command(self):

        try:
            ini_file = self.args[0]

            config = ConfigParser.ConfigParser()
            config.readfp(open(ini_file))        
        except:
            print "Please provide an ini file as argument"
            sys.exit(-1)
    
        host = config.get('server:main', 'host')
        port = config.get('server:main', 'port')
        usr, pwd = config.get('app:main', "pycms.admin_user").split(":")

        cj = cookielib.CookieJar()
        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        url = "http://%s:%s/login" % (host, port)
        req = urllib2.Request(url,
                              "login=%s&password=%s&form.submitted=1&came_from=/ajax_pack" % \
                              (usr, pwd))

        handle = urllib2.urlopen(req)

        print handle.info()
        
        #url = "http://%s:%s/ajax_pack" % (host, port)

        #r = opener.open(url)

        result = handle.read()

        print result

        
