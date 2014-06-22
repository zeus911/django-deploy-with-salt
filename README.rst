=====
Deploy With Salt
=====

Deploy with Salt is a Django command that allows you to connect to remote servers, setup a salt minion and deploy your project using salt files from a git repository.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'django-deploy-with-salt',
    )

2. Run `python manage.py deploy_with_salt` to start the deployment process
