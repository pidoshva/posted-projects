import numpy as np
import cv2
import time
import face_recognition as fr
import os

def face_capture():
    path = 'Faces'
    capture = cv2.VideoCapture(0) # Launching camera

    num = 0
    while num < 10:
        ret, frame = capture.read()

        rgb_frame = frame[:,:,::-1]

        face_locations = fr.face_locations(rgb_frame)

        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations,face_encodings):

            #creating rectangles for face highlight
            cv2.rectangle(frame,(left, top), (right, bottom), (0, 153, 0), 3)
            cv2.rectangle(frame,(left, bottom-35), (right, bottom), (0, 153, 0), cv2.FILLED)

            crop_face = frame[top:bottom,left:right] # Cropping face from the image

            cv2.imwrite(os.path.join(path,'img'+str(num)+'.jpg'),crop_face) # Writing image to a "path" directory
            print(f"img{str(num)}.jpg – Captured") # Printing message every time an image is captured

            num = num+1 # Counting captures

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    face_capture()
