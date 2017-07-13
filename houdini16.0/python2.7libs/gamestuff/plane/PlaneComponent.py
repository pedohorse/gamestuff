from gamestuff.Component import Component



class PlaneComponent(Component):
	def __init__(self,gobj):
		super(PlaneComponent,self).__init__(gobj)
		self.__trackedPoints=[]
		self.__shcomp=None
		self.__force=0
		self.__mass=1
		self.__tilt=0
		self.__backforce=0.5
	
	def onStart(self):
		self.__shcomp=self.gameObject().getComponent("ShapeComponent")
		self.__shcomp.setAnimated(True)
		self.__shcomp.setAnimationFrame(8) #for planes 8 is neutral state 0 is tilt left (screen), 16 is tilt right (screen)
		
	def setForce(self,force):
		self.__force=force
	
	def setMass(self,mass):
		self.__mass=mass
	
	def getTrackedPoints(self):
		return self.__trackedPoints
	
	def update(self):
		dt=self.time.deltaTime()
		self.__tilt=min(max(self.__tilt + self.__force/self.__mass * dt ,-1),1)
		if(self.__tilt>0):
			self.__tilt-=min(self.__tilt, ((self.__tilt>0) *2 -1)*self.__backforce/self.__mass *dt)
		else:
			self.__tilt-=max(self.__tilt, ((self.__tilt>0) *2 -1)*self.__backforce/self.__mass *dt)
		
		self.__shcomp.setAnimationFrame(round(8+self.__tilt*8))