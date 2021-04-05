# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 14:54:58 2021

@author: james
"""

from pyparrot.Bebop import Bebop
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
from pyparrot.DroneVisionGUI import DroneVisionGUI
from PyQt5.QtGui import QImage
import imutils
import os
import detect

#%%

def draw_current_photo():
    """
    Quick demo of returning an image to show in the user window.  Clearly one would want to make this a dynamic image
    """
    image = cv2.imread('test_image_000001.png')

    if (image is not None):
        if len(image.shape) < 3 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, byteValue = image.shape
        byteValue = byteValue * width

        qimage = QImage(image, width, height, byteValue, QImage.Format_RGB888)

        return qimage
    else:
        return None

class area:
    
    def __init__(self,width,length,height,tilt = True,dronepos = [0,0,None,0]):
        self.__width = width
        self.__length = length
        self.__height = height
        self.__home = np.array(dronepos)
        self.__pastcanetoads = [[],[],[],[]]
        self._dronepos = np.array(dronepos)
        self.bebop = Bebop()
        self._sensors = {'alt':None, 'roll':None, 'pitch':None, 'yaw':None}
        self.tilt = tilt
        self.bebopVision = None
        
        
        
        #space for sim code
        
        
        
    #space for sim code 'markpos()'
        #
        #
        #
        #
        #
        #
        #
        

    def get_sensors(self):
        self._sensors['alt'] = self.bebop.sensors.sensors_dict['AltitudeChanged_altitude']
        self._sensors['roll'] = self.bebop.sensors.sensors_dict['AttitudeChanged_roll']
        self._sensors['pitch'] = self.bebop.sensors.sensors_dict['AttitudeChanged_pitch']
        self._sensors['yaw'] = self.bebop.sensors.sensors_dict['AttitudeChanged_yaw']
        self._dronepos[2] = self._sensors['alt']
        print('SENSORS:\n')
        print(self._sensors)
        print('\n')

    def move_by(self,dx=0,dy=0,dz=0,rotcw=0):
        '''This only works with rotation = 0 currently.
        dx = right
        dy = forwards
        dz = up'''
        if dx == 0 and dy == 0 and dz ==0 and rotcw == 0:
            print('Error: No movement specified\n')
        self.bebop.move_relative(dy,dx,-dz,rotcw)
        self._dronepos[0] += dx
        self._dronepos[1] += dy
        self._dronepos[2] += dz
        self._dronepos[3] += rotcw
        
        #sim code markpos()

    def burst(self, detector):

        print('Capture started')
        for i in range(5):
            frame = self.bebopVision.get_latest_valid_picture()
            if frame is not None:
                vis_objects = detector.run_detection(frame)  # object detection bit
                vis_canetoads = []
                for obj in vis_objects:
                    box = obj["box_coords"]
                    # calculate centre coordinates of bounding box from corner coordinates
                    obj["centre_coord"] = (int((box[0][0] + box[1][0]) / 2), int((box[1][0] + box[1][1]) / 2))

                    if obj['class_name'] == 'Cane_Toad':
                        vis_canetoads.append(obj)
                        print('Cane toad spotted')
                cv2.imshow('Capture{}_{}'.format(i,self._dronepos[1]), frame)
            # print(vis_canetoads)
            # return vis_objects, vis_canetoads
            
                self.__pastcanetoads.pop(0) # update rolling list of canetoads
                self.__pastcanetoads.append(vis_canetoads)
        print(self.__pastcanetoads)
            
    def move_to_backflip_return(self, detector):
        print('Cane toad detected. Moving...')
        withcanetoads = [] # a list of the first cane toad in each frame
        for i in range(len(self.__pastcanetoads)):
            if len(self.__pastcanetoads[i]) != 0:
                withcanetoads.append(self.__pastcanetoads[i][0])

        # calulate weighted avg position of latest three frames
        # 0.15 for old, 0.35 for med and 0.5 for new
        box_coords = withcanetoads[-3]["centre_coord"]
        old_x = withcanetoads[-3]['centre_coord'][0]
        old_y = withcanetoads[-3]['centre_coord'][1]
        med_x = withcanetoads[-2]['centre_coord'][0]
        med_y = withcanetoads[-2]['centre_coord'][1]
        new_x = withcanetoads[-1]['centre_coord'][0]
        new_y = withcanetoads[-1]['centre_coord'][1]
        
        x_pix = old_x*0.15 + med_x*0.35 + new_x*0.5
        y_pix = old_y*0.15 + med_y*0.35 + new_y*0.5
        
        dx_pix = x_pix - 428
        dy_pix = y_pix - 240
        self.get_sensors()
        dy_m = self._sensors['alt']*dy_pix/587
        dx_m = self._sensors['alt']*dx_pix/587
        
        self.move_by(dx = dx_m, dy = dy_m)
        self.move_by(dz = -0.5)
        
        self.burst(detector)
        
        di = {1:0,2:0,3:0}
        print(self.__pastcanetoads)
        
        li = []
        for i in self.__pastcanetoads:
            li.append(len(i))
        for i in li:
            di[i] = li.count(i)
        print(di)
        if di[1] >= 3 or di[2] >= 3 or di[3] >= 3:
            self.bebop.flip('back')
        
        self.move_by(dx = -dx_m, dy = -dy_m, dz = 0.5)
        
    def run_with_vision(self,args):
        
        #setup
        step = args[0] # parameters
        length = args[1]
        flightalt = args[2]
        detector = args[3]
        if self.tilt:
            self.bebop.pan_tilt_camera_velocity(-30,0,3) # make sure camera facing down
        # takeoff and move to starting position
        self.bebop.safe_takeoff(5)
        self.bebop.get_sensors()
        dz = flightalt - self._sensors['alt']
        self.move_by(dz = dz)
        
        # movement loop
        while self._dronepos[1] < length:
            
            self.burst(detector)
            
            di = {1:0,2:0,3:0}
            print(self.__pastcanetoads)
            
            li = []
            for i in self.__pastcanetoads:
                li.append(len(i))
            for i in li:
                di[i] = li.count(i)
            print(di)
            if di[1] >= 3 or di[2] >= 3 or di[3] >= 3:
                self.move_to_backflip_return()
                    
            self.move_by(dy=step)
            
        self.move_by(-self.dronepos[0],-self._dronepos[1])
        self.bebop.smart_land(5)

    def run(self,step,length,flightalt, detector):
        success = self.bebop.connect(10)
        
        if success:
            bebopVision = DroneVisionGUI(self.bebop, is_bebop=True, user_code_to_run = self.run_with_vision,
                                         user_args=(step,length,flightalt, detector), user_draw_window_fn=draw_current_photo)
            bebopVision.open_video()
            self.bebopVision = bebopVision
        else:
            print("Error connecting to bebop.  Retry")
            
print('\n All files loaded\n')