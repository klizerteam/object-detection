import cv2
from ultralytics import YOLO


uplight_objects={"Tree","Fence","Door","Shrub","Window"}
pathlight_objects={"Pathway"}



def assign_lighting(results,class_names):
    lighting_output=[]
    for result in results:
      for box in result.boxes:
        class_id=int(box.cls[0])
        confidence = float(box.conf[0])
        object_name=class_names[class_id]
        if object_name in uplight_objects:
            light_type = "uplight"
        elif object_name in pathlight_objects:
            light_type = "pathlight"
        else:
            light_type = "no_light_rule"

        lighting_output.append({
            "object": object_name,
            "confidence": round(confidence, 3),
            "light": light_type
        })

    return lighting_output
class_names = [
    "Tree",
    "Fence",
    "Door",
    "Shrub",
    "Pathway",
    "Window"
]


