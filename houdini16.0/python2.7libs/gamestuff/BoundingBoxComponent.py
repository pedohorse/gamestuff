from BaseColliderComponent import BaseColliderComponent
from math import *
import hou

class BoundingBoxComponent(BaseColliderComponent):
	def __init__(self,gobj):
		super(BoundingBoxComponent,self).__init__(gobj)
		self.__bbmin=hou.Vector2()
		self.__bbmax=hou.Vector2()
		
		self.__chc_pos=hou.Vector2()
		self.__chc_ang=0
		self.__chc_chg=True
		
		try:
			self.readjust() #Shape component must be added before this
		except Exception:
			pass
		
		
	def readjust(self,restShapePostfix="0",restOppositeShapePostfix="8"):
		gobj=self.gameObject()
		shcomp=gobj.getComponent("ShapeComponent")
		#baseshape=shcomp.getBaseShape()
		node=shcomp.getHouNode()
		ne=hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
		if(ne is None):return
		
		curShape=node.userData("nodeshape")
		
		rect=None
		rect2=None
		divizor=-1
		if(curShape is not None):
			divizor=curShape.rfind("_")
		if(divizor!=-1 and restShapePostfix!="" and restOppositeShapePostfix!=""):
			baseshape=curShape[:divizor]
			
			node.setUserData("nodeshape","_".join([baseshape,restShapePostfix]))
			rect=ne.itemRect(node,False)
			node.setUserData("nodeshape","_".join([baseshape,restOppositeShapePostfix]))
			rect2=ne.itemRect(node,False)
		else:
			rect=ne.itemRect(node,False)
			rect2=rect
		
		if(curShape is not None):
			node.setUserData("nodeshape",curShape)
		
		#rect
		self.__bbmin=rect.min()
		self.__bbmax=rect.max()
		rect.enlargeToContain(rect2)
		rcenter=rect.center()		
		self.__bbmin-=rcenter
		self.__bbmax-=rcenter
		
		self._pivot=rcenter-node.position()
		
		self._radius2=max(self.__bbmin.lengthSquared(),self.__bbmax.lengthSquared())
		self._radius=sqrt(self._radius2)
		
		#print(self.__bbmin)
		#print(self.__bbmax)
	
	def offsetBbox(self,offsetmin,offsetmax=None):
		if(isinstance(offsetmin,int) or isinstance(offsetmin,float)):offsetmin=hou.Vector2((offsetmin,offsetmin))
		if(offsetmax is None):offsetmax=offsetmin
		else:
			if(isinstance(offsetmax,int) or isinstance(offsetmax,float)):offsetmax=hou.Vector2((offsetmax,offsetmax))
		size=self.__bbmax-self.__bbmin
		
		#the following restrictions are not covering cases of offset shifting beyond center! (legacy code)
		offsetmin[0]=min(size[0]*0.5 -0.000001,offsetmin[0])  #arbitrary tolerance
		offsetmin[1]=min(size[1]*0.5 -0.000001,offsetmin[1])  #arbitrary tolerance
		offsetmax[0]=min(size[0]*0.5 -0.000001,offsetmax[0])  #arbitrary tolerance
		offsetmax[1]=min(size[1]*0.5 -0.000001,offsetmax[1])  #arbitrary tolerance
		#offset=min(size[0]*0.5 -0.000001,size[1]*0.5 -0.000001,offset)
		self.__bbmin+=offsetmin
		self.__bbmax-=offsetmax
		
		self._radius2=max(self.__bbmin.lengthSquared(),self.__bbmax.lengthSquared())
		self._radius=sqrt(self._radius2)
	
	def getInitBBox(self):
		'''
		unclear... now it returns initial bbox, not bbox of current rotated shape
		should be renamed to getInitBBox
		'''
		return (self.__bbmin+self._pivot,self.__bbmax+self._pivot)
	
	def isPointInside(self,pointpos,offset=0):
		gobj=self.gameObject()
		pos=gobj.position
		ang=radians(gobj.angle)
		d=pointpos-pos
		if(d.lengthSquared()>self._radius2):return False
		
		co=cos(-ang)
		si=sim(-ang)
		xx=co*d[0]-si*d[1]
		yy=si*d[0]+co*d[1]
		
		isinside = xx>self.__bbmin[0]-offset and xx<self.__bbmax[0]+offset and yy>self.__bbmin[1]-offset and yy<self.__bbmax[1]+offset
		return isinside
	
	@classmethod
	def cross2d(cls,a,b):
		return a[0]*b[1]-a[1]*b[0]
	
	def getConvexHull(self):
		'''
		calculates and returns convex hull points for boxes
		it also tries to cache this shit
		returns mutable lists - plz dont fuck with them
		'''
		gobj=self.gameObject()
		if(not self.__chc_chg and self.__chc_pos==gobj.position and self.__chc_ang==gobj.angle):
			return self.__chc_pts
		pts=[hou.Vector2(self.__bbmin[0],self.__bbmin[1]),hou.Vector2(self.__bbmax[0],self.__bbmin[1]),hou.Vector2(self.__bbmax[0],self.__bbmax[1]),hou.Vector2(self.__bbmin[0],self.__bbmax[1])]
		rad=radians(gobj.angle)
		co=cos(rad)
		si=sin(rad)
		for pt in pts:
			x=pt[0]*co-pt[1]*si
			y=pt[0]*si+pt[1]*co
			pt[0]=x+gobj.position[0]+self._pivot[0] #TODO: if object is parented - figure out shit
			pt[1]=y+gobj.position[1]+self._pivot[1] #Looks like if shape was rotated not around 0,0 it's not valid for parenting at all !
			
		
		self.__chc_ang=gobj.angle
		self.__chc_pos=gobj.position
		self.__chc_chg=False
		self.__chc_pts=pts
		#print(self.__chc_pts)
		return self.__chc_pts
	
