from pyobjus import autoclass, protocol
from pyobjus.dylib_manager import load_framework, INCLUDE
load_framework(INCLUDE.AVFoundation)
load_framework('/System/Library/Frameworks/AppKit.framework')
load_framework('/System/Library/Frameworks/Foundation.framework')
from unitts.basedriver import BaseDriver
from unitts.voice import Voice
NSTimer = autoclass('NSTimer')
NSString = autoclass('NSString')
NSArray = autoclass('NSArray')
NSObject = autoclass('NSObject')
NSSpeechSynthesizer = autoclass('NSSpeechSynthesizer')
AVSpeechSynthesizer = autoclass('AVSpeechSynthesizer')
NSURL = autoclass('NSURL')
from .version import __version__

def buildDriver(proxy):
	return MacosxSpeechDriver(proxy)

def language_by_lang(lang):
	langs = {
		'zh':'zh_CN',
		'en':'en_US',
	}
	return langs.get(lang, 'zh_CN')

class MacosxSpeechDriver(BaseDriver):
	def __init__(self, proxy):
		super().__init__(proxy)
		self._tts = NSSpeechSynthesizer.alloc().init()
		self._tts.delegate = self
		# default rate
		self._tts.setRate_(200)
		self.rate = 200
		self.volume = 1
		self._completed = True
		print(f'mac os x TTS driver version {__version__}')

	def get_voice_by_lang(self, lang):
		language = language_by_lang(lang)
		for v in self.voices:
			if language in v.languages:
				print(v.id, lang)
				return v.id
		print('no voice found for', lang)

	def get_voices(self):
		voices = NSSpeechSynthesizer.availableVoices()
		# print(type(voices), dir(voices))
		x = [ self._toVoice(NSSpeechSynthesizer.attributesForVoice_(voices.objectAtIndex_(i))) 
					for i in range(voices.count()) ]
		self.voices = x
		return x

	def isSpeaking(self):
		return self._tts.isSpeaking()

	def destroy(self):
		self._tts.setDelegate_(None)
		del self._tts

	def set_type_voice(self, sentence):
		print('set_type_voice() called')
		attrs = self.normal_voice
		if sentence.dialog:
			attrs = self.dialog_voice
		y = self._tts
		rate = float(attrs.get('rate', self.rate))
		print('rate=', rate, type(rate))
		y.setRate_(rate)
		y.setVolume_(attrs.get('volume', self.rate))
		voice = self.get_voice_by_lang(sentence.lang)
		self.setProperty('voice', voice)
		
	def pre_command(self, sentence):
		# super().pre_command(sentence)
		return sentence.sentence_id, sentence

	def command(self, pos, sentence):
		text = sentence.text
		self.set_type_voice(sentence)
		print('command():', pos, text, len(text))
		self._tts.startSpeakingString_(text)
		
	def stop(self):
		if self._proxy.isBusy():
			self._completed = False
		self._tts.stopSpeaking()

	def nss2s(self, nsobj):
		x = nsobj.UTF8String()
		if isinstance(x, str):
			return x
		return x.decode('utf-8')

	def _toVoice(self, attr):
		try:
			lang = self.nss2s(attr.valueForKey_('VoiceLocaleIdentifier'))
		except KeyError:
			lang = self.nss2s(attr.valueForKey_('VoiceLanguage'))
		return Voice(self.nss2s(attr.valueForKey_('VoiceIdentifier')), 
						self.nss2s(attr.valueForKey_('VoiceName')),
					 [lang], attr.valueForKey_('VoiceGender'),
					 attr.valueForKey_('VoiceAge').intValue())

	def getProperty(self, name):
		if name == 'voices':
			return self.get_voices()

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
			vol = self._tts.volume
			rate = self._tts.rate
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

	@protocol('NSSpeechSynthesizerDelegate')
	def speechSynthesizer_willSpeakWord_ofString_(self,  *args):
		print('speechSynthesizer_willSpeakWord_of_(), args=',args)

	@protocol('NSSpeechSynthesizerDelegate')
	def speechSynthesizer_didFinishSpeaking_(self, *args):
		print('speechSynthesizer_didFinish_():args=', args)
		self.speak_finish()
		self._proxy.setBusy(False)

