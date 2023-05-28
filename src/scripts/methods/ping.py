import pandas
import datetime

from src.scripts.api_data import *
from src.scripts.loading_process import *


def ping_data_parser(result_data, data_frame_temp, id_key):
	for count, nod_location in enumerate(result_data, start=0):
		# id key data // api_data --> id_key_part()
		country = id_key["nodes"][nod_location][1]
		city    = id_key["nodes"][nod_location][2]
		if result_data[nod_location] != None:
			# result data // api_data --> result_data_part()
			data_in_result_data = result_data[nod_location][0]
			if data_in_result_data == None:
				data_frame_temp.loc[count] = [f"{country}, {city}", "no data", "no data", "no data"]
			if data_in_result_data != None:
				# result data // data_in_result_data
				time_1, time_2, time_3, time_4 = round(data_in_result_data[0][1] * 1000, 2), \
				                                 round(data_in_result_data[1][1] * 1000, 2), \
				                                 round(data_in_result_data[2][1] * 1000, 2), \
				                                 round(data_in_result_data[3][1] * 1000, 2)
				code_1, code_2, code_3, code_4 = data_in_result_data[0][0], \
				                                 data_in_result_data[1][0], \
				                                 data_in_result_data[2][0], \
				                                 data_in_result_data[3][0]
				ip_address = data_in_result_data[0][2]
				data_frame_temp.loc[count] = [f"{country}, {city}", f"{time_1}/{time_2}/{time_3}/{time_4} ms.", f"{code_1}/{code_2}/{code_3}/{code_4}", ip_address]
	# remove index // set index to ""
	data_frame_temp.index = [""] * len(data_frame_temp)
	return data_frame_temp


def ping_data_part(data_frame, id_key, index_count):
	# trigger // api_data --> id_key_part()
	if id_key == 0:
		return datetime.datetime.now().strftime("%H:%M:%S") + " { error } inf: reached API limit, wait a minute."
	result_data = result_data_part(id_key)
	for nod_location in result_data:
		if result_data[nod_location] == None:
			# next frame // index_frame
			index_count += 1
			print(loading_process_part(index_count), end="\r", flush=True)
			return ping_data_part(data_frame, id_key, index_count)
	# return final data frame // data_frame
	return ping_data_parser(result_data, data_frame, id_key)


def ping_part(args):
	data_frame = pandas.DataFrame(columns=["location", "time", "code", "IP address"])
	# data frame display width limit // 150
	pandas.set_option("display.width", 150)
	target = args.target
	# index_count = index // index_frame
	index_count = 0
	id_key = id_key_part(target, "ping")
	print("{ info } PING started at:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	print(ping_data_part(data_frame, id_key, index_count))
	print("{ info } PING ended in:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))