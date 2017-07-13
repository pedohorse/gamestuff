from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector

class TurretComponent(Component):
	def __init__(self,gobj):
		super(TurretComponent,self).__init__(gobj)
		
		self.__shootProjectilesCount=1
		self.__shootRowCount=10
		self.__shootReloadTime=4
		self.__shootRowDelay=0.1
		
		self.__rowCounter=0
		self.__reloadTimer=0
		
	
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
		player=PlaneGameDirector.instance().getPlayer()
		if(player is None):return
		
		gobj.angle=gobj.transform.lookAtPointAngle(player.position)
		if(self.__reloadTimer>0):self.__reloadTimer-=dt
		else:
			baseangle=gobj.angle
			
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