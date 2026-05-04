from ultralytics import YOLO
import os, pdb
# Load a model
#model = YOLO('runs/pose/ColorGuideModel/ColorGuide/weights/best.pt')  # pretrained YOLO26n model
#model2 = YOLO('runs/pose/FishPoseModel/FishPose/weights/best.pt')  # pretrained YOLO26n model
model3 = YOLO('runs/obb/ColorGuideModel/ColorGuide/weights/best.pt')
model4 = YOLO('runs/detect/FishPoseModel/FishPose/weights/best.pt')
image_files = ['Parentals/' + x for x in os.listdir('Parentals') if x[0] != '.' and 'FINS' not in x]
# Run batched inference on a list of images
#results = model(image_files)  # return a list of Results objects

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