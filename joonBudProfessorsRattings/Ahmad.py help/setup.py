import os,platform

osSystem = platform.system().lower()
if 'linux' in osSystem:
    os.system('pip3 install -r req.txt')
if 'windows' in osSystem:
    os.system('pip install -r req.txt')    
