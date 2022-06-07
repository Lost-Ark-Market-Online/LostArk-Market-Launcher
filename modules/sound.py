import sys
from threading import Thread
import simpleaudio as sa
import os
from pycaw.pycaw import AudioUtilities
from modules.common.singleton import Singleton
from modules.config import Config


class PlaySoundThread(Thread):
    def __init__(self, sound_file):
        Thread.__init__(self)
        self.sound_file = sound_file

    def run(self):
        self.playsound(self.sound_file)

    def playsound(self, file):
        if VolumeController().audio == None:
            VolumeController().searchProcess()
        wave_obj = sa.WaveObject.from_wave_file(file)
        play_obj = wave_obj.play()
        play_obj.wait_done()


def playSuccess():
    PlaySoundThread(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../assets/sounds/mixkit-arcade-bonus-alert-767.wav"))).start()


def playUpdateDetected():
    PlaySoundThread(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../assets/sounds/mixkit-unlock-game-notification-253.wav"))).start()


def playError():
    PlaySoundThread(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../assets/sounds/mixkit-game-warning-quick-notification-267.wav"))).start()

def playDownloadComplete():
    PlaySoundThread(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../assets/sounds/mixkit-fantasy-game-success-notification-270.wav"))).start()


class VolumeController(metaclass=Singleton):
    audio = None
    volume = 1.0

    def __init__(self):
        self.searchProcess()
        
    def searchProcess(self):
        sessions = AudioUtilities.GetAllSessions()
        file_name = os.path.basename(sys.executable)
        
        for session in sessions:
            if session.Process and session.Process.name() == file_name:
                self.audio = session.SimpleAudioVolume
                self.volume = self.audio.GetMasterVolume()
                self.setVolume(Config().volume/100)
                break

    def setVolume(self, volume):
        if self.audio:
            self.audio.SetMasterVolume(volume, None)
        else:
            self.searchProcess()
