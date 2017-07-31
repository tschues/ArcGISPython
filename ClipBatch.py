import os
import arcpy
from arcpy import env
def bianLi(rootDir,wildcard,recursion):
    exts = wildcard.split(" ")
    dirs = os.listdir(rootDir)
    count = len(dirs)
    #print count
    for dir in dirs:
        
        #get fullname
        fullname=rootDir+'/'+dir
        #print "rootDir:",rootDir
        
        #if the fullname is dir not a file,then re bianLi
        if (os.path.isdir(fullname) & recursion):
            bianLi(fullname,wildcard,recursion)
            
        # if the fullname is a '.tif' file,then do process
        else:
            
            #get file path
            rootDirPath=rootDir.split('/')

            #get the count of rootDirPath
            nPath_Count = len(rootDirPath)

            #get the last path of rootDirPath
            fileLastPath=rootDirPath[nPath_Count-1]
            #print('fileLastPath:----'+fileLastPath)
            
            InputImage = fileLastPath+".tif"
            
            
            #Creat the output file name without path:OutPutImageAfterClip
            OutPutImageAfterClip = fileLastPath+"_clip.tif"
            #print('OutPutImageAfterClip:----'+OutPutImageAfterClip)

            fullOutPutImageAfterClip = rootDir+"/"+OutPutImageAfterClip
            #print('fullOutPutImageAfterClip=='+fullOutPutImageAfterClip)
            ExtentionName =os.path.splitext(dir)[1]
            #print('ExtentionName:----'+ExtentionName)
            if(ExtentionName==exts[0]):
            #if (InputImage == dir):
                #if the folder's files are not layerstacked
                if not(os.path.isfile(fullOutPutImageAfterClip)):
                    print " "
                    print "---------------------------------------------"
        
                    print ('InputImage:----'+InputImage)
                    #print('dir:'+dir)
                    #creat env.workspace name
                    EWSName = rootDir
                    print('env.workspace:----'+EWSName)
                    env.workspace=EWSName
                    
                    try:
                        #do Clip_management use arcpy
                        arcpy.Clip_management(InputImage, "#", OutPutImageAfterClip,"D:/share/croppattern/Data_20170712/RasterRangeNoZY3.shp", "0", "ClippingGeometry")
                        print " "
                    except:
                        print "Clip example failed."
                        print arcpy.GetMessages()
                    print(OutPutImageAfterClip+'-----is ok')
       

#please change the file path:			
rootDir = "D:/share/croppattern/sentinel2"
wildcard = ".tif "
bianLi(rootDir,wildcard, 1)
print('all the files are finished')   
