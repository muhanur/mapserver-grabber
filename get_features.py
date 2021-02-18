import urllib.parse, urllib.request, os, json

url = "https://dbgis.menlhk.go.id/arcgis/rest/services/KLHK/Penutupan_Lahan_Tahun_2019/MapServer/0/query?"
geojson = '{"type":"FeatureCollection","crs":{"type":"name","properties":{"name":"EPSG:4326"}},"features":[]}'
z = json.loads(geojson)

# Write json file
def write_json(data, filename = "Penutupan_Lahan_Tahun_2019.geojson"): 
    with open(filename, "w") as f: 
        json.dump(data, f)

# Get ids of layers
params = {"where":"Provinsi='Jawa Tengah'",
    "geometryType": "esriGeometryEnvelope",
    "spatialRel": "esriSpatialRelIntersects",
    "relationParam": "",
    "outFields": "*",
    "returnGeometry": "false",
    "geometryPrecision":"",
    "outSR": "",
    "returnIdsOnly": "true",
    "returnCountOnly": "false",
    "orderByFields": "",
    "groupByFieldsForStatistics": "",
    "returnZ": "false",
    "returnM": "false",
    "returnDistinctValues": "false",
    "f": "pjson"
}
encode_params = urllib.parse.urlencode(params).encode("utf-8")
response = urllib.request.urlopen(url, encode_params)
data = json.load(response)
ids = data["objectIds"]

print('Jumlah Layer', len(ids))

# Write by Ids
for x in range(len(ids)):
    params = {"where": "FID=" + str(ids[x]),
        "geometryType": "esriGeometryEnvelope",
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
    print(ids[x])
    response = urllib.request.urlopen(url, encode_params)
    data = json.load(response)
    features = data["features"][0]
    z["features"].append(features)
    
write_json(z)