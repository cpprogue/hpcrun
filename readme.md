# hpcrun

A script for quickly running code on the High-Performance Compute cluster at
CalPoly Pomona. Developed based off of the HPC documentation provided in
CS 3700 - Parallel Processing

## Install

To install, simply run:

```
git clone https://github.com/cpprogues/hpcrun # Clone our repo
pip3 install hpcrun # Install the package on the system
```

## Example

```
$ hpcrun ./example [USERNAME]

Password:
Authenticating...
Zipping data...
Uploading to ZFS...
Uploading to HPC...
Running on HPC... (this may take a while)
Remote: Archive:  /home/[...]/example.zip
Remote:    creating: example/
Remote:   inflating: example/hello_c.sh      
Remote:   inflating: example/hello.c         
Remote: Submitted batch job 1433
Remote:   adding: example/hello (deflated 69%)
Remote:   adding: example/hello.c (deflated 26%)
Remote:   adding: example/hello_c.sh (deflated 39%)
Remote:   adding: example/HELLO_C.txt (deflated 25%)
Remote:
Uploading results back...
```
