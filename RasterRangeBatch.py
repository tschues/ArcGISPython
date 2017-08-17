# -*- coding: UTF-8 -*-
#批量栅格范围获取，并将栅格文件名写入范围数据的字段中
#author: lizy qq:77211356,email:lizy@radi.ac.cn
import os,time
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
    FileList=[]
    #遍历dirs下所有目录与文件
    for dir in dirs:
        
        #获取完整路径名
        fullname=rootDir+'\\'+dir
        #print "rootDir:",rootDir
        
        #判断完整路径是否是文件夹，如果是文件夹，继续迭代查询子文件夹及文件
        if (os.path.isdir(fullname) & recursion):
            bianLi(fullname,wildcard,recursion)
            
        # 如果是文件名而非文件夹目录
        else:
            #如果文件名中包含名为wildcard的扩展名，则继续:
            if(dir.endswith(wildcard)):

                #输入栅格文件名
                InputImage = dir
                 #拆分目录
                FileNames=os.path.splitext(InputImage)
                #文件基础名，无扩展名
                ImageBaseName = FileNames[0]
                
                #创建输出栅格范围矢量文件名，此处不包含路径
                outPoly = ImageBaseName+"_domain.shp"
                #创建完成文件名，包含路径
                fullOutPutPoly = rootDir+"\\"+outPoly
                #print('fullOutPutImageAfterClip=='+fullOutPutImageAfterClip)

               #creat env.workspace
                EWSName = rootDir
                env.workspace=EWSName

	#判断输出文件是否存在，不存在则处理
                if not(os.path.isfile(fullOutPutPoly)):
                    print('fullOutPutPoly:----'+fullOutPutPoly)
                   
                    # Set Local Variables
                    outGeom = "POLYGON" # output geometry type
					
                    try:
                        print "---------------------------------------------"
                        print " "
                        #调用提取栅格范围的arcpy
                        arcpy.RasterDomain_3d(InputImage, fullOutPutPoly, outGeom)
                        print(outPoly+'-----is ok')
                        #添加字段，将影像文件名写入字段
                        addNameToDomain(outPoly,ImageBaseName)
                        FileList.append(fullOutPutPoly)
                    except:
                        print "RasterDomain_3d example failed."
                        print arcpy.GetMessages()
                elif (os.path.isfile(fullOutPutPoly)):
                    #添加字段，将影像文件名写入字段
                    addNameToDomain(outPoly,ImageBaseName)
                    #FileList.append(fullOutPutPoly)



#********************************************添加 字段，将影像的谁的名加入字段中**************************************************                        
def addNameToDomain(feature_class,ImageBaseName):
        #Add a Field to identify the Class Result  
        fieldName1 = "ImageName"  
        #fieldPrecision = 4  
        fieldAlias = "is the result"  
          
        #List All the Field of Features  
        fieldObjList = arcpy.ListFields(feature_class)  
        # Create an empty list that will be populated with field names  
        fieldNameList = []  
        # For each field in the object list, add the field name to the  
        #  name list.  If the field is required, exclude it, to prevent errors  
        for field in fieldObjList:  
            if not field.required:  
                fieldNameList.append(field.name)  
        print fieldNameList
        # delete the same name field in the feature
        if fieldName1 in fieldNameList:  
            #arcpy.DeleteField_management(feature_class, fieldName1)
            return
            #print"Delete the "+fieldName1+" Fields"  
          
        #Function AddField_management
        arcpy.AddField_management(feature_class, fieldName1, "TEXT", "", "",100,  
                                      fieldAlias, "NULLABLE")  
        #update query  
        cursor = arcpy.UpdateCursor(feature_class)  
        for row in cursor:  
            # field1 will be equal to 0  
            row.setValue(fieldName1, ImageBaseName)  
            cursor.updateRow(row)  
        print feature_class+'-----add field Finished---:' + str(time.ctime())

#please change the file path:			
rootDir = r"D:\77211356\CropClass\Sentinel2\Hubei\Hubei_TIFF_Output"
wildcard = ".tif"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')   
