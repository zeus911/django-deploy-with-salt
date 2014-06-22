import sys
import os
from fabric.api import execute, parallel, sudo, env, cd
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
from django_deploy_with_salt.ask_question import AskQuestion
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Connect to remote servers, setup a salt minion and deploy your project using salt files from a git repository."

    def handle(self, **options):

        #look for DEPLOYMENT_DIR in settings
            # - this directory should contain salt files
            # - host configurations
        try:
            settings.DEPLOYMENT_DIR
        except AttributeError:
            print "DEPLOYMENT_DIR not found in your settings."
            print "To get started, please setup a deployment directory and add it to your settings as DEPLOYMENT_DIR"
            return

        #add the DEPLOYMENT_DIR to the PYTHON_PATH
        sys.path.insert(0, settings.DEPLOYMENT_DIR)

        #import the host settings from the deployment dir
        try:
            import hosts
        except ImportError:
            print "hosts.py not found in your DEPLOYMENT_DIR (" + settings.DEPLOYMENT_DIR + ")"
            print "A hosts.py is required and must contain a CONNECTIONS dict to manage your deployment hosts."
            return
        #validate 'hosts' settings file
        validate_hosts_file(hosts)

        #load the connection settings and display selection list
        host_list = []
        for name, values in hosts.CONNECTIONS.items():
            host_list.append(name)

        connection = AskQuestion('Select the host to deploy:', host_list)()

        connection_settings = hosts.CONNECTIONS[connection]
        validate_connection_settings(connection_settings)
        if 'user' not in connection_settings:
            print 'user not found for this host.'
            print 'Please update your CONNECTION_SETTINGS for this host'

        env.parallel = True
        env.hosts = [connection_settings['user'] + '@' + connection_settings['host']]
        env.connection_attempts = 5
        if 'password' in connection_settings:
            env.user = connection_settings['user']
            env.password = connection_settings['password']
        elif 'key_file' in connection_settings:
            env.key_filename = connection_settings['key_file']
        else:
            print 'No \'password\' or \'key_file\' found for this host'
            print 'Please update your CONNECTION_SETTINGS for this host'
            return

        print "Connecting to " + connection_settings['user'] + '@' + connection_settings['host']

        srv_dir = get_srv_dir(connection_settings)
        if not srv_dir:
            print "No srv directory containing salt files found."
            print "Please create a srv directory inside your DEPLOYMENT_DIR or " \
                  "specify a 'srv_dir' value for this connection and make sure it exists."
            return
        execute(salt, srv_dir=srv_dir)

        print "Deployment complete."

def get_srv_dir(connection_settings):
    try:
        srv_dir = connection_settings['srv_dir']
        if not os.path.exists(srv_dir):
            return False
    except KeyError:
        srv_dir = os.path.join(settings.DEPLOYMENT_DIR, './srv')
        if not os.path.exists(srv_dir):
            return False
    return srv_dir

def validate_connection_settings(connection_settings):
    return True

def validate_hosts_file(hosts):
    return True

@parallel
def salt(*args, **kwargs):

    extra_opts = ['--exclude=".git*"', '--copy-links', '--rsync-path="sudo rsync"']
    srv_dir = os.path.join(kwargs['srv_dir'], '*')

    if exists('/usr/bin/salt-minion'):
        #update salt files from deployment directory to remote
        rsync_project('/srv', srv_dir, extra_opts=' '.join(extra_opts), delete=True)
        sudo('salt-call --local state.highstate')
    else:
        sudo('apt-get --yes --force-yes install python-software-properties')
        sudo('add-apt-repository --yes ppa:saltstack/salt')
        sudo('deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list')
        sudo('wget -q -O- "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x4759FA960E27C0A6" | sudo apt-key add -')
        sudo('apt-get --yes --force-yes update')
        sudo('apt-get --yes --force-yes install salt-minion')
        #transfer salt files from deployment directory to remote
        rsync_project('/srv', srv_dir, extra_opts=' '.join(extra_opts), delete=True)
        sudo('salt-call --local state.highstate')
