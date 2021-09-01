#!/usr/bin/env python3


import os

# os.system("echo lsblk -o +UUID,SERIAL > log_drive.txt")

file_name_in = 'log_drive.txt'
file = open(file_name_in, mode='r', )
drive_number = 0
line = True
while line:
    line = file.readline()
    if line[:2] == 'sd':
        line = line.split()
        #print(line)
        if len(line) >= 8:
            drive_number += 1
            result_line = 'UUID=' + str(line[7]) + '  /export/brick' + str(drive_number).zfill(2) + '  xfs defaults 0 0    #' + '  ' + line[0] + '  ' + line[3]
            print(result_line)
else:
    print('EOF')
file.close()