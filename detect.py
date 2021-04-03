from darknet.darknet import *
import cv2

# darknet helper function to run detection on image
def run_detection(network, img, width, height):
    darknet_image = make_image(width, height, 3)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)

    # get image ratios to convert bounding boxes to proper size
    img_height, img_width, _ = img.shape
    width_ratio = img_width/width
    height_ratio = img_height/height

    # run model on darknet style image to get detections
    copy_image_from_bytes(darknet_image, img_resized.tobytes())
    detections = detect_image(network, class_names, darknet_image)
    free_image(darknet_image)
    return detections, width_ratio, height_ratio

# load in our YOLOv4 architecture network
vis_network, class_names, class_colors = load_network("./models/vis/yolov4-obj.cfg", "./models/vis/obj.data", "./models/vis/yolov4-obj_best.weights")  
width = network_width(vis_network)
height = network_height(vis_network)


image = cv2.imread("./data/img/vis_test1.png")

# run test on images
detections, width_ratio, height_ratio = run_detection(vis_network, image, width, height)
print(detections)

for label, confidence, bbox in detections:
    print(label, confidence, bbox)
    left, top, right, bottom = bbox2points(bbox)
    left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(bottom * height_ratio)
    cv2.rectangle(image, (left, top), (right, bottom), class_colors[label], 2)
    cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                        (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        class_colors[label], 2)
cv2.imshow("labelled", image)