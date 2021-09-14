import os

os.system('clear')

print('read col_config')

def get_file_config_content(filepath=None):
    file_configs = []
    if filepath == None:
        return

    with open(filepath) as f:
        content = f.read()
        file_configs = content.split('\n\n')
        f.close()

    file_configs = [item for item in file_configs if item != '']

    return file_configs

def read_config(filepath=None):
    file_configs = get_file_config_content(filepath)
    file_configs = [item for item in file_configs]

    FILES = []
    FILE_TABLE_TYPE = []
    LAYERS = []
    LAYER_CONFIG = []
    COLUMNS = []
    for txt_config in file_configs:
        config = txt_config.split('\n')

        # first line is tabel type
        # second line is source filepath
        table_type = config[0]
        config_path = config[1]
        # print(table_type, config_path, 'ye')

        # print('\nread layer config')
        layer_columns = iter(config[2:])
        # the rest is a pattern of layer_idx layer_name folowed by columns
        line = next(layer_columns, None)
        is_header = True
        col = {}
        layers = []
        while line != None:
            is_header = '=' not in line
            if is_header:
                layer_idx, layer_name = line.split(' ')
                layers.append(layer_name)
            else:
                g_col, ds_col = [item.strip() if item else None for item in line.split('=')]
                # print(g_col, ds_col)
                if g_col:
                    if g_col not in COLUMNS:
                        COLUMNS.append(g_col)
                    col[g_col] = ds_col

            line = next(layer_columns, None)
        LAYERS.append(layers)
        LAYER_CONFIG.append(col)
        FILE_TABLE_TYPE.append(table_type)
        FILES.append(config_path)
    #print(FILES)
    #print(LAYERS)
    #print(LAYER_CONFIG)
    #print(COLUMNS)
    if 'project' not in COLUMNS:
        COLUMNS.append('project')
    if 'latitude' not in COLUMNS:
        COLUMNS.append('latitude')
    if 'longitude' not in COLUMNS:
        COLUMNS.append('longitude')
    return FILES, LAYERS, LAYER_CONFIG, COLUMNS, FILE_TABLE_TYPE

# files, layers, layer_config, columns, table_type = read_config('col_config.txt')

# print(files, layers, layer_config, columns, table_type)
