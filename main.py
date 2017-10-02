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

size = 18
cont = Controller(size)
rend = Renderer(cont)

for x in range(1, size-1):
    for z in range(1, size-1):
        comp = Dust(x, 0, z, cont)
        cont.components[x][0][z] = comp

for x in range(2, size-2):
    for z in range(2, size-2):
        comp = Block(x, 0, z, cont)
        cont.components[x][0][z] = comp

comp = Torch(1, 0, 1, cont)
cont.components[1][0][1] = comp
comp.scheduleUpdate()


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

