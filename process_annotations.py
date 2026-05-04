import xml.etree.ElementTree as ET
import pandas as pd
import pdb, os, random, subprocess
from PIL import Image, ImageOps

#dt = pd.read_xml('annotations.xml')

fish_poses = ['BackLip','TopCaudal','BottomCaudal','BottomBody','Fork','Opercle','MidCaudal','OuterEye','Supraoccipital','TopBody','Nose','Interopercle']
box_poses = ['Black','White','Brown','Green']

tree = ET.parse('annotations.xml')
root = tree.getroot()

all_images = os.listdir('Parentals')
species_mapper = {'MC':0,'MCYHF1':1,'MCYHRF1':2,'YH':3}

for datatype in ['Detect','Pose']:
	for region in ['ColorBox','Fish']:
		for dtype in ['images','labels']:
			for dataset in ['train','val']:
				subprocess.run(['rm','-rf',datatype + '/' + region + '/' + dtype + '/' + dataset])
				os.makedirs(datatype + '/' + region + '/' + dtype + '/' + dataset)

# Iterate through elements
for child in root:
	if child.tag != 'image':
		continue

	image_file = child.get('name')
	if 'FINS' in image_file:
		continue
	try:
		assert image_file in all_images
	except:
		print(image_file)
		#pdb.set_trace()
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

		if random.random() < 0.8:
			dataset = 'train/'
		else:
			dataset = 'val/'

		# Calculate bounding boxes for color scale
		box_xmin = int(min([data[x][0] for x in data.keys() if x in box_poses]) - 0.05*width)
		box_xmax = int(max([data[x][0] for x in data.keys() if x in box_poses]) + 0.05*width)
		box_ymin = int(min([data[x][1] for x in data.keys() if x in box_poses]) - 0.05*height)
		box_ymax = int(max([data[x][1] for x in data.keys() if x in box_poses]) + 0.05*height)
		
		# Calculate bounding boxes for fish
		fish_xmin = int(min([data[x][0] for x in data.keys() if x in fish_poses]) - 0.05*width)
		fish_xmax = int(max([data[x][0] for x in data.keys() if x in fish_poses]) + 0.05*width)
		fish_ymin = int(min([data[x][1] for x in data.keys() if x in fish_poses]) - 0.05*height)
		fish_ymax = int(max([data[x][1] for x in data.keys() if x in fish_poses]) + 0.05*height)

		# Get images in the right spot
		subprocess.run(['cp', 'Parentals/' + image_file, 'Detect/ColorBox/images/' + dataset])
		subprocess.run(['cp', 'Parentals/' + image_file, 'Detect/Fish/images/' + dataset])


		# Crop images for pose
		img = Image.open('Parentals/' + image_file)
		img = ImageOps.exif_transpose(img)
		img.crop((box_xmin, box_ymin, box_xmax, box_ymax)).save('Pose/ColorBox/images/' + dataset + image_file)
		img.crop((fish_xmin, fish_ymin, fish_xmax, fish_ymax)).save('Pose/Fish/images/' + dataset + image_file)

		#outdata = [0, (box_xmin + box_xmax)/2, (box_ymin + box_ymax)/2, box_xmax-box_xmin, box_ymax-box_ymin]
		outdata = [0, (box_xmin + box_xmax)/2/width, (box_ymin + box_ymax)/2/height, (box_xmax-box_xmin)/width, (box_ymax-box_ymin)/height]
		
		with open('Detect/ColorBox/labels/' + dataset + '/' + image_file.replace('.jpg','.txt'), 'w') as outfile:
			print(' '.join([str(x) for x in outdata]), file = outfile)

		outdata = [species_mapper[image_file.split('-')[0]], (fish_xmin + fish_xmax)/2/width, (fish_ymin + fish_ymax)/2/height, (fish_xmax-fish_xmin)/width, (fish_ymax-fish_ymin)/height]
		with open('Detect/Fish/labels/' + dataset + '/' + image_file.replace('.jpg','.txt'), 'w') as outfile:
			print(' '.join([str(x) for x in outdata]), file = outfile)

		outdata = [0,0.5,0.5,1,1]
		for kp in box_poses:
			outdata += [(data[kp][0] - box_xmin)/(box_xmax-box_xmin), (data[kp][1] - box_ymin)/(box_ymax-box_ymin)]
		with open('Pose/ColorBox/labels/' + dataset + '/' + image_file.replace('.jpg','.txt'), 'w') as outfile:
			print(' '.join([str(x) for x in outdata]), file = outfile)
		outdata = [0,0.5,0.5,1,1]
		for kp in fish_poses:
			outdata += [(data[kp][0] - fish_xmin)/(fish_xmax-fish_xmin), (data[kp][1] - fish_ymin)/(fish_ymax-fish_ymin)]
		with open('Pose/Fish/labels/' + dataset + '/' + image_file.replace('.jpg','.txt'), 'w') as outfile:
			print(' '.join([str(x) for x in outdata]), file = outfile)
