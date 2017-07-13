from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
from hou import Vector2
from math import *

class PlaneEvilSimple(Component):
	
	def __init__(self,gobj):
		super(PlaneEvilSimple,self).__init__(gobj)
		self.__linearVel=Vector2()
		self.__actualVel=Vector2()
		self.__sinAmp=0
		self.__sinFreq=0
		self.__sinOffset=0
		
		self.__plane=None
		self.__timer=0
		self.__lives=1
		self.__shooting=False
		self.__shootRowCount=1
		self.__shootProjectilesCount=1
		self.__shootSpreadHalfangle=20
		self.__shootRowDelay=0.1
		self.__shootReloadTime=4
		self.__shootAngle=180
		self.__reloadTimer=self.__shootReloadTime
		self.__rowCounter=0
		
		self.__shape=None
		self.__oldClr=None
		self.__destroyCallback=None
		
	def setConfig(self,linVel=None,sinAmp=None,sinFreq=None,sinOffset=None,lives=None,shooting=None,shootRowCount=None,projectilesCount=None,spreadHalfangle=None,shootRowDelay=None,shootReloadTime=None,shootAngle=None,destroyCallback=None):
		if(linVel is not None):self.__linearVel=linVel
		if(sinAmp is not None):self.__sinAmp=sinAmp
		if(sinFreq is not None):self.__sinFreq=sinFreq
		if(sinOffset is not None):self.__sinOffset=radians(sinOffset)
		if(lives is not None):self.__lives=lives
		if(shooting is not None):self.__shooting=shooting
		if(shootRowCount is not None):self.__shootRowCount=shootRowCount
		if(projectilesCount is not None):self.__shootProjectilesCount=projectilesCount
		if(spreadHalfangle is not None):self.__shootSpreadHalfangle=spreadHalfangle
		if(shootRowDelay is not None):self.__shootRowDelay=shootRowDelay
		if(shootReloadTime is not None):
			self.__shootReloadTime=shootReloadTime
			self.__reloadTimer=self.__shootReloadTime
		if(shootAngle is not None):self.__shootAngle=shootAngle
		if(destroyCallback is not None):self.__destroyCallback=destroyCallback
	
	
	
	def onCollide(self,other):
		self.__lives-=1
		self.__oldClr=self.__shape.getHouNode().color()
		self.__shape.setColor((1,1,1))
		if(self.__lives<=0):
			self.gameObject().destroy()
	
	def onDestroy(self):
		if(self.__lives<=0):
			gobj=self.gameObject()
			if(self.__destroyCallback is not None):
				self.__destroyCallback(pos=gobj.position,vel=self.__actualVel,jitterShape=self.__shape.getBaseShape()+"_8")
				#PlaneGameDirector.instance().explosion
	
	def onStart(self):
		self.__plane=self.gameObject().getComponent("PlaneComponent")
		self.__plane.setMass(0.1)
		self.__shape=self.gameObject().getComponent("ShapeComponent")
	
	def setShapeMass(self,mass):
		self.__plane.setMass(mass)
	
	def update(self):
		gobj=self.gameObject()
		if(self.__oldClr is not None):
			self.__shape.setColor(self.__oldClr)
			self.__oldClr=None
		
		if(PlaneGameDirector.instance().isOutOfGameArea(gobj.position)):
			gobj.destroy()
			return
		
		
		dt=self.time.deltaTime()
		self.__timer+=dt
		
		if(self.__shooting):
			if(self.__reloadTimer>0):self.__reloadTimer-=dt
			else:
				baseangle=self.__shootAngle
				if(baseangle==-1):
					pass
					#means we are targeting player
					#TODO: do
				if(self.__shootProjectilesCount==1):
					PlaneGameDirector.instance().fireBullet(gobj.position,baseangle,10,"enemy",(1,0.35,0.35))
				else:
					angstep=2*self.__shootSpreadHalfangle/(self.__shootProjectilesCount-1)
					for i in range(self.__shootProjectilesCount):
						PlaneGameDirector.instance().fireBullet(gobj.position,baseangle-self.__shootSpreadHalfangle+i*angstep,10,"enemy",(1,0.35,0.35))
				#do shoot here
				self.__rowCounter+=1
				if(self.__rowCounter>=self.__shootRowCount):
					self.__reloadTimer=self.__shootReloadTime
					self.__rowCounter=0
				else:
					self.__reloadTimer+=self.__shootRowDelay
					
		
		sid=self.__sinFreq*cos(self.__sinFreq*self.__timer + self.__sinOffset)
		
		self.__actualVel=(Vector2(self.__sinAmp*sid,0)+self.__linearVel)
		gobj.position+=self.__actualVel*dt
		self.__plane.setForce(sid)