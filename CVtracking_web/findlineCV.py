import os
import cv2
from base_camera import BaseCamera
import numpy as np

def get_line(lineIndex_Pos, thickness, offset):
    lines = []
    left = 999
    right = 0
    for pixel in lineIndex_Pos[0]:
        if pixel != right + 1:
            if abs((right - left) - thickness) <= offset:
                line_center = (left + right) // 2
                lines.append(line_center)
                left = pixel
                continue
            left = pixel
        pixel_old = pixel
        right = pixel
    lines.sort(key=lambda x: abs(x - 320))
    return lines[0]

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()
    
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        
        linePos_1 = 440
        linePos_2 = 380
        lineColorSet = 0

        left_Pos1 = None
        right_Pos1 = None
        center_Pos1 = None

        left_Pos2 = None
        right_Pos2 = None
        center_Pos2 = None

        center = None

        thickness1 = 88
        thickness2 = 78

        offset = 20

        while True:
            # read current frame
            _, frame_image = camera.read()

            # OTSU 알고리즘으로 이분화 이미지
            frame_findline = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
            _, frame_findline = cv2.threshold(frame_findline, 0, 255, cv2.THRESH_OTSU)
            frame_findline = cv2.erode(frame_findline, None, iterations=6)

            colorPos_1 = frame_findline[linePos_1]
            colorPos_2 = frame_findline[linePos_2]
            try:
                lineIndex_Pos1 = np.where(colorPos_1 == lineColorSet)
                lineIndex_Pos2 = np.where(colorPos_2 == lineColorSet)

                center_Pos1 = get_line(lineIndex_Pos1, thickness1, offset)
                center_Pos2 = get_line(lineIndex_Pos2, thickness2, offset)

            except:
                center_Pos1 = 320
                center_Pos2 = 320
            
            yield frame_findline, center_Pos1, center_Pos2