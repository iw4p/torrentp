from setuptools import setup

setup(
    name='torrentp',
    version='0.1.0',    
    description='Download from torrent with magnet link or .torrent file',
    url='https://github.com/iw4p/torrentp',
    author='Nima Akbarzadeh',
    author_email='iw4p@protonmail.com',
    license='BSD 2-clause',
    packages=['torrentp'],
    install_requires=['libtorrent>=2.0.7',],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
