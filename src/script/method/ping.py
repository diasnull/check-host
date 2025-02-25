import time
import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class ping():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	"""
	"us1.node.check-host.net": [[
		["OK", 0.044, "94.242.206.94"],
		["OK", 0.005], 
		["OK", 0.045],
		["OK", 0.0433]
	]] -> dict[list[str, float]]
	"""
	def _ping_res_show(self, ping_req: dict[str, dict[list[str]]], ping_res: dict[list[str, float]]) -> pandas.DataFrame:
		d_for_df_list: list[dict[str, float]] = []
		for key, value in ping_res.items():
			# "us1.node.check-host.net": [None, [{"message": ""}]] -> if value[0] else "-"
			res_list: list[str] | str = [1 for item in value[0] if item[0] == "OK"] if value[0] else "-"
			rtt_list: list[float] | str = [item[1] * 1000 for item in value[0]] if value[0] else "-"
			res_count: int | str = round(sum(res_list), 3) if value[0] else "-"
			min_res: float | str = round(min(rtt_list), 3) if value[0] else "-"
			avg_res: float | str = round(sum(rtt_list) / len(rtt_list), 3) if value[0] else "-"
			max_res: float | str = round(max(rtt_list), 3) if value[0] else "-"
			d_for_df_list.append({
					"country": ping_req["nodes"][key][1],
					"city": ping_req["nodes"][key][2],
					"result": f"{res_count}/4",
					"rtt min / avg / max": f"{min_res} / {avg_res} / {max_res} ms",
					"ip address": value[0][0][2] if value[0] else "-"
				})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ch_get_result):
	{
		"us1.node.check-host.net": [[
			["OK", 0.044, "94.242.206.94"],
			["TIMEOUT", 3.005],
			["MALFORMED", 0.045],
			["OK", 0.0433]
		]],
		"ch1.node.check-host.net": [[null]],
		"pt1.node.check-host.net": null
	} -> dict[list[str, float]]
	"""
	def _ping_get_res(self, request_id: str, timeout: int = 30) -> dict[list[str, float]] | None:
		stime = time.time()
		while time.time() - stime < timeout:
			ping_res: dict = self.reqapi_class.reqapi_ch_get_result(request_id)
			self.logs_class.logs_load_process_print()
			if all(ping_res.get(key) is not None for key in ping_res.keys()):
				return ping_res
		return None
	

	"""
	example of response (reqapi_ch_get_request):
	{
		"ok":             1,
		"request_id":     "29",
		"permanent_link": "https://check-host.net/check-report/29",
		"nodes": {
			"us1.node.check-host.net": ["us", "USA", "Los Angeles", "5.253.30.82", "AS18978"],
		}
	} -> dict[str, dict[list[str]]]
	"""
	def _ping_get_req(self, target: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return self.reqapi_class.reqapi_ch_get_request(target, "ping", max_nodes)


	def ping_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("ping", "info", "runned")
		ping_req: dict[str, dict[list[str]]] = self._ping_get_req(args.target, args.max_nodes)
		if ping_req.get("request_id"):
			ping_res: dict[list[str, float]] = self._ping_get_res(ping_req["request_id"])
			if not ping_res:
				self.logs_class.logs_console_print("ping", "info", "no 'ping' result information, reached timeout")
			elif ping_res: self.logs_class.logs_result_print(self._ping_res_show(ping_req, ping_res))
		elif not ping_req.get("request_id"):
			self.logs_class.logs_console_print("ping", "info", "no 'ping' get information, reached api limit")
		self.logs_class.logs_console_print("ping", "info", "ended")