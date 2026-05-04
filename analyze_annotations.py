import xml.etree.ElementTree as ET
import pandas as pd
import pdb, os, random, subprocess
import seaborn as sns
import matplotlib.pyplot as plt
#dt = pd.read_xml('annotations.xml')

def distance(x,y):
	return abs(((y[0] - x[0])**2 + (y[1] - x[1])**2)**.5)

fish_poses = ['BackLip','TopCaudal','BottomCaudal','BottomBody','Fork','Opercle','MidCaudal','OuterEye','Supraoccipital','TopBody','Nose','Interopercle']
box_poses = ['Black','White','Brown','Green']

tree = ET.parse('annotations.xml')
root = tree.getroot()
dt = pd.DataFrame(columns = ['SampleID','Species','Scaling','BodyLength','FinLength','BodyHeight','HeadLength','HeadHeight'])

# Iterate through elements
for child in root:
	if child.tag != 'image':
		continue

	image_file = child.get('name')
	if 'FINS' in image_file or 'TAG' in image_file:
		continue
	
	width = int(child.get('width'))
	height = int(child.get('height'))
	#print(child.tag, child.attrib)
	if child.tag == 'image':
		data = {}
		for gc in child:
			label = gc.get('label')
			occluded = gc.get('occluded')
			if occluded != '0':
				pdb.set_trace()
			if label in ['OuterEye','InnerEye']:
				x,y = float(gc.get('cx')),float(gc.get('cy'))
			else:
				x,y = [float(x) for x in gc.get('points').split(',')]

			data[label] = [x,y]
		scaling = (distance(data['Brown'], data['Green']) + distance(data['White'], data['Black']))/2/13.2
		
		d1 = distance(data['Nose'], data['MidCaudal'])/scaling
		d2 = distance(data['MidCaudal'], data['Fork'])/scaling/d1
		d3 = distance(data['TopBody'], data['BottomBody'])/scaling/d1
		d4 = distance(data['Nose'], data['Opercle'])/scaling/d1
		d5 = distance(data['Supraoccipital'], data['Interopercle'])/scaling/d1

		dt.loc[len(dt)] = [image_file,image_file.split('-')[0],scaling, d1,d2,d3,d4,d5]
pdb.set_trace()

