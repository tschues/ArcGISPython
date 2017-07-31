import os
import arcpy
from arcpy import env
def bianLi(rootDir,wildcard,recursion):
    # Obtain a license for the ArcGIS 3D Analyst extension
    arcpy.CheckOutExtension("3D")
    
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
            
            InputImage = fileLastPath+"_clip.tif"
            
            
            #Creat the output file name without path:OutPutImageAfterClip
            outPoly = fileLastPath+"_clip_domain.shp"
            
            fullOutPutPoly = rootDir+"/"+outPoly
            #print('fullOutPutImageAfterClip=='+fullOutPutImageAfterClip)
            #print('dir:----'+dir)
            extentionName = os.path.splitext(dir)[1]
            extentionName= "_clip"+extentionName
            #print('extentionName:----'+extentionName)
            filterName = exts[0]
            #print('filterName:----'+filterName)
            if (extentionName==filterName):
                print "---------------------------------------------"
                print " "
            #if (InputImage == dir):
                #if the folder's files are not layerstacked
                if not(os.path.isfile(fullOutPutPoly)):
                    print ('InputImage:----'+InputImage)
                    #print('dir:'+dir)
                    print('outPoly:----'+outPoly)
                    #creat env.workspace name
                    EWSName = rootDir
                    print('env.workspace:----'+EWSName)
                    env.workspace=EWSName
                    # Set Local Variables
                    outGeom = "POLYGON" # output geometry type
                    
                    try:
                        #do Clip_management use arcpy
                        arcpy.RasterDomain_3d(InputImage, outPoly, outGeom)

                        print " "
                    except:
                        print "RasterDomain_3d example failed."
                        print arcpy.GetMessages()
                    print(outPoly+'-----is ok')
       

#please change the file path:			
rootDir = "D:/share/croppattern/sentinel2/hunan"
wildcard = "_clip.tif "
bianLi(rootDir,wildcard, 1)
print('all the files are finished')   
