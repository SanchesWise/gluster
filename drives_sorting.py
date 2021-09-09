#!/usr/bin/env python3

import os
import subprocess

class Layout:

    def __init__(self):
        self.disk_list = []
        self.drives_count = 0

    def get_drive_list(self):
        list_drives = subprocess.run(["sudo", "-S", "blockdev", "--report"], stdout=subprocess.PIPE)
        print("Найденые устройстваЖ:\n")
        print(list_drives.stdout)
        list_drives = list_drives.stdout.decode('utf-8').split("\n")
        #print(*list_drives, sep='\n')
        for line in list_drives:
            line = line.split()
            print(line)
            if line and line[4] == '0' and int(line[5]) > 14000509157370:
                self.disk_list.append(line[6])
                self.drives_count += 1
        print(*self.disk_list, sep='\n')

    def make_format(self):
        count = 0
        for path in self.disk_list:
            subprocess.run(["sudo", "-S", "mkfs.xfs", path])
            path_to_make = '/export/brick' + str(count).zfill(2) + '/tank01'
            count += 1
            if not os.access(path_to_make, os.F_OK):
                print("Making directory", path_to_make)
                os.mkdir(path_to_make)
                os.chmod(path_to_make, 0o0777)
            else:
                print("Directory", path_to_make, "already exist")
            UUID = subprocess.run(["lsblk", path, "-o", "+UUID,SERIAL"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            UUID = UUID.stdout.decode('utf-8').split()
            print(path, UUID[16])


    def make_mount_list(self):
        # os.system("lsblk -o +UUID,SERIAL > log_drive.txt")
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



gluster = Layout()

gluster.get_drive_list()
gluster.make_format()

