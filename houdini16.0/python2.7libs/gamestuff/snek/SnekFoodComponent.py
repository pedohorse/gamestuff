from gamestuff.Component import Component
from hou import Color
from math import sin,radians

class SnekFoodComponent(Component):
	__totalfoodcount=0
	def __init__(self,gobj):
		super(SnekFoodComponent,self).__init__(gobj)
		SnekFoodComponent.__totalfoodcount+=1
		self.__clrtimer=0
		self.__shapenode=None
		
	def onStart(self):
		self.__shapenode=self.gameObject().getComponent("ShapeComponent")

	def onDestroy(self):
		SnekFoodComponent.__totalfoodcount-=1
		
	def onCollide(self,otherobj):
		self.gameObject().destroy()
	
	def update(self):
		self.__clrtimer=(self.__clrtimer+self.time.deltaTime())%1
		self.__shapenode.setColor(Color(sin(radians(self.__clrtimer*360)),sin(radians(self.__clrtimer*360+120)),sin(radians(self.__clrtimer*240))))
		
	
	@classmethod
	def totalFoodCount(cls):
		return cls.__totalfoodcount