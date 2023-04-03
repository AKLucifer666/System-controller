import osascript
import cv2
import mediapipe as mp
import time
import handTrackingModule as hmt
import gestures as gest
from test import *
import time
from playsound import playsound
finger = [0,5,9,13,17]

def getVolume():
	result = osascript.osascript('get volume settings')
	volInfo = result[1].split(',')
	outputVol = int(volInfo[0].replace('output volume:', ''))
	return outputVol

def volumeIncrease():
	result = osascript.osascript('get volume settings')
	volInfo = result[1].split(',')
	outputVol = int(volInfo[0].replace('output volume:', ''))
	if outputVol>=100:
		playsound("audio/MaximumVolume.mp3",block=False)
	else:
		playsound("audio/VolumeUp.mp3",block=False)
	newVol = min(outputVol+10,100)
	vol = "set volume output volume " + str(min(outputVol+10,100))
	osascript.osascript(vol)
	return newVol

def volumeDecrease():
	result = osascript.osascript('get volume settings')
	volInfo = result[1].split(',')
	outputVol = int(volInfo[0].replace('output volume:', ''))
	playsound("audio/VolumeDown.mp3",block=False)
	newVol = min(outputVol+10,100)
	vol = "set volume output volume " + str(max(outputVol-10,0))
	osascript.osascript(vol)
	return newVol


def changeVolume(cap,detector):
	time.sleep(1)
	count=0
	chosen = "none"
	volume = getVolume()
	while True:
		success,img = cap.read()
		img = cv2.flip(img,1)
		cv2.putText(img,"CHANGE VOLUME",(800,100),cv2.FONT_HERSHEY_PLAIN,3,(14,14,146),3)
		img =  detector.findHands(img,draw=False)
		dhand1,dhand2 = skeleton(img,detector)
		fingerUp = []
		res = "none"
		try:
			for i in range(1,5):
				fingerUp+=[gest.finger_up(dhand1,finger[i])]
			if ((fingerUp[0]&fingerUp[1]&fingerUp[2]&fingerUp[3])==True):
				res = "Exit Volume Control"
			elif ((fingerUp[0] | fingerUp[1] | fingerUp[2] | fingerUp[3])==False):
				res = "none"
			else:
				res = "check"
		except:
			res = "check"
		if res=="check":
			try:
				if (gest.pinch_up(dhand1)):
					res="Volume Up"
			except:
				res="none"
			try:
				if (gest.pinch_down(dhand1)):
					res="Volume Down"
			except:
				res="none"

		if res not in ["Volume Up","Volume Down","Exit Volume Control"]:
			res = "none"
		cv2.putText(img,str(res)+"| Count="+str(count),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(14,14,146),3)
		cv2.putText(img,"Volume = "+str(volume) + "%",(10,120),cv2.FONT_HERSHEY_PLAIN,3,(14,14,146),3)
		cv2.imshow("Image",img)
		if count>=20 and chosen=="Exit Volume Control":
			return
		elif count>=5 and chosen=="Volume Up":
			volume=volumeIncrease()
			count=0
		elif count>=5 and chosen=="Volume Down":
			volume=volumeDecrease()
			count=0
		elif res in ["Volume Down","Volume Up","Exit Volume Control"] and chosen!=res:
			count=0
			chosen=res
		elif res in ["Volume Down","Volume Up","Exit Volume Control"] and chosen==res:
			count+=1
		else:
			count=0
			chosen = res
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break