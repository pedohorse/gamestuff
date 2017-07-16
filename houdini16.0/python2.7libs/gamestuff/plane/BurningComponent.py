from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
import random

class BurningComponent(Component):
	def __init__(self,gobj):
		super(BurningComponent,self).__init__(gobj)
		
		self.__length=0.5
		self.__intensity=1
		self.__angleRotation=30
		self.__angleVariation=30
		
	def setConfig(self,length=None,intensity=None,angleRotation=None,angleVariation=None):
		if(length is not None):
			self.__length=length*0.5 #cuz it's really halflength
		if(intensity is not None):
			self.__intensity=intensity
		if(angleRotation is not None):
			self.__angleRotation=angleRotation
		if(angleVariation is not None):
			self.__angleVariation=angleVariation
	
	
	def update(self):
		gobj=self.gameObject()
		left=gobj.left()
		pos=gobj.position
		ang=gobj.angle
		
		for i in range(int(round(self.__intensity*2*self.__length))):
			t=random.uniform(-1,1)
			PlaneGameDirector.instance().firePuff(pos+t*left*self.__length,ang-self.__angleRotation*t+random.uniform(-1,1)*self.__angleVariation)
			