import osascript
import cv2
import mediapipe as mp
import time
import handTrackingModule as hmt
import gestures as gest
from volumeModule  import *
from test import *
from playsound import playsound
import pyautogui
from mouseControl import *

finger = [0,5,9,13,17]

def system(): 
	cap = cv2.VideoCapture(0)
	pTime = 0
	cTime = 0
	detector = hmt.handDetector()
	count = 0
	chosen = "none"
	d = {"fourFingers":"Terminate Program","victory":"Volume Control","threeFingers":"Mouse Control"}
	while True:
		success,img = cap.read()
		img = cv2.flip(img,1)
		img =  detector.findHands(img,draw=False)
		dhand1,dhand2 = skeleton(img,detector)
		try:
			res = d[test(dhand1)]
		except:
			res = "none"

		cv2.putText(img,str(res)+"| Count="+str(count),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
		cv2.putText(img,"MAIN PAGE",(10,120),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
		cv2.imshow("Image",img)
		if count>=30 and chosen=="Terminate Program":
			playsound("audio/ProgramTerminated.mp3",block=False)
			time.sleep(2)
			break
		elif count>=30 and chosen=="Volume Control":
			playsound("audio/VolumeControl.mp3",block=False)
			changeVolume(cap,detector)
			playsound("audio/Exit.mp3",block=False)
			count=0
			continue
		elif count>=30 and chosen=="Mouse Control":
			playsound("audio/MouseControl.mp3",block=False)
			mouseControl(cap,detector)
			playsound("audio/Exit.mp3",block=False)
			count=0
			continue
		elif res==chosen and res!="none":
			count+=1
		else:
			count=0
			chosen = res
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

system()






