import argparse
import logging
import os
import socket
import sys
import time
import datetime
sys.path.append("C:/Users/Anna/Desktop/qqq/pydicom/pydicom")
from pydicom import read_file
from pydicom.dataset import Dataset
from pydicom.uid import UID
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, \
    ExplicitVRBigEndian

from pydicom.uid import UID

sys.path.append("C:/Users/Anna/Desktop/pynetdicom_git_clone/pynetdicom3")
from pynetdicom3 import AE, sop_class 
from pynetdicom3 import association
from pynetdicom3.sop_class import NCreateSetServiceClass

logger = logging.Logger('N-CREATE')
stream_logger = logging.StreamHandler()
formatter = logging.Formatter('%(levelname).1s: %(message)s')
stream_logger.setFormatter(formatter)
logger.addHandler(stream_logger)
logger.setLevel(logging.ERROR)

VERSION = '0.6.0'



def _setup_argparser():
    """Setup the command line arguments"""
    # Description
    parser = argparse.ArgumentParser(
        description="N-CREATE",
        usage="ncreate [options] peer port dcmfile-in")

    # Parameters
    req_opts = parser.add_argument_group('Parameters')
    req_opts.add_argument("peer", help="hostname of DICOM peer", type=str)
    req_opts.add_argument("port", help="TCP/IP port number of peer", type=int)
    req_opts.add_argument("dcmfile_in",
                          metavar="dcmfile-in",
                          help="DICOM file or directory to be transmitted",
                          type=str)

    # General Options
    gen_opts = parser.add_argument_group('General Options')
    gen_opts.add_argument("--version",
                          help="print version information and exit",
                          action="store_true")
    gen_opts.add_argument("-q", "--quiet",
                          help="quiet mode, print no warnings and errors",
                          action="store_true")
    gen_opts.add_argument("-v", "--verbose",
                          help="verbose mode, print processing details",
                          action="store_true")
    gen_opts.add_argument("-d", "--debug",
                          help="debug mode, print debug information",
                          action="store_true")
    gen_opts.add_argument("-ll", "--log-level", metavar='[l]',
                          help="use level l for the logger (fatal, error, warn, "
                               "info, debug, trace)",
                          type=str,
                          choices=['fatal', 'error', 'warn',
                                   'info', 'debug', 'trace'])
    gen_opts.add_argument("-lc", "--log-config", metavar='[f]',
                          help="use config file f for the logger",
                          type=str)

    # Network Options
    net_opts = parser.add_argument_group('Network Options')
    net_opts.add_argument("-aet", "--calling-aet", metavar='[a]etitle',
                          help="set my calling AE title (default: FINDSCU)",
                          type=str,
                          default='FINDSCU')
    net_opts.add_argument("-aec", "--called-aet", metavar='[a]etitle',
                          help="set called AE title of peer (default: ANY-SCP)",
                          type=str,
                          default='ANY-SCP')

    # Transfer Syntaxes
    ts_opts = parser.add_mutually_exclusive_group()
    ts_opts.add_argument("-xe", "--request-little",
                         help="request explicit VR little endian TS only",
                         action="store_true")
    ts_opts.add_argument("-xb", "--request-big",
                         help="request explicit VR big endian TS only",
                         action="store_true")
    ts_opts.add_argument("-xi", "--request-implicit",
                         help="request implicit VR little endian TS only",
                         action="store_true")


    return parser.parse_args()

args = _setup_argparser()

if args.verbose:
    logger.setLevel(logging.INFO)
    pynetdicom_logger = logging.getLogger('pynetdicom3')
    pynetdicom_logger.setLevel(logging.INFO)

if args.debug:
    logger.setLevel(logging.DEBUG)
    pynetdicom_logger = logging.getLogger('pynetdicom3')
    pynetdicom_logger.setLevel(logging.DEBUG)

#if args.version:
#    print('ncreate.py v{0!s} {1!s} $'.format(VERSION, '2017-02-04'))
#    sys.exit()

logger.debug('ncreate.py v{0!s} {1!s}'.format(VERSION, '2017-02-04'))
logger.debug('')


ae = AE(ae_title=args.calling_aet,
        port=0,
        scu_sop_class=NCreateSetServiceClass.__subclasses__(),
        scp_sop_class=[],
        transfer_syntax=[ImplicitVRLittleEndian])


# Request association with remote
assoc = ae.associate(args.peer, args.port, args.called_aet)

# Set Transfer Syntax options
transfer_syntax = [ExplicitVRLittleEndian,
                   ImplicitVRLittleEndian,
                   #DeflatedExplicitVRLittleEndian,
                   ExplicitVRBigEndian]

if args.request_little:
    transfer_syntax = [ExplicitVRLittleEndian]
elif args.request_big:
    transfer_syntax = [ExplicitVRBigEndian]
elif args.request_implicit:
    transfer_syntax = [ImplicitVRLittleEndian]

# Bind to port 0, OS will pick an available port

print("drukuj", NCreateSetServiceClass.__subclasses__()[0].UID)



#ae.on_n_create = on_n_create

if assoc.is_established:
    # Check file exists and is readable and DICOM
    logger.debug('Checking input files')
    try:
        f = open(args.dcmfile_in, 'rb')
        dataset = read_file(f, force=True)
        f.close()
    except IOError:
        logger.error('Cannot read input file {0!s}'.format(args.dcmfile_in))
        sys.exit()
    
    #dataset = Dataset()
    
    dataset.PerformedProcedureStepStartDate =datetime.datetime.now().strftime('%Y%m%d') 
    dataset.PerformedProcedureStepStartTime = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime(('%H%M%S'))
    
    #sop_class='1.2.826.0.1.3680043.2.1545.1'
    #sop_instance_iud = UID('1.2.840.10008.1.2.4.50')
    sop_class=NCreateSetServiceClass.__subclasses__()[0]
    sop_instance_iud='1.2.826.0.1.3680043.2.1545.1.2.1.7.20180830.132456.926.6'
    #sop_instance_iud='1.2.840.10008.5.1.4.1.1.1.1'
    #sop_instance_iud=dataset.StudyInstanceUID
    response = assoc._send_n_dimse("N-CREATE", dataset, sop_class , sop_instance_iud, msg_id=1)
    print("odpowiedz",response)
    

    

    #time.sleep(10)
    if response is not None:
        for value in response:
            print("wartosc",value)
            pass
            
    assoc.release()

ae.quit()


