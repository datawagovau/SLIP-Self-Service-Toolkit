import sys, getopt
from sde2gdb import sde2gdb
from gdb2zip import Zipfgdb
import datetime,logging,traceback,arcpy,sys
nowstart = datetime.datetime.now()
YearMonthDay = nowstart.strftime("%Y_%m_%d_%H_%M_%S")

ERROR_DETECTED = False

def setupLogging(logfilename) :
    newlogfilename = logfilename + YearMonthDay + '.log'
    logformatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(10) '10-Debug'
    filehandler = logging.FileHandler(newlogfilename)
    filehandler.setFormatter(logformatter)
    logger.addHandler(filehandler)
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(logformatter)
    logger.addHandler(consolehandler)

def execute_job(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE):
    try:
        logfile = TEMP_WORKING_DIRECTORY+ r'\\' + SLIP_DATASET_NAME + '_asat_'
        setupLogging(logfile)
        TEMP_FGDB = SLIP_DATASET_NAME + '_asat_'+YearMonthDay
        logging.info('**************************************************************************************************')
        logging.info("Starting program at " + str(datetime.datetime.now()))
        logging.info("Attempting to Connect to SDE workspace [%s].\n\t\t\t\tExporting SDE FeatureClass [%s] To [%s\\%s.gdb]"% (SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,TEMP_FGDB))
        my_temp_filegdb = sde2gdb(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,TEMP_FGDB,SLIP_DATASET_NAME)
        logging.info('Successfully created file geodatabase [%s]' % my_temp_filegdb)
        logging.info('Zipping up [%s]' % my_temp_filegdb)
        my_temp_zip = Zipfgdb(my_temp_filegdb)
        logging.info('Successfully created zip geodatabase [%s]' % my_temp_zip)
        logging.info('Uploading [%s] to S3' % my_temp_zip)
        logging.info("Completing program at " + str(datetime.datetime.now()))
        pass
    except arcpy.ExecuteError:
        arcpymsg = arcpy.GetMessages(2)
        arcpy.AddError(arcpymsg)
        logm = 'Encounter ArcPy Errors:\n' + str(arcpymsg)
        logging.error(logm)
        ERROR_DETECTED = True
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "Encounter Python Errors & Traceback info:\n" + str(tbinfo) + "\nError Info:\n" + str(sys.exc_info()[1])
        arcpy.AddError(pymsg)
        logging.error(pymsg)
        ERROR_DETECTED = True
    finally:
        logging.info('Script shutdown.')
        logging.info('**************************************************************************************************')
        logging.shutdown()
        logging.getLogger(None).handlers = []
        #if (ERROR_DETECTED == True):
        #    os.rename(TEMP_WORKING_DIRECTORY+ r'\\' + SLIP_DATASET_NAME + '_asat_' ++ YearMonthDay + '.log'+ YearMonthDay + '.log'

def main(argv):
    SDE_CONNECTION = ''
    SDE_FEATURE_CLASS_NAME = ''
    SLIP_DATASET_NAME = ''
    AWS_CREDENTIAL_PROFILE = ''
    TEMP_WORKING_DIRECTORY = ''
    try:
        opts, args = getopt.getopt(argv,'h',['sde=','ifc=','wd=','ofc=','aws='])

    except getopt.GetoptError:
        print ' --sde <SDE_Connection> --ifc <SDE_Input_FeatureClass_Name> --wd <Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws <AWS_Profile> '
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print '--sde <SDE_Connection> --ifc <SDE_Input_FeatureClass_Name> --wd <Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws <AWS_Profile> '
            sys.exit()
        elif opt == '--sde':
            SDE_CONNECTION = arg
        elif opt == '--ifc':
            SDE_FEATURE_CLASS_NAME = arg
        elif opt == '--wd':
            TEMP_WORKING_DIRECTORY = arg
        elif opt == '--ofc':
            SLIP_DATASET_NAME = arg
        elif opt == '--aws':
            AWS_CREDENTIAL_PROFILE = arg
    #check all flags have been populated
    if (SDE_CONNECTION == '' or SDE_FEATURE_CLASS_NAME == '' or SLIP_DATASET_NAME == '' or AWS_CREDENTIAL_PROFILE == '' or TEMP_WORKING_DIRECTORY == ''):
        print '#### Insufficent parameters provided ####'
        print 'SDE_CONNECTION [%s]'%SDE_CONNECTION
        print 'SDE_FEATURE_CLASS_NAME [%s]'%SDE_FEATURE_CLASS_NAME
        print 'TEMP_WORKING_DIRECTORY [%s]'%TEMP_WORKING_DIRECTORY
        print 'SLIP_DATASET_NAME [%s]'%SLIP_DATASET_NAME
        print 'AWS_CREDENTIAL_PROFILE [%s]'%AWS_CREDENTIAL_PROFILE
        print '\n\nRequired flags:'
        print '--sde <SDE_Connection>\n --ifc <SDE_Input_FeatureClass_Name>\n --wd <Tempory_Working_Directory_used_to_store_logs_and_the_fgdb>\n --ofc <Output_Feature_Class_Name>\n --aws <AWS_Profile>\n '
        sys.exit(2)
    
    print 'executing job'
    execute_job(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE)
     

if __name__ == "__main__":
    main(sys.argv[1:])
