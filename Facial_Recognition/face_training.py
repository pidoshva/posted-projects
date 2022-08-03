"""
Facial Recognition
by Vadim Pidoshva (Geleus)
Completed: 08/02/2022
https://geleus.io/
"""
import os
import cv2
from imutils import paths
import face_recognition as fr

def refresh_dataset():
    """Updating known faces dataset"""

    global known_faces_names
    global known_faces_encodings
    global known_images_paths

    known_faces_names = []
    known_faces_encodings = []
    known_images_paths = []

    path = "Faces/" # Directory path with all the faces

    for path in list(paths.list_images(path)):
        if path not in known_images_paths:
            known_images_paths.append(path) # Collecting all existing face paths
        if path.split("/")[1] not in known_faces_names:
            known_faces_names.append(path.split("/")[1]) # Separating name from the path

    for face in known_images_paths:
        loaded_img = fr.load_image_file(face) # Loading face image from the path
        known_faces_encodings.append(fr.face_encodings(loaded_img)[0]) # Encoding face with first choice of encoding

def use(ds):
    """Using dataset data structures"""

    if ds == "known_faces_names":
        return known_faces_names
    elif ds == "known_faces_encodings":
        return known_faces_encodings
