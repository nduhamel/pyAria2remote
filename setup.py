from setuptools import setup
import sys

VERSION = "0.1" # find a better way to do so.

requires = ['configobj','blinker']
setup(
    name = "pyariaremote",
    version = VERSION,
    author = 'Nicolas Duhamel',
    author_email = 'nicolas@jombi.fr',
    description = "a command line remote control interface for aria2",
    packages = ['pyaria2', 'mypyapp'],
    include_package_data = True,
    install_requires = requires, 
    scripts = ['bin/aria2remote'],
)
