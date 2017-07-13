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

	def setMaxspeed(self,maxspeed):
		self.__maxspeed=maxspeed
	
	def setInertForce(self,force):
		self.__inertForce=force
		
	def setSpeed(self,speed):
		self.__speed=speed
	
	def onStart(self):
		self.__plane=self.gameObject().getComponent("PlaneComponent")
		self.__plane.setMass(0.1)
		#print("found "+str(self.__plane))
		
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
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
			
		