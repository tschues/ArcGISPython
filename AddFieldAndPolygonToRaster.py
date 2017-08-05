import time,os,arcpy


####************please close the features which will be processed in ArcMap************


print 'Start:' + str(time.ctime())
# we're only looking for shapefiles
extension = "shp"
folder = r"D:\77211356\CropClass\results"
arcpy.env.workspace = folder
count = 0
# loop through files directory
for feature_class in (f for f in os.listdir(folder) if f.endswith(extension) ):
        #Add a Field to identify the Class Result  
        fieldName1 = "ClassMark"  
        fieldPrecision = 4  
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
            arcpy.DeleteField_management(feature_class, fieldName1)  
            print"Delete the "+fieldName1+" Fields"  
          
        #Function AddField_management
        arcpy.AddField_management(feature_class, fieldName1, "SHORT", fieldPrecision, "", "",  
                                      fieldAlias, "NULLABLE")  
        #the Field Name  
        field1 = "ClassMark" 
              
        #update query  
        cursor = arcpy.UpdateCursor(feature_class)  
        for row in cursor:  
            # field1 will be equal to 0  
            if((int)(row.getValue(field1)) == 0):  
                row.setValue(field1, 1)  
            else:  
                row.setValue(field1, 1)  
            cursor.updateRow(row)  
        print feature_class+'-----add field Finished---:' + str(time.ctime())

        #-----------------------------PolygonToRaster--------------------------------------
        inFeatures = feature_class
        valField = fieldName1
        outRaster = folder+ "\\" + feature_class.split('.')[0] + ".tif"
        print outRaster
        assignmentType = "MAXIMUM_AREA"
        priorityField = ""
        cellSize = 10
        if not(os.path.isfile(outRaster)):
                # Execute PolygonToRaster
                arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, 
                                                 assignmentType, priorityField, cellSize)

                print outRaster+'-----PolygonToRaster Finished---:' + str(time.ctime())
                
                count += 1
                print "count=:"+str(count)
        else:
                print "Output Raster Dataset--"+outRaster+": Dataset already exists"
print count, "all files processed."
