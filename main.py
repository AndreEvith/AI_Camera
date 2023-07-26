import cv2
from openpose import pyopenpose as op

# Setup OpenPose parameters
params = dict()
params["model_folder"] = r"C:\Users\Андрей\PycharmProjects\ai_project\body"  # Set the path to the OpenPose models folder
params["number_people_max"] = 10  # Set the maximum number of people to detect

# Initialize OpenPose
openpose = op.WrapperPython()
openpose.configure(params)
openpose.start()

cap = cv2.VideoCapture('videos/humans_ai.mp4')

while True:
    success, img = cap.read()
    if not success:
        break

    # Process the image with OpenPose
    datum = op.Datum()
    datum.cvInputData = img
    openpose.emplaceAndPop([datum])

    # Get the pose keypoints for each person
    poses = datum.poseKeypoints

    # Draw the pose keypoints for each person
    for pose in poses:
        for i, joint in enumerate(pose):
            if joint.all():
                x, y, _ = joint
                cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)

    cv2.imshow('Result', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
#import cv2
#import mediapipe as mp

#mp_drawing = mp.solutions.drawing_utils
#mp_pose = mp.solutions.pose

#cap = cv2.VideoCapture('videos/humans_ai.mp4')

#with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.5) as pose:
#    while True:
#        success, img = cap.read()
#        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#        img = cv2.resize(img, (img.shape[1] // 3, img.shape[0] // 3))
#        if not success:
#            break

#        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#        img.flags.writeable = False

#        results = pose.process(img)

#        img.flags.writeable = True
#        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#        if results.pose_landmarks:
#            for landmarks in results.pose_landmarks.landmark:
#                # Access individual landmark points using 'landmarks' variable
#                x = int(landmarks.x * img.shape[1])
#                y = int(landmarks.y * img.shape[0])
#                cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

#        cv2.imshow('Result', img)

#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break

#cap.release()
#cv2.destroyAllWindows()







