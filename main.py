import os
import cv2
from ultralytics import YOLO
from ocr import read_plate
from association import (
    find_violators,
    find_vehicle,
    find_plate
)
from database import save_violation
model = YOLO("runs/detect/train/weights/best.pt")

os.makedirs("outputs/vehicles", exist_ok=True)
os.makedirs("outputs/plates", exist_ok=True)
os.makedirs("outputs/riders", exist_ok=True)

saved = 0

# if True:
frame = cv2.imread(r"C:\Users\Hari Krishna\Pictures\ab39f1c78a3f789e844a2848bd965adc.jpg")
result = model(frame)[0]
helmets = []
no_helmets = []
plates = []
riders = []
vehicles = []

for box in result.boxes:
    cls = int(box.cls[0])
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    if cls == 0:
        helmets.append([x1, y1, x2, y2])

    elif cls == 1:
        no_helmets.append([x1, y1, x2, y2])

    elif cls == 2:
        plates.append([x1, y1, x2, y2])

    elif cls == 3:
        riders.append([x1, y1, x2, y2])

    elif cls == 4:
        vehicles.append([x1, y1, x2, y2])

violators = find_violators(
    riders,
    no_helmets
)
r=v=p=pt=None
for rider in violators:

    vehicle = find_vehicle(
        rider,
        vehicles
    )

    plate = find_plate(
        vehicle,
        plates
    )

    rx1, ry1, rx2, ry2 = rider

    cv2.rectangle(
        frame,
        (rx1, ry1),
        (rx2, ry2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "no helmet",
        (rx1, ry1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )
    crop = frame[ry1:ry2, rx1:rx2]
    r=f"outputs/riders/{saved}.jpg"
    cv2.imwrite(
        r,
        crop
    )
    if vehicle:

        vx1, vy1, vx2, vy2 = vehicle

        cv2.rectangle(
            frame,
            (vx1, vy1),
            (vx2, vy2),
            (255, 0, 0),
            2
        )

        crop = frame[vy1:vy2, vx1:vx2]
        v=f"outputs/vehicles/{saved}.jpg"
        cv2.imwrite(
            v,
            crop
        )

    if plate:

        px1, py1, px2, py2 = plate

        cv2.rectangle(
            frame,
            (px1, py1),
            (px2, py2),
            (0, 255, 255),
            2
        )

        plate_crop = frame[py1:py2, px1:px2]
        plate_text = read_plate(plate_crop)
        pt=plate_text
        if plate_text:
            print("NUMBER:", plate_text)
        p=f"outputs/plates/{saved}.jpg"
        cv2.imwrite(
                p,
                plate_crop
        )

    saved += 1
save_violation(pt,r,v,p,"no helmet")
cv2.imshow("Traffic Violation Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()


