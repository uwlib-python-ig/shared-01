from datetime import datetime

class GblRecord(object): 


    def __init__(self): 
        self.success = True
        self.ref_007_00= {
        'a': 'Map',
        'c': 'Electronic resource',
        'd': 'Globe',
        'f': 'Tactile material',
        'g': 'Projected graphic',
        'h': 'Microform',
        'k': 'Nonprojected graphic',
        'm': 'Motion picture',
        'o': 'Kit',
        'q': 'Notated music',
        'r': 'Remote-sensing image',
        's': 'Sound recording',
        't': 'Text',
        'v': 'Videorecording',
        'z': 'Unspecified'
        }
        self.data = {
            "dct_identifier_sm": [],
            "schema_provider_s": "University of Washington",
            "gbl_resourceClass_sm": [],
            "dct_accessRights_s": "Public", # hard code public access OK?
            "gbl_mdModified_dt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "gbl_mdVersion_s": "Aardvark"
            }


    def set_id(self, data):
        keyval = {'id': data}
        self.data.update(keyval)


    def set_dct_identifier_sm(self, mmsid):
        self.data['dct_identifier_sm'].append(mmsid)


    def set_dct_title_s(self, data):
        if data.endswith('/'):
            data = data.rstrip('/')
        # a great deal more title-cleaning needed, for example:
            # [titles enclosed in brackets]
            # Parallel titles ('=')?
            # Unicode escape characters!?!?
            # ...
        keyval = {'dct_title_s': data.strip()}
        self.data.update(keyval)


    def set_locn_geometry(self, d, e, f, g): # for this method I fail in main...
            if self.success == True:
                keyval = {'locn_geometry': f"ENVELOPE({d}, {e}, {f}, {g})"}
            elif self.success == False and d == 'KeyError':
                keyval = {'locn_geometry': d}
            else:
                keyval = {'locn_geometry': d}
            self.data.update(keyval)


    def set_gbl_resourceClass_sm(self, data): # ...but for this method I fail in GblRecord (inconsistent = bad?)
        if data == 'a':
            resource_class_value = "Maps"
        elif data in ['c', 'd', 'f', 'g', 'h', 'k', 'm', 'o', 'q', 'r', 's', 't','v', 'z']:
            self.success = False
            resource_class_value = "error - known 007/00 value but other than a/Map"
            # need to map  other of 007/00 values to Resource Class Values
            # https://opengeometadata.org/ogm-aardvark/#resource-class-values
        else:
            self.success = False
            resource_class_value = data
        self.data['gbl_resourceClass_sm'].append(resource_class_value)


    def set_test(self):
        self.data.update({'test': 'hello world'})


    # Class function naming convention is to include get/set when interacting with variables
    # Similarly, in OOP, instance variables from class objects are often accessed solely through get/set functions
    # although this matters very little in Python, as it doesnt have any concept of private or protected variables
