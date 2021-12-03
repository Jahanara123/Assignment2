#!/usr/bin/env python3

import subprocess, sys
import os
import argparse



'''
OPS435 Assignment 2 - Fall 2021
Program: duim.py 
Author: "Jahanara shirley"
The python code in this file (duim.py) is original work written by
"Jahanara shirley". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <improved DU command, to get information in files>

Date:2021-12-02
'''

def du_sub(target_directory) -> list:
    # create command list
    command = ["du", "-d", "1", target_directory]
    # call Popen to run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # parse stdout, stderr from process
    stdout, stderr = process.communicate()
    # strip new line and split into list and return to caller
    return [line.strip() for line in stdout.decode("UTF-8").strip().split('\n')]


def percent_to_graph(percent, total_chars) -> str:
    bar_graph = ""
    if isinstance(percent, int) and (0 <= percent <= 100):
        fill = int(total_chars * percent / 100)
        bar_graph = "{:<{width}}".format("=" * fill, width=total_chars)
    else:
        raise ValueError
    # return bar graph as string to caller
    return bar_graph

def ceate_dir_dict(dirs: list) -> dict:
    dir_dict = {}
    for entry in dirs:
        nbytes, directory = entry.split()
        dir_dict[directory] = int(nbytes)
    return dir_dict

def get_total_size(dir_dict: list) -> int:
    # return total number of bytes from directory dictionary
    return sum(dir_dict.values())

def get_unit(n):
    # returns the corresponding unit
    factor = 1000 # change to 1024 if required
    if n < factor:
        return 'B'
    elif factor <= n < factor ** 2:
        return 'KiB'
    elif factor**2 <= n < factor**3:
        return 'MiB'
    elif factor**3 <= n < factor**4:
        return 'GiB'
    else:
        return 'TiB'

def auto_scale_n(n):
    # scales output to be just 3 digits long
    factor = 1000 # change to 1024 if required
    scaled = n
    while scaled > factor:
        scaled /= factor
    return scaled

if __name__ == "__main__":
    _, *args = sys.argv
    if len(args) == 0:
        directory = "."
    elif len(args) > 1 or not os.path.isdir(args[0]):
        print("ERROR: Invalid number of arguments or path is not valid.")
        exit(0)
    else:
        directory = args[0] 
    
    # call our functions to get the requried data
    dir_dict = ceate_dir_dict(du_sub(directory))
    total_size = get_total_size(dir_dict)

    # max with taken by bar graph
    graph_max_size = 20

    # loop for each entry in directory dict and print required info with graph
    for subdir, size in dir_dict.items():
        percentage = int(size / total_size * 100)
        graph = percent_to_graph(percentage, graph_max_size)
        print("{:>2} % [{}] {:0.1f} {:<5}\t{}".format(percentage, graph, auto_scale_n(size),get_unit(size) , subdir))
    # print the total of the parent directory
    print("Total: {:0.1f} {}\t\t\t{}".format(auto_scale_n(total_size), get_unit(total_size), directory))
