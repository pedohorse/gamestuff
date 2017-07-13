import os
import subprocess
import re
import time

def locateHoudini(ver=()):
	if(len(ver)==0):ver=(9999,0,9999)
	elif(len(ver)==1):ver=(ver[0],0,9999)
	elif(len(ver)==2):
		if(ver[1]<10):ver=(ver[0],ver[1],9999)
		else:ver=(ver[0],0,ver[1])
	elif(len(ver)>3):raise ValueError("version must have max 3 components")
	#now ver has format (XX.X.XXX)
	
	commonpaths=[r"C:\Program Files\Side Effects Software"]
	
	houdinies={}
	for path in commonpaths:
		dirs=[]
		try:
			dirs=os.listdir(path)
		except:
			continue
			
		for dir in dirs:
			match=re.match(r"[Hh]oudini ?(\d+)(\.(\d))?(\.(\d{3,}))?",dir)
			if(not match):continue
			cver=(int(match.group(1)),0 if match.group(3)=="" else int(match.group(3)), 9999 if match.group(5)=="" else int(match.group(5)))
			houdinies[cver]=os.path.join(path,dir)
		
		vers=houdinies.keys()
		if(len(vers)==0):raise RuntimeError("houdini not found!!")
		#elif(len(vers)==1):return houdinies[vers[0]]
		
		sortvers=[((abs(x[0]-ver[0]),abs(x[1]-ver[1]),abs(x[2]-ver[2])),x) for x in vers]
		
		sortvers.sort(key=lambda el:el[0][0])
		sortvers=[x for x in sortvers if x[0][0]==sortvers[0][0][0]]
		sortvers.sort(key=lambda el:el[0][1])
		sortvers=[x for x in sortvers if x[0][1]==sortvers[0][0][1]]
		sortvers.sort(key=lambda el:el[0][2])
		sortvers=[x for x in sortvers if x[0][2]==sortvers[0][0][2]]
		
		return os.path.join(houdinies[sortvers[0][1]],"bin","houdinifx.exe")
			

def launchHoudini(ver=(),hsite=None,job=None):
	os.environ["JOB"]=r"c:\temp"
	if(not (hsite is None) and isinstance(hsite,str)):
		os.environ["HSITE"]=hsite
		print("HSITE set to %s"%(str(hsite),))
	if(not (job is None) and isinstance(job,str)):
		os.environ["JOB"]=job
		print("JOB   set to %s"%(str(job),))
	os.environ["FPS"]="25"
	houbin=locateHoudini(ver)
	print("Calling closest found version: %s"%(houbin,))
	subprocess.Popen(houbin,stdin=None,stdout=None,stderr=None)
	print("Done!")
	
	
print("Welcome to houdini hsite launcher ver. %s !!"%("0.0.0.001 preAlphaTechDemo"))
print("----------")
jobpath=os.path.join(os.path.split(os.getcwd())[0],"fxproject")
launchHoudini((16,0,600),os.getcwd(),jobpath)
print("----------")
print("you can now close this window, it will close automatically in 5 sec")
time.sleep(5)