#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 22:36:11 2020

@author: guru048

References:
	
	1. https://doi.org/10.1023/A:1011625728803

"""

import numpy as np
import sys
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

parallel_switch=False

num_cores = multiprocessing.cpu_count()

vdw_radii = {							# From Ref 1
		"H":1.2,
		"B":1.92,
		"C":1.70,
		"N":1.55,
		"O":1.52,
		"F":1.47,
		"SI":2.1,
		"S":1.80,
		"CL":1.75,
		"BR":1.85,
		"I":1.98
		}

def read_file(infile):
	with open(infile) as f:
		a = f.read().splitlines()
	lines=[]
	for i in a[2:]:
		i = i.lstrip(' ')
		i = i.upper()
		i = i.split()
		i[1] = float(i[1])			# Store in non-numpy format
		i[2] = float(i[2])
		i[3] = float(i[3])
		lines.append(i)
	return(lines)

def get_data(line):
	atomic_symbol = line[0]
	atomic_radius = vdw_radii[atomic_symbol]
	return(atomic_radius, [line[1], line[2], line[3]])
	
def execute_parallel_loop(iterables, rand_array):
	hit = False
	for i in range(len(iterables)):
		r, a = get_data(iterables)
		if np.linalg.norm(np.array(a)-np.array(rand_array)) < r:
			hit = True
	return(hit)


def compute_spheres(lines,maxmin_list):
	total_counter, hit_counter, hit_coord = 0, 0, [[],[],[]]
	cuboid_volume = maxmin_list[0] * maxmin_list[1] * maxmin_list[2]	# Compute overall volume of the cube of darts
	counter = 100000					# Increase counter for higher accuracy?!? Or use an analytical solution?!? :)
	pbar = tqdm(total=counter)
	while hit_counter < counter:										
		rand_array = []
		rand_array.append(np.random.uniform(0.0, maxmin_list[0]))
		rand_array.append(np.random.uniform(0.0, maxmin_list[1]))
		rand_array.append(np.random.uniform(0.0, maxmin_list[2]))
		if parallel_switch:
			inputs = tqdm(lines)
			hit = Parallel(n_jobs=num_cores)(delayed(execute_parallel_loop)(iterables, rand_array) for iterables in inputs)
		else:
			hit = False
			for i in range(len(lines)):
				r, a = get_data(lines[i])
				if np.linalg.norm(np.array(a)-np.array(rand_array)) < r:
					hit = True
		if hit == True:
			hit_counter += 1
			pbar.update(1)
			hit_coord[0].append(rand_array[0])
			hit_coord[1].append(rand_array[1])
			hit_coord[2].append(rand_array[2])
		total_counter += 1
#		print(hit_counter, total_counter, hit_counter*cuboid_volume/total_counter)
	pbar.close()
	return(hit_counter*cuboid_volume/total_counter, hit_coord)
	

def maxmin(lines):
	tempvarx, tempvary, tempvarz = [], [], []
	for i in lines:
		tempvarx.append(i[1])
		tempvary.append(i[2])
		tempvarz.append(i[3])
	min_x = min(tempvarx)
	min_y = min(tempvary)
	min_z = min(tempvarz)
	for i in range(len(lines)):
		lines[i][1] = lines[i][1] - min_x + 2.0			# 2 Angstrom buffer
		lines[i][2] = lines[i][2] - min_y + 2.0
		lines[i][3] = lines[i][3] - min_z + 2.0
	max_x = max(tempvarx) - min_x + 4.0					# 2 angstrom buffer on the other side...
	max_y = max(tempvary) - min_y + 4.0
	max_z = max(tempvarz) - min_z + 4.0
		
	return(lines, [max_x, max_y, max_z])				# Preserve the coordinates in non-numpy format for later use...


if __name__ == "__main__":
	lines = read_file(sys.argv[1])
	lines, maxmin_list = maxmin(lines)
	vol, hit_coord=compute_spheres(lines, maxmin_list)
	print("Approximate volume is %4.2f" % vol)
#	print(hit_coord)
	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.scatter3D(hit_coord[0], hit_coord[1], hit_coord[2], c=hit_coord[2]);
