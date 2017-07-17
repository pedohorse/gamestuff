from gamestuff.Component import Component
import hou

class SnekTailComponent(Component):
	def __init__(self,gobj):
		super(SnekTailComponent,self).__init__(gobj)
		self.__prevObj=None
		self.__tailOffset=0.25
		self.__alive=True
	
	def setAlive(self,alive):
		if(not isinstance(alive,bool)):return
		self.__alive=alive
	
	def getHead(self):
		return self.__prevObj
		
	def setHead(self,prevTailObj):
		self.__prevObj=prevTailObj
		#set node connection lol
		node=self.gameObject().getComponent("ShapeComponent").getHouNode()
		if(self.__prevObj is None):node.setFirstInput(None)
		else:
			prevNode=self.__prevObj.getComponent("ShapeComponent").getHouNode()
			node.setFirstInput(prevNode)
		
		
	def setTailOffset(self,offset):
		self.__tailOffset=offset
	
	def getTailOffset(self):
		return self.__tailOffset
	
	def update(self):
		super(SnekTailComponent,self).update()#totally not needed
		if(not self.__alive):return
		if(self.__prevObj is None):return
		
		gobj=self.gameObject()
		trailpart=self.__prevObj.getComponent("TrailComponent").getTrailByTime(self.__tailOffset)
		#trailpart=self.__prevObj.getComponent("TrailComponent").getTrailByDist(self.__tailOffset)
		#print(trailpart)
		gobj.position=trailpart[1]
		gobj.angle=trailpart[2]
		
	def onCollide(self,otherobj):
		if(self.time.time()<1):return
		gobj=self.gameObject()
		node=gobj.getComponent("ShapeComponent").getHouNode()
		node.setColor(hou.Color(1,1,0))