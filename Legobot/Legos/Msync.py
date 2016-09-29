import requests
import logging
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)
base_url = 'https://raw.githubusercontent.com/voxpupuli/'

class Audit(Lego):
    def listening_for(self, message):
        return message['text'].split()[0] == '!msync'

    def handle(self,message):
        arg = parse_args(message)
        if arg == "getver":
            try:
                modname = message['text'].split()[2]
                response = get_single_version(modname)
                self.reply(message,response)
            except Exception as e:
                self.reply(message, "womp womp :/ unable to get version.")
                logger.debug('Caught exception in !getver:' + e)
        return

    def get_name(self):
        return 'msync'

    def get_help(self):
        return 'Discover information about the status of modulesync on managed repositories. Usage: !msync [getver modulename].'

    def get_single_version(self,modname):
        try:
            msync_ver = requests.get(base_url + modname + '/master/.msync.yml')
            msync_ver = msync_ver.text
            return msync_ver.strip('\n')
        except:
            return 'Could not find a module to query :/'

    def parse_args(self,message):
        arg = None
        if len(message['text'].split()) == 1:
            # No args supplied
            arg = None
        elif len(message['text'].split()) > 1:
            arg = message['text'].split()[1]
        return arg
