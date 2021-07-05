# drone_detection

**Note: this repo should be run on a UNIX system.** If a GPU is used it must be NVIDIA and you should have CUDA, CUDNN and OPENCV set up.

##Prerequisites
**Prerequisites for use with GPU:**
1. CUDA
2. CUDNN
3. OPENCV

##Setup
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

##Use

**Set run configuration of main.py to inside the darknet directory**

1. Define area for drone in main.py using area class.
    Specify rectangular geofence for drone. Drone will not leave this defined space.
2. Run drone detections by calling the area.run() method.

    Specify step size between photographs, length of flight path and flight altitude.

###Filestructure

   main.py: Code to be edited by the user to run drone detections.
   
   

    
