Group members:
Jacob Sickafoose (jsickafo@ucsc.edu)
Wren Sakai (wsakai@ucsc.edu)
Duseok Choi (duchoi@ucsc.edu)


To run: Run 'python Main.py'


Three windows open when ran. Note that because of the large timeframe we use it will take a few moments for the windows to apear.

The first window, MAV State, displays six different MAV state values that we found
useful in our debugging. Before we had the target moving, it was usefully to see the
course angle and NED positions steadily oscillating.

The second window, "Course Test Overhead View", shows the mapped out path of the
target vehicle, as well as the path for the MAV while it tries to circle around the
moving target. Note that the target vehicle changes direction aproximately halfway in the simulation and UAV is able to track it.

The final window, Course Test 3D, maps out the path's of both vehicles in 3D, so the
graph can be moved around. A red line also displays a brief depiction of the camera's viewpath from the UAV to the target vehical. This window was supremely useful in our testing and it
might be even more useful than the simulator GUI.

So far in our project, we have completed our circle mode and started breaking ground
on using the camera to detect our target. At first, we were very stuck on a bug with the UAV's following and circeling behavoir. However after much debuging and tuning of PID gains, we were able to complete a very well-running module for following a moving target, which changes direction. The follow behavoir works very well in a variety of situations.

At the present moment we are working to complete the full camera module. The follow and search modes of our project have been completed and all that is left is to flesh out proper camera behavoir. Right now, the camera is always locked onto the target at any given time. However we wish to implement more realistic behavoir where the camera is first in "Search" mode before spotting and then locking onto the target. This is behavoir we hope to finish before our presentation. Additionally, we hope to find a good way of visualising the camera in our simulations. The graphing functions in python work extremely well for visualising the UAV flight path in 2d and 3d, but we have yet to find a good way to visualise the camera. For now we will likely just plot a "dot" on the ground to represent where the camera is pointing, but we hope to have some sort of line or cone. 

Lastly, as a stretch goal, we hope to make some changes to the vehical dynamics model to represent a more realistic camera, which effects the physical attributes of the plane. However this is going to be something we only do if the camera module works perfectly. 