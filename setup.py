import os.path
import pathlib
import re

from setuptools import setup

PROJECT_NAME = 'torrentp'
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def get_property(prop):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(os.path.join(PROJECT_NAME, '__init__.py')).read())
    return result.group(1)


setup(
    name='torrentp',
    version=get_property('__version__'),
    description='Download from torrent with magnet link or .torrent file',
    long_description=README,
    long_description_content_type="text/markdown",
    url=get_property('__url__'),
    author=get_property('__author__'),
    author_email=get_property('__author_email__'),
    license=get_property('__license__'),
    packages=['torrentp'],
    entry_points={
        'console_scripts': ['torrentp=torrentp.cli:run_cli']
    },
    install_requires=['libtorrent>=2.0.7', 'asyncclick>=8.1.7.2', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
