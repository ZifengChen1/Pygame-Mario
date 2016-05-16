import os
from glob import glob

directory = input("Enter directory: ")

files = [f for f in os.listdir(directory)]
print(files)

DRYRUN=False
BASE = input("Enter BASE: ")
num = 0

for filename in files:
    num += 1
    newname = BASE+str(num)+".png"
    if os.path.exists(newname):
        print("Cannot rename %s to %s, already exists" % (filename,newname))
        continue
    if DRYRUN:
        print("Would rename %s to %s" % (filename,newname))
    else:
        print("Renaming %s to %s" % (filename,newname))
        os.rename(filename,newname)
