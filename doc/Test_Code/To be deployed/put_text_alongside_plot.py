# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4 * np.pi, 1000)  
y = 10 * np.sin(x)

fig, ax = plt.subplots(1, figsize=(6, 4.5))
ax.plot(x, y, "r")
ax.text(2.0, 9.5, "Peak Value",fontsize=14)

ax.grid(True)

plt.show()
