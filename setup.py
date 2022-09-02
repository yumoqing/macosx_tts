# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

with open('macosx_tts/version.py', 'r') as f:
	x = f.read()
	y = x[x.index("'")+1:]
	z = y[:y.index("'")]
	version = z
with open("README.md", "r") as fh:
    long_description = fh.read()

name = "macosx_tts"
description = "macosx_tts is a ali tts driver for unitts engine"
author = "yumoqing"
email = "yumoqing@gmail.com"

package_data = {}

setup(
	name="macosx_tts",
	version=version,
	
	# uncomment the following lines if you fill them out in release.py
	description=description,
	author=author,
	author_email=email,
   	platforms='any',
	install_requires=[
	],
	packages=[
		"macosx_tts"
	],
	package_data=package_data,
	keywords = [
	],
	url="https://github.com/yumoqing/macosx_tts",
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers = [
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
	],
)
