from os import system
from pathlib import Path

from compile_fieldname_list import get_datasource_layers, open_datasource,\
    get_layer_fields_list, TAB_FILES

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
        print(idx, layer_name)
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
f.close()
