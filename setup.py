#########################################################################
# Copyright 2013 Shannon Cruey
#########################################################################

# TRICKY TO do this using setup.py - since we require external directories,
# and the code currently expects those directories to have a path relative
# to the executable.

# First, restructure the code so the package is installed in site-packages,
# the config file goes in /etc/flexapi.conf, and the conf file tells where
# the other directories go (defaulted to /opt/flexapi/*)


# import os
# from setuptools import setup, find_packages
# 
# def read(*paths):
#     """Build a file path from *paths* and return the contents."""
#     with open(os.path.join(*paths), 'r') as f:
#         return f.read()
# 
#  
# binscripts = [
#               "/bin/flexapi"
#               ]
# for f in os.listdir("bin"):
#     binscripts.append("bin/"+f)
#  
# setup(
#     name='FlexAPI',
#     version='0.1.0',
#     description=read('README.rst'),
#     license='Proprietary License',
#     author='Shannon Cruey',
#     author_email='',
#     url='http://flexapi.info',
#     install_requires=['web.py'],
#     packages=find_packages(exclude=[]),
#     include_package_data=True,
#     classifiers=[
#         'Development Status :: Beta',
#         'License :: Other/Proprietary License',
#         'Operating System :: OS Independent',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 2',
#         'Programming Language :: Python :: 2.7',
#         'Environment :: No Input/Output (Daemon)',
#     ],
#     scripts=binscripts,
#     py_modules=[])

