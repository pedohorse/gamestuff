from Component import Component
import hou

class DebugBboxComponent(Component):
	def __init__(self,gobj):
		super(DebugBboxComponent,self).__init__(gobj)
		
	def update(self):
		gobj=self.gameObject()
		bbx=gobj.getComponent("BaseColliderComponent")
		objs=[x for x in gobj.findObjects(".*") if x is not gobj]
		node=gobj.getComponent("ShapeComponent").getHouNode()
		clr=hou.Color(1,1,1)
		for obj in objs:
			if bbx.collidesWith(obj):
				clr=hou.Color(1,0,0)
				break
		node.setColor(clr)
				