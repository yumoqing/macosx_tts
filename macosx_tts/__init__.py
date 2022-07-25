from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework, INCLUDE
load_framework(INCLUDE.AVFoundation)
load_framework('/System/Library/Frameworks/AppKit.framework')
load_framework('/System/Library/Frameworks/Foundation.framework')
from PyObjCTools import AppHelper
from pyttsx3.voice import Voice
NSTimer = autoclass('NSTimer')
NSString = autoclass('NSString')
NSArray = autoclass('NSArray')
NSObject = autoclass('NSObject')
NSSpeechSynthesizer = autoclass('NSSpeechSynthesizer')
AVSpeechSynthesizer = autoclass('AVSpeechSynthesizer')
NSURL = autoclass('NSURL')

def buildDriver(proxy):
	return MacosxSpeechDriver(proxy)


class MacosxSpeechDriver:
	def __init__(self, proxy):
		self._proxy = proxy
		self._tts = AVSpeechSynthesizer.alloc().init()
		self._tts.setDelegate_(self)
		# default rate
		self._tts.setRate_(200)
		self._completed = True

	def destroy(self):
		self._tts.setDelegate_(None)
		del self._tts

	def onPumpFirst_(self, timer):
		self._proxy.setBusy(False)

	def startLoop(self):
		pass

	def endLoop(self):
		pass

	def iterate(self):
		self._proxy.setBusy(False)
		yield

	def say(self, text):
		self._proxy.setBusy(True)
		self._completed = True
		self._proxy.notify('started-utterance')
		self._tts.startSpeakingString_(text)

	def stop(self):
		if self._proxy.isBusy():
			self._completed = False
		self._tts.stopSpeaking()

	def _toVoice(self, attr):
		try:
			lang = attr['VoiceLocaleIdentifier']
		except KeyError:
			lang = attr['VoiceLanguage']
		return Voice(attr['VoiceIdentifier'], attr['VoiceName'],
					 [lang], attr['VoiceGender'],
					 attr['VoiceAge'])

	def getProperty(self, name):
		if name == 'voices':
			return [self._toVoice(NSSpeechSynthesizer.attributesForVoice_(v))
					for v in list(NSSpeechSynthesizer.availableVoices())]
		elif name == 'voice':
			return self._tts.voice()
		elif name == 'rate':
			return self._tts.rate()
		elif name == 'volume':
			return self._tts.volume()
		elif name == "pitch":
			print("Pitch adjustment not supported when using NSSS")
		else:
			raise KeyError('unknown property %s' % name)

	def setProperty(self, name, value):
		if name == 'voice':
			# vol/rate gets reset, so store and restore it
			vol = self._tts.volume()
			rate = self._tts.rate()
			self._tts.setVoice_(value)
			self._tts.setRate_(rate)
			self._tts.setVolume_(vol)
		elif name == 'rate':
			self._tts.setRate_(value)
		elif name == 'volume':
			self._tts.setVolume_(value)
		elif name == 'pitch':
			print("Pitch adjustment not supported when using NSSS")
		else:
			raise KeyError('unknown property %s' % name)

	def save_to_file(self, text, filename):
		url = NSURL.fileURLWithPath_(filename)
		self._tts.startSpeakingString_toURL_(text, url)

	def speechSynthesizer_didFinishSpeaking_(self, tts, success):
		if not self._completed:
			success = False
		else:
			success = True
		self._proxy.notify('finished-utterance', completed=success)
		self._proxy.setBusy(False)

	def speechSynthesizer_willSpeakWord_ofString_(self, tts, rng, text):
		self._proxy.notify('started-word', location=rng.location,
						   length=rng.length)
