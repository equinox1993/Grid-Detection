#!/bin/bash

mkdir build
cd build
cmake .. && make && echo "About to install the binarization library to your system. Sudo password will be required." && sudo make install
