from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author='Pelle Drijver',
    author_email='pelledrijver@gmail.com',
    url='https://github.com/pelledrijver/twitch-highlights',
    name='twitch-highlights',
    version='1.1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="An OS-independent and easy-to-use module for creating highlight videos from trending Twitch clips. "
                "Twitch highlight videos can be created by either specifying a category or a list of streamer "
                "names.",
    keywords="twitch, twitch highlights, twitch clips, twitch compilation",
    install_requires=[
        'requests',
        'datetime',
        'moviepy>=1.0.3',
        'python-slugify>=4.0'
    ],
    package_dir={'': 'src'},
    packages=['twitch_highlights'],
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ]
)
