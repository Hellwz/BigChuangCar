import cv2

camera = cv2.VideoCapture(0)
while True:
    ret,img = camera.read()
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
camera.release()
cv2.destroyAllWindows()

#cv2.imwrite('1.png',img,[int(cv2.IMWRITE_JPEG_QUALITY),95])
