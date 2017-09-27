#-*- coding: UTF-8 -*- #批量处理汇总另一个数据集区域内的栅格数据值并将结果报告到表 #author: lizy
#qq:77211356

##************please close the features which will be processed in ArcMap************
##************执行该程序之前请关闭ArcMap中已打开的待处理数据，否则会占用，无法运行************

#导入time,os,arcpy三个类库
import time,os,arcpy
from arcpy import env
from arcpy.sa import *
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
                
                #文件扩展名过滤，只处理指定扩展名文件，并且文件夹下没有生成对应的DBF文件
                if dir.endswith(extension):
                    
                    #开始提示，打印开始时间
                    print 'Start:' + str(time.ctime())
                    #arcpy工作空间
                    arcpy.env.workspace = rootDir
                    # Set local variables
                    #区域矢量文件
                    inZoneData = r"D:\77211356\JHPY_RapeSeed\GroundPoint\point_forest_RFP.shp"
                    #标识字段
                    zoneField = "FID"
                    #待统计栅格
                    inValueRaster = dir
                    #获取矢量文件名中的关键词，用来区分不同作物类型
                    ZoneDataBasename = os.path.basename(inZoneData)
                    #用下划线拆分文件名，并取第二个值
                    tempNameFromZoneData = ZoneDataBasename.split('_')[1]
                    #组装输出栅格文件完整路径名
                    outDBF = "ZonalSt_" + tempNameFromZoneData + "_"+ dir.split('.')[0] + ".dbf"
                    #输出DBF完整路径
                    fullOutDBFName=rootDir+'\\'+outDBF
                    # 如果目录下不存在，则执行
                    if not(os.path.isfile(fullOutDBFName)):
    
                        # Check out the ArcGIS Spatial Analyst extension license
                        arcpy.CheckOutExtension("Spatial")

                        # Execute ZonalStatisticsAsTable
                        outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster,outDBF, "NODATA", "MEAN")
                      #打印提示
                        print "Output DBF--"+outDBF+": is finished"
                        

                    #否则，跳过，并提示该数据已统计过，不必重复处理
                    
                    else:
                        #打印提示：栅格已经存在，无需重复处理
                        print "Output DBF--"+outDBF+": Dataset already exists"
                        

#**************************************此处为程序起始，输入参数，调用bianLi函数*****************************************************
#输入文件目录
rootDir = r"D:\77211356\JHPY_RapeSeed\VI"
#文件扩展名过滤
extension = ".tif"
#迭代次数
recursion=1
#调用函数
bianLi(rootDir,extension, recursion)
#打印提示全部完成
print('all the files are finished') 
