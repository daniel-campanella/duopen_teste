import requests
import json


CLIENT_ID = "76485c65-4541-4fef-9124-0c0f6a3da8e8"
CLIENT_SECRET = "7249a568-bf7a-450e-af59-8415049bed9d"
ITEM_ID = "b4d709eb-0c3b-4bf2-a9c4-137f4451ef97"


def createAPIKey():
	url = "https://api.pluggy.ai/auth"
	payload = {
	    "clientId": CLIENT_ID,
	    "clientSecret": CLIENT_SECRET
	}
	headers = {
	    "accept": "application/json",
	    "content-type": "application/json"
	}
	response = requests.post(url, json=payload, headers=headers)
	if response.status_code == 200:	
		try:
			data = json.loads(response.text)
			api_key = data["apiKey"]
		except Exception:
			api_key = None
	else:
		api_key = None
	return api_key


def createConnectToken(APIKey):
	url = "https://api.pluggy.ai/connect_token"
	payload = { "itemId": ITEM_ID }
	headers = {
	    "accept": "application/json",
	    "content-type": "application/json",
	    "X-API-KEY": APIKey
	}
	response = requests.post(url, json=payload, headers=headers)
	if response.status_code == 200:	
		try:
			data = json.loads(response.text)
			accessToken = data["accessToken"]
		except Exception:
			accessToken = None
	else:
		accessToken = None
	return accessToken


def retrieveItem(APIKey):
	url = f"https://api.pluggy.ai/items/{ITEM_ID}"
	headers = {
	    "accept": "application/json",
	    "X-API-KEY": APIKey
	}
	response = requests.get(url, headers=headers)


def listAccounts(APIKey):
	url = f"https://api.pluggy.ai/accounts?itemId={ITEM_ID}"
	headers = {
	    "accept": "application/json",
	    "X-API-KEY": APIKey
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:	
		try:
			data = json.loads(response.text)
			accounts = data["results"]
		except Exception:
			accounts = None
	else:
		accounts = None
	return accounts


def listTransactions(APIKey, Account_ID):
	url = f"https://api.pluggy.ai/transactions?accountId={Account_ID}"
	headers = {
	    "accept": "application/json",
	    "X-API-KEY": APIKey
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:	
		try:
			data = json.loads(response.text)
			transactions = data["results"]
		except Exception:
			transactions = None
	else:
		transactions = None
	return transactions

