from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
from hou import Vector2

class BossPartComponent(Component):
	def __init__(self,gobj):
		super(BossPartComponent,self).__init__(gobj)
		self.__active=False
		self.__lives=1
		self.__oldClr=None
		self.__shape=None
		self.__exradius=1
		self.__excenter=Vector2()
	
	
	def onStart(self):
		gobj=self.gameObject()
		if(self.__shape is None):
			self.__shape=gobj.getComponent("ShapeComponent")
		bbc=gobj.getComponent("BoundingBoxComponent")
		(bbmin,bbmax)=bbc.getInitBBox()
		self.__exradius=0.5*max(bbmax-bbmin)
		self.__excenter=0.5*(bbmin+bbmax)
	
	
	def setLives(self,lives):
		self.__lives=lives
	
	
	def setActive(self,active):
		self.__active=active
		
	
	def onCollide(self,other):
		if(not self.__active):return
		
		self.__lives-=1
		if(self.__oldClr is None):
			self.__oldClr=self.__shape.getHouNode().color()
			self.__shape.setColor((1,1,1))
		if(self.__lives<=0):
			self.gameObject().destroy()
	
	def onDestroy(self):
		if(self.__lives<=0):
			gobj=self.gameObject()
			core=gobj.transform.parent().gameObject()
			core.sendMessage("partDestroyed",gobj)
			
			for tr in gobj.transform.children():
				print(tr.gameObject().getName())
				tr.gameObject().destroy()
			
			ex=PlaneGameDirector.instance().bigExplosion(gobj.position,jitterShape=self.__shape.getBaseShape())
			ex.getComponent("BigExplosionComponent").setExplosionParams(self.__exradius,self.__excenter)
			ex.transform.setParent(gobj.transform.parent())
	
	
	def update(self):
		gobj=self.gameObject()
		if(self.__oldClr is not None):
			self.__shape.setColor(self.__oldClr)
			self.__oldClr=None