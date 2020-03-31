import os
import os.path
from datetime import datetime
import gdal
import numpy as np


def convert_hdf_subdataset_into_gtiff(tile):
	ds = gdal.Open(tile)
	subds = gdal.Open(ds.GetSubDatasets()[0][0])
	subds_array = subds.ReadAsArray()

	out_path = "%s.tif" % tile[:-4]

	out_ds = gdal.GetDriverByName("GTiff").Create(out_path,
		subds.RasterXSize,
		subds.RasterYSize,
		1,
		gdal.GDT_Byte)
	out_ds.SetGeoTransform(subds.GetGeoTransform())
	out_ds.SetProjection(subds.GetProjection())
	out_ds.GetRasterBand(1).WriteArray(subds_array)
	out_ds.GetRasterBand(1).SetNoDataValue(0)

	out_ds = None

	return out_path


def merge_gtiff_tiles(tile_list):
	dirname = os.path.dirname(tile_list[0])
	basename = "%s.%s.tif" % (tile_list[0].split(".")[0], tile_list[0].split(".")[1])
	merged = os.path.join(dirname, basename)
	input_files = " ".join(tile_list)
	cmd = 'gdal_merge.py -o %s %s' % (merged, input_files)
	os.system(cmd)
	return merged


def merge_hdf_tiles(tile_list):
	dirname = os.path.dirname(tile_list[0])
	target_name = os.path.join(dirname, "example.vrt")
	gdal.BuildVRT(target_name, tile_list)

	print target_name

	return target_name


def crop(input_tif, vector_cutline, suffix=None):

	if suffix is None:
		suffix = "Ladoga"

	output_tif = "%s.%s.tif" % (input_tif[:-4], suffix)
	cmd = 'gdalwarp -overwrite -dstnodata 0 -co COMPRESS=DEFLATE -crop_to_cutline -cutline %s %s %s' % (vector_cutline, input_tif, output_tif)
	os.system(cmd)
	return output_tif


def calc_stats(input_tif, csv_output_file):
	
	result = False

	modis_cell_area = 0.2146587  # SQ KM

	period_string = os.path.basename(input_tif).split(".")[1][1:]
	period = datetime.strptime(period_string, "%Y%j")
	period = period.strftime("%Y%m%d")
	
	dataset = gdal.Open(input_tif)
	band = dataset.GetRasterBand(1)
	array = band.ReadAsArray()
	
	lake_px = np.count_nonzero(array == 37)
	lake_sq_km = lake_px * modis_cell_area
	
	ice_px = np.count_nonzero(array == 100)
	ice_sq_km = ice_px * modis_cell_area
	
	cloud_px = np.count_nonzero(array == 50)
	cloud_sq_km = cloud_px * modis_cell_area

	try:
		with open(csv_output_file, "a") as csv:
			new_string = "\n%s,%d,%.2f,%d,%.2f,%d,%.2f" % (period, lake_px, lake_sq_km, ice_px, ice_sq_km, cloud_px, cloud_sq_km)
			csv.write(new_string)
		result = True
	except Exception as e:
		print e
	finally:
		return result

