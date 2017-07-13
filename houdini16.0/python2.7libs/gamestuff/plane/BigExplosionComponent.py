from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
import random
from hou import Vector2

class BigExplosionComponent(Component):
	def __init__(self,gobj):
		super(BigExplosionComponent,self).__init__(gobj)
		
		self.__timer=0
		self.__delayTimer=0
		self.__delayTime=0.02
		self.__radius=1 #actually, not radius, but half square side for now
		self.__shape=None
		
		
	def setTimer(self,time):
		self.__timer=time
		
	def setJitterShape(self,shape):
		gobj=self.gameObject()
		self.__shape=gobj.getComponent("ShapeComponent")
		if(self.__shape is None):
			self.__shape=gobj.addComponent("ShapeComponent")
		self.__shape.setBaseShape(shape)
		self.__shape.setColor((0,0,0))
		self.__flipclr=False
	

	def setExplosionParams(self,radius=None,offset=None):
		if(radius is not None):
			self.__radius=radius
		if(offset is not None):
			self.__offset=offset*1 #to ensure no refs. fuck this Vector2, fuck people who designed it to be mutable
		
	def update(self):
		if(self.__timer<=0):
			self.gameObject().destroy()
			return
		if(self.__shape is not None):
			self.__flipclr=not self.__flipclr
			if(self.__flipclr):
				self.gameObject().position+=Vector2(0.05,0)
				self.__shape.setColor((1,1,1))
			else:
				self.gameObject().position-=Vector2(0.05,0)
				self.__shape.setColor((0,0,0))
				
			
		dt=self.time.deltaTime()
		self.__timer-=dt
		if(self.__delayTimer<=0):
			gobj=self.gameObject()
			for i in range(2):
				pos=gobj.position+self.__offset+Vector2(random.uniform(-self.__radius,self.__radius),random.uniform(-self.__radius,self.__radius))
				PlaneGameDirector.instance().explosion(pos)
			self.__delayTimer=self.__delayTime
		else:
			self.__delayTimer-=dt