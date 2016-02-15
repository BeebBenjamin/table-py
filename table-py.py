import serial
import sys
import os
import subprocess
import time
import atexit

from serial import SerialException

try:

	def exit_handler():
		ser = serial.Serial(serial_name, 9600)
		ser.write('N')
		print "\n\nApplication terminating, closing down motor, Goodbye!\n"

	atexit.register(exit_handler)

	serial_name = "/dev/cu.usbmodem1411"

	#do you want the working directory to be optional?

	working_directory = "/Users/Ardern/Desktop/3D_scan/1" #sys.path[0] # example would be '/home/richard/Documents' but currently just grabs the directory the python script is in! "/Users/Ardern/Desktop/NMBE/1"

	try:

		ser = serial.Serial(serial_name, 9600)

		#look for flags in the system command line

		options = sys.argv

		#if there is an override '--o' flag then the user will be prompted for the custom number of steps they want the table to make, it's usually around 35 per turn. 

		if "--o" in options:

			while True:

			#loop until user gives correct answer

				iterations = raw_input("\nHow many iterations do you need? ")

				try:

					iterations = int(iterations)

					break

				except:

					print "\nThis is not an integer (whole number), please type in an integer value!\n"

		#otherwise use the default value.

		else:

			iterations = 38

	

		#if there is an override '--c' flag then the user will be prompted for the number of seconds they want the delay to be between each step and photo!

		if "--c" in options:

			camera_override = True

			while True:

				#loop until user gives correct answer

				time_interval = raw_input("\nHow many seconds would you like inbetween each step? ")

				try:

					time_interval = int(time_interval)

					break

				except:

					print "\nThis is not an integer (whole number), please type in an integer value!\n"

		#otherwise assume a camera is attached!

		else:

			while True:
				
				while True:
			
					motor_type = raw_input("\nWhat type of motor are you using (e.g. 1 for 5v, 2 for 12v)? ")
					
					if motor_type not in ['1','2']:
						print "\nPlease select only a '1' or a '2'"
					else:
						break
					
			
				print ""
			
				institution_ID = raw_input("What is the institutional code and unique id for this specimen (e.g. NMBE_XXXX)? ")

				print ""

				confirmation = raw_input("Are you sure you wish to use this ID#: " + institution_ID + "?  Type y/n: ")

				if confirmation == "y":

					print ""

					break

				elif confirmation == "n":

					print ""

		

			while True:

				position = raw_input("Dorsal or Ventral?  Type d/v: ")

				print ""

				confirmation = raw_input("Are you sure you want to use this position: " + position + "?  Type y/n: ")

				if confirmation == "y":

					if position == "d":

						position = "DORSAL"
						break

					elif position == "v":

						position = "VENTRAL"
						break
					
					else:
						print "\n'd' or 'v' has not been selected, please specify ventral or dorsal by following the instructions!\n"
				

				elif confirmation == "n":

					print ""

			

			camera_override = False

			time_interval = 0

		#warn the user of the default settings and the override options.

		if "--o" in options and "--c" in options:

			print "\nRunning program with user specified steps and camera overridden!\n"

		elif "--o" in options and "--c" not in options:

			print "\nRunning program with user specified steps and camera active!\n"

		elif "--o" not in options and "--c" in options:

			print "\nRunning program with default steps and camera overridden!\n" 

		else:

			print "Running program in default mode: of 35 photos and steps.\n\nIf you require more per revolution include the flag '--o'.\n\nIf you want to turn off the camera include '--c'.\n"

	

		#specify the camera options here by separating them with a comma!

		cmd = ['gphoto2','--auto-detect','--capture-image','--keep']



		check = False
	
		#here it runs three times prompting the user to change camera positions
		for i in range(0,3):
			for a in range(1,int(iterations)+1):
				if camera_override == True:
					if motor_type == '1':
						ser.write('1')
					elif motor_type == '2':
						ser.write('2')			

					time.sleep(time_interval)

				else:

				#check for camera errors!  If it can't connect to the camera to take a picture it will 

					if check != True:

						print "Taking a test image to see if the camera is working!"

						try:

							subprocess.check_output(cmd,cwd=working_directory)

							print ""

							print "Camera works, runing through iterations now!\n"

							check = True

						except:

							print "/nThere seems to be an issue communicating with your camera, please check it is plugged in, the battery is charged, it is unmounted, and a supported model for gphoto2!\n"

							break

					run gphoto2 as a subprocess and feed it the cmd string

					process = subprocess.Popen(cmd,cwd=working_directory)

					output = process.communicate()[0]
					
					time.sleep(0.25)
				
					print output

					process.wait()
				
				
				
					proceed=''

					if motor_type == '1':
						ser.write('1')
						print str(a) + " Using motor 1"
					elif motor_type == '2':
						ser.write('2')
						print str(a) + " Using motor 2"
					while (proceed != 'D'):
						proceed = ser.read()
						print proceed
						pass

					print ""

				last_int = a-1
				
			time.sleep(3)

			ser.write('N')
			
			while True:
				
				if i !=2:
					continue_run = raw_input("Run " + str(i+1) + " of 3 complete, please reposition the camera, type 'y' and enter to confirm or 'n' to cancel and stop the run. ")
				
					if continue_run != 'y':
						if continue_run == 'n':
							print "\nEnding run, continuing with image processing...\n"
							break
						else:
							print "\nPlease type either 'y' or 'n'\n"
					else:
						break
				if continue_run == 'n': break
				
				if i==2:
					print "Run 3 of 3 complete, moving on to image processing!"
					break
			print ""
		
		cmd = ['gphoto2','--auto-detect','--list-files']

		process = subprocess.Popen(cmd,cwd=working_directory,stdout=subprocess.PIPE)

		process.wait()

		files = []

		for line in iter(process.stdout.readline,''):

			if "#" in line.rstrip():

				files.append(line.rstrip())

		#only one indent here or it wont work!

		last_pic = int(files[-1].split(" ")[0].strip("#"))

		loop in reverse using number of photos taken and last file number in order to calculate which files to rename and download

		for i in reversed(range(1,last_int+1)):

			cmd = ['gphoto2','--auto-detect',"--filename=" + institution_ID + "_" + position + "_" + str(i) + ".jpg",'--get-file',str(last_pic-i)]

			process = subprocess.Popen(cmd,cwd=working_directory)

			process.wait()

		print "Done!"

	except SerialException:

		print "Port not found, please make sure the arduino is plugged into the USB port!"

except KeyboardInterrupt:
	sys.tracebacklimit = 0
