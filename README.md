<h1> Introduction to table-py</h2>
<p align="justify">table-py is a Python (2.7) wrapper and Arduino UNO driver for a Lego based or completely 3D printable photogrammetry machine!  The setup is basically a stepper motor driven by an Adafruit v1.0 or v2.0 motor shield; attached to an Arduino UNO and connected by serial/USB to a PC.  The wrapper is for utilising the program gphoto2 in order to control a digital SLR, which takes a picture of an object placed on the turn-table and then tells the motor to step via the Arduino.  In this way, a user can take pictures of a object around a fixed point for later use in photogrammetry software in order to build a 3D model of the chosen object.  Such a set up is useful as it frees up the user from having to aim the camera, or move the object themselves, potentially saving both time and improving overall consistency.</p>

<h2>Build Instructions (for the actual machine)</h2>
<p align="justify">Build instructions for the Lego machine are not available, however, the Lego Digital Designer file is included <a href="https://github.com/BeebBenjamin/table-py/blob/master/parts/lego%20parts/turn-table-m3.lxf">here</a> and can therefore be reverse engineered using Lego Digital Designer (available from www.Lego.com).  A BOM can also be found in this repository on GitHub <a href="https://github.com/BeebBenjamin/table-py/edit/master/BOM.xlsx">here</a></p>

<h2>Software</h2>
table-py consists of a python wrapper and Arduino firmware that makes use of a number of third party libraries/programs that need to be installed on your computer for it to work correctly and these are listed below:

<h3>Arduino libraries</h3>

AFMotor.h (library) obtained from GitHub <a href="https://github.com/adafruit/Adafruit-Motor-Shield-library/zipball/master">here</a>.

<h3>Python modules</h3>

python2.7 (installation) obtained from <a href="https://www.python.org/download/releases/2.7/">here</a>.

pyserial (module) obtained through apt (Advanced Package Tool) for Linux or from GitHub 
<a href="https://github.com/pyserial/pyserial/zipball/master">here</a>.

<h3>External programs</h3>

gphoto2 (program) obtained through apt (Advanced Package Tool) for Linux or from GitHub
<a href="https://github.com/gphoto/gphoto2/zipball/master">here</a>.  It can be a real pain getting things like this onto a Mac, however, I believe gphoto is available on "Macports" which has saved my bacon before.

<h2>Instructions of Use</h2>

Once you have built the machine and have all of these packages/libraries installed follow the instructions below in order to control your setup!

<p align="justify">Using the Ardunio IDE (after you have installed the AFMotor library) copy and paste the code in table-py.ino into the code window and save with whatever name you like.  Then with your Ardunio board (UNO) connected via a USB cable press upload.  You shouldn't get any error messages if you have the required library installed.  To test it's working you can open the serial monitor and type a 'M' this should tell the firmware to make one step.  The motor will step once and hold until you type an 'N' into the serial monitor (to release the motor).  <b>N.B. if you do not release the motor after testing you wont be able to turn it manually and the motor may get hot.</b></p>

<p align="justify">Next attach you digital SLR camera via a USB cable and unmount it if using Linux, on a Mac this is done in the terminal using the command "killall PTPCamera".  N.B. I have only tested this with a Canon EOS 30D and a Nikon D5100 on Ubuntu/OSx and would appreciate feedback on another camera/OS.  I do know that cameras which are PTP only e.g. Canon Powershot cameras etc may not work properly with gphoto2 using their native firmware and an alternative program using CHDK and the PTP extension needs to be used.  As such my current setup won't work for you. Yet.  A list of cameras supported by gphoto2 can be found <a href="http://gphoto.sourceforge.net/proj/libgphoto2/support.php">here</a>.</p>

<p align="justify">If you have installed the pyserial module and Python 2.7 and have your Python path set correctly (particularly an issue in Windows) then you can browse to where your python script is located using the terminal and type the following command: "python table-py.py" in order to run the turn-table "in default mode" (camera active and the motor will step 35 times taking 35 pictures).  Please note that it is possible to make use of the following "flags" inorder to change those default settings:  

"--o" (override) will allow you to enter a user defined number of times you wish the table to turn and take a photo.

"--c" (camera off) will allow you to turn off gphoto2 and just make use of the turn-table, should you so wish.

These flags are entered as follows: python table-py.py --o --c in any combination depending on what you want to do.

The user will also be asked before the run to define a custom name to label photos with, if you care about this sort of thing (if nothing is entered table-py will use the camera defaults).  If all goes well, the camera will take a test photo and the table will turn and take a photo the number of times specified.  Then at the end of the run the photos will be transfered to the directory the script is running from with the user specified labels.</p>

<h2>Trouble Shooting</h2>

<h3>Camera specific Issues</h3>

Here are some things to check out if you get the "There seems to be an issue communicating with your camera" error. 
Check the camera is unmounted.

Check the USB is plugged in.

Check that the battery is working and charged.

Check your camera model is compatible with gphoto2.

Some cameras need to have "Normal" or "PC communication" activated and not "Print/PTP" in order to work with gphoto2.

<h3>Arduino Issues</h3>

<p align="justify">If the motor doesn't step check which motor slot it is attached to.  The firmware specifies "M4" of the Adafruit v1.2 motor shield as the default.  You may change this if you want to.</p>
