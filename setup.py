# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import blockdiag

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]


setup(
    name='blockdiag',
    version=blockdiag.__version__,
    description='blockdiag generates block-diagram image from text',
    long_description=open("README.rst").read(),
    classifiers=classifiers,
    keywords=['diagram', 'generator'],
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    url='http://blockdiag.com/',
    download_url='http://pypi.python.org/pypi/blockdiag',
    license='Apache License 2.0',
    py_modules=['blockdiag_sphinxhelper'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'funcparserlib',
        'Pillow',
        'webcolors',
    ],
    extras_require={
        'pdf': [
            'reportlab'
        ],
        'rst': [
            'docutils'
        ],
        'testing': [
            'nose',
            'mock',
            'flake8',
            'flake8-coding',
            'flake8-copyright',
            'reportlab',
            'docutils',
        ],
    },
    test_suite='nose.collector',
    entry_points="""
       [console_scripts]
       blockdiag = blockdiag.command:main

       [blockdiag_noderenderer]
       box = blockdiag.noderenderer.box
       square = blockdiag.noderenderer.square
       roundedbox = blockdiag.noderenderer.roundedbox
       diamond = blockdiag.noderenderer.diamond
       minidiamond = blockdiag.noderenderer.minidiamond
       mail = blockdiag.noderenderer.mail
       note = blockdiag.noderenderer.note
       cloud = blockdiag.noderenderer.cloud
       circle = blockdiag.noderenderer.circle
       ellipse = blockdiag.noderenderer.ellipse
       beginpoint = blockdiag.noderenderer.beginpoint
       endpoint = blockdiag.noderenderer.endpoint
       actor = blockdiag.noderenderer.actor
       flowchart.database = blockdiag.noderenderer.flowchart.database
       flowchart.input = blockdiag.noderenderer.flowchart.input
       flowchart.loopin = blockdiag.noderenderer.flowchart.loopin
       flowchart.loopout = blockdiag.noderenderer.flowchart.loopout
       flowchart.terminator = blockdiag.noderenderer.flowchart.terminator
       textbox = blockdiag.noderenderer.textbox
       dots = blockdiag.noderenderer.dots
       none = blockdiag.noderenderer.none

       [blockdiag_plugins]
       attributes = blockdiag.plugins.attributes
       autoclass = blockdiag.plugins.autoclass

       [blockdiag_imagedrawers]
       imagedraw_png = blockdiag.imagedraw.png
       imagedraw_svg = blockdiag.imagedraw.svg
       imagedraw_pdf = blockdiag.imagedraw.pdf
       imagedraw_tikz = blockdiag.imagedraw.tikz
    """,
)
