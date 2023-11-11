import cv2 as cv
import numpy as np

cap = cv.VideoCapture(1, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

while True:


    def canny(frame):
        gray = cv.cvtColor(lane_image, cv.COLOR_RGB2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        canny = cv.Canny(blur, 200, 300)
        return canny
    
    def display_lines(frame, lines):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image
    
    def region_of_interest(frame):
        height = frame.shape[0]
        polygons = np.array([[(0, height), (850, height), (400, 260), (600, 260)]])

        mask = np.zeros_like(frame)
        cv.fillPoly(mask, polygons, 255)
        masked_image = cv.bitwise_and(frame, mask)
        return masked_image
    
    ret, frame = cap.read()
    lane_image = np.copy(frame)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    lines = cv.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=30, maxLineGap=40)
    line_image = display_lines(lane_image, lines)
    combo_image = cv.addWeighted(lane_image, 0.8, line_image, 1, 1)
    


    if not ret:
        print("Não foi possivel abrir a stream. Saindo...")
        break
   
    cv.imshow('frame', combo_image)

    if cv.waitKey(1) == ord('q'):
        break   

cap.release()
cv.destroyAllWindows()

