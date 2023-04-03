def dist(l1,l2):
	return (int(((l1[1]-l2[1])**2 + (l1[2]-l2[2])**2)**0.5))

def finger_up(dhand,base):
	try:
		if dist(dhand[base+3],dhand[base])>dist(dhand[base+1],dhand[base]) and dist(dhand[base+3],dhand[0])>dist(dhand[base],dhand[0]):
			return True
		else:
			return False
	except:
		False

def thumbs_up(dhand):
	try:
		if dist(dhand[4],dhand[6])>dist(dhand[5],dhand[6]):
			return True
		else:
			return False
	except:
		False

def pinch_up(dhand):
	try:
		if dist(dhand[4],dhand[8])>dist(dhand[4],dhand[5]):
			return True
		else:
			return False
	except:
		False

def pinch_down(dhand):
	try:
		if dist(dhand[4],dhand[8])<dist(dhand[4],dhand[5]):
			return True
		else:
			return False
	except:
		False
