from os import getenv, path, system
from osgeo import ogr
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

system('clear')

load_dotenv()

POSTGRES_HOST=getenv('POSTGRES_HOST')
POSTGRES_PORT=getenv('POSTGRES_PORT')
POSTGRES_USER=getenv('POSTGRES_USER')
POSTGRES_PASS=getenv('POSTGRES_PASS')
POSTGRES_DB=getenv('POSTGRES_DB')
POSTGIS_DATABASE = "postgres://{}:{}@{}:{}/{}".format(POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)

def db_conn():
    return connect(POSTGIS_DATABASE)

def get_conn_cursor():
    conn = db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur_nondict = conn.cursor()
    return conn, cur, cur_nondict

# read sqlite
# read layers
# get available column in each layers
# QUESTIN: do we entirely copy geometry from file source,
#   or is it entirely dependable to input x-y since we have trigger
#   or both?
# get database connection
# remove where project = layer_name
def le():
    le_data = None
    conn, cur, _ = get_conn_cursor()
    try:
        cur.execute('SELECT NOW()')
    except Exception as exc:
        print(exc)
    else:
        print('success')
        le_data = cur.fetchall()
    finally:
        conn.close()
    print(le_data)

def get_g_datasource(filepath=None):
    if filepath == None:
        return None

    if not path.exists(filepath):
        return None

    datasource = ogr.Open(filepath)
    return datasource

# TODO test seed in local geofix table, then update remote table
def get_row_query(layer_name, field_name_list, *args):
    table_map = {
        'BLEG': 'geofix.surface_bleg',
        'SOIL': 'geofix.surface_soil',
        'ROCK': 'geofix.surface_rock',
        'SS': 'geofix.surface_ss',
    }

    query = """
INSERT INTO {table_name} (
{rows_str}
) VALUES ({vals})
    """.format(
        table_name=table_map[layer_name],
        #table_name='public.le_surface_ss',
        rows_str=',\n'.join(field_name_list),
        vals=','.join(['%s' for _ in field_name_list]),
    )
    return query

def execute_row(query=None, values=None, **kwargs):
    try:
        conn, cur, _ = get_conn_cursor()
        cur.execute(query, values)
    except Exception as exc:
        print(exc)
        conn.rollback()
    else:
        conn.commit()
    finally:
        conn.close()

ds = get_g_datasource('lombok.sqlite')
for layer_idx in range(ds.GetLayerCount()):
    layer = ds.GetLayer(layer_idx)
    layer_name = str(layer.GetName()).upper()
    layer_defn = layer.GetLayerDefn()
    field_name_list = [
        layer_defn.GetFieldDefn(layer_field_idx).GetName()
        for layer_field_idx in range(layer_defn.GetFieldCount())
    ]
    print(layer_name, layer.GetFeatureCount())
    # print(field_name_list)
    query = get_row_query(layer_name, field_name_list)
    print(field_name_list)
    for feature_idx in range(layer.GetFeatureCount()):
        feature = layer.GetNextFeature()
        feature_values = [
            feature.GetField(field_name)
            for field_name in field_name_list
        ]
        # print(feature_values)
        execute_row(query, feature_values)

print('success')
