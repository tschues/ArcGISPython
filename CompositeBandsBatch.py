import os
import arcpy
from arcpy import env
def bianLi(rootDir,wildcard,recursion):
    exts = wildcard.split(" ")
    dirs = os.listdir(rootDir)
    count = len(dirs)
    print count
    FileList=[]
    for dir in dirs:
       
        #get fullname
        fullname=rootDir+'\\'+dir
        #print "rootDir:",rootDir
        
        #if the fullname is dir not a file,then re bianLi
        if (os.path.isdir(fullname) & recursion):
            bianLi(fullname,wildcard,recursion)
            
        # if the fullname is a '.jp2' file,then do process
        else:
            #get file path
            rootDirPath=rootDir.split('\\')

            #get the count of rootDirPath
            nPath_Count = len(rootDirPath)

            #get the last path of rootDirPath
            fileLastPath=rootDirPath[nPath_Count-1]
            
            #print('fileLastPath:----'+fileLastPath)

            #Creat the output file name without path:ComBandsFile
            ComBandsFile = fileLastPath+".tif"
            #print('ComBandsFile:----'+ComBandsFile)

            fullComBansFile = rootDir+"\\"+ComBandsFile
            #print('fullComBansFile=='+fullComBansFile)
            #if the folder's files are not layerstacked
            if not(os.path.isfile(fullComBansFile)):
                #creat env.workspace name
                EWSName = rootDir
                
                env.workspace=EWSName

                #get all the 'jp2' files from one folder
                ExtentionName =os.path.splitext(dir)[1]
                #print('ExtentionName:----'+ExtentionName)
                if(ExtentionName==exts[0]):
                    FileList.append(dir)
                    if len(FileList)==4:
                        print "---------------------------------------------"
                        print('env.workspace:----'+EWSName)
                        FileList.sort() 
                        print(FileList)
                        Band1=FileList[0]
                        Band2=FileList[1]
                        Band3=FileList[2]
                        Band4=FileList[3]

                        InputBands = Band1+";"+Band2+";"+Band3+";"+Band4
                        try:
                            #do CompositeBands use arcpy
                            arcpy.CompositeBands_management(InputBands,ComBandsFile)
                            print " "
                        except:
                            print "Composite Bands example failed."
                            print arcpy.GetMessages()
                        print(ComBandsFile+'-----is ok')
       

#please change the file path:			
rootDir = r"D:\77211356\Sentinel2\Hubei_other\S2A_tile_20170326_49RGP_0"
wildcard = ".jp2"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')    
