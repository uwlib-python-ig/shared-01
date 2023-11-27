# code review: marc2geoblacklight

### NOTES on code
*From @briesenberg07, who wrote this*  
- This code:
    - takes as input pre-processed MARC binary records\*\*
    - outputs JSON files which conform to the OpenGeoMetadata (OGM) Aardvark Schema (see [field reference](https://opengeometadata.org/ogm-aardvark/), [JSON schema](https://opengeometadata.org/schema/geoblacklight-schema-aardvark.json))
- It's been so long since I've touched this that I hardly remember how it works!
- was a first for me in terms of implementing a class and class methods to accomplish some tasks
- This code has *not* been implemented in production, the project seems to be on hold at the moment
- Much room for improvement--for example:
    - Improve cleaning of MARC field data (see `set_dct_title()`)
    - Improve validation for MARC field data pushing values to JSON
    - Map additional 007 values to the available GeoBlacklight [Resource Class values](https://opengeometadata.org/ogm-aardvark/#resource-class-values), if possible
    - Add validation for output JSON files
    - Instead of pre-processing MARC binary data to replace **034 $d $e $f $g** hours/minutes/seconds with decimal degrees, do this in the script

\*\* *If you want to try running the code you can download and use [this pre-processed binary file](https://uwnetid-my.sharepoint.com/:u:/g/personal/ries07_uw_edu/EQpjv2Li0ahMsZyuaHOO5ocBKuY4zap-8Q1DXC74eKjQTw?e=Dplfyf)*  

### QUESTIONS
- Very generally speaking, do the classes and class methods make sense? Are there any glaring mistakes in the class/method implementation?
    - For example, output JSON is counted and output as either a 'success' (ready to load) or 'failure' (not ready to load), depending on the boolean class variable `success`. For some methods, the failure (if there is a failure) happens in main.py, and for some, it happens in the method. Does it matter that this is inconsistent?
