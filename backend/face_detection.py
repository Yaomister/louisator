
import face_recognition
import numpy as np
import pathlib
import cv2
from io import BytesIO

class FaceDetection:
    def __init__(self, known_faces):
        self.known_faces = []
        self.known_names = []
        if (known_faces is not None and len(known_faces) > 0):
            for name, face in known_faces:
                print(f"Added {name}")
                face_image = face_recognition.load_image_file(BytesIO(face))
                self.known_faces.append(face_recognition.face_encodings(face_image)[0])
                self.known_names.append(name)

        else:
            base_dir = pathlib.Path(__file__).resolve().parent
            path = base_dir / "known_faces"
            for img_path in path.iterdir():
                if img_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                    img = face_recognition.load_image_file(img_path)
                    self.known_faces.append(face_recognition.face_encodings(img)[0])
                    self.known_names.append(img_path.stem)


    def recognize(self, frame):

        face_locations = face_recognition.face_locations(frame)

        face_encodings = face_recognition.face_encodings(frame, face_locations)

        res = []
        for encoding, location in zip(face_encodings, face_locations):

            matches = face_recognition.compare_faces(self.known_faces, encoding)
            name = "unknown"
            if True in matches:
                index = matches.index(True)
                name = self.known_names[index]
            res.append((name, location))

        return res


            
            

            
