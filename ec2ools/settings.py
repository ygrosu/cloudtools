__author__ = 'yairgrosu'

import os, json

PRIMARY_PROPS = ['env_tag', 'region', 'aws_key', 'aws_secret', 'name_tag', 'key_name']
DEFAULT_PROPS = {'env_tag': 'env', 'env': 'test', 'name_tag': 'Name', 'region': 'us-west-2',
                 'key_name': 'KEY_FILE_PLACEHOLDER', 'type': 'ALL'}

SETTINGS_ALTERNATIVES = ['./ec2settings.json', '.ec2l2/ec2settings.json', '~/.ec2l2/ec2settings.json',
                         '/etc/ec2l2/ec2settings.json']


class CTSettings:
    def __init__(self, mappings=dict(), settings_file=None):
        self.mappings = DEFAULT_PROPS
        self.mappings.update(mappings)
        settings_file = CTSettings.locate_settings_file(settings_file)
        if settings_file is not None:
            self.mappings.update(json.load(open(settings_file)))

    @classmethod
    def locate_settings_file(self, settings_file):
        settings_options = [settings_file]
        settings_options.extend(SETTINGS_ALTERNATIVES)
        print settings_options.remove(None)
        print settings_options
        for fl in settings_options:
            if os.path.exists(fl):
                print "found it: (%s)"%fl
                return fl
        return None

    def __getitem__(self, item):
        return self.mappings.get(item)

    def __setitem__(self, key, value):
        self.mappings[key]=value