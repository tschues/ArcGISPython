import time,os
import arcpy
from arcpy import env

def bianLi(rootDir,wildcard,recursion):
    exts = wildcard.split(" ")
    dirs = os.listdir(rootDir)
    count = 0
    FileList=[]
    mergeshp=""
    fullname=rootDir
    #print count
    for dir in dirs:
    #for dir in (f for f in dirs if f.endswith(wildcard)):
        #get fullname
        fullname=rootDir+'\\'+dir
        #print "fullname:",fullname
        #get file path
        rootDirPath=rootDir.split('\\')

        #get the count of rootDirPath
        nPath_Count = len(rootDirPath)

        #get the last folder of rootDirPath
        LastFolderName=rootDirPath[nPath_Count-1]
        mergeshp=rootDir+'\\'+LastFolderName+"merge.shp"
        
        #if the fullname is dir not a file,then re bianLi
        if (os.path.isdir(fullname) & recursion):
            bianLi(fullname,wildcard,recursion)
            
        # if the fullname is a '.shp' file,then do process
        else:
            if(dir.endswith(wildcard)):
                
                #if there is no merge file in the folder 
                if not(os.path.isfile(mergeshp)):
                    print "---------------------------------------------"
                    count += 1
                    print "count:"+str(count)
                    FileList.append(dir)
                    #print('dir:'+dir)
    print('mergeshp:----'+mergeshp)
    if not(os.path.isdir(fullname)):
        print "mergeFileList:"+str(FileList)
        if not(os.path.isfile(mergeshp)):
            #creat env.workspace name
            env.workspace=rootDir
            arcpy.Merge_management(FileList, mergeshp)
            print "merge is ok:---"+mergeshp
#please change the file path:			
rootDir = r"D:\share\croppattern\results\wheat\hubei"
wildcard = ".shp"
bianLi(rootDir,wildcard, 1)
print('all the files are finished')   
