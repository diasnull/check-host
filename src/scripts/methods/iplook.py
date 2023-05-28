import json
import pandas
import datetime
import requests


def iplook_data(target, data_frame):
	# ip lookup // 45 requests per minute from an IP address
	iplook_req = json.loads(requests.get(f"http://ip-api.com/json/{target}").text)
	if iplook_req["status"] == "success":
		for count, title_of_data in enumerate(iplook_req, start=0):
			data_frame.loc[count] = [title_of_data, iplook_req[title_of_data]]
		# remove index // set index to ""
		data_frame.index = [""] * len(data_frame)
		return data_frame
	return datetime.datetime.now().strftime("%H:%M:%S") + " { error } inf: invalid target."


def iplook_part(args):
	data_frame = pandas.DataFrame(columns=["title", "data"])
	# data frame display width limit // 150
	pandas.set_option("display.width", 150)
	target = args.target
	print("{ info } IP address lookup started at:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	print(iplook_data(target, data_frame))
	print("{ info } IP address lookup ended in:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))