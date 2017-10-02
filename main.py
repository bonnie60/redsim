from Controller import Controller
from Components.Base import *
from Components.Dust import *
from Components.Torch import *
from Components.Block import *
from Renderer import *
from array2gif import write_gif
from PIL import Image, ImageDraw, ImageFont
import scipy.misc as sp
import numpy as np
from Interface import Interface


size = 18
cont = Controller(size)
rend = Renderer(cont)
interface = Interface(cont)

for x in range(1, size-1):
    for z in range(1, size-1):
        interface.addDust(x, 0, z)

for x in range(2, size-2):
    for z in range(2, size-2):
        interface.addBlock(x, 0, z)

interface.addTorch(1, 0, 1).scheduleUpdate()


# Write to gif
runtime = 200
frames = []
emptyCount = 0
for i in range(runtime):
    cont.tick()
    data = rend.render(0)
    data = sp.imrotate(data, 180)
    data = np.fliplr(data)
    im = sp.toimage(data)
    drw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('DroidSansMono.ttf', 40)
    drw.text((1, 1), str(i), font=fnt, fill=(0, 0, 255, 255))
    data = sp.fromimage(im)
    frames.append(data)
    if not cont.toUpdate:
        emptyCount += 1
    else:
        emptyCount = 0
    if emptyCount > 3:
        break

rend.gif('output.gif', frames, fps=1)

