import pyaudio
import wave
from datetime import datetime


class recorder(pyaudio.PyAudio):
    def __init__(self):
        super(recorder, self).__init__()
        self.chunk = 5000  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 30000  # Record at 44100 samples per second
        self.filename = str(datetime.timestamp(datetime.today())) + ".wav"
        self.stream = self.open(format=self.sample_format,
                                channels=self.channels,
                                rate=self.fs,
                                frames_per_buffer=self.chunk,
                                input=True)
        self.frames = []

    def record(self):
        data = self.stream.read(self.chunk)
        self.frames.append(data)

    def done(self):
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
