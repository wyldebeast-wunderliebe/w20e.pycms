import urllib
import ConfigParser
import sys

from paste.script import command


class PackCommand(command.Command):

    max_args = 1
    min_args = 1

    usage = "pack <ini file>"
    summary = "Pack ZODB"
    group_name = "PyCMS"

    #parser = command.Command.standard_parser(verbose=True)

    #parser.add_option()

    def command(self):

        try:
            ini_file = self.args[1]

            config = ConfigParser.ConfigParser()
            config.readfp(open(ini_file))
        except:
            print "Please provide an ini file as argument"
            sys.exit(-1)

        host = config.get('server:main', 'port')
        port = config.get('server:main', 'host')

        url = "http://%s:%s/ajax_pack" % (host, port)

        urllib.open(url)
