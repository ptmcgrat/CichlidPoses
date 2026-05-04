from ultralytics import YOLO
import pdb
from file_manager import FileManager as FM

fm_obj = FM()
fm_obj.downloadData(fm_obj.localAnnotationsDir)

"""
model_fd = YOLO("yolo26l.pt")
results_fd = model_fd.train(data = fm_obj.localAnnotationsDir + 'fish_detect.yaml', epochs=100, imgsz=640, project = fm_obj.localMLMDir, name = 'FishDetect', degrees = 10, shear = 1.0, flipud = 0.5, fliplr = 0.5, mosaic = 1.0, exist_ok = True, batch = -1)
model_cd = YOLO("yolo26l.pt")
results_cd = model_cd.train(data = fm_obj.localAnnotationsDir + 'color_detect.yaml', epochs=100, imgsz=640, project = fm_obj.localMLMDir, name = 'ColorDetect', degrees = 10, shear = 1.0, flipud = 0.5, fliplr = 0.5, mosaic = 1.0, exist_ok = True, batch = -1)

model_fp = YOLO("yolo26l-pose.pt")  # load a pretrained model (recommended for training)
results_fp = model_fp.train(data = fm_obj.localAnnotationsDir + 'fish_pose.yaml', epochs=200, imgsz=640, project = fm_obj.localMLMDir, name = 'FishPose', exist_ok = True, batch = -1, translate = 0.02, scale = 0.02, flipud = 0.5, hsv_h = 0.005, hsv_s = 0.2, hsv_v = 0.2, mosaic = 0.0)
"""
model_cp = YOLO("yolo26l-pose.pt")  # load a pretrained model (recommended for training)
results_cp = model_cp.train(data = fm_obj.localAnnotationsDir + 'color_pose.yaml', epochs=200, imgsz=640, project = fm_obj.localMLMDir, name = 'ColorPose', exist_ok = True, batch = -1, translate = 0.02, scale = 0.02, flipud = 0.5, hsv_h = 0.005, hsv_s = 0.2, hsv_v = 0.2, mosaic = 0.0)

fm_obj.uploadData(fm_obj.localMLMDir)
pdb.set_trace()	