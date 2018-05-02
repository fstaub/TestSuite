import subprocess
import datetime
import time
import os
import shutil
import pyslha

import config
import checks


#-------------------------------------  
# Mathematica Run 
#-------------------------------------

def RunSARAH(model,short,cwd,log):
  os.chdir(config.sarah_dir)    
  f= open("input_"+short+".m","w+")
  f.write("<<\"SARAH.m\";\n")
  f.write("Off[Superpotential::MaybeChargeViolation];\n")
  f.write("Off[Superpotential::ViolationGlobal];\n")
  f.write("Off[TeXOutput::NoRGEs];\n")
  f.write("Off[TeXOutput::NoLoops];\n")
  f.write("Off[Lagrange::ViolationGlobal];\n")
  f.write("Off[Superpotential::ChargeViolation];\n")
  f.write("Off[CalcHep::UnknownColorFlow];")
  f.write("Start[\""+model+"\"];\n")
  #f.write("Print[\"::\"];\n") # Necessary to add one 'error'; otherwise subprocess.check_output doesn't work
  #f.write("MakeSPheno[];\n")
  f.write("MakeSPheno[];\n")
  f.write("MakeCHep[];\n")
  f.write("MakeUFO[];\n")          
  f.write("MakeTeX[];\n")    
  f.write("Exit[];\n")
  f.close()
  
  out= open(cwd+"/"+DebugDir+"math_out.txt","wb")
  err= open(cwd+"/"+DebugDir+"math_err.txt","wb")
  subprocess.call("math -run < input_"+short+".m",shell=True,stdout=out,stderr=err)
  out.close()
  err.close()  
  os.remove("input_"+short+".m")
  os.chdir(cwd)

def CheckSARAH(model,short,cwd,log):
  with open(DebugDir+"math_out.txt") as f:
    contents = f.read()
    errors = contents.count("::")
  log.write("Errors in Mathematica Run:                    "+str(errors)+"\n\n")    
  #if errors>0:  
    #log.write("Mathematica faultless:                no\n")
  #else:
    #log.write("Mathematica faultless:                yes\n")   

#-------------------------------------  
# SPheno Run 
#-------------------------------------
  
def CompileSPheno(model,short,cwd,log):
  out= open(DebugDir+"stdout.txt","wb")
  err= open(DebugDir+"stderr.txt","wb")
  subprocess.call("rm -r "+config.spheno_dir+"/"+short+"/",shell=True,stdout=out,stderr=err)  
  subprocess.call("cp -r "+config.sarah_dir+"/Output/"+short+"/EWSB/SPheno/ "+config.spheno_dir+"/"+short+"/",shell=True,stdout=out,stderr=err)
  out.close()
  err.close()

  sphenoout= open(DebugDir+"spheno_compile_out.txt","wb")
  sphenoerr= open(DebugDir+"spheno_compile_err.txt","wb")
  os.chdir(config.spheno_dir)
  subprocess.call("make Model="+short,shell=True,stdout=sphenoout,stderr=sphenoerr)
  sphenoout.close()
  sphenoerr.close()
  os.chdir(cwd)
  
def CheckSPheno(model,short,cwd,log):
   with open(DebugDir+"spheno_compile_err.txt") as f:
    contents = f.read()
    errors = contents.count("error")
   log.write("Errors in SPheno compilation:                "+str(errors)+"\n\n")      
   #if errors>0:   
    #log.write("SPheno compilation faultless:         no\n") 
   #else:
    #log.write("SPheno compilation faultless:         yes\n")        
   
def RunSPheno(model,short,cwd,log):
   files= os.listdir(config.spheno_dir+short+"/Input_Files/")
   global name 
   name= files[0].replace("_low","").replace("LesHouches.in.","")
   sphenoout= open(DebugDir+"spheno_run_out.txt","wb")
   sphenoerr= open(DebugDir+"spheno_run_err.txt","wb")
   os.chdir(config.spheno_dir)
   os.remove("SPheno.spc."+name) 
   subprocess.call("./bin/SPheno"+name+" "+short+"/Input_Files/LesHouches.in."+name,shell=True,stdout=sphenoout,stderr=sphenoerr)
   sphenoout.close()
   sphenoerr.close()   
   os.chdir(cwd)   

def CheckSPhenoRun(model,short,cwd,log):
   if os.path.exists(config.spheno_dir+"SPheno.spc."+name):
    log.write("SPheno spectrum file:                         yes\n")    
   else:  
    log.write("SPheno spectrum file:                         no\n")    

#-------------------------------------  
# CalcHep Run 
#-------------------------------------


def SetupCalcHep(model,short,cwd,log):
  out= open("Debug/stdout.txt","wb")
  err= open("Debug/stderr.txt","wb")
  subprocess.call("rm -r "+config.calchep_dir+"/"+short+"/",shell=True,stdout=out,stderr=err)  
  os.chdir(config.calchep_dir)
  subprocess.call("./mkWORKdir "+short,shell=True,stdout=out,stderr=err)
  subprocess.call("cp "+config.sarah_dir+"/Output/"+short+"/EWSB/CHep/* "+short+"/models/",shell=True,stdout=out,stderr=err)
  os.chdir(cwd)   
  out.close()
  err.close()    
  
