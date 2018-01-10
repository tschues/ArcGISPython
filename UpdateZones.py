# Name: UpdateZones.py
# Purpose: Update the "lots" feature class with features from "cutzones"

# Import system modules
import arcpy
import os


for num in range(420000,430001):
 
   #Determine if the file exists
   strDir = "F:\DLGGC-4\DLG"+str(num)+".gdb"

   if os.path.exists(strDir):

      # Set the workspace
      arcpy.env.workspace = strDir

      # Set local parameters
      inFeatures = "V_LCRA"
      updateFeatures = "V_HYDA"
      outFeatures = "Update0"

      # Process: Update
      arcpy.Update_analysis(inFeatures, updateFeatures, outFeatures)
      print(str(num)+":Status:OK!")

   else:
        
       print 'The '+str(num)+' file is not exists!'
