import os
import os.path as osp
import glob
import shutil
import requests
import socket

try:
    from tile_convert import bbox_to_xyz, tile_edges
except ImportError:  # for import
    from .tile_convert import bbox_to_xyz, tile_edges

try:
    import gdal
except ImportError:
    from osgeo import gdal


def fetch_tile(x, y, z, tile_source, tmp_dir):
    url = tile_source.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f"{tmp_dir}/{x}_{y}_{z}.png"
    # print(url)
    try:
        pic = requests.get(url)
        with open(path, "wb") as f:
            f.write(pic.content)
            f.flush()
        return path
    except Exception as e:
        print(e)
        return None


def merge_tiles(input_pattern, output_path):
    # merge_command = ["gdal_merge.py", "-o", output_path]
    merge_command = []
    for name in glob.glob(input_pattern):
        merge_command.append(name)
    # subprocess.call(merge_command)
    gdal.Warp(output_path, merge_command, options="COMPRESS=LZW")


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, _ = os.path.splitext(path)
    gdal.Translate(filename + ".tif",
                   path,
                   outputSRS="EPSG:4326",
                   outputBounds=bounds)
                   
                   
def get_raster_from_titles(ranges, save_path, token, zoom=18, tmp_dir=None):
    # setting
    timeout = 20
    socket.setdefaulttimeout(timeout)
    tile_source = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + \
                  token
    # starting
    if tmp_dir is None:
        tmp_dir = os.path.join(os.path.dirname(__file__), "temp")
        print(f"Temp dir: {tmp_dir}.")
        if not osp.exists(tmp_dir):
            os.makedirs(tmp_dir)
    lon_min = ranges["lon_min"]
    lon_max = ranges["lon_max"]
    lat_min = ranges["lat_min"]
    lat_max = ranges["lat_max"]
    x_min, x_max, y_min, y_max = bbox_to_xyz(
        lon_min, lon_max, lat_min, lat_max, zoom)
    print(f"Fetching {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles.")
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            png_path = fetch_tile(x, y, zoom, tile_source, tmp_dir)
            if png_path is not None:
                georeference_raster_tile(x, y, zoom, png_path)
                print(f"{x},{y} fetched.")
    print("Fetching of tiles complete.")
    print("Merging tiles.")
    merge_tiles(tmp_dir + "/*.tif", save_path)
    print("Merge complete.")
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    ranges = {"lon_min": 21.49547,
              "lon_max": 21.5,
              "lat_min": 65.31016,
              "lat_max": 65.31188}
    save_path = os.path.join(os.path.dirname(__file__), "test.tif")
    get_raster_from_titles(ranges, save_path, os.environ["Mapbox_token"])
