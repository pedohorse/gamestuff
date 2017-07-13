from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
import random
from hou import Vector2

class ExplosionComponent(Component):
	clrs=[(0,0,0),(1,1,1),(1,0.988,0.647),(1,0.588,0),(0.654,0.5,0.325)]
	
	def __init__(self,gobj):
		super(ExplosionComponent,self).__init__(gobj)
		self.__shape=None
		self.__frame=0
		self.__timer=0.00
		self.__vel=Vector2()
		
	def onStart(self):
		gobj=self.gameObject()
		self.__shape=gobj.getComponent("ShapeComponent")
		self.__shape.setAnimated(True)
	
	def setVel(self,vel):
		self.__vel=vel
	
	def update(self):
		dt=self.time.deltaTime()
		gobj=self.gameObject()
		
		gobj.position+=self.__vel*dt
		vstep=PlaneGameDirector.instance().getGlobalVel()-self.__vel
		lvstep=vstep.length()
		if(lvstep>0):
			self.__vel+=min(10,lvstep)*(vstep/lvstep)*dt
		
		if(self.__timer<=0):
			if(self.__frame<4):
				self.__frame+=1
				self.__shape.setColor(ExplosionComponent.clrs[self.__frame])
				self.__timer=+0.04
				self.__shape.setAnimationFrame(self.__frame)
				
				if(self.__frame==2):
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,0  +random.uniform(-60,60),self.__vel,random.uniform(0.1,0.3))
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,120+random.uniform(-60,60),self.__vel,random.uniform(0.1,0.3))
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,240+random.uniform(-60,60),self.__vel,random.uniform(0.1,0.3))
				if(self.__frame==3):
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,0  +random.uniform(-90,90),self.__vel,random.uniform(0.1,0.3))
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,180+random.uniform(-90,90),self.__vel,random.uniform(0.1,0.3))
				if(self.__frame==4):
					PlaneGameDirector.instance().firePuff(gobj.position*1.0,0  +random.uniform(-180,180),self.__vel,random.uniform(0.1,0.3))
			else:
				gobj.destroy()
		self.__timer-=dt	
		
	