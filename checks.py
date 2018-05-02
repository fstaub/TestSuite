import subprocess
import os
import shutil
import pyslha

import run
import config

def run_check_GM_RGEs(cwd,log,DebugDir):
    print "Checking the one-loop RGEs for the generalised GM"
    log.write("Checking the one-loop RGEs for the generalised GM\n")
    log.write("------------------------------------------------------------------\n")    
    out= open(cwd+"/"+DebugDir+"GM_RGEs_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"GM_RGEs_err.txt","wb")    
    shutil.copyfile("Files/RGE_checks/GM_RGEs.m",os.path.join(config.sarah_dir,"GM_RGEs.m"))
    os.chdir(config.sarah_dir)
    subprocess.call("math -run < GM_RGEs.m",shell=True,stdout=out,stderr=err)
    os.remove("GM_RGEs.m")
    with open("GM_RGEs_debug.txt") as f:
      contents = f.read()
      errors = contents.count("error")
    log.write("Errors in GM RGEs:                            "+str(errors)+"\n\n")  
    os.chdir(cwd) 
    out.close()
    err.close() 
    log.flush()
    
def run_check_SM_RGEs(cwd,log,DebugDir):
    print "Checking the two-loop RGEs for the SM"
    log.write("Checking the two-loop RGEs for the SM\n")
    log.write("------------------------------------------------------------------\n")    
    out= open(cwd+"/"+DebugDir+"SM_RGEs_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"SM_RGEs_err.txt","wb")    
    shutil.copyfile("Files/RGE_checks/SM_RGEs.m",os.path.join(config.sarah_dir,"SM_RGEs.m"))
    os.chdir(config.sarah_dir)
    subprocess.call("math -run < SM_RGEs.m",shell=True,stdout=out,stderr=err)
    os.remove("SM_RGEs.m")
    with open("SM_RGEs_debug.txt") as f:
      contents = f.read()
      errors = contents.count("error")
    log.write("Errors in SM RGEs:                            "+str(errors)+"\n\n")  
    os.chdir(cwd) 
    out.close()
    err.close()    
    log.flush()
    
def run_check_THDM_Unitarity(cwd,log,DebugDir):
    print "Checking the unitarity constraints in the large s limit for the THDM"
    log.write("Checking the unitarity constraints in the large s limit for the THDM\n")
    log.write("------------------------------------------------------------------\n")    
    out= open(cwd+"/"+DebugDir+"THDM_uni_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"THDM_uni_err.txt","wb")    
    shutil.copyfile("Files/Unitarity/THDM_comparison.m",os.path.join(config.sarah_dir,"THDM_comparison.m"))
    os.chdir(config.sarah_dir)
    subprocess.call("math -run < THDM_comparison.m",shell=True,stdout=out,stderr=err)
    os.remove("THDM_comparison.m")
    with open("THDM_Unitarity_debug.txt") as f:
      errors = f.read().splitlines()
    log.write("Errors in THDM unitarity constraints:         "+str(errors[0])+"\n\n")  
    os.chdir(cwd) 
    out.close()
    err.close()       
    log.flush()


def run_check_THDMCPV_RGEs(cwd,log,DebugDir):
    print "Checking the one-loop RGEs for the complex THDM"
    log.write("Checking the one-loop RGEs for the complex THDM\n")
    log.write("------------------------------------------------------------------\n")
    out= open(cwd+"/"+DebugDir+"THDM_RGEs_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"THDM_RGEs_err.txt","wb")    
    
    shutil.copyfile("Files/RGE_checks/Complex_RGEs_THDM.m",os.path.join(config.sarah_dir,"Complex_RGEs_THDM.m"))
    os.chdir(config.sarah_dir)
    subprocess.call("math -run < Complex_RGEs_THDM.m",shell=True,stdout=out,stderr=err)
    os.remove("Complex_RGEs_THDM.m")
    with open("THDM_RGEs_debug.txt") as f:
      contents = f.read()
      errors = contents.count("error")
    log.write("Errors in complex THDM RGEs:                  "+str(errors)+"\n\n")        
    os.chdir(cwd)
    out.close()
    err.close()
    log.flush()
    
def run_check_MSSM_2L(cwd,log,DebugDir):
    print "Checking two-loop Higgs masses in the MSSM"
    log.write("Checking two-loop Higgs masses in the MSSM\n")
    log.write("------------------------------------------------------------------\n")
    # Run SARAH 
    os.chdir(config.sarah_dir)    
    f= open("input_MSSM.m","w+")
    f.write("<<\"SARAH.m\";\n")
    f.write("Start[\"MSSM\"];\n")
    f.write("MakeSPheno[IncludeLoopDecays->False,IncludeFlavorKit->False];\n")
    f.write("Exit[];\n")
    f.close()
    out= open(cwd+"/"+DebugDir+"MSSM2L_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"MSSM2L_err.txt","wb")
    subprocess.call("math -run < input_MSSM.m",shell=True,stdout=out,stderr=err)
    os.remove("input_MSSM.m")
    os.chdir(cwd)
    
    # Compile SPheno
    subprocess.call("rm -r "+config.spheno_dir+"/MSSM/",shell=True,stdout=out,stderr=err)  
    subprocess.call("cp -r "+config.sarah_dir+"/Output/MSSM/EWSB/SPheno/ "+config.spheno_dir+"/MSSM/",shell=True,stdout=out,stderr=err)
    os.chdir(config.spheno_dir)
    subprocess.call("make Model=MSSM",shell=True,stdout=out,stderr=err)

    
    # Run SPheno
    os.chdir(config.spheno_dir)
    if os.path.exists("SPheno.spc.MSSM"):
       os.remove("SPheno.spc.MSSM") 
    shutil.copyfile(cwd+"/Files/MSSM_2L/LesHouches.in.MSSM_83","LesHouches.in.MSSM")   
    subprocess.call("./bin/SPhenoMSSM",shell=True,stdout=out,stderr=err)
    spc1 = pyslha.read("SPheno.spc.MSSM")
    
    shutil.copyfile(cwd+"/Files/MSSM_2L/LesHouches.in.MSSM_89","LesHouches.in.MSSM")   
    os.remove("SPheno.spc.MSSM")     
    subprocess.call("./bin/SPhenoMSSM",shell=True,stdout=out,stderr=err)    
    spc2 = pyslha.read("SPheno.spc.MSSM")    

    log.write('Difference in h_1:                           %10.4e\n' % (spc1.blocks['MASS'][25]-spc2.blocks['MASS'][25]))
    log.write('Difference in h_2:                           %10.4e\n' % (spc1.blocks['MASS'][35]-spc2.blocks['MASS'][35]))      
    log.write('\n')  
    os.chdir(cwd)
    out.close()
    err.close()  
    log.flush()    
    