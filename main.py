from Controller import Controller
from Components.Base import *
from Components.Dust import *
from Components.Torch import *
from Components.Block import *
from Renderer import *
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

interface.addTorch(4, 0, 4, 3, 0, 4).scheduleUpdate()
interface.addDust(5, 0, 4)
interface.addTorch(6, 0, 5, 6, 0, 4)
interface.addDust(6, 0, 6)
interface.addDust(5, 0, 6)
interface.addBlock(4, 0, 6)
cont.scheduleUpdate(interface.addTorch(3, 0, 6, 4, 0, 6), 2)
interface.addDust(3, 0, 5)

cont.simulate(40, 'output.gif', fps=20)

