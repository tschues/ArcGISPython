import os
import arcpy
from arcpy import env
def bianLi(rootDir):
    
    dirs = os.listdir(rootDir)
    for dir in dirs:
        if (os.path.isdir(dir)):
            print dir
            ComBandsFile = dir+".tif"
            print('ComBandsFile:----'+ComBandsFile)
            #is ok file in dir
            if not(os.path.isfile(ComBandsFile)):
                #creat env.workspace name
                EWSName = rootDir+'/'+dir
                print('EWSName:----'+EWSName)
                env.workspace=EWSName            
                FileList=[]
                #get all files and dirs from every dir
                for root,dirs,files in os.walk(dir):
                    for file in files:
                        if ('.jp2' in file):
                            print('file===='+file)
                            #fullfilename = rootDir+'/'+dir+'/'+file
                            #print(fullfilename)
                            FileList.append(file)
                    print(FileList)
                    #arcpy.CompositeBands_management(FileList[0];FileList[1];FileList[2];FileList[3],
                                                    #ComBandsFile)
                    print(ComBandsFile+'-----is ok')
rootDir = "D:/77211356/CropClass/Sentinel2"
bianLi(rootDir)
