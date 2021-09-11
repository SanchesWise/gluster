#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

class Layout:

    def __init__(self):
        self.disk_list = []
        self.drives_count = 0

    def get_drive_list(self):
        list_drives = subprocess.run(["blockdev", "--report"], stdout=subprocess.PIPE)
        print("Found devices:\n")
        list_drives = list_drives.stdout.decode('utf-8').split("\n")
        print(*list_drives, sep='\n')
        for line in list_drives:
            line = line.split()
            if line and line[4] == '0' and int(line[5]) > 14000509157370:
                self.disk_list.append(line[6])
                self.drives_count += 1
        print("Found devices to use:\n")
        print(*self.disk_list, sep='\n')

    def make_format(self):
        print("Preparing devices:\n")
        count = 0
        for path in self.disk_list:
            print("formatting :", path)
            subprocess.run(["mkfs.xfs", path, "-f"], stderr=subprocess.DEVNULL)
            path_to_make = '/export/brick' + str(count).zfill(2)
            if not os.access(path_to_make, os.F_OK):
                print("Making directory", path_to_make)
                Path(path_to_make).mkdir(0o777, parents=True, exist_ok=True)

            else:
                print("Directory", path_to_make, "already exist")
            subprocess.run(["mount", path, path_to_make])  # stderr=subprocess.DEVNULL)
            os.chmod(path_to_make, 0o777)
            UUID = subprocess.run(["lsblk", path, "-o", "+UUID,SERIAL"], stdout=subprocess.PIPE)
            UUID = UUID.stdout.decode('utf-8').split()
            result_line = 'UUID=' + str(UUID[16]) + '  /export/brick' + str(count).zfill(
                2) + '  xfs defaults 0 0    #' + '  ' + str(UUID[9] + "\n")
            print(path, UUID[16])
            print("Making record to fstab --", result_line)
            file_name = '/etc/fstab'
            with open(file_name, mode='a', encoding='utf8') as file:
                file.write(result_line)
            count += 1

gluster = Layout()

gluster.get_drive_list()
gluster.make_format()

