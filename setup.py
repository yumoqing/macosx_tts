try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

#with open('README.rst', 'r') as f:
#	long_description = f.read()

setup(
	name='macosx_tts',
	packages=['macosx_tts'],
	version='0.0.1',
	description='a pyttsx3 driver for ios device, it use AVFoundation.AVSpeechSynthesizer',
	long_description='',
	summary='pyttsx3 driver for ios device',
	author='Yu Moqing',
	url='https://github.com/yumoqing/macosx_tts',
	author_email='yumoqing@gmail.com',
	# install_requires=install_requires ,
	keywords=['pyttsx' , 'macosx', 'offline tts engine'],
	classifiers = [
		  'Intended Audience :: End Users/Desktop',
		  'Intended Audience :: Developers',
		  'Intended Audience :: Information Technology',
		  'Intended Audience :: System Administrators',
		  'Operating System :: OS Independent',
		  'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
		  'Programming Language :: Python :: 3'
	],
)
