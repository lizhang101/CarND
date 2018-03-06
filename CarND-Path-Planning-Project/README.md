# CarND-Path-Planning-Project
Self-Driving Car Engineer Nanodegree Program
   
# Overview

## Goal: safely navigate the car on a virtual highway with other traffic that is driving +-10 MPH of the 50 MPH speed limit in the simulator.

* The car should try to go as close as possible to the 50 MPH speed limit.
* Bypass slower traffic if possible.
* Avoid collisions with other cars at all cost. 
* Driving in the marked lanes at all times, unless when changing lanes.
* Finish one whole loop.
* The car should not experience total acceleration over 10 m/s^2 and jerk that is greater than 10 m/s^3.

### Input: 

* Car's localization and sensor fusion data. 
* A sparse map list of waypoints around the highway.

For detailed description of the input data, please visit [Udacity's Project](https://github.com/udacity/CarND-Path-Planning-Project)

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./path_planning`.

# Prerequisites

The project has the following dependencies (from Udacity's seed project):

- cmake >= 3.5
- make >= 4.1
- gcc/g++ >= 5.4
- libuv 1.12.0
- Udacity's simulator.

# Rubic

* Car passed 10 miles without incidents.  
![10 miles](images/10_miles.png)
* Car is able to behavior correctly under those cases:
![to left](images/change_to_left.png)
![to right](images/change_to_right.png)
![to center](images/go_back_to_center.png)

* No speed limit red message was seen.
* Max acceleration and jerk are not exceeded.
* No collisions.
* The car stays in its lane most of the time, and changes lane when necessary. 

## Reflection

I put all my code in main function, between the comments "Student Code Start" and "Student Code End". It would be better to create separate classes in different files.

### Prediction [line 257 to line 297](./src/main.cpp#L257)

Predict other cars speeds and positions with the given telemetry and sensor fusion data. In this project, I only detect following situations from the environment:
- There is at least one car in front of us.
- There is at least one car to the right of us.
- There is at lesst one car to the left of us.

These are detected by calculating the lane each other car is and the position it will be at at the end of the last plan trajectory. If the car is within 30m in front or behind us, it's taken as "dangerous".

### Behavior [line 300 to line 329](./src/main.cpp#L300)
Based on the situations detected in prediction stage, this part of code will make decision of:
- If a car blocks us ahead: try to change left lane, if can't, try to change to right lane, if still not, slow down.
- Change back to center lane whenever feasible.
- Speed up to 49.5 MPH if safe.
`speed_change` is used to accumulate the speed changing decisions.

### Trajectory [line 364 to line 435](./src/main.cpp#L364)
This code generates the trajectory based on the speed and lane output from the behavior, car coordinates and past path points.

First, a spline is initialized based on the last 2 points of the previous trajectory, or the car position if there are no previous trajectory(line 338 to line 362), and 3 points at a far distance (line 368 to line 391). These coordinates are transformed into local car coordinates to make the spline calculation easier.  
Then, the pass trajectory points are copied into the new trajectory to make the path more continuity(line 397 to 400).  
Finally, the rest of points are calculated by evaluating the spline to the target position, and transform those output points back to global coordinates (line 403 to line 433). The speed used to calculate these points is also adjusted according to the behavior stage output.
