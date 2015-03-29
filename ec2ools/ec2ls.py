#! /usr/bin/env python
""" listing of ec2 instances
"""
__author__ = 'yairgrosu'
__email__ = 'yair@grosu.io'

import argparse
import os
import json
import boto
import boto.ec2
import boto.vpc
import boto.rds


def get_settings():
    """
    :return:obtain the settings to use
    """
    settings = {'env': 'test', 'type': 'ALL', 'env_tag': 'Env', 'region': 'us-west-2',
                'key_name': 'KEY_FILE_PLACEHOLDER'}
    settings_fl = os.getenv('EC2LS_FILE', './ec2settings.json')
    if os.path.exists(settings_fl):
        settings.update(json.load(open('./ec2settings.json')))
    else:
        print "Missing environment value: 'EC2LS_FILE', and no ./ec2settings.json in workdir."
        print "Exiting."
        os.sys.exit(1)
    return settings

SETTINGS = get_settings()


def get_org_instances(the_env, prefix, suffix="", partial=""):
    """gets the instances according to the filtering parameters.  """
    ec2conn = boto.ec2.connect_to_region(SETTINGS['region'])
    ec2_instances = ec2conn.get_only_instances()
    instances = list()
    environments = set()
    for inst in ec2_instances:
        if 'Name' in inst.tags and 'Env' in inst.tags:
            curr_name = inst.tags['Name']
            curr_env = inst.tags['Env']
            environments.add(curr_env)
            ip_addr = inst.ip_address if inst.ip_address is not None else inst.private_ip_address
            if prefix == 'ALL':
                if curr_env == the_env:
                    instances.append((inst.id, ip_addr, curr_name, inst.launch_time, inst.state))
            else:
                if curr_env == the_env and curr_name.startswith(prefix) and \
                        curr_name.endswith(suffix) and partial in curr_name:
                    instances.append((inst.id, ip_addr, curr_name, inst.launch_time, inst.state))
    return instances, environments


def ec2ls():
    """ parse input and invoke ec2 listing, provide the results back.  """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.description = """
EC2 listing of nodes, with specific filtering by tags.

Setup:
    AWS credentials:
    Make sure the following env variables are set in advance:
        export AWS_ACCESS_KEY_ID=....
        export AWS_SECRET_ACCESS_KEY=....

    For ease of use - just add to the PATH, or alias it in your ~/.bashrc
    alias ec2ls='~/YOUR_TOOLS_PATH/ec2ls.py'

Set the EC2LS_FILE env to point to the settings file:  export EC2LS_FILE=~/.ec2ls/settings.json
Alternatively, you can just put an ec2settings.json file in the working directory.
A sample json file
    {
        "key_name":"my_aws_key.pem",
        "region":"us-east-1",
        "env":"qa-123",
        "env_tag":"TAG_USED_FOR_ENV_SELECTION",
    }

For example:
ec2ls -e prod -t Worker -i -2
    running		2015-02-19T20:02:34.000Z	i-xxxyyy14	Worker-1
        ssh -i ~/.ssh/my_aws_key.pem ubuntu@xx.ww.yy.zz

    running		2015-02-19T20:02:34.000Z	i-xxxyyy13	Worker-3
        ssh -i ~/.ssh/my_aws_key.pem ubuntu@xx.ww.yy.zz

    running		2015-02-19T20:02:34.000Z	i-xxxyyy54	Worker-92
        ssh -i ~/.ssh/my_aws_key.pem ubuntu@xx.ww.yy.zz

    running		2015-02-20T20:02:34.000Z	i-xxxyyy12	Worker-8
        ssh -i ~/.ssh/my_aws_key.pem ubuntu@xx.ww.yy.zz


    ... put this in clipboard: ssh -i ~/.ssh/my_aws_key.pem ubuntu@xx.ww.yy.zz
     ===  Worker-92  ===

Now ... just Command-V and press ENTER.

    """

    parser.add_argument('-e', help="Name of the %s tag of the nodes. default is (%s)" %
                        (SETTINGS['env_tag'], SETTINGS['env']), default=SETTINGS['env'])
    parser.add_argument('-t', help="Name prefix. 'ALL' is the default", default='ALL')
    parser.add_argument('-s', help='suffix of type: [optional]', default="")
    parser.add_argument('-p', help='partial text to look for: [optional]', default="")
    parser.add_argument('-i', type=int,
                        help='position of item to put in clipboard, see numbering in the, default  last(-1), -2 is before...'
                             ' 0 is the first, 1 is the 2nd ...', default=-1)

    args = parser.parse_args()
    print "%s\n" % args

    the_instances, the_envs = get_org_instances(args.e, args.t, args.s, args.p)

    the_instances.sort(cmp=lambda x, y: cmp(x[3].lower(), y[3].lower()))

    commands = list()
    if len(the_instances) > 0:
        for item in the_instances:
            cmd_str = "ssh -i ~/.ssh/%s ubuntu@%s" % (SETTINGS['key_name'], item[1])
            print "%s\t\t%s\t%s\t%s\n\t%s\n" % (item[4], item[3], item[0], item[2], cmd_str)

            commands.append(cmd_str)

    print "\n\t\tExisting envs are: << %s >>" % the_envs
    if abs(args.i) <= len(commands):
        cmd = "echo %s | tr -d \"\n\" | pbcopy" % commands[args.i]
        os.system(cmd)
        print "copied this to clipboard: %s" % commands[args.i]
        print "===  %s  ===\n" % the_instances[args.i][2]

def main():
    ec2ls()

if __name__ == '__main__':
    main()
