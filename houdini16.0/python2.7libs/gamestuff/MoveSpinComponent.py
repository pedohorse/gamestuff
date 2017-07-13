from Component import Component
from hou import Vector2

class MoveSpinComponent(Component):
	def __init__(self,gobj):
		super(MoveSpinComponent,self).__init__(gobj)
		self.__lvel=Vector2()
		self.__avel=0
	
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
		gobj.position+=self.__lvel*dt
		gobj.angle+=self.__avel*dt
	
	def setVel(self,linvel,angvel):
		self.__lvel=linvel
		self.__avel=angvel