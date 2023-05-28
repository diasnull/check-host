import time
import pandas
import datetime

from src.scripts.api_data import *
from src.scripts.loading_process import *


def dns_data_parser(result_data, data_frame_temp, id_key):
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
				a_record    = ", ".join(data_in_result_data["A"]) if data_in_result_data["A"] else "no A record"
				aaaa_record = ", ".join(data_in_result_data["AAAA"]) if data_in_result_data["AAAA"] else "no AAAA record"
				ttl         = time.gmtime(data_in_result_data["TTL"])
				data_frame_temp.loc[count] = [f"{country}, {city}", a_record, aaaa_record, time.strftime("%M m. %S s.", ttl)]
	# remove index // set index to ""
	data_frame_temp.index = [""] * len(data_frame_temp)
	return data_frame_temp


def dns_data_part(data_frame, id_key, index_count):
	# trigger // api_data --> id_key_part()
	if id_key == 0:
		return datetime.datetime.now().strftime("%H:%M:%S") + " { error } inf: reached API limit, wait a minute."
	result_data = result_data_part(id_key)
	for nod_location in result_data:
		if result_data[nod_location] == None:
			# next frame // index_frame
			index_count += 1
			print(loading_process_part(index_count), end="\r", flush=True)
			return dns_data_part(data_frame, id_key, index_count)
	# return final data frame // data_frame
	return dns_data_parser(result_data, data_frame, id_key)


def dns_part(args):
	data_frame = pandas.DataFrame(columns=["location", "A record", "AAAA record", "ttl"])
	# data frame display width limit // 150
	pandas.set_option("display.width", 150)
	target = args.target
	# index_count = index // index_frame
	index_count = 0
	id_key = id_key_part(target, "dns")
	print("{ info } DNS started at:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	print(dns_data_part(data_frame, id_key, index_count))
	print("{ info } DNS ended in:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))