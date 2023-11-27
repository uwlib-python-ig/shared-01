import os
import pymarc
from GblRecord import GblRecord
import uuid
import json


def write_record(outputpath, record_id, data):
    with open(f"{outputpath}{record_id}.json", "w") as jsonfile:
        json.dump(data, jsonfile)


success_path = '../../marc4geoblacklight/load/' # for testing, same dir as output
fail_path = '../../marc4geoblacklight/failed/'
inputpath = '../../marc4geoblacklight/exports/'

# load uuids previously assigned per MMS ID
if os.path.exists('reuse_ids.json'):
    with open('reuse_ids.json', 'r') as jsonfile:
        reuse_ids = json.load(jsonfile)
        reuse_ids_count = len(reuse_ids)
else:
    reuse_ids = {}
    reuse_ids_count = 0

# convert marc
success = 0
fail = 0
filename = input("input MARC binary filename including extension\n>>>")
inputfile = f"{inputpath}{filename}"
print(f"{reuse_ids_count} IDs for reuse before processing")
with open(inputfile, 'rb') as mrcfile:
    reader = pymarc.MARCReader(mrcfile, force_utf8=True)
    for record in reader:
        gblrecord = GblRecord()
        # gblrecord.set_test() # testing here
        mmsid = f"mmsid_{record['001'].value()}" # assuming I will never fail to retrieve 001 - see notes_002_other.ipynb
        if mmsid in reuse_ids:
            recordid = reuse_ids[mmsid]
            gblrecord.set_id(recordid)
        else:
            recordid = f"uwashington_{uuid.uuid4()}"
            # need to update reuse_ids
            reuse_ids.update({mmsid: recordid})
            gblrecord.set_id(recordid)
        gblrecord.set_dct_identifier_sm(mmsid) # assuming I will never fail to retrieve 001 -
        gblrecord.set_dct_title_s(record.title) # also assuming that Record.title will never fail
        try:
            d, e, f, g, = record['034']['d'], record['034']['e'], record['034']['f'], record['034']['g']
            gblrecord.set_locn_geometry(d, e, f, g)
        except KeyError as error:
            gblrecord.success = False
            gblrecord.set_locn_geometry('KeyError', '', '', '') # call func without unneeded args?
        except:
            gblrecord.success = False
            gblrecord.set_locn_geometry('other error', '', '', '') # call func without unneeded args?
        try:
            if record['007'].value()[0] in gblrecord.ref_007_00:
                gblrecord.set_gbl_resourceClass_sm(record['007'].value()[0])
            else:
                gblrecord.set_gbl_resourceClass_sm('error - unknown 007/00 value')
        except KeyError as error:
            gblrecord.set_gbl_resourceClass_sm('KeyError')
        # more fields to do
        # dcat_bbox - same as locn_geo? See https://opengeometadata.org/ogm-aardvark/#bounding-box
        # spatial coverage
        # keywords
        # some kind of published date???
        if gblrecord.success == True:
            success += 1
            write_record(success_path, recordid, gblrecord.data)
        else:
            fail += 1
            write_record(fail_path, recordid, gblrecord.data)

with open('reuse_ids.json', 'w') as jsonfile:
    json.dump(reuse_ids, jsonfile)

reuse_ids_count = len(reuse_ids)
print(f"{reuse_ids_count} IDs for reuse after processing")

# to do -- add locn_geometry check -- see notes_003.ipynb

print(f"SUCCESS: {success}")
print(f"FAIL: {fail}")
print(F"TOTAL OUTPUT FILES: {success + fail}")
