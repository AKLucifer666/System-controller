import osascript
import cv2
import mediapipe as mp
import time
import handTrackingModule as hmt
import gestures as gest
from test import *

finger = [0,5,9,13,17]

def skeleton(img,detector):
	dhand1 = {}
	dhand2 = {}
	for i in range(21):
		finger1 = detector.findPositions(img,handNo=0,pos=i,draw=False)
		finger2 = detector.findPositions(img,handNo=1,pos=i,draw=False)
		dhand1[i]=finger1
		dhand2[i]=finger2

	return (dhand1,dhand2)

def test(dhand1):
	fingerUp = []
	try:
		for i in range(1,5):
			fingerUp+=[gest.finger_up(dhand1,finger[i])]
	except:
		return "none"
	try:
		if ((fingerUp[0]&fingerUp[1])==True) and ((fingerUp[2] | fingerUp[3])==False):
			return "victory"
	except:
		return "none"
	try:
		if ((fingerUp[0]&fingerUp[1]&fingerUp[2])==True) and ((fingerUp[3])==False):
			return "threeFingers"
	except:
		return "none"
	try:
		if ((fingerUp[0])==True) and ((fingerUp[1] | fingerUp[2] | fingerUp[3])==False):
			return "indexFinger"
	except:
		return "none"
	try:
		if ((fingerUp[3])==True) and ((fingerUp[0] | fingerUp[1] | fingerUp[2])==False):
			return "littleFinger"
	except:
		return "none"
	try:
		if ((fingerUp[0]&fingerUp[1]&fingerUp[2]&fingerUp[3])==True):
			return "fourFingers"
		else:
			return "none"
	except:
		return "none"	