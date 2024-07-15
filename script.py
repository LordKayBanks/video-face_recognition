# https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_batches.py
# https://github.com/ageitgey/face_recognition?tab=readme-ov-file#deployment
# https://github.com/ageitgey/face_recognition/blob/master/docker/README.md
# https://hub.docker.com/r/animcogn/face_recognition
# https://github.com/ageitgey/face_recognition/issues/357

import face_recognition
import cv2
import os


# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

known_images_folder_path = "known_faces/"
input_video_folder_path = "video_files/short_hamilton_clip.mp4"
# input_video_folder_path = "video_files/hamilton_clip.mp4"

# Open the input movie file
input_movie = cv2.VideoCapture(input_video_folder_path)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('output.avi', fourcc, 29.97, (640, 360))


known_faces_encodings = []
known_faces_names = []
for filename in os.listdir(known_images_folder_path):
    file_path = os.path.join(known_images_folder_path, filename)
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Load the image file
        image = face_recognition.load_image_file(file_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            known_faces_encodings.append(face_encodings[0])
            known_faces_names.append(filename)
# ==================================================



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
   #  print("\nface_encodings: \n", face_encodings)

    face_names = []
    for i,face_encoding in enumerate(face_encodings):
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.50)
        name = None
        for match in matches:
           name = os.path.splitext(os.path.basename(known_faces_names[i]))
           face_names.append(name)

        
    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name[0], (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("Writing frame {} / {}".format(frame_number, length))
    output_movie.write(frame)

# All done!
input_movie.release()
# cv2.destroyAllWindows()