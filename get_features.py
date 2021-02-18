import urllib.parse, urllib.request, os, json

# Configuration you need to change
url = "https://host/arcgis/rest/services/directory/layer/MapServer/0/"
query = "1=1"
output_dir = "C:/ESRI/"

# Getting layer information
params = {"f": "pjson"}
encode_params = urllib.parse.urlencode(params).encode("utf-8")
response = urllib.request.urlopen(url, encode_params)
layer_info = json.load(response)

geometryType = layer_info["geometryType"]
name = layer_info["name"]

print('Geometry Type: ', geometryType)
print('Layer Name: ', name)

# Preparing geojson output
geojson = '{"type":"FeatureCollection","crs":{"type":"name","properties":{"name":"EPSG:4326"}},"features":[]}'
z = json.loads(geojson)

# Write json file
def write_json(data, filename = output_dir + name + ".geojson"):
    with open(filename, "w") as f:
        json.dump(data, f)

# Get ids of layers
params = {"where": query,
    "text": "",
    "objectIds": "",
    "time": "",
    "geometry": "",
    "geometryType": "esriGeometryEnvelope",
    "inSR": "",
    "spatialRel": "esriSpatialRelIntersects",
    "relationParam": "",
    "outFields": "*",
    "returnGeometry": "false",
    "returnTrueCurves": "false",
    "maxAllowableOffset": "",
    "geometryPrecision": "",
    "outSR": "",
    "returnIdsOnly": "true",
    "returnCountOnly": "false",
    "orderByFields": "",
    "groupByFieldsForStatistics": "",
    "outStatistics": "",
    "returnZ": "false",
    "returnM": "false",
    "gdbVersion": "",
    "returnDistinctValues": "false",
    "resultOffset": "",
    "resultRecordCount": "",
    "f": "pjson"
}
encode_params = urllib.parse.urlencode(params).encode("utf-8")
response = urllib.request.urlopen(url + "query", encode_params)
data = json.load(response)
idFN = data["objectIdFieldName"]
ids = data["objectIds"]

print('Number of feature Layer: ', len(ids))

# Write by Ids
for x in range(len(ids)):
    params = {"where": idFN + "=" + str(ids[x]),
        "geometryType": geometryType,
        "spatialRel": "esriSpatialRelIntersects",
        "relationParam": "",
        "outFields": "*",
        "returnGeometry": "true",
        "geometryPrecision":"",
        "outSR": "",
        "returnIdsOnly": "false",
        "returnCountOnly": "false",
        "orderByFields": "",
        "groupByFieldsForStatistics": "",
        "returnZ": "false",
        "returnM": "false",
        "returnDistinctValues": "false",
        "f": "geojson"
    }

    encode_params = urllib.parse.urlencode(params).encode("utf-8")
    print('Getting Feature ' + idFN + ': ', ids[x])
    response = urllib.request.urlopen(url + "query", encode_params)
    data = json.load(response)
    features = data["features"][0]
    z["features"].append(features)

write_json(z)
