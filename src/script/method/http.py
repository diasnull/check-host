import time
import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class http():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	"""
	{
		"us1.node.check-host.net": [[1, 0.13, "OK", "200", "94.242.206.94"]],
		"ch1.node.check-host.net": [[0, 0.17, "Not Found", "404", "94.242.206.94"]],
	} -> dict[list[int, str, float]]
	"""
	def _http_res_show(self, http_req: dict[str, dict[list[str]]], http_res: dict[list[int, str, float]]) -> pandas.DataFrame:
		d_for_df_list: list[dict[int, str, float]] = []
		for key, value in http_res.items():
			# "us1.node.check-host.net": [None, [{"message": ""}]]
			if not value[0]:
				d_for_df_list.append({
					"country": http_req["nodes"][key][1],
					"city": http_req["nodes"][key][2],
					"result": "-",
					"time": "-",
					"code": "-",
					"ip address": "-"
				})
			if value[0]:
				d_for_df_list.append({
						"country": http_req["nodes"][key][1],
						"city": http_req["nodes"][key][2],
						"result": value[0][2],
						"time": f"{round(value[0][1], 3)} s.",
						"code": value[0][3] if value[0][3] else "-",
						"ip address": value[0][4] if value[0][4] else "-"
					})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ch_get_result):
	{
		"us1.node.check-host.net": [[1, 0.13, "OK", "200", "94.242.206.94"]],
		"ch1.node.check-host.net": [[0, 0.17, "Not Found", "404", "94.242.206.94"]],
		"pt1.node.check-host.net": [[0, 0.07, "No such device or address", null, null]]
	} -> dict[list[int, str, float]]
	"""
	def _http_get_res(self, request_id: str, timeout: int = 30) -> dict[list[int, str, float]] | None:
		stime = time.time()
		while time.time() - stime < timeout:
			http_res: dict = self.reqapi_class.reqapi_ch_get_result(request_id)
			self.logs_class.logs_load_process_print()
			if all(http_res.get(key) is not None for key in http_res.keys()):
				return http_res
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
	def _http_get_req(self, target: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return self.reqapi_class.reqapi_ch_get_request(target, "http", max_nodes)


	def http_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("http", "info", "runned")
		http_req: dict[str, dict[list[str]]] = self._http_get_req(args.target, args.max_nodes)
		if http_req.get("request_id"):
			http_res: dict[list[int, str, float]] = self._http_get_res(http_req["request_id"])
			if not http_res:
				self.logs_class.logs_console_print("http", "info", "no 'http' result information, reached timeout")
			elif http_res: self.logs_class.logs_result_print(self._http_res_show(http_req, http_res))
		if not http_req.get("request_id"):
			self.logs_class.logs_console_print("http", "info", "no 'http' get information, reached api limit")
		self.logs_class.logs_console_print("http", "info", "ended")