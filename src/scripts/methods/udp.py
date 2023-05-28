import pandas
import datetime

from src.scripts.api_data import *
from src.scripts.loading_process import *


def udp_data_parser(result_data, data_frame_temp, id_key):
	for count, nod_location in enumerate(result_data, start=0):
		# id key data // api_data --> id_key_part()
		country = id_key["nodes"][nod_location][1]
		city    = id_key["nodes"][nod_location][2]
		if result_data[nod_location] != None:
			# result data // api_data --> result_data_part()
			data_in_result_data = result_data[nod_location][0]
			if data_in_result_data == None:
				data_frame_temp.loc[count] = [f"{country}, {city}", "no data", "no data"]
			if data_in_result_data != None:
				if "address" not in data_in_result_data:
					data_frame_temp.loc[count] = [f"{country}, {city}", data_in_result_data["error"], "None"]
				if "address" in data_in_result_data:
					# result data // data_in_result_data
					reason     = "open or filtered"
					ip_address = data_in_result_data["address"]
					data_frame_temp.loc[count] = [f"{country}, {city}", reason, ip_address]
	# remove index // set index to ""
	data_frame_temp.index = [""] * len(data_frame_temp)
	return data_frame_temp


def udp_data_part(data_frame, id_key, index_count):
	# trigger // api_data --> id_key_part()
	if id_key == 0:
		return datetime.datetime.now().strftime("%H:%M:%S") + " { error } inf: reached API limit, wait a minute."
	result_data = result_data_part(id_key)
	for nod_location in result_data:
		if result_data[nod_location] == None:
			# next frame // index_frame
			index_count += 1
			print(loading_process_part(index_count), end="\r", flush=True)
			return udp_data_part(data_frame, id_key, index_count)
	# return final data frame // data_frame
	return udp_data_parser(result_data, data_frame, id_key)


def udp_part(args):
	data_frame = pandas.DataFrame(columns=["location", "reason", "IP address"])
	# data frame display width limit // 150
	pandas.set_option("display.width", 150)
	target = args.target
	# index_count = index // index_frame
	index_count = 0
	id_key = id_key_part(target, "udp")
	print("{ info } UDP started at:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	print(udp_data_part(data_frame, id_key, index_count))
	print("{ info } UDP ended in:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))