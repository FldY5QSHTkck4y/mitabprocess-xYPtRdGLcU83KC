import os
from osgeo import ogr, osr, __version__ as osgeo_version

import fields
import read_config

# do something with read_config
"""
read config
will get:
    - files: file list
    - layers: layer list for each file
    - layer_config: maping of column to be inserted to g_table
    - columns: list of used g_table's column from all config listed
"""

# create g_table
# create compilation g_layer: BLEG, SOIL, ROCK, SS
# for each layer create column from 'columns'
# for layer geometry, use EPSG4326
# read each file in 'files'
# read each layer in 'layers'
# convert each layer from any spatial ref to EPSG4326
# copy layer data mapped in 'layer_config'
# copy layer geometry data, not mapped in layer_config
# on finish output to sqlite

def create_g_table_datasource(path=None, **kwargs):
    output_path = 'output.sqlite'
    if path:
        output_path = path
    driver = ogr.GetDriverByName('SQLite')
    if os.path.exists(output_path):
        driver.DeleteDataSource(output_path)
    datasource = driver.CreateDataSource(output_path)
    return datasource

def get_srs(srid=None, **kwargs):
    layer_srid = 4326
    if srid == None:
        layer_srid = srid
    layer_srs = osr.SpatialReference()
    if int(osgeo_version[0]) >= 3:
        # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
        layer_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    layer_srs.ImportFromEPSG(4326)
    return layer_srs

def add_g_table_layer(datasource, name, columns, **kwargs):
    if datasource == None:
        return
    layer = datasource.CreateLayer(
        name=name,
        geom_type=ogr.wkbUnknown,
        srs=get_srs(4326),
    )

    for col in columns:
        layer.CreateField(ogr.FieldDefn(col, fields.column_map[col]))
    return layer

def is_ppb_column(column_name=None):
    if column_name == None:
        return False

    col = str(column_name).lower()

    if '_ppb' in col:
        return True
    else:
        return False

def is_pct_column(column_name=None):
    if column_name == None:
        return False

    col = str(column_name).lower()

    if '_pct' in col or '%' in col:
        return True
    else:
        return False

def ppm_value(text='', **kwargs):
    value = None
    try:
        value = float(text)
    except:
        value = 1e-4
    return value

ds = create_g_table_datasource(path='project.sqlite')

files, layers, layer_config, columns, table_types = read_config.read_config('project_config.txt')

target_srs = get_srs(4326)

bleg_layer = add_g_table_layer(ds, 'BLEG', columns)
rock_layer = add_g_table_layer(ds, 'ROCK', columns)
soil_layer = add_g_table_layer(ds, 'SOIL', columns)
ss_layer = add_g_table_layer(ds, 'SS', columns)
layer_map = {
    'BLEG': bleg_layer,
    'ROCK': rock_layer,
    'SOIL': soil_layer,
    'SS': ss_layer,
}

for idx, file in enumerate(files):
    source_ds = ogr.Open(file)
    layer = layer_map[table_types[idx]]
    layer_defn = layer.GetLayerDefn()
    for idl, layer_name in enumerate(layers[idx]):
        # read layer idl of source_ds
        src_layer = source_ds.GetLayer(idl)
        src_layer_srs = src_layer.GetSpatialRef()
        print(src_layer_srs)
        srs_transform = osr.CoordinateTransformation(src_layer_srs, target_srs)
        src_layer_config = layer_config[idx]
        layer_cols_assign = [ *src_layer_config.keys() ]
        print([*layer_config[idx].keys()])
        for feature_idx in range(src_layer.GetFeatureCount()):
            # print(feature_idx)
            src_feature = src_layer.GetNextFeature()
            feature = ogr.Feature(layer_defn)
            geom = src_feature.GetGeometryRef()
            if src_feature == None or geom == None:
                continue
            geom.Transform(srs_transform)
            # set row/feature field and geometry
            feature.SetField('project', layer_name)
            feature.SetField('latitude', geom.GetY())
            feature.SetField('longitude', geom.GetX())
            for col_name in layer_cols_assign:
                src_col_name = str(src_layer_config[col_name])
                src_col_value =\
                    src_feature.GetField(src_col_name)
                src_col_value = src_col_value if src_col_value else None
                # column conversion happens here
                if '_ppm' in col_name and src_col_value != None:
                    src_col_value = ppm_value(src_col_value)
                    if is_pct_column(src_col_name):
                        src_col_value *= 1e4
                    elif is_ppb_column(src_col_name):
                        src_col_value /= 1e3
                feature.SetField(col_name, src_col_value)
            feature.SetGeometry(geom)
            # add to layer
            layer.CreateFeature(feature)

ds.SyncToDisk()
