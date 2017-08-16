# -*- coding: UTF-8 -*-
#批量处理指定文件夹所有文件及子文件夹下的矢量添加ClassType字段，更新字段值为1，并转栅格程序
#author: lizy qq:77211356,email:lizy@radi.ac.cn

####************please close the features which will be processed in ArcMap************
####************执行该程序之前请关闭ArcMap中已打开的待处理数据，否则会占用，无法运行************

#导入time,os,arcpy三个类库
import time,os,arcpy

#函数：遍历指定文件夹下的所有文件夹和所有文件
#参数有三个：
#rootDir：查询路径
#wildcard：扩展名过滤，可以指定文件扩展名
#recursion迭代次数，默认为1
def bianLi(rootDir,extension,recursion):
    #rootDir = unicode(rootDir, 'utf8').encode('gbk')
        
    #用于返回指定的文件夹包含的文件或文件夹的名字的列表
    if os.listdir(rootDir):
        #用于返回指定的文件夹包含的文件或文件夹的名字的列表给dirs
        dirs = os.listdir(rootDir)
        #计数，最后统计处理的文件个数
        count = 0
        #遍历dirs中所有文件夹和文件
        for dir in dirs:
            #组装完整路径
            fullname=rootDir+'\\'+dir            
            #判断fullname是否为文件夹，如果是文件夹，进入迭代继续向子文件夹查询
            if (os.path.isdir(fullname) & recursion):
                bianLi(fullname,extension,recursion)
                
            # 如果fullname是文件，则跳入执行
            else:
                #组装输出栅格文件完整路径名
                outRaster = rootDir+ "\\" + dir.split('.')[0] + ".tif"
                #文件扩展名过滤，只处理指定扩展名文件，并且文件夹下没有生成对应的栅格
                if dir.endswith(extension)  and  not (os.path.isfile(outRaster)):

                        #开始提示，打印开始时间
                        print 'Start:' + str(time.ctime())
                        #arcpy工作空间
                        arcpy.env.workspace = rootDir
                        #要素赋值
                        feature_class=dir
                        #Add a Field to identify the Class Result  
                        fieldName1 = "ClassType"
                        #字段精度
                        fieldPrecision = 4
                        #字段别名
                        fieldAlias = "is the result"  
                          
                        #列出矢量文件的全部字段  
                        fieldObjList = arcpy.ListFields(feature_class)  
                        # Create an empty list that will be populated with field names  
                        fieldNameList = []  
                        # For each field in the object list, add the field name to the  
                        #  name list.  If the field is required, exclude it, to prevent errors  
                        for field in fieldObjList:  
                            if not field.required:  
                                fieldNameList.append(field.name)  
                        print fieldNameList
                        # 如果矢量文件中已有名为“ClassType”的字段，则删除
                        if fieldName1 in fieldNameList:  
                            arcpy.DeleteField_management(feature_class, fieldName1)  
                            print"Delete the "+fieldName1+" Fields"  
                          
                        #添加名为“ClassType”的字段字段
                        arcpy.AddField_management(feature_class, fieldName1, "SHORT", fieldPrecision, "", "",  
                                                      fieldAlias, "NULLABLE")  
                              
                        #update query，要素指针
                        cursor = arcpy.UpdateCursor(feature_class)
                        #遍历要素中的每个要素
                        for row in cursor:  
                            # field1 will be equal to 0 ，如果该字段的值为0，则全部更新为1
                            if((int)(row.getValue(fieldName1)) == 0):
                                #将字段值设置为1
                                row.setValue(fieldName1, 1)  
                            else:  
                                row.setValue(fieldName1, 1)  
                            cursor.updateRow(row)
                        #字段添加并将值更新为1完成提示 
                        print feature_class+'-----add field Finished---:' + str(time.ctime())

                        #--------------------------------------------PolygonToRaster矢量转栅格参数部分-----------------------------------------------------
                        #输入矢量
                        inFeatures = feature_class
                        #转栅格关键字段
                        valField = fieldName1
                        #打印栅格完成路径进行提示
                        print outRaster
                        #
                        assignmentType = "MAXIMUM_AREA"
                        #
                        priorityField = ""
                        #****************************转出栅格分辨率**********此参数很重要**********************
                        cellSize = 10
                        # Execute PolygonToRaster
                        arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, 
                                                                 assignmentType, priorityField, cellSize)
                        #打印提示：该文件已经处理完毕
                        print outRaster+'-----PolygonToRaster Finished---:' + str(time.ctime())
                        #计数，统计处理数量        
                        count += 1
                        print "count=:"+str(count)
                #else:
                        #打印提示：栅格已经存在，无需重复处理
                        #print "Output Raster Dataset--"+outRaster+": Dataset already exists"
                #print str(count), " files processed."

#************函数，如果文件名中有点"."【扩展名中的"."除外】，则需要将点"."替换为下划线"_"*******************************************************************************
def ReNameForDeletePoint(path,extension,recursion):
    filelist = os.listdir(path)
    count=0
    for files in filelist:
        
        Olddir=os.path.join(path,files)
        
        #if the fullname is dir not a file,then re bianLi
        if (os.path.isdir(Olddir) & recursion):
            bianLi(Olddir,extension,recursion)
            
        # if the fullname is a '.shp' file,then do process
        else:
                if ".tiff" in Olddir:
                        Newdir=Olddir.replace('.tiff','_')
                        print "Newdir:"+Newdir
                        #filename=os.path.splitext(files)[0]
                        #filetype = os.path.splitext(files)[1]
                        os.rename(Olddir,Newdir)
                        count +=1
                        print "ok:"+str(count)
                if ".v" in Olddir:
                        Newdir=Olddir.replace('.v','_')
                        print "Newdir:"+Newdir
                        #filename=os.path.splitext(files)[0]
                        #filetype = os.path.splitext(files)[1]
                        os.rename(Olddir,Newdir)
                        count +=1
                        print "ok:"+str(count)


#**************************************此处为程序起始，输入参数，调用bianLi函数*****************************************************
# 输入文件目录
rootDir = r"D:\77211356\CropClass\Sentinel2\Hubei\S2A_tile_20170227_49"
#文件扩展名过滤
extension = ".shp"
#迭代次数
recursion=1

#调用文件名处理函数，去除文件中除扩展名之外的'.'
ReNameForDeletePoint(rootDir,extension,recursion)
#调用函数
bianLi(rootDir,extension, recursion)
#打印提示全部完成
print('all the files are finished') 
