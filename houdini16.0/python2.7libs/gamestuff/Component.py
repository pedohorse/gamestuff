import gameobject

class Component(object):
	
	
	def __init__(self,gobj):
		self.__gameObject=gobj
		self.time=gameobject.GameObject.TimeData(0,0)
		
	def gameObject(self):
		return self.__gameObject
	
	def onStart(self):
		pass
	
	def update(self):
		pass
		
	def onDestroy(self):
		pass