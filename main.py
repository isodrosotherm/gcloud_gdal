# app.py
from flask import Flask, request, jsonify
import os 
from osgeo import gdal

gdal.UseExceptions()
gdal.SetConfigOption('CPL_CURL_VERBOSE', 'YES')
gdal.SetConfigOption('CPL_DEBUG', 'YES')
gdal.SetConfigOption('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', '.TIF')

def get_pixel_value_from_raster(lat, lon):
    ds = gdal.Open('/vsigs/era_test_bucket/wind_gust_kts_00z_model_run_000hr_anl_valid_00Z.tif')
    gt = ds.GetGeoTransform()
    rb = ds.GetRasterBand(1)

    lat = float(lat)
    lon = float(lon)

    if (lat < gt[3] and lat > (gt[4] - gt[3]) and
        lon > gt[0] and lon < (gt[2] - gt[0])):
        
        px = int((lon-gt[0])/gt[1])
        py = int((lat-gt[3])/gt[5])

        intval = rb.ReadAsArray(px, py, 1, 1)

    return str(intval)


app = Flask(__name__)

@app.route('/api')
def api_id():
    lat = (request.args['lat'])
    lon = (request.args['lon'])
    result = get_pixel_value_from_raster(lat, lon)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
