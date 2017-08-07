##==================================
##Mosaic
##Usage: Mosaic_management inputs;inputs... target {LAST | FIRST | BLEND | MEAN | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH} 
##                         {background_value} {nodata_value} {NONE | OneBitTo8Bit} {mosaicking_tolerance}  
##                         {NONE | STATISTIC_MATCHING | HISTOGRAM_MATCHING 
##                         | LINEARCORRELATION_MATCHING}
try:
    import arcpy
    arcpy.env.workspace = r"D:\77211356\CropClass\results"

    ##Create a empty TIFF format Raster Dataset with the following parameters
    ##Cellsize: 2
    ##Pixel type: 8 Bit Unsigned Integer
    ##Number of Bands: 3
    ##Pyramid: Build full pyramids with NEAREST interpolation and JPEG compression
    ##Compression: NONE
    ##Projection: World_Mercator
    ##Tile size: 128 128
    arcpy.CreateRasterDataset_management("CreateRD","EmptyTIFF.tif","10","8_BIT_UNSIGNED",\
                                         "World_Mercator.prj", "1", "", "PYRAMIDS -1 NEAREST JPEG",\
                                         "128 128", "NONE", "")


    
    ##Mosaic two TIFF images to a single TIFF image
    ##Background value: 0
    ##Nodata value: 9
    arcpy.Mosaic_management("EXGBoundry_Clip.tif;rc.tif","EmptyTIFF.tif","LAST","FIRST","0", "0", "", "", "")
    
    ##Mosaic several 3-band TIFF images to FGDB Raster Dataset with Color Correction
    ##Set Mosaic Tolerance to 0.3. Mismatch larget than 0.3 will be resampled
    #arcpy.Mosaic_management("rgb1.tif;rgb2.tif;rgb3.tif", "Mosaic.gdb\\rgb","LAST","FIRST","", "", "", "0.3", "HISTOGRAM_MATCHING")
except:
    print "Mosaic example failed."
    print arcpy.GetMessages()
