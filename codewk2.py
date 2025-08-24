import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

tello.connect()

keepRecording = True

tello.streamon()
frame_read = tello.get_frame_read()


def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


recorder = Thread(target=videoRecorder)
recorder.start()

tello.enable_mission_pads()
tello.set_mission_pad_detection_direction(2)

tello.takeoff()

pad = tello.get_mission_pad_id()

while pad != 1:
    if pad == 2:
        tello.rotate_clockwise(180)
        tello.rotate_counter_clockwise(180)
    elif pad == 3:
        cv2.imwrite("pictureo108.png", frame_read.frame)
    elif pad == 7:
        tello.move_left(50)
        tello.move_right(50)
    elif pad == 5:
        print(tello.get_battery())
    elif pad == 6:
        tello.move_forward(50)
        tello.move_back(50)

    pad = tello.get_mission_pad_id()

tello.land()
keepRecording = False
recorder.join()
