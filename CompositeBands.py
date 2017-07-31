import arcpy
from arcpy import env
env.workspace = "D:/share/croppattern/sentinel2/hubei/S2A_tile_20170227_49RGP_0"
arcpy.CompositeBands_management("B02.jp2;B03.jp2;B04.jp2;B08.jp2","S2A_tile_20170227_49RGP_0.tif")
print("OK")
