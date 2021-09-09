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
        list_drives = list_drives.stdout.decode('utf-8').split("\n")
        print(*list_drives, sep='\n')
        for line in list_drives:
            line = line.split()
            if line and line[4] == '0' and int(line[5]) > 14000509157370:
                self.disk_list.append(line[6])
                self.drives_count += 1
        print(*self.disk_list, sep='\n')

    def make_format(self):
        count = 0
        for path in self.disk_list:
            subprocess.run(["sudo", "-S", "mkfs.xfs", path], stderr=subprocess.DEVNULL)
            path_to_make = '/export/brick' + str(count).zfill(2) + '/tank01'
            count += 1
            if not os.access(path_to_make, os.F_OK):
                print("Making directory", path_to_make)
                os.mkdir(path_to_make)
                os.chmod(path_to_make, 0o0777)
            else:
                print("Directory", path_to_make, "already exist")
            UUID = subprocess.run(["lsblk", path, "-o", "+UUID,SERIAL"], stdout=subprocess.PIPE)
            UUID = UUID.stdout.decode('utf-8').split()
            result_line = 'UUID=' + str(UUID[16]) + '  /export/brick' + str(count).zfill(
                2) + '  xfs defaults 0 0    #' + '  ' + str(UUID[9])
            print(path, UUID[16])
            print(result_line)





gluster = Layout()

gluster.get_drive_list()
gluster.make_format()