def CheckCalcHep(model,short,cwd,log):
  calchep_out= open(DebugDir+"calchep_out.txt","wb")
  calchep_err= open(DebugDir+"calchep_err.txt","wb")
  os.chdir(config.calchep_dir+"/"+short)
  subprocess.call("./calchep -blind \"{[[{[[[[[[{}}}\"",shell=True,stdout=calchep_out,stderr=calchep_err)
  calchep_out.close()
  calchep_err.close()
  os.chdir(cwd)
  with open(DebugDir+"calchep_out.txt") as f:
    contents = f.read()
    errors = contents.count("ERROR")
  log.write("Errors in CalcHep model:                      "+str(errors)+"\n\n")          
  #if errors>0:   
    #log.write("CalcHep model accepted:               no\n") 
  #else:
    #log.write("CalcHep model accepted:               yes\n")   
  
#-------------------------------------  
# MadGraph Run 
#-------------------------------------
  
  
def SetupMG(model,short,cwd,log):
  out= open("Debug/stdout.txt","wb")
  err= open("Debug/stderr.txt","wb")
  subprocess.call("rm -r "+config.mg_dir+"/models/"+short+"/",shell=True,stdout=out,stderr=err)  
  subprocess.call("cp -r "+config.sarah_dir+"/Output/"+short+"/EWSB/UFO/ "+config.mg_dir+"/models/"+short,shell=True,stdout=out,stderr=err)
  out.close()
  err.close() 
  
def RunMG(model,short,cwd,log):
  mg_out= open(DebugDir+"mg_out.txt","wb")
  mg_err= open(DebugDir+"mg_err.txt","wb")
  os.chdir(config.mg_dir)
  mg_in= open("test_process.dat","w+")
  mg_in.write("import model "+short+" -modelname\n")
  mg_in.write("generate e1 e1bar > e1 e1bar\n")
  mg_in.write("output dir_check_sarah\n")
  mg_in.write("exit\n")
  subprocess.call("./bin/mg5_aMC test_process.dat",shell=True,stdout=mg_out,stderr=mg_err)
  mg_out.close()
  mg_err.close()
  os.chdir(cwd) 
  #shutil.copyfile(mg_dir+"MG_Debug", DebugDir+"MG_Debug")

def CheckMG(model,short,cwd,log):
  with open(DebugDir+"mg_err.txt") as f:
    contents = f.read()
    errors = contents.count("Error")
  log.write("Errors while loading UFO file in MG:          "+str(errors)+"\n\n")        
  #if errors>0:  
    #log.write("UFO model accepted by MG:             no\n")
  #else:
    #log.write("UFO model accepted by MG:             yes\n")


#-------------------------------------  
# LaTeX Compilation 
#-------------------------------------

  
def CreateTeX(model,short,cwd,log):
  tex_out= open(DebugDir+"tex_out.txt","wb")
  tex_err= open(DebugDir+"tex_err.txt","wb")
  os.chdir(config.sarah_dir+"/Output/"+short+"/EWSB/TeX/")
  subprocess.call("sed -e \"s#pdflatex#pdflatex -interaction=nonstopmode#\" MakePDF.sh > test.sh",shell=True,stdout=tex_out,stderr=tex_err)
  subprocess.call("chmod 775 test.sh",shell=True,stdout=tex_out,stderr=tex_err)
  subprocess.call("./test.sh",shell=True,stdout=tex_out,stderr=tex_err)
  tex_out.close()
  tex_err.close()
  
def CheckTeX(model,short,cwd,log):
   with open(DebugDir+"tex_out.txt") as f:
    contents = f.read()
    errors = contents.count("Error")
   with open(DebugDir+"tex_err.txt") as f:
    contents = f.read()
    errors += contents.count("Error")   
   log.write("Errors during pdflatex:                      "+str(errors)+"\n\n")            
   #if errors>0:   
    #log.write("pdflatex was sucessfull:              no\n") 
   #else:
    #log.write("pdflatex was sucessfull:              yes\n")      


#-------------------------------------  
# Run everything for each model
#-------------------------------------

def RunModel(model,length,nr,cwd,log):
  print model+" ("+str(nr)+"/"+str(length)+")"
  short = model.replace("/", "-")  
  global DebugDir
  DebugDir="Debug/"+short+"/"
  if os.path.exists(DebugDir):
     shutil.rmtree(DebugDir)
  os.makedirs(DebugDir)
  
  log.write(model+"\n")
  log.write("-------------------\n")
# Mathematica session
  RunSARAH(model,short,cwd,log)
  CheckSARAH(model,short,cwd,log)
# SPheno part
  if config.check_spheno_all==True:
    CompileSPheno(model,short,cwd,log)
    CheckSPheno(model,short,cwd,log)
    RunSPheno(model,short,cwd,log)
    CheckSPhenoRun(model,short,cwd,log)  
# MC part 
  if config.check_calchep_all==True:
    SetupCalcHep(model,short,cwd,log)
    CheckCalcHep(model,short,cwd,log)
  if config.check_ufo_all==True:
    SetupMG(model,short,cwd,log)
    RunMG(model,short,cwd,log)  
    CheckMG(model,short,cwd,log)
# LaTeX 
  if config.check_latex_all == True:
    CreateTeX(model,short,cwd,log)
    CheckTeX(model,short,cwd,log)
# Tar file
  #tar_files(model,short)
  log.write("\n")
  
def run_check_all_models(cwd,log):
   with open('models.txt') as f:
      models = f.read().splitlines()
   print "number of models: "+str(len(models))
   nr=1
   for x in models:
     RunModel(x,len(models),nr,cwd,log)
     nr+=1

