from gamestuff.Component import Component
from gamestuff.ShapeComponent import ShapeComponent
from hou import Vector2

class ExistingNodeShapeComponent(ShapeComponent):

	def __init__(self,gobj):
		Component.__init__(self,gobj)
		#super(ExistingNodeShapeComponent,self).__init__(gobj)
		self.__mynode=None
	
	def assignHouNode(self,node):
		if(self.__mynode is None or node is None):
			self.__mynode=node
		else:
			raise RuntimeError("this component already have an assigned node. please unassign first explicitly to avoid messups")
		
	def setColor(self,clr):
		'''
		here it shouldnt do anything
		'''
		pass
	
	def getHouNode(self):
		return self.__mynode
	
	def update(self):
		gobj=self.gameObject()
		
		pos=gobj.position
		self.__mynode.setPosition(pos)
		
	def onDestroy(self):
		self.__mynode.destroy()