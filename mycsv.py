#!/usr/bin/python

import os

def read_csv(filename,delimeter:str):
	table = []
	if os.path.exist(filename):

		
		with open(filename) as file:
			for line in file:
				table.append(line.split(delimeter))
	else:
		print("Error, such file doesn't exist")

# P.S. I suppose throw of exception instead printing is better approach
	
	return table 




def write_csv(filename,data,delimeter:str):

# What is incorrect call for write_csv?

	with open(filename,'w') as file:
		for row in data:
			file.write(delimeter.join(row))



