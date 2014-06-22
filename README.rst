=====
Django Deploy With Salt
=====

Deploy with Salt is a Django command that allows you to connect to remote servers, setup a salt minion and deploy your project using salt files from a git repository.

Quick start
-----------

1. Add "django-deploy-with-salt" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'django-deploy-with-salt',
    )

2. Add DEPLOYMENT_DIR to your settings. DEPLOYMENT_DIR should be a directory outside of your project code where you will store your salt files and connection settings.

   DEPLOYMENT_DIR = '/path/to/your/deployment/files/'

3. In DEPLOYMENT_DIR create a 'hosts.py' file. This file should contain a CONNECTIONS dictionary like this:

    CONNECTIONS = {
        'production_server_1': {
            'host': 'example.com',

            'user': 'example_user',

            'password': 'example_password',  # must specify either 'password' OR 'key_filename'

            'key_filename': '/private/key/file.pem',

            'srv_dir': '/path/to/salt/files/'  # (optional) path to salt srv files
        }
    }

4. In DEPLOYMENT_DIR create 'srv' directory to contain your salt and pillar files.

3. Run `python manage.py deploy_with_salt` to start the deployment process
