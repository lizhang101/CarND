# PID-Control
Udacity Self-Driving Car Nanodegree - PID Control project

# Overview

This project implements a [PID controller](https://en.wikipedia.org/wiki/PID_controller) to control a car in Udacity's simulator. The simulator sends cross-track error, speed and angle to the PID controller(PID) and it receives the steering angle ([-1, 1] normalized) and the throttle to drive the car. 

# Prerequisites

The project has the following dependencies:

- cmake >= 3.5
- make >= 4.1
- gcc/g++ >= 5.4
- Udacity's simulator.


# Compiling and executing the project
1. Run build.sh. It will create a build directory and generate execution binary named "pid". 
2. Run "pid" along with the simulator, choose PID project in the simulator. 

# Effect of the control parameters P, I, D
1. P (Propotional gain): It computes the propotianal output to the cross-track error. It tries to steer the car to the center of the road. If it's used along, the car oscillate from the central of the road. An example video for this effct is [./videos/only_propotional.mov](./videos/only_propotional.mov)
2. I (Integral gain): It computes the sum of cross-track error over time. It can mitigate the bias and reduce the propotional gain in high speed. Using it along will cause the car running off the road quickly. Here is an example video: [./videos/only_integral.mov](./videos/only_integral.mov)
3. D (Differential gain): It's propotinal to the derivative of cross-track error. It helps to mitigate the overshooting caused by only using P. Using it along will make the car can't follow the center of the road and run off road. Here is an example video[./videos/differential_only.mov](./videos/differential_only.mov)

# Tune the parameters
I tuned the parameters manually. A better way should be using a script sweeping the parameter space, and running the simulation without the GUI.
I first set all the parameters to be 0 and increase P slowly till the car to be able to follow the track but start to oscilliate. Then Increasing the D untill oscillation subside. Parameter I should use a small value like 0.001. Here I used 0 in the final parameters. In the tuning, if the car can't track the center of the road quickly, or reactive too slow, we then should increase P, I. If it's overshooting too much, we can reduce the P,I and increase the D.


# Screen shots

Here are some screen shots from the simulator running with the PID controller. 



![screenshot 1](snapshot/1.png)



![screenshot 2](snapshot/2.png)



