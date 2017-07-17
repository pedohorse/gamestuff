from gamestuff.Component import Component
from gamestuff import gameobject
from PySide2.QtCore import Qt #for keys
from hou import Vector2

class SnekHeadComponent(Component):
	def __init__(self,gobj):
		super(SnekHeadComponent,self).__init__(gobj)
		self.__targetangle=0.0
		self.__rotpausetimer=0
		self.__speed=2
		self.__taillist=[]
		self.__alive=True
		self.__invincibleTimer=1;
		self.__frame=0
		self.__animfwd=True
		self.__shape=None
	
	def onStart(self):
		if(self.__shape==None):
			self.__shape=self.gameObject().getComponent("ShapeComponent")
		self.__shape.setAnimated(True)
		
	
	def setAlive(self,alive):
		if(not isinstance(alive,bool)):return
		self.__alive=alive
		for tail in self.__taillist:
			tail.setAlive(alive)
	
	def addControllableTailObjects(self,objlist):
		cmps=[]
		for obj in objlist:
			cmp=obj.getComponent("SnekTailComponent")
			if(cmp is not None):cmps.append(cmp)
			
		self.__taillist.extend(cmps)
		self.updateTailSpeed()
		
	def getSpeed(self):
		return self.__speed
	
	def setSpeed(self,speed):
		self.__speed=speed
		self.updateTailSpeed()
		
	def updateTailSpeed(self):
		for tail in self.__taillist:
			if(self.__speed!=0):
				tail.setTailOffset(0.7/self.__speed**1.3) #it's time offset,
			else:
				tail.setTailOffset(0)
	
	def update(self):
		super(SnekHeadComponent,self).update()#this is super not needed
		if(not self.__alive):return
		dt=self.time.deltaTime()
		
		if(self.__invincibleTimer>0):self.__invincibleTimer-=dt
		
		if(self.__animfwd):
			self.__frame+=1
		else:
			self.__frame-=1
		if(self.__frame==2 or self.__frame==0):self.__animfwd=not self.__animfwd
		self.__shape.setAnimationFrame(self.__frame)
		
		gobj=self.gameObject()
		ang=gobj.angle
		
		gobj.position+=self.__speed*gobj.fwd()*dt
		
		dang=self.__targetangle-gobj.angle
		if(dang>180):dang-=360
		elif(dang<-180):dang+=360
		
		angstep=720*dt
		gobj.angle+=max(min(dang,angstep),-angstep)
		
		if(self.__rotpausetimer<=0):
			pausetime=0.2
			if(gobj.isKeyDown(Qt.Key_Down) and self.__targetangle!=0):
				self.__targetangle=180
				self.__rotpausetimer=pausetime
			
			if(gobj.isKeyDown(Qt.Key_Up) and self.__targetangle!=180):
				self.__targetangle=0
				self.__rotpausetimer=pausetime
				
			if(gobj.isKeyDown(Qt.Key_Left) and self.__targetangle!=270):
				self.__targetangle=90
				self.__rotpausetimer=pausetime
				
			if(gobj.isKeyDown(Qt.Key_Right) and self.__targetangle!=90):
				self.__targetangle=270
				self.__rotpausetimer=pausetime
			
			if(gobj.isKeyDown(Qt.Key_1)):
				self.setSpeed(self.getSpeed()-0.05)
				
			if(gobj.isKeyDown(Qt.Key_2)):
				self.setSpeed(self.getSpeed()+0.05)
				
			if(gobj.isKeyDown(Qt.Key_4)):
				self.grow()
			
		else:
			self.__rotpausetimer-=dt
		
		#check bounds
		pos=gobj.position
		if(pos[0]<-10 or pos[0]>10-1 or pos[1]<-10+1 or pos[1]>10):
			self.loose()

	def grow(self):
		#assume we have nonzero tail
		gobj=self.gameObject()
		ftail=[x.gameObject() for x in self.__taillist if x.getHead()==gobj][0]
		ftailstc=ftail.getComponent("SnekTailComponent")
		
		g=gameobject.GameObject()
		g.setName(ftail.getName())
		g.position=ftail.position+Vector2()
		g.angle=ftail.angle
		
		shp=g.addComponent("ShapeComponent")
		shp.setBaseShape("snek_torso")
		shp.setColor((0.2,0.5,0.15))		
		
		g.addComponent("TrailComponent")
		stc=g.addComponent("SnekTailComponent")
		stc.setHead(gobj)
		stc.setTailOffset(ftailstc.getTailOffset())
		ftailstc.setHead(g)
		
		g.addComponent("BoundingBoxComponent")
		#g.addComponent("DebugBboxComponent")
		
		self.addControllableTailObjects([g])
		
	def loose(self):
		self.setAlive(False)
		gdir=self.gameObject().findObject("DIRECTOR")
		if(gdir is not None):
			gdir.sendMessage("snekDied")
	
	def onCollide(self,otherobj):
		if(not self.__alive):return
		
		if(otherobj.getComponent("SnekFoodComponent") is not None):
			self.grow()
			self.setSpeed(self.getSpeed()+0.1)
			gdir=self.gameObject().findObject("DIRECTOR")
			if(gdir is not None):
				gdir.sendMessage("snekAte")
				
		elif(self.__invincibleTimer<=0 and otherobj in [x.gameObject() for x in self.__taillist]):
			self.loose()