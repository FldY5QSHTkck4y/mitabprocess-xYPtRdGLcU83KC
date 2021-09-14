from osgeo import ogr

STRING = ogr.OFTString
REAL = ogr.OFTReal
DATETIME = ogr.OFTDateTime

column_map = {
    'latitude': REAL,
    'longitude': REAL,
    'sample_type': STRING,
    'sample_id': STRING,
    'utm_east': REAL,
    'utm_north': REAL,
    'elevation': REAL,
    'collectiondate': STRING, # need to test DATETIME first
    'geologist': STRING,
    'description': STRING,
    'locality': STRING,
    'ag_ppm': REAL,
    'al_ppm': REAL,
    'as_ppm': REAL,
    'au_ppm': REAL,
    'au1_ppm': REAL,
    'au2_ppm': REAL,
    'au3_ppm': REAL,
    'au4_ppm': REAL,
    'ba_ppm': REAL,
    'be_ppm': REAL,
    'bi_ppm': REAL,
    'c_ppm': REAL,
    'cu_ppm': REAL,
    'fe_ppm': REAL,
    'hg_ppm': REAL,
    'mn_ppm': REAL,
    'mo_ppm': REAL,
    'pb_ppm': REAL,
    's_ppm': REAL,
    'sb_ppm': REAL,
    'se_ppm': REAL,
    'sn_ppm': REAL,
    'te_ppm': REAL,
    'zn_ppm': REAL,
    'project': STRING,
}
