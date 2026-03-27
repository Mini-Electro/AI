import cv2

image = cv2.imread("C://Users//ADMIN//Downloads//AIEPCM2L2_Activities-72a4//example.jpg")

if image is None:
    print("Error: Image is not found.")
    exit()

(h, w) = image.shape[:2]
center = (w//2,h//2)

rotation_matrix = cv2.getRotationMatrix2D(center, 50,1.0)
rotated = cv2.warpAffine(image,rotation_matrix, (w, h))

cropped = image[50:300, 50:300]

brightness = 50
bright = cv2.convertScaleAbs(image, alpha=1, beta=brightness)

cv2.imshow("Original", image)
cv2.imshow("Rotated", rotated)
cv2.imshow("Cropped", cropped)
cv2.imshow("Brightness Adjusted", bright)

cv2.imwrite("rotated.jpg", rotated)
cv2.imwrite("cropped.jpg", cropped)
cv2.imwrite("bright.jpg", bright)

cv2.waitKey(0)
cv2.destroyAllWindows()