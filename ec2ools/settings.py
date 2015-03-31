"""
Find and load the customization settings to use.
"""
__author__ = 'yairgrosu'
import os
import json

PRIMARY_PROPS = ['env_tag', 'region', 'aws_key', 'aws_secret', 'name_tag', 'key_name']
DEFAULT_PROPS = {'env_tag': 'env', 'env': 'test', 'name_tag': 'Name', 'region': 'us-west-2',
                 'key_name': 'KEY_FILE_PLACEHOLDER', 'type': 'ALL'}

SETTINGS_ALTERNATIVES = ['./ec2settings.json', '.ec2l2/ec2settings.json',
                         '~/.ec2l2/ec2settings.json', '/etc/ec2l2/ec2settings.json']


class CTSettings(object):
    """ Settings object. Also contains the logic to find the file to use.
    """
    def __init__(self, mappings=dict(), settings_file=None):
        self.mappings = DEFAULT_PROPS
        self.mappings.update(mappings)
        settings_file = CTSettings.locate_settings_file(settings_file)
        if settings_file is not None:
            self.mappings.update(json.load(open(settings_file)))

    @classmethod
    def locate_settings_file(cls, settings_file):
        """
        :param settings_file: the provided settings file name.
        :return: the located file name that will be used
        """
        if settings_file is not None:
            if os.path.exists(settings_file):
                raise IOError("can't find settings file: (%s)" % settings_file)
            else:
                print "Using the given settings file: (%s)"%settings_file
                return settings_file
        settings_options = list()
        settings_options.extend(SETTINGS_ALTERNATIVES)
        for file_candidate in settings_options:
            if os.path.exists(file_candidate):
                print "found it: (%s)"%file_candidate
                return file_candidate
        return None

    def __getitem__(self, item):
        return self.mappings.get(item)

    def __setitem__(self, key, value):
        self.mappings[key] = value
