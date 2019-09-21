import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import sounddevice as sd

def fft_generator(wavsamples, samples_per_fft,samplerate):
    i = 0
    length = 2* samples_per_fft - 1
    start_time = time.time()

    while True:
        if (i + 1) * length > len(wavsamples):
            break
        samples = wavsamples[i*length: (i + 1)*length]
        output = np.abs(np.fft.rfft(samples)[:144])

        assert len(output) == 144, f"got length {len(output)}"
        t = i*length/samplerate

        yield output, t, start_time

        i += 1

    return

update_rate = 120

music = 'bensound-evolution.wav'

data, samplerate = sf.read(music)
if data.ndim == 1:
    pass
else:
    data = data[:, 0]

assert data.ndim == 1 #make sure dimensions are ok :)

samples_per_fft = samplerate//update_rate

assert samples_per_fft >= 144*2

fig, ax = plt.subplots()

start = time.time()

ax.set_ylim(-10, 250)

line, = ax.plot(np.zeros(144))
text = ax.text(60, 120, "{:.2f}".format(0))


def draw(frame, *fargs):

    data, t, start_time = frame
    line.set_ydata(data)
    text.set_text("{:.2f}, {:.2f}".format(t, time.time() - start_time))
    return line, text


sd.play(data, samplerate)

def data_2_arduino(data):
    print(data)

for n in fft_generator(data, samples_per_fft,samplerate):
    data_2_arduino(data)

print(time.time() - start, 1/update_rate)

funcanimation = FuncAnimation(fig, draw, iter(fft_generator(data, samples_per_fft,samplerate)), interval=1000/update_rate, repeat=False)

plt.show()



