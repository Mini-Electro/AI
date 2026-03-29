import cv2

img = cv2.imread("C://Users//ADMIN//Downloads//Image_annotation_AIEPCM2L3A1-3dd2//example.jpg")

h, w = img.shape[:2]

start_point = (50, h // 2)
end_point = (w - 50, h // 2)

cv2.arrowedLine(img, start_point, end_point, (0, 255, 0), 2, tipLength=0.05)
cv2.arrowedLine(img, end_point, start_point, (0, 255, 0), 2, tipLength=0.05)

text = f"Width: {w}px"
cv2.putText(img, text, (w // 3, h // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

cv2.imshow("Annotated Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()