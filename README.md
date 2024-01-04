# Greet Bot
Project Objective
1.	To develop a robot that can recognize the face of a person and greet him/her in real time.
2.	The robot should give the directions of certain locations when asked.

Project Details
When the robot detects the human using the Mediapipe person pose library, it will move towards it by following a black line. After reaching near to the person, his/her face is detected using the Mediapipe face mesh library. This ML model detected 468 landmarks on the face of a person. An algorithm has been developed to reorient the camera of the robot so that the detected face is in the middle of the camera. If multiple faces are present in the video frame, then the camera is reoriented such that maximum number of faces are in the camera frame. Face recognition is performed using the face recognition library of python. The comparison will be made using 128 features between the person on the camera frame and the person in the database. Our system will interact with people around using Natural Language Processing. The audio input is done through the microphone and a real time audio processing is performed to get the output sentence.

Block diagram of working of the robot (Face Recognition and Greeting)
 
Working Videos:
1.	Tracking algorithm to tracks the face of the person
https://drive.google.com/file/d/1l6zYVzZll-iYgvyrnrfNwLvh6kwmOmh3/view?usp=sharing
2.	Working video of face recognition
https://drive.google.com/file/d/1IinYFmgeuvjoJxyFn3UbzyuMBFPyYGVj/view?usp=sharing

Fund Details
1.	Cost for all the items (Face Recognition and Greeting)
ITEM	REQUIREMENT	COST (Approx.)
RDS3115 Servo with servo mount brackets x2	Mounted at the top of the body for 2 degrees of freedom of camera	Rs. 5,500
1080p camera x2	One camera will be mounted with servos.
Second camera will be installed on the back of the robot so that it can detect persons behind it	Rs. 8,000
USB Speaker	For greeting the person
with his/her name.	Rs. 1,000
USB Microphone	For capturing person’s name	Rs. 3,000
NVIDIA Jetson Nano	Making a small CPU+GPU for the robot that will contain all the required codes, the database and will perform image processing	Rs. 15,000
Arduino Mega	All logical operations will be performed by this microcontroller.	Rs. 3,000
Power bank (5V,3Amp)	To power up jetson nano	 To be decided
Miscellaneous		10,000
Total	Rs. 45,500/-

2.	Cost for all the items used in Locomotion 
ITEM	REQUIREMENT	COST
Long threaded rod (Diameter-5mm, length-500mm) x6	To connect all the chassis of the robot	Rs. 2,400/-
M5 nuts	To fasten the threaded rods	Rs. 1,000/-
M5 washers	To fasten the threaded rods	Rs. 500/-
A4988 motor drivers x2	For powering motors	Rs. 1,500/-
LIPO battery 	For powering motor driver	To be decided
RLS-08 Line sensor array	To detect black line	Rs. 1,000
Jumper wires	To connect electronic components	Rs. 600/-
Wheels	Used for locomotion	To be decided
Nema 17 Stepper motor x2	For moving the robot as it provides better precision and is less noisy than DC motor	Rs. 2,000
Clamps x2	Used for connecting motors to the chassis of the robot	Rs. 400/-
Miscellaneous 		Rs. 1,100/-
Total	Rs. 10,500/-

Future Scope:
1.	The robot can be further utilized as an AI personal assistant that can assist with daily tasks, provide reminders.
2.	The robot serves as a valuable support system for elderly individuals and those with special abilities, providing assistance and offering companionship.
3.	The robot can serve as a receptionist enhancing Efficiency and Providing Interactive Experiences for Consumers.
4.	The robot can act as a personalized tutor, adapting teaching methods to individual learning styles.
