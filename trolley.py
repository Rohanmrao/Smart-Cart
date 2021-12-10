import numpy as np
import cv2
from time import sleep

from pyfirmata import Arduino
from time import sleep

red_left_path_threshold = 150
red_right_path_threshold = 400

counter = 0

echopin = 12
# trigpin = 12

in1 = 2
in2 = 4
in3 = 7
in4 = 8

ir = 13

start = 0 
end = 0

direction_memory = "" # stores a string , whisch is the direction the person took on the turn 



def vision():

	global counter , direction_memory

	my_feed = cv2.VideoCapture(0)

	while True:

		print(counter)

		_,frame = my_feed.read()

		
		hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
		red_lb = np.array([136, 87, 111],np.uint8)
		red_ub = np.array([180, 255, 255],np.uint8)
		red_mask= cv2.inRange(hsv1,red_lb,red_ub)

		kernel=np.ones((40,40),"uint8")
		ret,thresh1 = cv2.threshold(red_mask,127,255,0)

		red_mask = cv2.dilate(red_mask,kernel)
		res_red = cv2.bitwise_and(frame,frame,mask=red_mask)
	
		contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # red tracker contours 

		for current_contour in contours:

			if(trolley.digital[ir].read() == 0):  #increment and decrement counters 
				counter += 1
			if(trolley.digital[ir].read() == 1):
				if (counter != 0):
					counter -= 1

			idling(trolley = trolley) # initial idling 

			M = cv2.moments(thresh1)

			if M["m00"] != 0:
				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])
			else:
				cx = 0
				cy = 0

			
			if(cx <= red_left_path_threshold):
				print("left",cx)
				direction_memory = "left"
				left(trolley = trolley)
				sleep(0)

				if (cx >= red_left_path_threshold and (counter == 2)):

					while (trolley.digital[ir].read() == 1): # cuz the while loop ends at a new black spot, i.e ctr = 3
						fwd(trolley = trolley)
						# till the last black spot is reached

					dir_mem(trolley = trolley)

			if(cx <= red_right_path_threshold):
				print("right",cx)
				direction_memory = "right"
				right(trolley = trolley)
				sleep(0)

				if (cx >= red_right_path_threshold and (counter == 2)):
					while (trolley.digital[ir].read() == 1):
						fwd(trolley = trolley)
						# till the last black spot is reached

					dir_mem(trolley = trolley)

			else:
				while counter != 3:
					print("fwd",cx)
					fwd(trolley = trolley)
					sleep(0)

				idling(trolley = trolley)
				# to add the button to stop following 


		for pic, contour in enumerate(contours):
			red_area = cv2.contourArea(contour)

			if(red_area > 10000):
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y),(x + w, y + h),(0, 0, 255), 2)
				cv2.putText(frame, "RED", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))

			elif(red_area < 10000):
				Red_signature = 0


		cv2.imshow("Frame",frame)
		# cv2.imshow("Mask",red_mask)
		if(cv2.waitKey(1)==0):
			break
        
	my_feed.release()
	cv2.destroyAllWindows()

trolley = Arduino("COM4")

print("version - ",trolley.get_firmata_version())


def fwd(trolley:Arduino):
    trolley.digital[in1].write(1)
    trolley.digital[in2].write(0)
    trolley.digital[in3].write(1)
    trolley.digital[in4].write(0)
    trolley.pass_time(1)

def bwd(trolley:Arduino):
    trolley.digital[in1].write(0)
    trolley.digital[in2].write(1)
    trolley.digital[in3].write(0)
    trolley.digital[in4].write(1)
    trolley.pass_time(1)

def left(trolley:Arduino):
    trolley.digital[in1].write(1)
    trolley.digital[in2].write(0)
    trolley.digital[in3].write(0)
    trolley.digital[in4].write(0)
    trolley.pass_time(1)

def right(trolley:Arduino):
    trolley.digital[in1].write(0)
    trolley.digital[in2].write(0)
    trolley.digital[in3].write(1)
    trolley.digital[in4].write(0)
    trolley.pass_time(1)

def idling(trolley:Arduino):
    trolley.digital[in1].write(0)
    trolley.digital[in2].write(0)
    trolley.digital[in3].write(0)
    trolley.digital[in4].write(0)

def dir_mem(trolley:Arduino):
	global direction_memory

	if (direction_memory == "left"):
		left(trolley = trolley)

	if(direction_memory == "right"):
		right(trolley = trolley)


		
def terminal():
	print("Welcome to Team Firebird's follow cart ")
	print("---------------------------------------------")

	vision()	

	

terminal()