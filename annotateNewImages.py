from ultralytics import YOLO
import os, pdb
from file_manager import FileManager as FM
from PIL import Image, ImageOps

fm_obj = FM()
fm_obj.downloadData(fm_obj.localMLMDir)
fm_obj.downloadData(fm_obj.localProjectDir)

model_fd = YOLO(fm_obj.localMLMDir + 'FishDetect/weights/best.pt')
model_cd = YOLO(fm_obj.localMLMDir + 'ColorDetect/weights/best.pt')
model_fp = YOLO(fm_obj.localMLMDir + 'FishPose/weights/best.pt')
model_cp = YOLO(fm_obj.localMLMDir + 'ColorPose/weights/best.pt')

image_files = {}
all_species = os.listdir(fm_obj.localProjectDir + 'Parentals')
for species in all_species:
    image_files[species] = [fm_obj.localProjectDir + 'Parentals/' + species + '/' + x for x in os.listdir(fm_obj.localProjectDir + 'Parentals/' + species) if '.jpg' in x]
# Run batched inference on a list of images
#results = model(image_files)  # return a list of Results objects
# Process results list
for species in all_species:
    for im_file in image_files[species]:
        result_fd = model_fd(im_file)
        result_cd = model_cd(im_file)

        img = Image.open(im_file)
        img = ImageOps.exif_transpose(img)
        crop_fd = result_fd[0].boxes[0].xyxy.cpu().numpy()[0]
        crop_cd = result_cd[0].boxes[0].xyxy.cpu().numpy()[0]

        result_fp =model_fp(img.crop(crop_fd))
        result_cp =model_cp(img.crop(crop_cd))
        result_fp[0].save(fm_obj.localProjectDir + 'Outputs/Fish/'+im_file.split('/')[-1])
        result_cp[0].save(fm_obj.localProjectDir + 'Outputs/ColorBox/'+im_file.split('/')[-1])

    pdb.set_trace()
    #boxes = result.boxes  # Boxes object for bounding box outputs
    #masks = result.masks  # Masks object for segmentation masks outputs
    #keypoints = result.keypoints  # Keypoints object for pose outputs
    #probs = result.probs  # Probs object for classification outputs
    #obb = result.obb  # Oriented boxes object for OBB outputs
    result[0].show()  # display to screen
    pdb.set_trace()
    #result.save(filename="result.jpg")  # save to disk