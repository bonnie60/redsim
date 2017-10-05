from Controller import Controller
from Components.Base import *
from Components.Dust import *
from Components.Torch import *
from Components.Block import *
from Renderer import *
from Interface import Interface


size = 18
cont = Controller.Controller(size)
interface = Interface(cont)

# XOR Gate
interface.addBlock(0, 0, 0)
interface.addBlock(1, 0, 0)
interface.addBlock(2, 0, 0)
interface.addBlock(1, 0, 1)
interface.addBlock(0, 0, 3)
interface.addBlock(2, 0, 3)

interface.addTorch(0, 1, 0)
interface.addTorch(2, 1, 0)
interface.addTorch(0, 0, 1, 0, 0, 0)
interface.addTorch(2, 0, 1, 2, 0, 0)
interface.addTorch(1, 0, 2, 1, 0, 1)
interface.addTorch(0, 0, 4, 0, 0, 3)
interface.addTorch(2, 0, 4, 2, 0, 3)

interface.addDust(1, 1, 0)
interface.addDust(1, 1, 1)
interface.addDust(0, 0, 2)
interface.addDust(2, 0, 2)
interface.addDust(0, 1, 3)
interface.addDust(2, 1, 3)
interface.addDust(1, 0, 4)

cont.simulate(40, 'output.gif', fps=20)

