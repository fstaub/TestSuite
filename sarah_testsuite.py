import subprocess
import datetime
import time
import os
import shutil
import pyslha

import config
import checks
import run



#-------------------------------------  
# Main program 
#-------------------------------------

print "---------------------------------"
print "Starting the new SARAH Test-Suite"
print "---------------------------------"

cwd = os.getcwd()
DebugDir="nix"
name="nix"
timestamp= datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
log= open("Logs/log_"+timestamp+".txt","w+")


log.write("   _____         _____            _    _   _______        _    _____       _ _        \n")
log.write("  / ____|  /\   |  __ \     /\   | |  | | |__   __|      | |  / ____|     (_) |       \n")
log.write(" | (___   /  \  | |__) |   /  \  | |__| |    | | ___  ___| |_| (___  _   _ _| |_ ___  \n")
log.write("  \___ \ / /\ \ |  _  /   / /\ \ |  __  |    | |/ _ \/ __| __|\___ \| | | | | __/ _ \ \n")
log.write("  ____) / ____ \| | \ \  / ____ \| |  | |    | |  __/\__ \ |_ ____) | |_| | | ||  __/ \n")
log.write(" |_____/_/    \_\_|  \_\/_/    \_\_|  |_|    |_|\___||___/\__|_____/ \__,_|_|\__\___| \n\n\n")
                                                                                     
log.write("Version: 0.001, run start: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d, %H:%M:%S'))+"\n\n\n\n")


log.write("##################################################################\n")
log.write("Individual Checks\n")
log.write("##################################################################\n\n")
   
if (config.check_GM_RGEs==True):
   checks.run_check_GM_RGEs(cwd,log,"Debug/")
   
if (config.check_THDMCPV_RGEs==True):
   checks.run_check_THDMCPV_RGEs(cwd,log,"Debug/")   
   
if (config.check_MSSM_2L==True):
   checks.run_check_MSSM_2L(cwd,log,"Debug/")    

log.write("\n\n\n")

log.write("##################################################################\n")
log.write("Run all Models\n")
log.write("##################################################################\n\n")


if (config.check_calchep_all==True) or (config.check_spheno_all==True) or (config.check_ufo_all==True) or (config.check_latex_all==True):
   run.run_check_all_models(cwd,log)


log.close
print "finished"