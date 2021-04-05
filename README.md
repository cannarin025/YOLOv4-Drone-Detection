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
    
    **Options:**

   GPU: 

4. Build darknet 
   
    Run `make_darknet.sh`
   
    If when run the following error is thrown:
    
        ./darknet ./darknet: error while loading shared libraries: libopencv_highgui.so.3.4: cannot open shared object file: No such file or directory

    please run the following commands:
    
        sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
        sudo ldconfig

##Use
###Filestructure

