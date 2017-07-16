from gamestuff.gameobject import GameObject
from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
import random
from hou import Vector2
from math import *

class AssfireComponent(Component):
	
	def __init__(self,gobj):
		super(AssfireComponent,self).__init__(gobj)
		self.__timer=0
		self.__shape=None
		self.__gomeds=None
		self.__gohigs=None
		
		self.__bbmin=Vector2()
		self.__bbmax=Vector2()
		self.__mode=0
		self.__ot1=0.0
		self.__ot2=0.0
		
		
	def onStart(self):
		gobj=self.gameObject()
		self.__shape=gobj.getComponent("ShapeComponent")
		if(self.__shape is None):
			self.__shape=gobj.addComponent("ShapeComponent")
		self.__shape.setBaseShape("big_boss_assfirelow")
		self.__shape.setAnimated(True)
		
		gm=GameObject("killzone_enemy_m")
		gm.transform.setParent(gobj.transform,False)
		gm.transform.localPosition=Vector2((0,-50))
		self.__gomeds=gm.addComponent("ShapeComponent")
		self.__gomeds.setBaseShape("big_boss_assfiremed")
		self.__gomeds.setAnimated(True)
		gm.addComponent("BoundingBoxComponent").readjust("0","0")
		
		
		gh=GameObject("killzone_enemy_h")
		gh.transform.setParent(gobj.transform,False)
		gh.transform.localPosition=Vector2((0,-50))
		self.__gohigs=gh.addComponent("ShapeComponent")
		self.__gohigs.setBaseShape("big_boss_assfirehig")
		self.__gohigs.setAnimated(True)
		gh.addComponent("BoundingBoxComponent").readjust("0","0")
		
		
		#self.__shapem=self.gameObject().addComponent("ShapeComponent")
		#self.__shapem.setBaseShape("big_boss_assfirelow")
		#self.__shapem.setAnimated(True)
		
		#self.__shapeh=self.gameObject().addComponent("ShapeComponent")
		#self.__shapeh.setBaseShape("big_boss_assfirelow")
		#self.__shapeh.setAnimated(True)
		
		bbx=self.gameObject().getComponent("BoundingBoxComponent")
		if(bbx is None):
			bbx=self.gameObject().addComponent("BoundingBoxComponent")
		bbx.readjust("0","0")
		(self.__bbmin,self.__bbmax)=bbx.getInitBBox()
		
	
	def setFlameMode(self,mode):
		if(self.__gomeds is None or type(mode) is not int or mode==self.__mode or mode<0 or mode>3):return
		if(mode==0):
			self.__gomeds.gameObject().transform.localPosition=Vector2((0,-50))
			self.__gohigs.gameObject().transform.localPosition=Vector2((0,-50))
		elif(mode==1):
			self.__gomeds.gameObject().transform.localPosition=Vector2((0,0))
			self.__gohigs.gameObject().transform.localPosition=Vector2((0,-50))
		elif(mode==2):
			self.__gomeds.gameObject().transform.localPosition=Vector2((0,0))
			self.__gohigs.gameObject().transform.localPosition=Vector2((0,0))
		self.__mode=mode
	
	def __getColor(self,t,ttcor=0):
		rgb1=(1,0.16,0.1176)
		rgb2=(1,0.851,0.1176)
		a=0.8
		tt=0.75+0.25*(sin(t)+a*sin(t*2+1.231451)+a*a*sin(t*4+3.28172)+a*a*a*sin(t*8+1.816728)+a*a*a*a*sin(t*16+7.9626964))/(a*(1+a*(1+a*(1+a))))
		tt=min(1,max(0,tt+ttcor))
		return (rgb1[0]*(1-tt) + rgb2[0]*tt,rgb1[1]*(1-tt) + rgb2[1]*tt,rgb1[2]*(1-tt) + rgb2[2]*tt)
		
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
		self.__timer+=dt
		
		af=round(self.__timer/0.04)%6
		self.__shape.setAnimationFrame(af)
		self.__gomeds.setAnimationFrame(af)
		self.__gohigs.setAnimationFrame(af)
		
		t=self.time.time()*2
		
		self.__shape.setColor(self.__getColor(t))
		self.__gomeds.setColor(self.__getColor(self.__ot1,-0.2))
		self.__gohigs.setColor(self.__getColor(self.__ot2,-0.4))
		self.__ot2=self.__ot1
		self.__ot1=t
		
		for i in range(2):
			pos=Vector2((random.uniform(self.__bbmin[0],self.__bbmax[0]),random.uniform(self.__bbmin[1],self.__bbmax[1]))) + gobj.position
			PlaneGameDirector.instance().firePuff(pos,random.uniform(0,360))
			