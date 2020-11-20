import cv2

name = "Duration of video"
id = "duration-of-video"

def process(path):
  cap = cv2.VideoCapture(path)
  fps = cap.get(cv2.CAP_PROP_FPS)
  frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

  duration = frame_count / fps

  cap.release()

  return {"good": True, "str": "Video length is " + str(round(duration, 2)) + " seconds"}
