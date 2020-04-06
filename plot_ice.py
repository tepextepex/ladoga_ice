# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

data_dir = "/home/tepex/INOZ/LadogaIce/"

df = pd.read_csv("/home/tepex/INOZ/LadogaIce/stats_ladoga.csv")
# filtering cloudy days:
# df = df.loc[df["CLOUD_PX"] < 8750*2]  # roughly 20 percent
df = df.loc[df["CLOUD_PX"] < 8750]  # roughly 10 percent

ind_df = pd.read_csv("/home/tepex/INOZ/LadogaIce/indices.csv")

print list(df)

df["PERIOD"] = pd.to_datetime(df["PERIOD"], format="%Y%m%d")
ind_df["PERIOD"] = pd.to_datetime(ind_df["PERIOD"], format="%Y%m%d")
# df.loc[(df["PERIOD"].dt.month >= 5) & (df["PERIOD"].dt.month < 9), "ICE_PX"] = 0
df.loc[(df["PERIOD"].dt.dayofyear >= 121) & (df["PERIOD"].dt.dayofyear < 305), "ICE_SQ_KM"] = 0

myFmt = mdates.DateFormatter("%m-%Y")
# plt.plot(df["PERIOD"], df["ICE_PX"], label="Lake Ice (px)")
twins = []
f, axarr = plt.subplots(4)
for i in range(0, 4):
	axarr[i].plot(df["PERIOD"], df["CLOUD_SQ_KM"], label="Clouds (sq km)")
	axarr[i].plot(df["PERIOD"], df["ICE_SQ_KM"], label="Lake ice (sq km)")
	# axarr[i].plot(df["PERIOD"], df["LAKE_PX"], label="Open water (px)")
	# twins.append(axarr[i].twinx())
	# twins[i].plot(ind_df["PERIOD"], ind_df["NAO"], 'g-', linewidth=1, label="NAO Index")
	left_year = 2000 + i * 5
	right_year = left_year + 5
	axarr[i].set_xlim(datetime.strptime("%d0601" % left_year, "%Y%m%d"),
					  datetime.strptime("%d0601" % right_year, "%Y%m%d"))
	axarr[i].xaxis.set_major_formatter(myFmt)
	axarr[i].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
	axarr[i].xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
	# axarr[i].set_ylabel("Area, sq km", fontsize=9)
	axarr[i].set_ylabel(u"Area, sq km", fontsize=7)
	for tick in axarr[i].xaxis.get_major_ticks():
		tick.label.set_fontsize(7)
		tick.label.set_rotation("vertical")

	# axarr[i].set_title("Lake Ice (MODIS)")

# plt.legend(loc=4)
# axarr[3].legend(loc=4)
# twins[2].legend(loc=1)
f.tight_layout()

plt.show()
