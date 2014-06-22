import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-deploy-with-salt',
    version='0.1.0',
    packages=['deploy_with_salt'],
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='Django command that allows you to connect to remote servers, setup a salt minion and deploy your project using salt files from a git repository.',
    long_description=README,
    url='https://github.com/codewithcheese/django-deploy-with-salt',
    author='Thomas Manning',
    author_email='mr.tmanning@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    requires=['django(>=1.5)'],
    install_requires = [
        'Fabric==1.8.1',
    ],
)
