from Component import Component
import hou

class ActiveCollisionCheckerComponent(Component):
	def __init__(self,gobj):
		super(ActiveCollisionCheckerComponent,self).__init__(gobj)
		self.__dodebug=False
		self.__collisionmask=".*"
		
	def setCollisionMask(self,mask):
		#todo: check mask re here
		self.__collisionmask=mask
		
	def update(self):
		gobj=self.gameObject()
		bbx=gobj.getComponent("BaseColliderComponent")
		objs=[x for x in gobj.findObjects(self.__collisionmask) if x is not gobj]
		node=gobj.getComponent("ShapeComponent").getHouNode()
		clr=hou.Color(1,1,1)
		for obj in objs:
			if bbx.collidesWith(obj):
				gobj.sendMessage("onCollide",obj)
				obj.sendMessage("onCollide",gobj)
				clr=hou.Color(1,0,0)
				#break #DA FUCK IS THIS BREAK HERE???
		if(self.__dodebug):
			node.setColor(clr)
				