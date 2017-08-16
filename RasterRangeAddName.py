# -*- coding: UTF-8 -*-
#批量栅格范围获取，并将栅格文件名写入范围数据的字段中
#author: lizy qq:77211356,email:lizy@radi.ac.cn
import os
import arcpy
from arcpy import env

#遍历目录函数
#rootDir：目录
#wildcard：文件扩展名，用于过滤文件名
#recursion：迭代次数，默认为1
def bianLi(rootDir,wildcard,recursion):
    # Obtain a license for the ArcGIS 3D Analyst extension，获取3D分析的许可
    arcpy.CheckOutExtension("3D")
    	#查询rootDir下所有目录与文件，赋值给dirs
    dirs = os.listdir(rootDir)

    #遍历dirs下所有目录与文件
    for dir in dirs:
        
        #获取完整路径名
        fullname=rootDir+'/'+dir
        #print "rootDir:",rootDir
        
        #判断完整路径是否是文件夹，如果是文件夹，继续迭代查询子文件夹及文件
        if (os.path.isdir(fullname) & recursion):
            bianLi(fullname,wildcard,recursion)
            
        # 如果是文件名而非文件夹目录
        else:
            #如果文件名中包含名为wildcard的扩展名，则继续:
            if(dir.endswith(wildcard)):
                #拆分目录
                rootDirPath=rootDir.split('/')

                #获取拆分后数组 rootDirPath的个数count
                nPath_Count = len(rootDirPath)

                #截取最末级目录
                fileLastPath=rootDirPath[nPath_Count-1]
                #print('fileLastPath:----'+fileLastPath)

                #输入栅格文件名
                InputImage = dir
                
                #创建输出栅格范围矢量文件名，此处不包含路径
                outPoly = fileLastPath+"_domain.shp"
                #创建完成文件名，包含路径
                fullOutPutPoly = rootDir+"/"+outPoly
                #print('fullOutPutImageAfterClip=='+fullOutPutImageAfterClip)

                print "---------------------------------------------"
                print " "

				#判断输出文件是否存在，不存在则处理
				if not(os.path.isfile(fullOutPutPoly)):
					#print ('InputImage:----'+InputImage)
					#print('dir:'+dir)
					print('outPoly:----'+outPoly)
					#creat env.workspace name
					EWSName = rootDir
					#print('env.workspace:----'+EWSName)
					env.workspace=EWSName
					# Set Local Variables
					outGeom = "POLYGON" # output geometry type
					
					try:
						#调用提取栅格范围的arcpy
						arcpy.RasterDomain_3d(InputImage, fullOutPutPoly, outGeom)

						print " "
					except:
						print "RasterDomain_3d example failed."
						print arcpy.GetMessages()
					print(outPoly+'-----is ok')
	   

#please change the file path:			
rootDir = "D:/share/croppattern/sentinel2/hunan"
wildcard = ".tif"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')   
