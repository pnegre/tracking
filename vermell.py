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
	

def returnEllipses(contours):
	ellipses = []
	for c in contours.hrange():
		count = c.total;
		if( count < 6 ):
			continue;
		PointArray = cv.cvCreateMat(1, count, cv.CV_32SC2)
		PointArray2D32f= cv.cvCreateMat( 1, count, cv.CV_32FC2)
		cv.cvCvtSeqToArray(c, PointArray, cv.cvSlice(0, cv.CV_WHOLE_SEQ_END_INDEX));
		cv.cvConvert( PointArray, PointArray2D32f )
		
		box = cv.CvBox2D()
		box = cv.cvFitEllipse2(PointArray2D32f);
		#cv.cvDrawContours(frame, c, cv.CV_RGB(255,255,255), cv.CV_RGB(255,255,255),0,1,8,cv.cvPoint(0,0));

		center = cv.CvPoint()
		size = cv.CvSize()
		center.x = cv.cvRound(box.center.x);
		center.y = cv.cvRound(box.center.y);
		size.width = cv.cvRound(box.size.width*0.5);
		size.height = cv.cvRound(box.size.height*0.5);
		box.angle = -box.angle;
		ellipses.append({'center':center, 'size':size, 'angle':box.angle})
	return ellipses


# so, here is the main part of the program
def main():

	# create windows 
	create_and_position_window('RGB_VideoFrame', 10+cam_width, 10)
	#create_and_position_window('red', 10, 10)

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
		
		c_count, contours = cv.cvFindContours (laser_img, 
												storage,
												cv.sizeof_CvContour,
												cv.CV_RETR_LIST,
												cv.CV_CHAIN_APPROX_NONE,
												cv.cvPoint (0,0))
		
		if c_count:
			ellipses = returnEllipses(contours)
			for e in ellipses:
				cv.cvEllipse(frame, e['center'], e['size'],
						e['angle'], 0, 360,
						cv.CV_RGB(0,0,255), 1, cv.CV_AA, 0);
				
				
		highgui.cvShowImage ('RGB_VideoFrame', frame)
		#highgui.cvShowImage ('red', laser_img)

		# handle events
		k = highgui.cvWaitKey (10)

		if k == '\x1b' or k == 'q':
			# user has press the ESC key, so exit
			break


if __name__ == '__main__':
	main()
