from paddleocr import PaddleOCR
import re
import cv2
# Load OCR model only once
ocr = PaddleOCR(lang="en")


def read_plate(plate_img):

    if plate_img is None:
        return None

    result = ocr.ocr(plate_img, cls=False)

    if not result or not result[0]:
        return None

    plates = []

    for line in result[0]:
        text = line[1][0]

        # Remove spaces and special characters
        text = re.sub(r'[^A-Z0-9]', '', text.upper())

        plates.append(text)

    return plates[0] if plates else ""
#
# img=cv2.imread(r"C:\Users\Hari Krishna\PycharmProjects\trafficsystem\old\outputs\plates\0.jpg")
# print(img.shape)
# # cv2.imshow("img",img)
# print(read_plate(img))