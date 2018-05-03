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
    log.write("Errors in SM RGEs:                            "+str(errors)+"\n\n\n")  
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
    log.write("Errors in THDM unitarity constraints:         "+str(errors[0])+"\n\n\n")  
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
    log.write("Errors in complex THDM RGEs:                  "+str(errors)+"\n\n\n")        
    os.chdir(cwd)
    out.close()
    err.close()
    log.flush()
    
def generate_spheno(cwd,log,DebugDir,model,short,flags):
    # Run SARAH 
    os.chdir(config.sarah_dir)    
    f= open("input_"+short+".m","w+")
    f.write("<<\"SARAH.m\";\n")
    f.write("Start[\""+model+"\"];\n")
    f.write("MakeSPheno["+flags+"];\n")
    f.write("Exit[];\n")
    f.close()
    out= open(cwd+"/"+DebugDir+"SPheno"+short+"_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"SPheno"+short+"_err.txt","wb")
#    subprocess.call("math -run < input_"+short+".m",shell=True,stdout=out,stderr=err)
    os.remove("input_"+short+".m")
    
    # Compile SPheno
    subprocess.call("rm -r "+config.spheno_dir+"/"+short+"/",shell=True,stdout=out,stderr=err)  
    subprocess.call("cp -r "+config.sarah_dir+"/Output/"+model+"/EWSB/SPheno/ "+config.spheno_dir+"/"+short+"/",shell=True,stdout=out,stderr=err)
    os.chdir(config.spheno_dir)
    subprocess.call("make Model="+short+"",shell=True,stdout=out,stderr=err)
    out.close()
    err.close()
    os.chdir(cwd)

def get_spheno_spc(cwd,log,DebugDir,short):
    os.chdir(config.spheno_dir)
    out= open(cwd+"/"+DebugDir+"SPheno"+short+"_out.txt","wb")
    err= open(cwd+"/"+DebugDir+"SPheno"+short+"_err.txt","wb")
    if os.path.exists("SPheno.spc."+short):
       os.remove("SPheno.spc."+short) 
    subprocess.call("./bin/SPheno"+short,shell=True,stdout=out,stderr=err)
    subprocess.call("sed -i 's/DECAY1L/decay/g' SPheno.spc."+short,shell=True,stdout=out,stderr=err)
    subprocess.call("sed -i 's/DECAY/DECAYTREE/g' SPheno.spc."+short,shell=True,stdout=out,stderr=err)    
    subprocess.call("sed -i 's/decay/DECAY/g' SPheno.spc."+short,shell=True,stdout=out,stderr=err)    
    out.close()
    err.close()  
    
    return pyslha.read("SPheno.spc."+short)   
    
def run_check_MSSM_2L(cwd,log,DebugDir):
    print "Checking two-loop Higgs masses in the MSSM"
    log.write("Checking two-loop Higgs masses in the MSSM\n")
    log.write("------------------------------------------------------------------\n")
    
#    generate_spheno(cwd,log,DebugDir,"MSSM","MSSM","IncludeLoopDecays->False,IncludeFlavorKit->False")

    os.chdir(config.spheno_dir)
    shutil.copyfile(cwd+"/Files/MSSM_2L/LesHouches.in.MSSM_83","LesHouches.in.MSSM")   
    spc1=get_spheno_spc(cwd,log,DebugDir,"MSSM")
    
    shutil.copyfile(cwd+"/Files/MSSM_2L/LesHouches.in.MSSM_89","LesHouches.in.MSSM")   
    spc2=get_spheno_spc(cwd,log,DebugDir,"MSSM")

    log.write('Difference in h_1:                           %10.4e\n' % (spc1.blocks['MASS'][25]-spc2.blocks['MASS'][25]))
    log.write('Difference in h_2:                           %10.4e\n' % (spc1.blocks['MASS'][35]-spc2.blocks['MASS'][35]))      
    log.write('\n\n')  
    os.chdir(cwd)
    log.flush()    
    
    
def run_check_LoopDecays_IR(cwd,log,DebugDir):   
    os.chdir(config.spheno_dir)
    print "Checking IR divergences in loop decays"
    log.write("Checking IR divergences in loop decays\n")
    log.write("------------------------------------------------------------------\n")    
#    generate_spheno(cwd,log,DebugDir,"MSSM","MSSM","IncludeFlavorKit->False")
    shutil.copyfile(cwd+"/Files/LoopDecays_IR/LesHouches.in.MSSM_10","LesHouches.in.MSSM")       
    spc1=get_spheno_spc(cwd,log,DebugDir,"MSSM")
   
    shutil.copyfile(cwd+"/Files/LoopDecays_IR/LesHouches.in.MSSM_15","LesHouches.in.MSSM")       
    spc2=get_spheno_spc(cwd,log,DebugDir,"MSSM")
    
   
    for f in spc1.decays.keys():
        maxdiff=0.        
        for g in range(0,len(spc1.decays[f].decays)):
            br1= spc1.decays[f].decays[g].br
            br2= spc2.decays[f].decays[g].br
            diff = abs(br1-br2)/br1
            if diff>maxdiff:
                maxdiff=diff
        log.write('Maximal difference in 1-loop BR of %i:                           %10.4e\n' % (f,maxdiff))        
    os.chdir(cwd)     
    log.flush()    