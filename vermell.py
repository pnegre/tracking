#! /usr/bin/env python
# -*- coding: utf-8 -*-


#############################################################################
import sys
from opencv import cv
from opencv import highgui

#############################################################################
# definition of some constants
cam_width = 640
cam_height = 480


#############################################################################

def create_and_position_window(name, xpos, ypos):
	''' a function to created a named widow (from name), 
		and place it on the screen at (xpos, ypos) '''
	highgui.cvNamedWindow(name, highgui.CV_WINDOW_AUTOSIZE) # create the window
	highgui.cvResizeWindow(name, cam_width, cam_height) # resize it
	highgui.cvMoveWindow(name, xpos, ypos) # move it to (xpos,ypos) on the screen

def setup_camera_capture(device_num=0):
	''' perform camera setup for the device number (default device = 0) i
		return a reference to the camera Capture
	'''
	try:
		# try to get the device number from the command line
		device = int(device_num)
	except (IndexError, ValueError):
		# no device number on the command line, assume we want the 1st device
		device = 0
	print 'Using Camera device %d'%device

	# no argument on the command line, try to use the camera
	capture = highgui.cvCreateCameraCapture (device)

	# set the wanted image size from the camera
	highgui.cvSetCaptureProperty (capture,highgui.CV_CAP_PROP_FRAME_WIDTH, cam_width)
	highgui.cvSetCaptureProperty (capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, cam_height)

	# check that capture device is OK
	if not capture:
		print "Error opening capture device"
		sys.exit (1)

	return capture    

# so, here is the main part of the program
def main():

	# create windows 
	#create_and_position_window('RGB_VideoFrame', 10+cam_width, 10)
	create_and_position_window('red', 10, 10)

	capture = setup_camera_capture()

	# create images for the different channels
	r_img = cv.cvCreateImage (cv.cvSize (cam_width,cam_height), 8, 1)
	g_img = cv.cvCreateImage (cv.cvSize (cam_width,cam_height), 8, 1)
	b_img = cv.cvCreateImage (cv.cvSize (cam_width,cam_height), 8, 1)
	laser_img = cv.cvCreateImage (cv.cvSize (cam_width,cam_height), 8, 1)
	cv.cvSetZero(r_img)
	cv.cvSetZero(g_img)
	cv.cvSetZero(b_img)
	cv.cvSetZero(laser_img)
	
	storage = cv.cvCreateMemStorage(0)

	while True: 
		# 1. capture the current image
		frame = highgui.cvQueryFrame (capture)
		if frame is None:
			# no image captured... end the processing
			break

		cv.cvSplit(frame, b_img, g_img, r_img, None)
		cv.cvInRangeS(r_img, 150, 255, r_img)
		cv.cvInRangeS(g_img, 0, 100, g_img)
		cv.cvInRangeS(b_img, 0, 100, b_img)

		cv.cvAnd(r_img, g_img, laser_img)
		cv.cvAnd(laser_img, b_img, laser_img)
		cv.cvErode(laser_img,laser_img) #,0,2)
		cv.cvDilate(laser_img,laser_img)
		
		c_count, contours = cv.cvFindContours (laser_img, storage, cv.CV_CHAIN_APPROX_NONE)
		
		#highgui.cvShowImage ('RGB_VideoFrame', frame)
		highgui.cvShowImage ('red', laser_img)

		# handle events
		k = highgui.cvWaitKey (10)

		if k == '\x1b' or k == 'q':
			# user has press the ESC key, so exit
			break


if __name__ == '__main__':
	main()