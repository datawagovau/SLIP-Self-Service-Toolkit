import os
import shutil
import zipfile
# Function Name: Zipfgdb()
# Purpose:
#   Creates a zip file containing the contents of a filegeodatabase ready for uploading into selfservice
#   The function will return the location of the zipped file geodatabase. ie D:\selfservice\filegeodatabase.zip
#          
# usage:
#      Zipfgdb <inFileGDB> <Delete filegeodatabase after compression TRUEorFALSE> 
#           ie Zipfgdb(r'D:\selfservice\filegeodatabase.gdb', False)
def Zipfgdb(inFileGDB, Delete = True):
    #Directory of file geodatabase
    inLocation = os.path.dirname (inFileGDB)
    #Base name of shapefile
    inName = os.path.basename (os.path.splitext(inFileGDB)[0])
    #Create the zipfile name 
    zipfl = os.path.join (inLocation, inName + ".zip")
    #Create zipfile object
    ZIP = zipfile.ZipFile (zipfl, "w")
    #Iterate files in shapefile directory
    for fl in os.listdir (inFileGDB):
        #Get full path of file
        inFile = os.path.join (inFileGDB, fl)
        #Add file to zipfile. exclude any lock files
        if os.path.splitext(fl)[1][1:] <> 'lock':
            ZIP.write(inFile,fl)
    #Delete filegeodatabase if indicated
    if Delete == True:
        shutil.rmtree(inFileGDB)
    #Close zipfile object
    ZIP.close()
    #Return zipfile full path
    return zipfl

#test zipping a geodatabase.
#print Zipfgdb(r'D:\selfservice\filegeodatabase.gdb', False)