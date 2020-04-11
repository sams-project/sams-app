import sounddevice as sd
from numpy import median


class MicrophoneHelper:
    @staticmethod
    def get_fft_data():
        fs = int(16000)

        try:
            audiodata = sd.rec(int(3) * fs, samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            if median(data[0]) == 0:
                return False
            else:
                return True

        except Exception as e:
            print(e)
            return False
