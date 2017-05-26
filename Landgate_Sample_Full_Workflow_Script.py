from sde2gdb import sde2gdb
from gdb2zip import Zipfgdb
import datetime,logging,traceback,arcpy,sys
nowstart = datetime.datetime.now()
YearMonthDay = nowstart.strftime("%Y_%m_%d_%H_%M_%S")

########### User Environment dependent variables ###############
SDE_CONNECTION = r'C:\AARON_DATA\Connection to PEAS71 - DISS - SDE.sde'
SDE_FEATURE_CLASS_NAME = 'GDB.W_IMAGERY_METADATA'

SLIP_DATASET_NAME= 'LGATE071' #this needs to be the same name as the dataset used to initialise in selfsevice
AWS_CREDENTIAL_PROFILE = 'SLIP_UAT'
TEMP_WORKING_DIRECTORY = r'C:\Selfservice_uploads'
TEMP_FGDB = SLIP_DATASET_NAME + '_asat_'+YearMonthDay

LOGFILENAME = TEMP_WORKING_DIRECTORY+ r'\\' + SLIP_DATASET_NAME + '_asat_'
LOGLEVEL = logging.DEBUG
################################################################

def setupLogging() :
    newlogfilename = LOGFILENAME + YearMonthDay + '.log'
    logformatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(LOGLEVEL)

    filehandler = logging.FileHandler(newlogfilename)
    filehandler.setFormatter(logformatter)
    logger.addHandler(filehandler)

    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(logformatter)
    logger.addHandler(consolehandler)

try:
    setupLogging()
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
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "Encounter Python Errors & Traceback info:\n" + str(tbinfo) + "\nError Info:\n" + str(sys.exc_info()[1])
    arcpy.AddError(pymsg)
    logging.error(pymsg)
finally:
    logging.info('Script shutdown.')
    logging.info('**************************************************************************************************')
    logging.shutdown()
    logging.getLogger(None).handlers = []



