from darknet import darknet
import cv2
import os


class Detector:
    """
    A class to load all necessary model components and carry out detections using YOLOv4
    """
    def __init__(self, model_path):
        model_files = list(os.path.join(model_path, file) for file in os.listdir(model_path))
        weights_path = [file_path for file_path in model_files if file_path.endswith(".weights")][0]
        cfg_path = [file_path for file_path in model_files if file_path.endswith(".cfg")][0]
        data_path = [file_path for file_path in model_files if file_path.endswith(".data")][0]

        self.__network, self.__class_names, self.__class_colors = darknet.load_network(cfg_path, data_path, weights_path)

    def run_detection(self, img):
        width = darknet.network_width(self.__network)
        height = darknet.network_height(self.__network)
        darknet_image = darknet.make_image(width, height, 3)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (width, height),
                                 interpolation=cv2.INTER_LINEAR)
        # get image ratios to convert bounding boxes to proper size
        img_height, img_width, _ = img.shape
        width_ratio = img_width / width
        height_ratio = img_height / height
        # run model on darknet style image to get detections
        darknet.copy_image_from_bytes(darknet_image, img_resized.tobytes())
        detections = darknet.detect_image(self.__network, self.__class_names, darknet_image)
        darknet.free_image(darknet_image)

        predictions = []
        for label, confidence, bbox in detections:
            x1, y1, x2, y2 = darknet.bbox2points(bbox)
            x1, y1, x2, y2 = int(x1 * width_ratio), int(y1 * height_ratio), int(x2 * width_ratio), int(
                y2 * height_ratio)
            predictions.append({"class_name": label, "box_coords": [(x1, y1), (x2, y2)], "confidence": confidence})

        if predictions == []:
            predictions = None

        return predictions

    def draw_detections(self, img, detections):
        if detections is not None:
            for detection in detections:
                cv2.rectangle(img,
                              detection["box_coords"][0],
                              detection["box_coords"][1],
                              self.__class_colors[detection["class_name"]], 2)

                cv2.putText(img,
                            "{} [{:.2f}]".format(detection["class_name"],
                                                 float(detection["confidence"])),
                            (detection["box_coords"][0][0], detection["box_coords"][0][1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            self.__class_colors[detection["class_name"]], 2)
        return img

    def detect_img(self, img):
        detections = self.run_detection(img)
        img = self.draw_detections(img, detections)
        cv2.imshow("labelled", img)
        cv2.waitKey(0)

    def save_detection(self, img, savepath):
        detections = self.run_detection(img)
        img = self.draw_detections(img, detections)
        cv2.imwrite(savepath, img)

    def detect_video(self, cap):
        frame_count = 0
        run = True
        while run:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                run = False
            else:
                frame_count += 1
                detections = self.run_detection(frame)
                print(detections)
                self.draw_detections(frame, detections)

                cv2.imshow("video detection", frame)
                cv2.waitKey(1)

        #When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
