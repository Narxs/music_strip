import numpy as np
import matplotlib.pyplot as plt

a = 1
pi = np.pi
x = np.linspace(0, 2*pi, 1000)

input = np.sin(x) + np.sin(10*x)

output = np.abs(np.fft.rfft(input))

plt.plot(input)
plt.plot(output, marker='+')
plt.show()