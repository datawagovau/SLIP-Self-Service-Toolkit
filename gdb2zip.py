import os
import shutil
import zipfile
# Creates a zip file containing the all the files inside the filegeodatabase folder
#   inShp: Full path to shapefile to be zipped
#   Delete: Set to True to delete shapefile files after zip

# Creates a zip file containing the contents of a filegeodatabase
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
print Zipfgdb(r'D:\selfservice\filegeodatabase.gdb', False)