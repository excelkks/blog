---
title: cmake编译与测试opencv4
date: 2019-11-28 15:43:42
categores: opencv
tags: 
- opencv
- cmake
---
保证已经安装：
1. GCC 4.4.x or later
2. CMake 2.8.7 or higher
3. Git
4. GTK+2.x or higher, incuding headers(libgtk2.0-dev)
5. pkg-config
6. Python 2.6 or later and Numpy 1.5 or later with developer package (python-dev, python-numpy)
7. ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev
8. [optional] libtbb2 libtbb-dev
9. [optional] libdc1394 2.x
10. [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev
11. [optional] CUDA Toolkit 6.5 or higher
可通过以下命令安装
```bash
# [compiler]
sudo apt-get install build-essential
# required
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
# [optional]
 sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

```
### 1 编译opencv
#### 1.1 下载opencv4源码
打开[opencv sources](https://opencv.org/releases/)，下载源码Sources
#### 1.2 CMake编译opencv4库
进入opencv源码目录，创建build文件夹
```bash
cd opencv
mkdir build
cd build
```
配置CMAKE参数，例如

1. `CMAKE_BUILD_TYPE=Release`  设置编译版本
2. `CMAKE_INSTALL_PREFIX=/usr/local` 设置opencv库的安装目录
   
```bash
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ..
```
此时，opencv库将被安装在/usr/local目录中

### 2 测试opencv4
新建测试文件DisplayImage.cpp
```c++
#include <stdio.h>
#include "opencv2/opencv.hpp"

using namespace cv;

int main(int argc, char **argv)
{
    if(argc != 2){
        printf("usage: DisplayImage.out <Image_Path>\n")
        return -1;
    }

    Mat image;
    image = imread(argv[1], 1);

    if(!image.data){
        printf("No image data\n")
        return -1;
    }

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", image);

    waitKey(0);
    return 0;
}
```
新建CMakeLists.txt文件
```cmake
cmake_minimum_required(VERSION 2.8)

project(DisplayImage)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

find_package(OpenCV HINTS "/usr/local/opencv") # “/usr/local/opencv” is the path of compiled opencv
include_directories(${OpenCV_INCLUDE_DIRS})
aux_source_directory(. DIR_SRCS)
add_executable(DisplayImage ${DIR_SRCS})
target_link_libraries(DisplayImage ${OpenCV_LIBS})
```

接下来cmake，可能需要安装提示将cuda指定版本
```bash 
cmake -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-9=8.0 .
```
最后直接make即可编译二进制可执行文件。

