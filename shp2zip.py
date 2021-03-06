import os
import shutil
import zipfile
# Function Name: ZipShp()
# Purpose:
#   Creates a zip file containing all the files associated with a shapefile
#   The function will return the location of the zipped shapefile . ie (r'D:\selfservice\shapefile\DOT_Vavids.zip')
#          
# usage:
#      ZipShp <inShapeFile> <Delete files after compression TRUEorFALSE> 
#           ie ZipShp(r'D:\selfservice\shapefile\DOT_Vavids.shp', False)
#
# Author: Aaron Thorn        
# Version : 0.1 26/5/2017   

def ZipShp (inShp, Delete = True):
    #List of shapefile file extensions
    extensions = [".shp",".shx",".dbf",".sbn",".sbx",".fbn",".fbx",".ain",".aih",".atx",".ixs",".mxs",".prj",".xml",".cpg",".shp.xml"]
    #Directory of shapefile
    inLocation = os.path.dirname (inShp)
    #Base name of shapefile
    inName = os.path.basename (os.path.splitext (inShp)[0])
    #Create zipfile name
    zipfl = os.path.join (inLocation, inName + ".zip")
    #Create zipfile object
    ZIP = zipfile.ZipFile (zipfl, "w")
    #Empty list to store files to delete
    delFiles = []
    #Iterate files in shapefile directory
    for fl in os.listdir (inLocation):
        #Iterate extensions
        for extension in extensions:
            #Check if file is shapefile file
            if fl == inName + extension:
                #Get full path of file
                inFile = os.path.join (inLocation, fl)
                #Add file to delete files list
                delFiles += [inFile]
                #Add file to zipfile
                ZIP.write (inFile, fl)
                break
    #Delete shapefile if indicated
    if Delete == True:
        for fl in delFiles:
            os.remove (fl)
    #Close zipfile object
    ZIP.close()
    #Return zipfile full path
    return zipfl

#test zipping a shapefile. The output zip files is 
#print ZipShp(r'D:\selfservice\shapefile\DOT_Vavids.shp', False)
