## Introduction
This project implements Opensource ROS navigation stack porting on Qualcomm RB3. with use of depth camera sensor available on RB3 for navigation, obstacle detection and avoidance

##  Pre-requisites

 1. Install Android SDK tools (ADB, Fastboot)
 2. Install and configure the USB driver
 3. Flash the RB3 firmware image on to the board
 4. Setup serial port for debugging purpose
 5. Wi-Fi connection is setup and internet is accessible 
 6. Download and Install the [App Tool chain
    SDK](https://www.thundercomm.com/app_en/product/1544580412842651) 
    which is present under Technical Documents tab.
  7. Qualcomm RB3 is setup with docker container with ROS Melodic
    installed as described below
  8. Turtlebot burger is assembled, operational and is connected to RB3

## Steps to prepare ROS navigation stack
Download the repo code into your local folder. For ex: workspace

## Steps to create docker container with necessary packages
RB3 comes with docker preinstalled. Follow the instructions below for ROS melodic setup in a docker container. We need to make this setup in a docker container as RB3 Linux OS does not support recent ROS versions:
```
	$ sudo docker build --tag rosdlr -f Dockerfile.rosdlr
```

Now launch the docker container using the command:

``` 
	 $ sudo docker run -it -v $(pwd):/app rosdlr
```
Full repo can be viewed under /app inside the container. Let’s first build talker.cpp
```
	$ cd talker

	$ catkin_make
```
Clone turtlebot3 navigation packages
```
	$ mkdir -p catkin_ws/src

	 $ cd catkin_ws/src

	$ git clone -b melodic-devel [https://github.com/ROBOTIS-GIT/turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3)
```

Add depthimage to laserscan conversion nodelet code to catkin_ws/src/turtlebot3/turtlebot3_navigation/launch/turtlebot3_navigation.launch file.

Please add following contents:
```
<node pkg="nodelet" type="nodelet" name="laserscan_nodelet_manager" args="manager"/>

<node pkg="nodelet" type="nodelet" name="depthimage_to_laserscan"

args="load depthimage_to_laserscan/DepthImageToLaserScanNodelet laserscan_nodelet_manager">

<param name="scan_height" value="1"/>

<param name="output_frame_id" value="base_scan"/>

<param name="range_min" value="0.5"/>

<param name="range_max" value="4.5"/>

<remap from="image" to="/camera/depth/image_raw"/>

<remap from="scan" to="/scan"/>

</node>
```

Also Remove the rviz pkg from catkin_ws/src/turtlebot3/turtlebot3_navigation/launch/turtlebot3_navigation.launch, as rviz window cannot launch in RB3. We’ll need to specify a map. Replace the default map files with the required map files in the turtlebot3_naviagiton/maps folder and build the package.

We are now ready to build ROS navigation stack:
```
	$ cd catkin_ws

	$ catkin_make
```
It’s time to save all our work done inside the docker container. Start another adb terminal into RB3 and type following commands:

  
```
docker container ls

Use the container ID (CID) and run

docker commit CID rosdlr:v2
```
  

Exit the container where we have built the navigation stack. We can now use rosdlr:v2 image which contains all our work.


## Launch ROS navigation stack

  
```
docker run -it --name test -v $(pwd):/app --device=/dev/ttyACM0 --network=host rosdlr:v2
```
Once inside the container:
```
export ROS_MASTER_URI=[http://RB3_IP:1131](http://10.42.0.186:11311/)1

export ROS_HOSTNAME=RB3_IP

source /opt/ros/melodic/setup.bash

source devel/setup_bash

roslaunch turtlebot3_navigation turtlebot3_navigation.launch
```
 
Start/talker that publishes depth images. We’ll start another terminal into the docker container to start talker. First start another adb shell and type following command:
```
docker exec -it test bash
```
Once inside the container:
 ```
export ROS_MASTER_URI=[http://RB3_IP:1131](http://10.42.0.186:11311/)1

export ROS_HOSTNAME=RB3_IP

source /opt/ros/melodic/setup.bash

source devel/setup.bash

cd devel/lib/talker

./talker
```

## Prepare a linux 18.04 PC/laptop for Rviz with ROS melodic

  

Install and build all the ROS navigation packages. We’ll use Rviz tool from here to set the maps and goals to our robot:
```
source /opt/ros/melodic/setup_bash

cd catkin_ws

git clone -b melodic-devel [https://github.com/ROBOTIS-GIT/turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3)
```

In order to launch the rviz in the host, open catkin_ws/src/turtlebot3/turtlebot3_navigation/launch/turtlebot3_navigation.launch

and remove all the code except the rviz package launch code. We’ll need to specify a map. Replace the default map files with the required map files in the turtlebot3_naviagiton/maps folder and build the package. Refer the sample turtlebot3_navigation.launch in the project repo
 
Now build the package
```
export ROS_MASTER_URI=[http://RB3_IP:1131](http://10.42.0.186:11311/)1

export ROS_HOSTNAME=HOST_IP

cd catkin_ws

source devel/setup_bash

roslaunch turtlebot3_navigation turtlebot3_navigation.launch
```

## Steps to port RB3 components

Porting ROS Navigation stack involves following steps:

1.  Communication strategy between RB3 host and Docker container
    
2.  Publish depth camera streams to the ROS navigation stack
    
3.  We need to capture depth camera streams from Qualcomm RB3 Depth camera
    
4.  Publish camerainfo (calibration information) to the ROS navigation stack
    
## Communication strategy between RB3 host and Docker container

Please note that Melodic ROS navigation stack cannot be used on RB3 directly as RB3 Linux distribution is incompatible with recent ROS versions. RB3 comes preinstalled with ROS Indigo. The ROS navigation stack for this project runs inside a docker container (ubuntu 18.04). Camera application which is needed for this project runs directly on the RB3 host. To enable communications between these 2 applications, so that depth camera streams can be posted to the ROS navigation stack running inside the docker container, we build a simple client-server mechanism. Client is integrated into the camera application and posts raw depth camera streams to the server running inside the docker container.

  

## Publishing depth camera streams to the ROS navigation stack

  

We need to publish depth camera streams to the ROS navigation stack. This information enables the navigation stack to detect and avoid obstacles as it finds its way to the goal. Please have a look at ./talker/src/talker.cpp in the repo. This application runs inside the docker container. The server which communicates with the camera application running on RB3 host is integrated in this application. Steps to build and run this application are explained above as part of the talker package.

  

## Publish CameraInfo (calibration information) to the ROS navigation stack

  

We could not find calibration information for V4T-EVM. We have used the calibration information based on its fov i.e. 70 degrees or 1.22 radians. The CameraInfo message gets published along with a depth image. Please see ./talker/src/talker.cpp and here is the listing of the same:

  ```
camera_info_msg_.K[0] = 457.84999843514953;
camera_info_msg_.K[1] = 0.0;
camera_info_msg_.K[2] = 320.5;
camera_info_msg_.K[3] = 0.0;
camera_info_msg_.K[4] = 457.84999843514953;
camera_info_msg_.K[5] = 240.5;
camera_info_msg_.K[6] = 0.0;
camera_info_msg_.K[7] = 0.0;
camera_info_msg_.K[8] = 1.0;
camera_info_msg_.R[0] = 1.0;
camera_info_msg_.R[1] = 0.0;
camera_info_msg_.R[2] = 0.0;
camera_info_msg_.R[3] = 0.0;
camera_info_msg_.R[4] = 1.0;
camera_info_msg_.R[5] = 0.0;
camera_info_msg_.R[6] = 0.0;
camera_info_msg_.R[7] = 0.0;
camera_info_msg_.R[8] = 1.0;
camera_info_msg_.P[0] = 457.84999843514953;
camera_info_msg_.P[1] = 0.0;
camera_info_msg_.P[2] = 320.5;
camera_info_msg_.P[3] = -0.0;
camera_info_msg_.P[4] = 0.0;
camera_info_msg_.P[5] = 457.84999843514953;
camera_info_msg_.P[6] = 240.5;
camera_info_msg_.P[7] = 0.0;
camera_info_msg_.P[8] = 0.0;
camera_info_msg_.P[9] = 0.0;
camera_info_msg_.P[10] = 1.0;
camera_info_msg_.P[11] = 0.0;
```
  

## Capturing Depth Camera Streams

  

RB3 includes sample applications related to camera preview capture, snapshot capture as well as depth camera preview capture. The depth camera preview capture module needs some changes so that it can be used for posting raw depth images to the ROS navigation stack.

[https://www.thundercomm.com/app_en/product/1544580412842651](https://www.thundercomm.com/app_en/product/1544580412842651)

Visit the URL above, browse to “Technical documents” tab. camera_test.rar implements the RB3 sample application to demonstrate camera capabilities. You can find SDK setup and build instructions related documentation in the user guide (Qualcomm Robotics RB3 Platform Linux User Guide). We have used this code and added some changes on top.

  

Let’s see the changes in camera_test application in this project repo now:

  

In the file (from this repo) camera_test\src\QCameraHAL3TestTOF.cpp, function – CapturePostProcess we comment the existing processing - that stores preview images to file. We also bring in changes needed to post raw depth data to the server running inside the docker container.

  

Take a look at the client integration in the “main” function in file camera_test\src\QCameraHAL3Testmain.cpp – function create_client()

  

#### Another key information to note here is depth image attributes. RB3 depth image is:

 - 480 pixels high (rows) and 640 pixels wide (columns)
 -  Depth information is encoded in milli-meters
 -  Each depth pixel is encoded as unsigned 16 bits integer
 -  Depth camera operates in 2 modes:
   
	-   Mode 0: near distance 0.2mtrs and farthest is 1.2 mtrs
	-   Mode 1: near distance 0.5mtrs and farthest is 4.5 mtrs
	-   We use mode 1
    
   -  We use only 4 rows of data in the centre of the image i.e. rows 238, 239, 240, 241 as laser scan makes use of only 1 row of depth data
    
-   This strategy also prevents potential huge data transfer between client and server (down from 614400-> 5120 bytes)
    
Build the camera application (./camera_test folder from repo) according to instructions given in the user-guide post installing the SDK. Instructions to adb push the built application are also provided in the same section.

Run the application and type following command at the prompt (see screenshot below):
A: id=0, psize=320x240,pformat=raw16,dsize=640x480,dformat=raw16

![](https://lh3.googleusercontent.com/RXT2_vGmiISlRlsko2KgeHjPVKQlhaUzNqbkkA0iHteXi07DgQTWOyCoKs2hjay0wxMoPNlUgcYRWvKvvspW3gX6MyXT0Hu4vS0ot0iuC1QRINsTiGbZpxh0_pe1PLaNxSMROb_l)
This command adds a camera for preview and also starts sending raw depth camera streams to the server running inside docker container. At this stage turtlebot should start moving to the goal specified
