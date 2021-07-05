def calc_centre_coords(detections):
    for detection in detections:
        box = detection["box_coords"]
        detection["centre_coord"] = (int((box[0][0] + box[1][0]) / 2),
                                     int((box[1][0] + box[1][1]) / 2))


def multimodal_detection(detections1, detections2, tolerance):
    if detections1 is None:
        detections1 = []
    if detections2 is None:
        detections2 = []

    calc_centre_coords(detections1)
    calc_centre_coords(detections2)
    combined_detections = []
    for detection1 in detections1:
        for detection2 in detections2:
            # check to see if boxes are within tolerance of each other
            if (abs(detection1["centre_coord"][0] - detection2["centre_coord"][0]) < tolerance \
            and abs(detection1["centre_coord"][1] - detection2["centre_coord"][1] < tolerance)):

                detection_pair = (detection1, detection2)
                combined_conf = (detection1["confidence"] + detection2["confidence"])/2

                if detection_pair[0]["confidence"] > detection_pair[1]["confidence"]:
                    combined_class = detection_pair[0]["class_name"]
                else:
                    combined_class = detection_pair[1]["class_name"]

                # combined box coordinates
                # min x
                if detection_pair[0]["box_coords"][0][0] < detection_pair[1]["box_coords"][0][0]:
                    xmin = detection_pair[0]["box_coords"][0][0]
                else:
                    xmin = detection_pair[1]["box_coords"][0][0]

                # min y
                if detection_pair[0]["box_coords"][0][1] < detection_pair[1]["box_coords"][0][1]:
                    ymin = detection_pair[0]["box_coords"][0][1]
                else:
                    ymin = detection_pair[1]["box_coords"][0][1]

                # max x
                if detection_pair[0]["box_coords"][1][0] > detection_pair[1]["box_coords"][1][0]:
                    xmax = detection_pair[0]["box_coords"][1][0]
                else:
                    xmax = detection_pair[1]["box_coords"][1][0]

                # max y
                if detection_pair[0]["box_coords"][1][1] > detection_pair[1]["box_coords"][1][1]:
                    ymax = detection_pair[0]["box_coords"][1][1]
                else:
                    ymax = detection_pair[1]["box_coords"][1][1]

                combined_detection = {"class_name": combined_class, "box_coords": [(xmin, ymin), (xmax, ymax)], "confidence": combined_conf}
                combined_detections.append(combined_detection)

    return combined_detections