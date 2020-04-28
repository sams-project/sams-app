import os

pull = os.system("git pull origin master")
if pull == 0:
    print("done!")