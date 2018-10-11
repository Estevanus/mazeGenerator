import bge
import GameObjects


def setUpBlockAdder(cont):
	own = GameObjects.KX_BlockAdder(cont.owner)
	for i in cont.actuators:
		cont.activate(i)
	
def run(cont):
	cont.owner.run()