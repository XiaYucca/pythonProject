import os

os.system('gcc -dynamiclib -o mega1280Protect.dylib mega1280Protect.c Burnerinterfaces.c')
os.system('echo')
os.system('echo')

os.system('echo start test_Megaburner.py')

os.system('echo')
os.system('echo')

os.system('python test_MegaBuner.py')
