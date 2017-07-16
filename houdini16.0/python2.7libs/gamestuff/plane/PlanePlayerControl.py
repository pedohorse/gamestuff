from gamestuff.Component import Component
from gamestuff.gameobject import GameObject
from PlaneGameDirector import PlaneGameDirector
from PySide2.QtCore import Qt #for keys
from hou import Vector2

class PlanePlayerControl(Component):
	
	def __init__(self,gobj):
		super(PlanePlayerControl,self).__init__(gobj)
		self.__plane=None
		self.__maxspeed=8
		self.__inertForce=20
		self.__speed=0
		self.__reloadtimer=0
		self.__invincibletimer=0
		self.__oldClr=None
		self.__lives=10
		self.__shape=None
	
	def setLives(self,lives):
		self.__lives=lives
		
	def lives(self):
		return self.__lives
	
	def setMaxspeed(self,maxspeed):
		self.__maxspeed=maxspeed
	
	def setInertForce(self,force):
		self.__inertForce=force
		
	def setSpeed(self,speed):
		self.__speed=speed
	
	def onStart(self):
		self.__plane=self.gameObject().getComponent("PlaneComponent")
		self.__plane.setMass(0.1)
		self.__shape=self.gameObject().getComponent("ShapeComponent")
		
		
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
		
		if(self.__invincibletimer>0):
			self.__invincibletimer-=dt
		if(self.__oldClr is None):
			if(self.__invincibletimer>0):
				self.__oldClr=self.__shape.getHouNode().color()
				self.__shape.setColor((1,0.5,0.5))
		else:
			self.__shape.setColor(self.__oldClr)
			self.__oldClr=None
		#keyboard check
		
		
		if(GameObject.isKeyDown(Qt.Key_Left)):
			self.__plane.setForce(-1)
			self.__speed-=self.__inertForce*dt
		elif(GameObject.isKeyDown(Qt.Key_Right)):
			self.__plane.setForce(1)
			self.__speed+=self.__inertForce*dt
		else:
			self.__plane.setForce(0)
			if(self.__speed>0):
				self.__speed-=min(self.__speed,self.__inertForce*dt)
			else:
				self.__speed+=min(-self.__speed,self.__inertForce*dt)
		
		if(self.__reloadtimer>0):self.__reloadtimer-=dt
		if(GameObject.isKeyDown(Qt.Key_Control) and self.__reloadtimer<=0):
			self.__reloadtimer=0.1
			PlaneGameDirector.instance().fireBullet(gobj.position+Vector2(-0.41,0.28),0,15,"player")
			PlaneGameDirector.instance().fireBullet(gobj.position+Vector2(0.41,0.28),0,15,"player")
			
		if(GameObject.isKeyPressed(Qt.Key_Space)):
			PlaneGameDirector.instance().explosion(Vector2(0,0))
		
		
		self.__speed=max(min(self.__speed,self.__maxspeed),-self.__maxspeed)
		
		gobj.position+=Vector2(self.__speed*dt,0)
		if(gobj.position[0]<-9.5):gobj.position[0]=-9.5
		elif(gobj.position[0]>9.5):gobj.position[0]=9.5
			
	
	def onCollide(self,other):
		if(self.__invincibletimer>0):return
		self.__lives-=1
		PlaneGameDirector.instance().playerHit(self.__lives)
		if(self.__lives<=0):
			self.gameObject().destroy()
			PlaneGameDirector.instance().bigExplosion(self.gameObject().position,time=4,jitterShape="plane_plane_8")
			PlaneGameDirector.instance().playerDied()
			
		self.__invincibletimer=2.0