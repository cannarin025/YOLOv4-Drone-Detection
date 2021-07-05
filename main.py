import detect
import DroneCode_Vis as dc
import sys
import cv2
import os
import time

os.chdir(os.path.dirname(os.getcwd()))  # sets working directory back up a level

# test to confirm detectors are working
vis_img = cv2.imread("./data/img/vis_test1.jpg")
IR_img = cv2.imread("./data/img/toad_lowlight5_IR.jpg")

# load in our YOLOv4 architecture network
vis_detector = detect.Detector("./models/vis")
IR_detector = detect.Detector("./models/IR")

print("starting detections")
start = time.time()
vis_detections = vis_detector.run_detection(vis_img)
IR_detections = IR_detector.run_detection(IR_img)

print(vis_detections, "vis detections")
print(IR_detections, "IR detections")
end = time.time()
print("finished detection", f"inference time: {end-start}")

# drone detection
myar = dc.area(5, 5, 3, detector=vis_detector)
myar.run(0.2, 1.2, 1.2)