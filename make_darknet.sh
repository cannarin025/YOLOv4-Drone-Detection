#!/bin/bash

cd ./darknet/
sed -i 's/GPU=0/GPU=0/' Makefile  # sets makefile to use GPU
sed -i 's/OPENCV=0/OPENCV=1/' Makefile  # sets makefile to use OPENCV
sed -i 's/CUDNN=0/CUDNN=0/' Makefile  # sets makefile to use CUDNN
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=0/' Makefile  # sets makefile to use CUDNN_half
sed -i 's/LIBSO=0/LIBSO=1/' Makefile  # creates python importables for darknet

# build darknet
make