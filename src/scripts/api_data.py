import json
import requests


def id_key_part(target, method):
	id_key_req = json.loads(requests.get(f"https://check-host.net/check-{method}?host={target}", headers={"Accept": "application/json"}).text)
	return id_key_req


def result_data_part(id_key):
	result_data_req = json.loads(requests.get(f"https://check-host.net/check-result/" + id_key["request_id"]).text)
	return result_data_req