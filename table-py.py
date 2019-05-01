#!/usr/bin/python2

#import all python 2.7 native modules
import serial, sys, os, subprocess, time, atexit

#import all non-native modules including: distance, biopython and numpy
from serial import SerialException

def main():	
	#try until user uses a keyboard interrupt
	try:
		#function send a motor off signal to the arduino upon exiting
		def exit_handler():
			ser = serial.Serial(serial_name, 9600)
			ser.write('N')
			print "\n\nApplication terminating, closing down motor, Goodbye!\n"
		
		#register the exit_handler function to exit event
		atexit.register(exit_handler)
		
		#serial name will be different for a Mac or Linux/GNU
		serial_name = "/dev/cu.usbmodem1411" #set for Mac
		
		#define working directory by grabbing the path of the current script
		working_directory = sys.path[0] # can be changed to something like '/home/user/Documents/subfolder' but currently just grabs the directory the python script is in!
		
		#try establishing a serial connection
		try:
			#define serial using name grabbed above
			ser = serial.Serial(serial_name, 9600)

			#look for flags passed as arguments in the system command line
			options = sys.argv

			#if there is an override '--o' flag then the user will be prompted for the custom number of steps they want the table to make, it's usually around 35 per turn. 
			if "--o" in options:
				
				#loop until user gives correct answer
				while True:
					
					#ask user to define how many pictures they need per 360 degs via the terminal
					iterations = raw_input("\nHow many iterations do you need? ")
					
					#try to convert the answer given by the user to a integer
					try:
						
						iterations = int(iterations)

						break
					
					#if variable isnt convertable to an integer ask again for correct input
					except:

						print "\nThis is not an integer (whole number), please type in an integer value!\n"

			#otherwise use the default value.
			else:

				iterations = 38



			#if there is an override '--c' flag then the user will be prompted for the number of seconds they want the delay to be between each step and photo.  The camera will turn off and the table will just turn with the object on.
			if "--c" in options:
				
				#do not use the camera
				camera_override = True
				
				#loop until user gives correct answer
				while True:
					
					#ask user to define how many seconds they want to wait between each step (to simulate presence of a camera)
					time_interval = raw_input("\nHow many seconds would you like inbetween each step? ")
					
					#try to convert the answer given by the user to a integer
					try:

						time_interval = int(time_interval)

						break
						
					#if variable isnt convertable to an integer ask again for correct input
					except:

						print "\nThis is not an integer (whole number), please type in an integer value!\n"

			#otherwise assume a camera is attached!
			else:
				#loop until user gives correct answer re: institution ID
				while True:
					
					#loop until user gives correct answer re: motor type
					while True:
						
						#ask for user to choose between a 5v or a 12v motor by typing a 1 or a 2
						motor_type = raw_input("\nWhat type of motor are you using (e.g. 1 for 5v, 2 for 12v)? ")
						
						#if answer isn't a 1 or a 2 ask again for correct input
						if motor_type not in ['1','2']:
							print "\nPlease select only a '1' or a '2'"
						else:
							break

					#terminal text spacer
					print ""
					
					#ask for user to define a unique sample code for each set of photos
					institution_ID = raw_input("What is the institutional code and unique id for this specimen (e.g. NMBE_XXXX)? ")
					
					#terminal text spacer
					print ""
					
					#ask user to confirm their choice of sample code
					confirmation = raw_input("Are you sure you wish to use this ID#: " + institution_ID + "?  Type y/n: ")
					
					#if the user confirms move on
					if confirmation == "y":
						
						#terminal text spacer
						print ""

						break
						
					#if the user rejects ask for input again
					elif confirmation == "n":
						
						#terminal text spacer
						print ""
				
				#loop until the user defines if the sample being photographed is the dorsal or ventral side
				while True:
					
					#ask user to use a 'd' or a 'v' to select dorsal or ventral 
					position = raw_input("Dorsal or Ventral?  Type d/v: ")
					
					#terminal text spacer
					print ""
					
					#ask user to confirm their choice of side
					confirmation = raw_input("Are you sure you want to use this position: " + position + "?  Type y/n: ")
					
					#if the user confirms move on
					if confirmation == "y":
						
						#if dorsal selected set position variable to "DORSAL"
						if position == "d":

							position = "DORSAL"
							break
							
						#if ventral selected set position variable to "VENTRAL"
						elif position == "v":

							position = "VENTRAL"
							break
						
						#if neither dorsal or ventral selected then ask user to reconfirm their input
						else:
							print "\n'd' or 'v' has not been selected, please specify ventral or dorsal by following the instructions!\n"

					#if the user rejects ask for input again
					elif confirmation == "n":
						
						#terminal text spacer
						print ""

				#flag camera as in user
				camera_override = False
				
				#adjust the timings if you need to here, default is 0 but if the camera is slow, user can set this higher
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



			#define gphoto2 command to capture images
			cmd = ['gphoto2','--auto-detect','--capture-image','--keep']
			
			#change to true to attempt test image capture at the start of capture
			check = False

			#here the for loop runs three times prompting the user to change camera positions
			for i in range(0,3):
				for a in range(1,int(iterations)+1):
					#code to execute in loop only if camera has been overidden using the --c flag
					if camera_override == True:
						if motor_type == '1':
							ser.write('1')
						elif motor_type == '2':
							ser.write('2')			
						
						#pause program for time interval defined earlier
						time.sleep(time_interval)

					else:

						#check for camera errors!  If it can't connect to the camera to take a picture it will 
						if check != True:

							print "Taking a test image to see if the camera is working!"
							
							#attempt to take a picture using gphoto to control the camera
							try:
								#use subprocess to run the gphoto2 terminal program shelless and pass it the command list defined above and the working directory 
								subprocess.check_output(cmd,cwd=working_directory)
								
								#terminal text spacer
								print ""

								print "Camera works, runing through iterations now!\n"
								
								#flag check as True once complete so that no more test photos get taken with each loop
								check = True
							
							#if the subprocess fails tell the user and exit the program
							except:

								print "/nThere seems to be an issue communicating with your camera, please check it is plugged in, the battery is charged, it is unmounted, and a supported model for gphoto2!\n"

								break
						
						#use subprocess to run the gphoto2 terminal program shelless and pass it the command list defined above and the working directory 
						process = subprocess.Popen(cmd,cwd=working_directory)

						output = process.communicate()[0]

						time.sleep(0.25)

						print output

						process.wait()

						#reset proceed variable each iteration
						proceed=''
						
						#write to the serial port which motor is in use
						if motor_type == '1':
							ser.write('1')
							print str(a) + " Using motor 1"
						elif motor_type == '2':
							ser.write('2')
							print str(a) + " Using motor 2"
						
						#wait for the arduino to signal it is done turning by reading the serial port and looking for a 'D'
						while (proceed != 'D'):
							proceed = ser.read()
							print proceed
							pass

						print ""
						
					#define the last_int variable by grabbing last count of loop
					last_int = a-1
				
				#wait for 3 seconds
				time.sleep(3)
				
				#write an 'N' to the USB serial port to instruct the arudino to turn off the motor 
				ser.write('N')
				
				#wait for the user to confirm if they wish to keep taking photographs and finish 3 rounds at 3 camera angles?
				while True:

					#if number of rounds is not equal to 3 (index 0) then keep asking user for input each round
					if i !=2:
						continue_run = raw_input("Run " + str(i+1) + " of 3 complete, please reposition the camera, type 'y' and enter to confirm or 'n' to cancel and stop the run. ")
						
						#check if user has used a 'y' or an 'n'
						if continue_run != 'y':
							
							#if user rejects continue with an 'n' then break loop
							if continue_run == 'n':
								print "\nEnding run, continuing with image processing...\n"
								break
								
							#ask user again if answer was not a 'y' or a 'n'
							else:
								print "\nPlease type either 'y' or 'n'\n"
						
						#if user confirms with a 'y' then break loop
						elif continue_run == 'y':
							break
						else:
							print "\nPlease type either 'y' or 'n'\n"
							
					#if user rejects continue with an 'n' then break loop
					if continue_run == 'n': break
					
					#if number of rounds is equal to 3 (index 0) then break loop
					if i==2:
						print "Run 3 of 3 complete, moving on to image processing!"
						break
				print ""
			
			#define gphoto2 command to list files on camera
			cmd = ['gphoto2','--auto-detect','--list-files']
			
			#use subprocess to run the gphoto2 terminal program shelless and pass it the command list defined above and the working directory 
			process = subprocess.Popen(cmd,cwd=working_directory,stdout=subprocess.PIPE)

			process.wait()
			
			#define a variable to hold the list of photographs
			files = []
			
			#iterate through the output of subprocess and append the file names to the files variable
			for line in iter(process.stdout.readline,''):

				if "#" in line.rstrip():

					files.append(line.rstrip())

			#define the number of the last picture taken
			last_pic = int(files[-1].split(" ")[0].strip("#"))

			#loop in reverse using number of photos taken and last file number in order to calculate which files to rename and download
			for i in reversed(range(1,last_int+1)):
				
				#define the gphoto2 command to download a target image to the working directory
				cmd = ['gphoto2','--auto-detect',"--filename=" + institution_ID + "_" + position + "_" + str(i) + ".jpg",'--get-file',str(last_pic-i)]

				#use subprocess to run the gphoto2 terminal program shelless and pass it the command list defined above and the working directory
				process = subprocess.Popen(cmd,cwd=working_directory)

				process.wait()
			
			#tell the user that capture is done
			print "Done!"
		
		#if serial connection fails to initiate tell the user this is what the issue is
		except SerialException:

			print "Port not found, please make sure the arduino is plugged into the USB port!"
	
	#trigger keyboard interrupt function and shut down the arduino motors	
	except KeyboardInterrupt:
		sys.tracebacklimit = 0

#if script is running from this file run main()
if __name__ == "__main__":
	main()
