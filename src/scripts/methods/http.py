import pandas
import datetime

from src.scripts.api_data import *
from src.scripts.loading_process import *


def http_data_parser(result_data, data_frame_temp, id_key):
	for count, nod_location in enumerate(result_data, start=0):
		# id key data // api_data --> id_key_part()
		country = id_key["nodes"][nod_location][1]
		city    = id_key["nodes"][nod_location][2]
		if result_data[nod_location] != None:
			# result data // api_data --> result_data_part()
			data_in_result_data = result_data[nod_location][0]
			if data_in_result_data == None:
				data_frame_temp.loc[count] = [f"{country}, {city}", "no data", "no data", "no data", "no data"]
			if data_in_result_data != None:
				# result data // data_in_result_data
				time       = round(data_in_result_data[1], 3)
				reason     = data_in_result_data[2]
				code       = data_in_result_data[3]
				ip_address = data_in_result_data[4]
				data_frame_temp.loc[count] = [f"{country}, {city}", f"{time} s.", reason, code, ip_address]
	# remove index // set index to ""
	data_frame_temp.index = [""] * len(data_frame_temp)
	return data_frame_temp


def http_data_part(data_frame, id_key, index_count):
	# trigger // api_data --> id_key_part()
	if id_key == 0:
		return datetime.datetime.now().strftime("%H:%M:%S") + " { error } inf: reached API limit, wait a minute."
	result_data = result_data_part(id_key)
	for nod_location in result_data:
		if result_data[nod_location] == None:
			# next frame // index_frame
			index_count += 1
			print(loading_process_part(index_count), end="\r", flush=True)
			return http_data_part(data_frame, id_key, index_count)
	# return final data frame // data_frame
	return http_data_parser(result_data, data_frame, id_key)


def http_part(args):
	data_frame = pandas.DataFrame(columns=["location", "time", "reason", "code", "IP address"])
	# data frame display width limit // 150
	pandas.set_option("display.width", 150)
	target = args.target
	# index_count = index // index_frame
	index_count = 0
	id_key = id_key_part(target, "http")
	print("{ info } HTTP started at:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	print(http_data_part(data_frame, id_key, index_count))
	print("{ info } HTTP ended in:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))