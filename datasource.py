import os
from osgeo import ogr

osr = ogr.osr

FILE = 'test01.sqlite'

os.system('clear')

def get_sqlite_driver():
    return ogr.GetDriverByName('SQLite')

driver = get_sqlite_driver()
if os.path.exists( FILE ):
    driver.DeleteDataSource( FILE )

# need to set filepath
datasource = driver.CreateDataSource('test01.sqlite')

# create spatial ref
layer_srs = osr.SpatialReference()
layer_srs.AutoIdentifyEPSG()
# create layer
layer = datasource.CreateLayer(
    name='layer01',
    geom_type=ogr.wkbPoint,
    srs=layer_srs
)
layer_defn = layer.GetLayerDefn()

# no need to add id field
# id_field = ogr.FieldDefn('id', ogr.OFTInteger)
# layer.CreateField(id_field)

# geometry already made from CreateLayer
# geom_field = ogr.GeomFieldDefn('geometry')
# layer.CreateGeomField(geom_field)

cu_field = ogr.FieldDefn('cu_ppm', ogr.OFTReal)
utm_east_field = ogr.FieldDefn('Easting', ogr.OFTReal)
utm_north_field = ogr.FieldDefn('Northing', ogr.OFTReal)
layer.CreateField(cu_field)
layer.CreateField(utm_east_field)
layer.CreateField(utm_north_field)

field_name_list = [
    layer_defn.GetFieldDefn(layer_field_idx).GetName()
    for layer_field_idx in range(layer_defn.GetFieldCount())
]


# Adding features
## feature #1
feature = ogr.Feature( layer_defn )
geometry = ogr.Geometry(type=ogr.wkbPoint)
feature.SetField('cu_ppm', 90)
feature.SetField('Easting', 423446.783829)
feature.SetField('Northing', 9017235.293323)
print(feature.GetField('easting'))
geometry.AddPoint(feature.GetField('Easting'),
                  feature.GetField('Northing'))
feature.SetGeometry(geometry)
# nonexistent field will get KeyError on GetField
# feature.GetField('ag_ppm')
# or will get 'Invalid index' prompt on SetField
# feature.SetField('ag_ppm', 90)
layer.CreateFeature(feature)
feature.Destroy()

"""
## feature #2 etc
feature = ogr.Feature( layer_defn )
geometry = ogr.Geometry(type=ogr.wkbPoint)
geometry.AddPoint(1, 0)
feature.SetGeometry(geometry)
feature.SetField(cu_field.GetName(), 99)
layer.CreateFeature(feature)
feature.Destroy()
"""

# flush / commit to disk
datasource.SyncToDisk()

# dev
print(field_name_list)
print(layer.GetFeatureCount())
datasource.Destroy()
