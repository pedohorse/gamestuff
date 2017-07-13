from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
from hou import Vector2

class PlaneBullet(Component):
	
	def __init__(self,gobj):
		super(PlaneBullet,self).__init__(gobj)
		self.__speed=10
		self.__active=True
		self.__shape=None
	
	def setActive(self,active):
		self.__active=active
		if(not self.__active):
			self.gameObject().position=Vector2(-15,0)
	
	def onStart(self):
		self.__shape=self.gameObject().getComponent("ShapeComponent")
			
	def setConfig(self, speed):
		self.__speed=speed
		
	def shapeShortcut(self):
		return self.__shape
	
	def update(self):
		if(not self.__active):return
		
		dt=self.time.deltaTime()
		gobj=self.gameObject()
		if(PlaneGameDirector.instance().isOutOfGameArea(gobj.position)):
			#gobj.destroy()#noo, no destroy - cache!
			self.cacheDelete()
			return
		gobj.position+=gobj.fwd()*self.__speed*dt
	
	def onCollide(self,other):
		if(not self.__active):return
		
		gobj=self.gameObject()
		PlaneGameDirector.instance().firePuff(gobj.position,gobj.angle+180,animSpeed=3)
		self.cacheDelete()
	
	def cacheDelete(self):
		self.setActive(False)
		PlaneGameDirector.instance()._bulletcache.insert(0,self)