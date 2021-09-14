from pathlib import Path
from os import system
from osgeo import ogr

BLEG = 'BLEG'
ROCK = 'ROCK'
SOIL = 'SOIL'
SS = 'SS'

# list of input MiTAB files
TAB_FILES = [
    {
        'file': './INPUT.TAB',
        'table': BLEG,
    },
]

def _ye():
    datasource = ogr.Open(TAB_FILES[0]['file'])
    print(datasource.GetLayerCount())
    for layer_idx in range(datasource.GetLayerCount()):
        layer = datasource.GetLayer(layer_idx)
        layer_defn = layer.GetLayerDefn()
        layer_name = layer_defn.GetName()
        print(layer_idx, layer_name)
        field_name_list = [
            layer_defn.GetFieldDefn(layer_field_idx).GetName()
            for layer_field_idx in range(layer_defn.GetFieldCount())
        ]
        for feature_idx in range(layer.GetFeatureCount()):
            feature = layer.GetNextFeature()
            row = [
                feature.GetField(field_name)
                for field_name in field_name_list
            ]
            geom = feature.GetGeometryRef()
            print(row, geom.GetSpatialReference().GetName())
        print(field_name_list)
    print(datasource.GetName())
    print(datasource.GetSummaryRefCount())

def get_epsg():
    pass

def open_datasource(filepath, driver=None, **kwargs):
    _open_fun = None

    if driver:
        _open_fun = driver.Open
    else:
        _open_fun = ogr.Open

    return _open_fun(filepath)


def get_datasource_layers(datasource=None, **kwargs):
    if datasource == None:
        return
    layers = [
        datasource.GetLayer(layer_idx)
        for layer_idx in range(datasource.GetLayerCount())
    ]
    return layers

def get_layer_fields_list(layer=None, **kwargs):
    if layer == None:
        return
    layer_defn = layer.GetLayerDefn()
    field_name_list = [
        layer_defn.GetFieldDefn(layer_field_idx).GetName()
        for layer_field_idx in range(layer_defn.GetFieldCount())
    ]
    return field_name_list

# split 'LELE=' into ['LELE', '']
# b = [item.strip() for item in a.split('=')]
# split 'LELE=' into ['LELE']
# b = [item.strip() for item in a.split('=') if item != '']
# split 'LELE'
# b = [item.strip() if item else None for item in a.split('=')]

def main():
    system('clear')
    f = open("output.txt", "w")
    for FILE in TAB_FILES:
        filepath = str(Path(FILE['file']).resolve())
        filename = filepath.split('/')[-1]
        table_type = FILE['table']
        print(filename, table_type)
        datasource = open_datasource(filepath)
        layers = get_datasource_layers(datasource)
        f.write(table_type)
        f.write('\n')
        f.write(
            '{filepath}'.format(
                filepath=filepath,
            )
        )
        f.write('\n')
        for idx, layer in enumerate(layers):
            fields_list = get_layer_fields_list(layer)
            layer_name = layer.GetName()
            layer_srs = layer.GetSpatialRef()
            print(idx, 'layer_name =', layer_name, 'layer_srs =', layer_srs.GetName())
            f.write(
                '{layer_idx} {layer_name}'.format(
                    layer_idx=idx,
                    layer_name=layer_name,
                )
            )
            f.write('\n')
            print(filename, len(layers))
            print(fields_list)
            f.writelines(
                [
                    '=' + line + '\n'
                    for line in fields_list
                ]
            )
        f.write('\n')
        break
    f.close()

# _ye()
#main()
