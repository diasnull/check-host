import json
import requests


class reqapi():
	def __init__(self):
		super(reqapi, self).__init__()


	def reqapi_ia_get_result(self, target: str) -> dict[str, int, float]:
		return json.loads(requests.get(f"http://ip-api.com/json/{target}").text)
	

	def reqapi_ch_post_request(self, target: str) -> str:
		return requests.post("https://check-host.net/ip-info/whois", data={"host": target}).text
	

	def reqapi_ch_get_request(self, target: str, method: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return json.loads(requests.get(f"https://check-host.net/check-{method}?host={target}&max_nodes={max_nodes}",
								headers={"Accept": "application/json"}).text)


	def reqapi_ch_get_result(self, request_id: int) -> dict:
		return json.loads(requests.get(f"https://check-host.net/check-result/{request_id}").text)