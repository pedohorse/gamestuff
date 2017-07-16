from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
from hou import Vector2

class FirePuffComponent(Component):
	clrs=[(1,0.988,0.647),(1,0.588,0),(0.596,0.596,0.596)]
	
	def __init__(self,gobj):
		super(FirePuffComponent,self).__init__(gobj)
		self.__shape=None
		self.__frame=0
		self.__timer=0.04
		self.__vel=Vector2()
		self.__active=True
		self.__animspeed=1.0
		
	def onStart(self):
		gobj=self.gameObject()
		self.__shape=gobj.getComponent("ShapeComponent")
		self.__shape.setAnimated(True)
		self.__shape.setColor(self.clrs[0])
	
	def shapeShortcut(self):
		return self.__shape
	
	def setVel(self,vel):
		self.__vel=vel
	
	def setAnimSpeed(self,speed):
		self.__animspeed=speed
	
	def setActive(self,active):
		self.__active=active
		if(self.__active):
			self.__shape.setColor(self.clrs[0])
			self.__frame=0
			self.__timer=0.04
			self.__shape.setAnimationFrame(self.__frame)
		else:
			self.gameObject().position=Vector2(-16,0)
	
	def update(self):
		if(not self.__active):return
		dt=self.time.deltaTime()
		gobj=self.gameObject()
		
		gobj.position+=self.__vel*dt
		vstep=PlaneGameDirector.instance().getGlobalVel()-self.__vel
		lvstep=vstep.length()
		if(lvstep>0):
			self.__vel+=min(10,lvstep)*(vstep/lvstep)*dt
			
		if(self.__timer<=0):
			if(self.__frame<16):
				self.__frame=min(self.__frame+self.__animspeed,16)
				clr=FirePuffComponent.clrs[2]
				ifr=int(round(self.__frame))
				if(ifr<5):
					t=ifr/7.0
					clrs=FirePuffComponent.clrs
					clr=(clrs[0][0]*(1-t)+clrs[1][0]*t,clrs[0][1]*(1-t)+clrs[1][1]*t,clrs[0][2]*(1-t)+clrs[1][2]*t)
				elif(ifr<8):
					t=(ifr-5)/3.0
					clrs=FirePuffComponent.clrs
					clr=(clrs[1][0]*(1-t)+clrs[2][0]*t,clrs[1][1]*(1-t)+clrs[2][1]*t,clrs[1][2]*(1-t)+clrs[2][2]*t)
				self.__shape.setColor(clr)
				self.__timer+=0.02
				self.__shape.setAnimationFrame(self.__frame)
				#do the color work here
			else:
				self.cacheDelete()
				#gobj.destroy()
		self.__timer-=dt	
		
	def cacheDelete(self):
		self.setActive(False)
		PlaneGameDirector.instance()._firepuffcache.insert(0,self)