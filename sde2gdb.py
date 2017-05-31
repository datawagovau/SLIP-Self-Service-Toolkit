import arcpy
import os
import shutil

# Function Name: sde2fgdb()
# Purpose:
#   Function to export a SDE feature class to a file geodatabase.
#   The function will return location of the file geodatabase. ie C:\AARON_DATA\LGATE071.gdb
#          
# usage:
#      sde2fgdb <SDE_Connection> <SDE_FC_Name> <path_to_output_fGDB> <fGDB_Name> <Output_FC_Name>
#
#
# Author: Aaron Thorn        
# Version : 0.1 26/5/2017   
#
def sde2gdb(sde_connection,featureclass_name,output_path,fgdb_name,outFCname):
    #establish sde connection workspace
    arcpy.env.workspace = sde_connection
    #does the geodatabase exist if so delete it
    if (os.path.isdir(output_path+'\\'+fgdb_name+'.gdb')== True):
        shutil.rmtree(output_path+'\\'+fgdb_name+'.gdb')
    #create a version 10 FileGDB. Note Selfservice only supports FileGDB <10.3
    arcpy.CreateFileGDB_management(output_path, fgdb_name,"10.0")
    #Export the sde featureclass to the filegdb
    arcpy.FeatureClassToFeatureClass_conversion(sde_connection+'//'+featureclass_name, 
                                            output_path+'\\'+fgdb_name+'.gdb', 
                                            outFCname)
    #drop SDE connection 
    arcpy.ClearWorkspaceCache_management()
    return output_path+'\\'+fgdb_name+'.gdb'

# Test fuction calls
#test sde2fgdb <SDE_Connection> <SDE_FC_Name> <path_to_output_fGDB> <fGDB_Name> <Output_FC_Name>
#print sde2fgdb(r'C:\AARON_DATA\Connection to PEAS71 - DISS - SDE.sde','GDB.W_IMAGERY_METADATA',r'C:\AARON_DATA','mygdb.gdb','LGATE71')