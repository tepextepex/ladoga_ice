# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import pandas as pd

data_dir = "/home/tepex/INOZ/LadogaIce/"

out_file = "/home/tepex/INOZ/LadogaIce/output.csv"  # will be created if does not exist

df = pd.read_csv("/home/tepex/INOZ/LadogaIce/stats_ladoga.csv")

# filtering cloudy days:
# df = df.loc[df["CLOUD_PX"] < 8750*2]  # roughly 20 percent of cloud cover
df = df.loc[df["CLOUD_PX"] < 8750]  # roughly 10 percent of cloud cover

ind_df = pd.read_csv("/home/tepex/INOZ/LadogaIce/indices.csv")

with open(out_file, "w") as f:
	f.write("YEAR_FROM,YEAR_TO,ICE_COVERAGE_SQ_KM*DAY,ANOMALY")

df["PERIOD"] = pd.to_datetime(df["PERIOD"], format="%Y%m%d")
ind_df["PERIOD"] = pd.to_datetime(ind_df["PERIOD"], format="%Y%m%d")

# df.loc[(df["PERIOD"].dt.month >= 5) & (df["PERIOD"].dt.month < 9), "ICE_PX"] = 0
# df.loc[(df["PERIOD"].dt.dayofyear >= 135) & (df["PERIOD"].dt.dayofyear < 244), "ICE_SQ_KM"] = 0
df.loc[(df["PERIOD"].dt.dayofyear >= 135) & (df["PERIOD"].dt.dayofyear < 305), "ICE_SQ_KM"] = 0

total_ice_for_all_seasons = 0

seasonal_ice = {}

for year in range(2001, 2021):
	try:
		# season_df = df.loc[(df["PERIOD"] > "%s-9-1" % (year - 1)) & (df["PERIOD"] < "%s-5-15" % (year))]
		season_df = df.loc[(df["PERIOD"] > "%s-9-1" % (year - 1)) & (df["PERIOD"] < "%s-11-01" % (year))]
		y = season_df["ICE_SQ_KM"].tolist()
		x = season_df["PERIOD"].dt.strftime("%j").astype(int).tolist()
		x = season_df["PERIOD"].dt.strftime("%j").astype(int)
		# x = x - 365
		x.loc[x > 240] -= 365
		x = x.tolist()
		total_seasonal_ice = np.trapz(y, x=x)
		seasonal_ice[year] = total_seasonal_ice
		total_ice_for_all_seasons += total_seasonal_ice
		print "Ice per season %s-%s: %0.f sq km" % (year-1, year, total_seasonal_ice)
	except Exception as e:
		print e 

# calculating anomalies of seasonal ice cover from average ice cover:
average_ice_per_season = total_ice_for_all_seasons / 17
print "Average: %0.f sq km" % average_ice_per_season

anomalies = {}
for year, value in seasonal_ice.iteritems():
	print "Anomaly for season %s-%s is %s" % (year - 1, year, value / average_ice_per_season - 1)
	anomalies[year] = value / average_ice_per_season - 1
	with open(out_file, "a") as f:
		f.write("\n%s,%s,%.0f,%.3f" % (year - 1, year, value, value / average_ice_per_season - 1))

# plotting anomalies and their linear trend line:
anomalies_df = pd.DataFrame.from_dict(anomalies, orient='index')

trend_coefs = np.polyfit(anomalies_df.index, anomalies_df[0], 1)

p = np.poly1d(trend_coefs)

anomalies_df = anomalies_df.sort_index()
plt.plot(anomalies_df.index, anomalies_df[0], 'g-', linewidth=1, label="Seasonal ice cover anomalies")
plt.plot(anomalies_df.index, p(anomalies_df.index), 'r-', linewidth=1, label="Trend line")
plt.ylim(-1, 1)
plt.legend(loc=3)
plt.xticks(np.arange(2000, 2021, 2))
plt.show()

# myFmt = mdates.DateFormatter("%m-%Y")
