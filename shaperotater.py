import sys
import os
import json
from math import *

def rotate(jsondata,angle,center=None):
	angle=radians(angle)
	icon=jsondata["icon"]
	if(center is None):
		center=[(icon[0][0]+icon[1][0])*0.5,(icon[0][1]+icon[1][1])*0.5]
	flags=jsondata["flags"]
	for i in range(4):
		rotatepts(flags[str(i)]["outline"],angle,center)
	rotatepts(jsondata["outline"],angle,center)
	rotateicon(icon,angle,center)
	rotatepts(jsondata["inputs"],angle,center)
	rotatepts(jsondata["outputs"],angle,center)
	
def rotateicon(icon,rads,center):
	si=sin(rads)
	co=cos(rads)
	iconcenter=[(icon[0][0]+icon[1][0])*0.5,(icon[0][1]+icon[1][1])*0.5]
	il=[[],[]]
	il[0]=[icon[0][0]-iconcenter[0],icon[0][1]-iconcenter[1]]
	il[1]=[icon[1][0]-iconcenter[0],icon[1][1]-iconcenter[1]]
	
	x=iconcenter[0]-center[0]
	y=iconcenter[1]-center[1]
	
	x1=x*co-y*si +center[0]
	y1=x*si+y*co +center[1]
	#round up values
	iconcenter[0]=floor(x1*10000)/10000;
	iconcenter[1]=floor(y1*10000)/10000;
	
	icon[0][0]=iconcenter[0]+il[0][0]
	icon[0][1]=iconcenter[1]+il[0][1]
	icon[1][0]=iconcenter[0]+il[1][0]
	icon[1][1]=iconcenter[1]+il[1][1]
	
def rotatepts(pts,rads,center):
	si=sin(rads)
	co=cos(rads)
	for pt in pts:
		x=pt[0]-center[0]
		y=pt[1]-center[1]
		if(len(pt)==3):
			pt[2]+=degrees(rads)
		x1=x*co-y*si +center[0]
		y1=x*si+y*co +center[1]
		#round up values
		pt[0]=floor(x1*10000)/10000;
		pt[1]=floor(y1*10000)/10000;
		
	
def main():
	if(len(sys.argv)<2):
		print("need 1 json in")
		return
	fname=sys.argv[1]
	with open(fname,"r") as file:
		data=json.load(file)
	
	center=None
	if(len(sys.argv)>=4):center=[float(sys.argv[2]),float(sys.argv[3])]
	fnamesplit=os.path.splitext(fname)
	origname=data["name"]
	for i in range(16):
		data["name"]=origname+"_"+str(i)
		
		
		wfname=fnamesplit[0]+"_"+str(i)+fnamesplit[1]
		with open(wfname,"w") as file:
			json.dump(data,file)
			
		rotate(data,22.5,center)
		
if(__name__=="__main__"):
	main()