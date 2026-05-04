from ultralytics import YOLO
import os, pdb
from file_manager import FileManager as FM

fm_obj = FM()
fm_obj.downloadData(fm_obj.localMLMDir)
fm_obj.downloadData(fm_obj.localProjectDir)

model_fd = YOLO(fm_obj.localMLMDir + 'FishDetect/weights/best.pt')
model_cd = YOLO(fm_obj.localMLMDir + 'ColorDetect/weights/best.pt')
model_fp = YOLO(fm_obj.localMLMDir + 'FishPose/weights/best.pt')
model_cp = YOLO(fm_obj.localMLMDir + 'ColorPose/weights/best.pt')

image_files = {}
all_species = os.listdir(fm_obj.localProjectDir)
for species in all_species:
    image_files[species] = [fm_obj.localProjectDir + x for x in os.listdir(fm_obj.localProjectDir + species) if '.jpg' in x]
# Run batched inference on a list of images
#results = model(image_files)  # return a list of Results objects
pdb.set_trace()
# Process results list
for im_file in image_files:
    result = model3(im_file)
    #boxes = result.boxes  # Boxes object for bounding box outputs
    #masks = result.masks  # Masks object for segmentation masks outputs
    #keypoints = result.keypoints  # Keypoints object for pose outputs
    #probs = result.probs  # Probs object for classification outputs
    #obb = result.obb  # Oriented boxes object for OBB outputs
    result[0].show()  # display to screen
    pdb.set_trace()
    #result.save(filename="result.jpg")  # save to disk