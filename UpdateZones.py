# -*- coding: cp936 -*-
# Name: UpdateZones.py
# Purpose: Update the "lots" feature class with features from "cutzones"
# Import system modules

import arcpy,os

count = 0
path = r"E:\test"
fileList = os.listdir(path)
for files in fileList:
   fileDir = os.path.join(path,files)
   
   if ".gdb" in fileDir:
      
      #Step 1:Set the workspace
      arcpy.env.workspace = fileDir

      #Spet 2:Set local parameters
      inFeatures = "lcra"
      updateFeatures = "hyda"
      fileName = fileDir.split('.')
      outFeatures = fileName[0]

      # Sept 3:Process: Update
      arcpy.Update_analysis(inFeatures, updateFeatures, outFeatures)
      count = count + 1

      # Sept 4:Print count
      print "Finish number of works is ："+str(count)
      
   else:
      print "There have no gdb files"
      
print "All the files are finished"
