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

def mouseControl(cap,detector):
	cnt=0
	while True:
		success,img = cap.read()
		img = cv2.flip(img,1)
		img =  detector.findHands(img,draw=False)
		dhand1,dhand2 = skeleton(img,detector)
		cv2.putText(img,"Mouse Control",(10,120),cv2.FONT_HERSHEY_PLAIN,3,(228,5,139),3)
		try:
			res = test(dhand1)
		except:
			res = "none"
		if res in ["indexFinger","littleFinger"]:
			count=0
			if res=="indexFinger":
				fx,fy = dhand1[8][1],dhand1[8][2]
			else:
				fx,fy = dhand1[20][1],dhand1[20][2]
			#img = cv2.circle(img,(fx,fy),15,(0,255,0),cv2.FILLED)
			rx,ry = pyautogui.size()
			alpha = 1.2
			scalex = int(((fx-(img.shape[1]/2))/img.shape[1])*rx*alpha) + rx//2
			scaley = int(((fy-(img.shape[0]/2))/img.shape[0])*ry*alpha) + ry//2
			pyautogui.moveTo(scalex,scaley)
			if len(dhand2[4])*len(dhand2[8])*len(dhand2[0])!=0:
				cnt+=1
			else:
				cnt=0
			if cnt>=5:
				if not gest.thumbs_up(dhand2) and not gest.finger_up(dhand2,5):
					pyautogui.click()
				if gest.finger_up(dhand2,5):
					pyautogui.rightClick()
		elif res=="fourFingers":
			count+=1
		else:
			count=0
		if count>=30:
			break
		#cv2.putText(img,str(res)+"| Count="+str(count),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
		cv2.imshow("Image",img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break