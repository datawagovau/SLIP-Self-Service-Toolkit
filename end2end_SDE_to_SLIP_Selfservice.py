import sys, getopt
from sde2gdb import sde2gdb
from gdb2zip import Zipfgdb
from upload2S3 import UploadFile
import datetime,logging,traceback,arcpy,sys
nowstart = datetime.datetime.now()
YearMonthDay = nowstart.strftime("%Y_%m_%d_%H_%M_%S")

ERROR_DETECTED = False

def setupLogging(logfilename) :
    newlogfilename = logfilename + YearMonthDay + '.log'
    logformatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(10) #'10-Debug'
    filehandler = logging.FileHandler(newlogfilename)
    filehandler.setFormatter(logformatter)
    logger.addHandler(filehandler)
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(logformatter)
    logger.addHandler(consolehandler)

def execute_job(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE,AWS_S3_BUCKET,AWS_S3_FOLDER_KEY):
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
        s3_uploadURL = UploadFile(my_temp_zip,AWS_S3_BUCKET,AWS_S3_FOLDER_KEY+my_temp_zip,AWS_CREDENTIAL_PROFILE)
        logging.info('Successfully Uploading [%s] to S3' % my_temp_zip)
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
    AWS_S3_BUCKET = ''
    AWS_S3_FOLDER_KEY = ''
    TEMP_WORKING_DIRECTORY = ''

    try:
        opts, args = getopt.getopt(argv,'h',['sde_Connection=','inputFeatureClass=','workingDir=','outputFeatureClass=','aws_profile=','S3_Bucket=','S3_FolderKey='])

    except getopt.GetoptError:
        print ' --sde_Connection <SDE_Connection> --inputFeatureClass <SDE_Input_FeatureClass_Name> --workingDir <Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws_profile <AWS_Profile> --S3_Bucket <AWS_Bucket> --S3_Key <AWS_folderKey'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print '--sde_Connection <SDE_Connection> --inputFeatureClass <SDE_Input_FeatureClass_Name> --workingDir <Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws_profile <AWS_Profile>  --S3_Bucket <AWS_Bucket> --S3_Key <AWS_folderKey'
            sys.exit()
        elif opt == '--sde_Connection':
            SDE_CONNECTION = arg
        elif opt == '--inputFeatureClass':
            SDE_FEATURE_CLASS_NAME = arg
        elif opt == '--workingDir':
            TEMP_WORKING_DIRECTORY = arg
        elif opt == '--outputFeatureClass':
            SLIP_DATASET_NAME = arg
        elif opt == '--aws_profile':
            AWS_CREDENTIAL_PROFILE = arg
        elif opt == '--S3_Bucket':
            AWS_S3_BUCKET = arg
        elif opt == '--S3_FolderKey':
            AWS_S3_FOLDERKEY = arg

    #check all flags have been populated
    if (SDE_CONNECTION == '' or SDE_FEATURE_CLASS_NAME == '' or SLIP_DATASET_NAME == '' or AWS_CREDENTIAL_PROFILE == '' or TEMP_WORKING_DIRECTORY == ''):
        print '#### Insufficent parameters provided ####'
        print '--sde_Connection [%s] (ie. "C:\\selfservice_uploads\\Connection_to_PEAS71-DISS-SDE.sde " )'%SDE_CONNECTION
        print '--inputFeatureClass [%s] (ie. "GDB.W_IMAGERY_METADATA" )'%SDE_FEATURE_CLASS_NAME
        print '--workingDir [%s] (ie. "C:\\selfservice_uploads" )'%TEMP_WORKING_DIRECTORY
        print '--outputFeatureClass [%s] (ie. "LGATE071" )'%SLIP_DATASET_NAME
        print '--aws_profile [%s]( ie "SLIP_UAT_USER" )'%AWS_CREDENTIAL_PROFILE
        print '--S3_Bucket [%s] (ie. "lg-slip-selfservice-data-uat" )'%AWS_S3_BUCKET
        print '--S3_FolderKey [%s] (ie. "data-load//6//" )'%AWS_S3_FOLDER_KEY
        sys.exit(2)
    
    print 'executing job'
    execute_job(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE,AWS_S3_BUCKET,AWS_S3_FOLDER_KEY)
     

if __name__ == "__main__":
    main(sys.argv[1:])
