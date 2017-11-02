# -*- coding: UTF-8 -*-
#批量波段组合程序，将任意多个jp2文件组合并输出到单独文件夹中
#如果只有2.3.4.8四个波段，则文件名和原来保持不变，为文件夹的名字
#如果有多个波段，比如2,3,4,5,8,12，则输出文件会命名为"文件夹名_B02B03B04B05B08B12.tif"
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
        InputBands=""
        bandname=""
        
        #read the folder
        for dir in dirs:
            BandCount=0
            jp2Files = os.listdir(rootDir)
            for jp2 in jp2Files:
                if(dir.endswith(wildcard)):
                    BandCount +=1
            #print('BandCount:----'+str(BandCount))
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
                    shotname= os.path.splitext(dir)[0];
                    bandname += shotname
                    #Creat the output file name without path:ComBandsFile
                    ComBandsFile = fileLastPath+".tif"
                    if not(BandCount == 4):
                        #Creat the output file name without path:ComBandsFile
                        ComBandsFile = fileLastPath+"_"+bandname+".tif"
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
                        FileList.append(dir)
                        InputBands +=dir+";"
                        
                        if len(FileList)==BandCount:
                                InputBands=InputBands[0:-1]
                                print('InputBands:----'+InputBands)
                                
                                print('env.workspace:----'+EWSName)
                                print 'Start:' + str(time.ctime())
                                try:
                                    #do CompositeBands use arcpy
                                    arcpy.CompositeBands_management(InputBands,fullComBansFile)
                                    print " "
                                except:
                                    print "Composite Bands example failed."
                                    print arcpy.GetMessages()
                                print(fullComBansFile+'-----is ok')
                                print 'End:' +str(time.ctime())
                                print "---------------------------------------------"
                    else:
                         print fullComBansFile+":::--is exitsted"
                         print "---------------------------------------------"
                         break

#请修改以下路径【文件夹名称】:			
rootDir = r"D:\77211356\Sentinel2\Hubei_other"
#扩展名为jp2
wildcard = ".jp2"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')    
