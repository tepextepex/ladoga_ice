import os
from datetime import datetime, timedelta
from earthdata_credentials import login, password

# name example: MOD10A2.A2000049.h31v11.006.2016064132703.hdf
# naming convention: MOD[PID].A[YYYY][DDD].h[NN]v[NN].[VVV].[yyyy][ddd][hhmmss].hdf
# tiles for Lake Ladoga: h19v02 and h19v03

target_dir = "MOD10A2/"

for year in (2020, ):
	start_date = datetime(year, 1, 1)  # year, month, day
	end_date = datetime(year, 12, 31)  # will stop at TODAY

	current_date = start_date  # TODO: validation of start_date. Note that leap years do exist!

	while current_date <= end_date and current_date <= datetime.today():
		url = "https://n5eil01u.ecs.nsidc.org/MOST/MOD10A2.006/%s/" % current_date.strftime("%Y.%m.%d")
		cmd = 'wget --no-parent -nd --http-user=%s --http-password=%s -A "*h19v0[2-3]*" --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -P %s %s' % (login, password, target_dir, url)
		try:
			os.system(cmd)
		except Exception as e:
			print e
		finally:
			current_date += timedelta(days=8)  # this is ok in a leap year, MODIS products do not have 29th Feb
