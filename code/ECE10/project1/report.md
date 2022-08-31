Individual Lab Report

1. Group Members: Jacob Sickafoose (jsickafo) -Master repo

2.	I've worked with Python in ECE163 - Introduction to Small-Scale UAV Theory and Practice,
	but that was about a year ago and it was also my first time seeing Python. I have much more
	experience with C, but I need to grow my experience with Python.

3.	I spent roughly 7 hours working on this lab. It took me 30 minutes to come up with the 
	state machine and pseudocode. It then took me 6 hours to figure out how to code the robot.
	I couldn't find any of the libraries with the commands and how to use them for the robot.
	I just know we had to import the Robot, Motors, and Distance Sensor libraries but I didn't
	find the documentation on them.

	I ended up just watching YouTube videos to figure out which commands to use. It took me a long
	time to find out that I want to set the Motor.setPosition(float('inf')) and never touch it again.
	I initially was using that to give me an exact 180 degree turn but it was messing everything up,
	so I ended up just turning right and stoping after sleep(2.82) which depended on the motor speed.

	The distance sensors were also giving me grief because of how noisy they are. The signal is
	indistinguishable from the noise until <0.03m. At least without applying some filtering but I wanted
	to finish this lab quickly.

4. 	I had many problems working with other members in my group.