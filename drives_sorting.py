#!/usr/bin/env python3

import os
import subprocess

class Layout:

    def __init__(self):
        self.disk_list = []
        self.drives_count = 0

    def get_drive_list(self):
        list_drives = subprocess.run(["blockdev", "--report"], stdout=subprocess.PIPE)
        # os.system("sudo blockdev --report > log_blks.txt")
        #file_name_in = 'log_blks.txt'
        #file = open(file_name_in, mode='r', )
        line = True
        while line:
            line = file.readline()
            line = line.split()
            #print(line)
            if line and line[4] == '0' and int(line[5]) > 14000509157370:
                #print(line[6])
                self.disk_list.append(line[6])
                self.drives_count += 1
        else:
            print(*self.disk_list, sep='\n')
        file.close()

    def make_format(self):
        for path, count in self.disk_list, self.drives_count:

            os.system('sudo mkfs.xfs /dev/sd$i -f')
            path_to_make = '/export/brick' + str(count).zfill(2) + '/tank01'
            if not os.access(path_to_make, os.F_OK):
                os.mkdir(path_to_make)
                os.chmod(path_to_make, 0o0777)



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


get_drive_list()

