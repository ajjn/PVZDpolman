import simplejson as json
import os.path

inputdataJSON = open(os.path.abspath('testdata/test04_a01.json')).read()
appendList = json.loads(inputdataJSON)
print(appendlist)