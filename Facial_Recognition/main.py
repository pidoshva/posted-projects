"""
Facial Recognition
by Vadim Pidoshva (Geleus)
Completed: 08/02/2022
https://geleus.io/
"""
import cv2
import numpy as np
import face_recognition as fr
import os
from pronounce import *
from face_training import *

def facial_recognition():
    """Running facial recognition module"""
    global top
    global right
    global bottom
    global left
    global frame
    global font
    global name
    global unknown_faces

    recognized_faces = [] # List of recognized faces during session
    unknown_faces = [] # List of unknown faces during session

    # Updating Dataset
    refresh_dataset()

    # Launching camera
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 60)
    print("Running Facial Recognition...")
    pronounce("Running facial recognition")

    while True:

        ret, frame = capture.read() # Reading frames

        rgb_frame = frame[:,:,::-1] # Converting colors

        face_locations = fr.face_locations(rgb_frame) # Finding face in the frame

        face_encodings = fr.face_encodings(rgb_frame, face_locations) # Encoding face

        for (top, right, bottom, left), face_encoding in zip(face_locations,face_encodings):
            matches = fr.compare_faces(use("known_faces_encodings"),face_encoding) # Comparing face to the faces in the dataset
            name = "Unknown" # Default name
            face_distance = fr.face_distance(use("known_faces_encodings"),face_encoding)
            best_match_index = np.argmin(face_distance) # Deriving match index

            if matches[best_match_index]: # If face is found
                name = use("known_faces_names")[best_match_index] # Setting corresponding name to the face
                # Taking action if the face appears for the first time
                if name not in recognized_faces: # If face is recognized for the first time during session
                    print(f"Face is Recognized --- {name}")
                    recognized_faces.append(name) # Adding face to recognized faces list
                    print(recognized_faces)
                    if "Unknown" not in name: # If name is known
                        pronounce(f"Hello {name.replace('_', ' ')}") # Greeting
                        if len(recognized_faces) > 1:
                        # Announcing the amount of recognized faces
                            pronounce(f"{len(recognized_faces)} people recognized.")
                        else:
                            pronounce(f"{len(recognized_faces)} person recognized.")
            elif name == "Unknown":
                # Taking action if the face is Unknown
                print("Face is NOT Recognized")
                unknown_faces.append(f"{name}_{len(unknown_faces)+1}") # Adding face to the list of unknown faces in session
                print(unknown_faces)
                capture_face(name) # Initializing function that captures and saves unknown face for further training
                pronounce(f"Hello stranger. Adding your face to the dataset.") # Need to actually add the face to the dataset><

                refresh_dataset() # Updating dataset to get all the newly added faces

            # Setting up face highlights
            if "Unknown" not in name:
                # Highlighting Recognized face with green rectangle with name
                cv2.rectangle(frame,(left, top), (right, bottom), (0, 153, 0), 3)
                cv2.rectangle(frame,(left, bottom-35), (right, bottom), (0, 153, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, name, (left-6, bottom-6), font, 1.0, (255, 255, 255), 1)
            else:
                # Highlighting Unknown face with red rectangle with name
                cv2.rectangle(frame,(left, top), (right, bottom), (0, 0, 225), 3)
                cv2.rectangle(frame,(left, bottom-35), (right, bottom), (0, 0, 225), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, name, (left-6, bottom-6), font, 1.0, (255, 255, 255), 1)

        # Displaying video capturing screen
        cv2.imshow("Facial Recognition", frame)
        # Quitting settings
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    # Termination of the program
    capture.release()
    cv2.destroyAllWindows()

def capture_face(name=None):
    """Capturing, cropping and saving unknown face to a new directory"""
    # Determining path for the new face
    path = f"Faces/{name}_{len(unknown_faces)}"
    if os.path.isfile(path) == False:
        os.mkdir(f"{path}") # Creating directory to store newly captured face
        pass

    crop_face = frame[top:bottom+1,left:right+1] # Cropping face from the image

    if name == "Unknown":
        face_file = f"{name}_{str(len(unknown_faces))+'.jpg'}"
        cv2.imwrite(os.path.join(path, face_file),crop_face) # Writing image to a "path" directory

    print(f"---Captured---") # Printing message every time an image is captured

def main():
    """Initializing main function"""
    facial_recognition()

if __name__ == "__main__":
    main()
