#Import opencv library
import cv2
#Import time and datetime
import time
import datetime
#Read data from webcam (video)
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

frame_size = (int(cap.get(3)),int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#Before the while loop
recording = False
detection_stopped_time = None
timer_started = False
Seconds_to_record_after_detection = 20
while(True):
    _, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,6)
    bodies = body_cascade.detectMultiScale(gray,1.3,6)
    profiles = profile_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,width,height) in bodies:
        cv2.rectangle(frame, (x,y) , (x+width ,y+height) , (0,255,0) ,3)

    for (x,y,width,height) in faces:
        cv2.rectangle(frame, (x,y) , (x+width ,y+height) , (0,0,255) ,3)

    for (x,y,width,height) in profiles:
        cv2.rectangle(frame, (x,y) , (x+width ,y+height) , (255,0,0) ,3)

    #Inside the while loop
    if(len(faces) + len(bodies) + len(profiles) > 0):
        if(recording):
            timer_started = False
        else:
            recording = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter("{}.mp4".format(current_time),fourcc,20,frame_size)
            print("Started Recording")
    elif recording:
        if timer_started:
            if time.time() -detection_stopped_time >= Seconds_to_record_after_detection:
                recording = False
                timer_started = False
                out.release()
                print("Stop Recording")
        else:
            timer_started = True
            detection_stopped_time = time.time()
    if (recording):
        out.write(frame)
    # Display the resulting frame
    cv2.imshow('Camera', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) == ord('q'):
        break
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()