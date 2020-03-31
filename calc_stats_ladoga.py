import glob
from modis_utils import *
from datetime import datetime, timedelta
# MOD10A2.A2000049.h31v11.006.2016064132703.hdf
# MOD[PID].A[YYYY][DDD].h[NN]v[NN].[VVV].[yyyy][ddd][hhmmss].hdf
# for Lake Ladoga: h19v02 and h19v03

target_dir = "/home/tepex/INOZ/LadogaIce/MOD10A2/"
vector_mask = "/home/tepex/INOZ/LadogaIce/shp/modis_ladoga_mask_wo_rings.shp"
out_csv_file = "/home/tepex/INOZ/LadogaIce/stats_Ladoga_2019.csv"

for year in (2020, ):
	start_date = datetime(year, 1, 1)
	end_date = datetime(year, 12, 31)

	current_date = start_date
	print "Processing %s" % current_date.strftime("%j")
	while current_date <= end_date and current_date <= datetime.today():
		try:
			pattern = os.path.join(target_dir, "MOD10A2.A%s%s*.hdf" % (current_date.strftime("%Y"), current_date.strftime("%j")))
			tile_list = glob.glob(pattern)

			tif_tile_list = []

			for tile in tile_list:
				tif_tile = convert_hdf_subdataset_into_gtiff(tile)
				tif_tile_list.append(tif_tile)

			merged = merge_gtiff_tiles(tif_tile_list)
			for tif_tile in tif_tile_list:
				os.remove(tif_tile)

			cropped_tif = crop(merged, vector_mask)
			print cropped_tif

			calc_stats(cropped_tif, out_csv_file)

			os.remove(merged)

		except Exception as e:
			print e
			
		finally:
			current_date += timedelta(days=8)
