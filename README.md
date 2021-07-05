# drone_detection

## About 
This is a repository enabling a Parrot Bebop 2 drone to detect and track custom objects using a trained YOLOv4 object detection model. This repository was created in collaboration with [Jcm4318](https://github.com/jcm4318) as part of our Bachelor's project where we proposed a new solution to Australia's invasive Cane Toad problem.

**Note: this repo should be run on a UNIX system.** If a GPU is used it must be NVIDIA and you should have CUDA, CUDNN and OPENCV set up. It is highly recommended that a GPU is used.

## Prerequisites
1. Trained YOLOv4 Model. See [Darknet](https://github.com/AlexeyAB/darknet) to learn how to do this.
2. Parrot Bebop 2 drone.

**Prerequisites for use with GPU:**
1. CUDA
2. CUDNN
3. OPENCV

## Setup
1. Install dependencies

    Run `pip install -r requirements.txt`
   

2. Fetch the contents of the darknet submodule:
    
   Run the following:
   
        > git submodule init 
        > git submodule update
   
3. Edit `make_darknet.sh` to configure as desired.
    
    **Makefile Options:**

   GPU: Enable the use of GPU
   
   OPENCV: Enable the use of OpenCV
   
   CUDNN: Enable the use of CUDNN
   
   CUDNN_HALF: Enables support for tensor cores

4. Build darknet 
   
    Run `make_darknet.sh`
   
    If when run the following error is thrown:
    
        ./darknet ./darknet: error while loading shared libraries: libopencv_highgui.so.3.4: cannot open shared object file: No such file or directory

    please run the following commands:
    
        sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
        sudo ldconfig

## Use

**Set run configuration of main.py to be inside the darknet directory**

1. Put trained YOLOv4 model files into corresponding Vis/IR folder inside the models directory.
2. Define area for drone in main.py using area class.
    Specify rectangular geofence for drone. Drone will not leave this defined space.
3. Run drone detections by calling the area.run() methodd. Specify step size between photographs, length of flight path and flight altitude.

### Filestructure

   main.py: Code to be edited by the user to run drone detections.
   
   detect.py: Code containing detecor class.
   
   DroneCode_Vis.py: Code containing area class and drone control.
   
   multimodal_detection.py: Code enabling IR and Visible detections to be combined.
   
   make_darknet.sh: Bash script to configure and make darkent.
   
   darknet: Directory containing darknet files and executable.
   
   models: Directory where trained model .weights, .data, .names and .cfg files should be placed
   
   data: Directory where frames containing classes will be saved, and where test images / videos should be placed.
   
   

    
