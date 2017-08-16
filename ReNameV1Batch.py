import time,os

def bianLi(path,recursion):
    filelist = os.listdir(path)
    count=0
    for files in filelist:
        
        Olddir=os.path.join(path,files)
        
        #if the fullname is dir not a file,then re bianLi
        if (os.path.isdir(Olddir) & recursion):
            bianLi(Olddir,recursion)
            
        # if the fullname is a '.shp' file,then do process
        else:
            if ".v1" in Olddir:
                Newdir=Olddir.replace('.v1','')
                print "Newdir:"+Newdir
                #filename=os.path.splitext(files)[0]
                #filetype = os.path.splitext(files)[1]
                os.rename(Olddir,Newdir)
                count +=1
                print "ok:"+str(count)
            if ".tiff" in Olddir:
                Newdir=Olddir.replace('.tiff','')
                print "Newdir:"+Newdir
                #filename=os.path.splitext(files)[0]
                #filetype = os.path.splitext(files)[1]
                os.rename(Olddir,Newdir)
                count +=1
                print "ok:"+str(count)
#please change the file path:			
path = r"\\crop27\share\croppattern\zy3_sentinel2_compare"
bianLi(path, 1)
print('all the files are finished')   

