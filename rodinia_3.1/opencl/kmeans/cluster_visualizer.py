#!/usr/bin/python
# Cluster Visualizer, Yeseong Kim, UCSD, 2017

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib as mpl

class_colors = [
	"#ffcc00",
	"#b9341b",
	"#2b90f5",
	"#55b64e",
	"#00ffff",
	"#d3b7d6",
	"#a389c1",
	"#feebc9",
	"#e0f3b0",
	"#bfd5e8",
	"#fddeee",
	"#fca985",
	"#85ca5d",
	"#7589bf",
	"#f98cb6",
	"#f0e8cd",
]

# BODY ----------------------------------------------------------------

if (len(sys.argv) < 2):
	print("python visualizer.py DATA_FILE [OUTPUT_IMAGE]")
	sys.exit()

data_filename = sys.argv[1]
img_filename = None
if len(sys.argv) == 3:
	img_filename = sys.argv[3]

# Read data
X = []
y = []
for line in open(data_filename):
    elems = line.split(",")
    print elems[0]
    print elems[1]
    X.append((float(elems[0]), float(elems[1])))
    y.append(int(elems[2]))


figure = plt.figure(figsize=(6, 6))

X = np.array(X)

# draw dataset plot
nClass = len(set(y))
color_list = class_colors[:nClass]
cm_bright = ListedColormap(color_list)

ax = plt.subplot(1, 1, 0)
ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cm_bright)
ax.axis([0,1,0,1])

if img_filename is not None:
	figure.savefig(img_filename)
plt.show()
