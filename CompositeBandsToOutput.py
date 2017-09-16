# -*- coding: UTF-8 -*-
#批量波段组合程序，将jp2文件组合成四波段的.tif文件，并输出到单独文件夹中
#author: lizy qq:77211356,email:lizy@radi.ac.cn

import time,os
import arcpy
from arcpy import env
def bianLi(rootDir,wildcard,recursion):
    #rootDir = unicode(rootDir, 'utf8').encode('gbk')
    #the folder is empty or not
    if os.listdir(rootDir):
        dirs = os.listdir(rootDir)
        FileList=[]
        #read the folder
        for dir in dirs:
           
            #get fullname
            fullname=rootDir+'\\'+dir
            #print "rootDir:",rootDir
            
            #if the fullname is dir not a file,then re bianLi
            if (os.path.isdir(fullname) & recursion):
                bianLi(fullname,wildcard,recursion)
                
            # if the fullname is a '.jp2' file,then do process
            else:
                #filter the extention file
                if(dir.endswith(wildcard)):
                    # get the father folder of rootDir
                    tempath=os.path.dirname(rootDir)
                    #print('tempath:----'+tempath)
                    tempOut = tempath.split('\\')
                    #creat the output folder name
                    OutputFolder = tempath+"\\"+tempOut[len(tempOut)-1]+"_TIFF_Output"
                    #print('OutputFolder:----'+OutputFolder)
                    
                    #if there is not a output folder,then creat a Tiff output folder
                    if not(os.path.exists(OutputFolder)):
                        os.makedirs(OutputFolder)
                        print OutputFolder +"  is created"
                    
                    #get file path
                    rootDirPath=rootDir.split('\\')
                    #print('rootDir:----'+rootDir)
                    #get the count of rootDirPath
                    nPath_Count = len(rootDirPath)

                    #get the last path of rootDirPath
                    fileLastPath=rootDirPath[nPath_Count-1]
                    
                    #print('fileLastPath:----'+fileLastPath)

                    #Creat the output file name without path:ComBandsFile
                    ComBandsFile = fileLastPath+".tif"
                    #print('ComBandsFile:----'+ComBandsFile)
                    InputFolderFile = rootDir+"\\"+ComBandsFile
                    
                    fullComBansFile = OutputFolder+"\\"+ComBandsFile
                    #print('fullComBansFile=='+fullComBansFile)
                    #if the folder's files are not layerstacked:the output folder and the input folder are not TIF file
                    if not(os.path.isfile(fullComBansFile)) and not(os.path.isfile(InputFolderFile)):
                        
                        #creat env.workspace name
                        EWSName = rootDir
                        
                        env.workspace=EWSName

                        #get all the 'jp2' files from one folder
                        #ExtentionName =os.path.splitext(dir)[1]
                        #print('ExtentionName:----'+ExtentionName)
                        #if(ExtentionName==exts[0]):
                        FileList.append(dir)
                        if len(FileList)==4:
                                print "---------------------------------------------"
                                print('env.workspace:----'+EWSName)
                                print 'Start:' + str(time.ctime())
                                FileList.sort() 
                                print(FileList)
                                Band1=FileList[0]
                                Band2=FileList[1]
                                Band3=FileList[2]
                                Band4=FileList[3]

                                InputBands = Band1+";"+Band2+";"+Band3+";"+Band4
                                try:
                                    #do CompositeBands use arcpy
                                    arcpy.CompositeBands_management(InputBands,fullComBansFile)
                                    print " "
                                except:
                                    print "Composite Bands example failed."
                                    print arcpy.GetMessages()
                                print(fullComBansFile+'-----is ok')
                                print 'End:' +str(time.ctime())
                                
                    else:
                         print fullComBansFile+":::--is exitsted"
                         break

#请修改以下路径【文件夹名称】:			
rootDir = r"D:\77211356\Sentinel2\Hubei"
#扩展名为jp2
wildcard = ".jp2"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')    
