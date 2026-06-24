import requests, json, sys, time

match_id = int(sys.argv[1])
selection_ids = int(sys.argv[2])
file_name = sys.argv[3]
bet_type = sys.argv[4] # Whether bet is live or not
file_name2 = sys.argv[5] # file for storing odd status

if 'true' in bet_type:
    bet_type = True
else:
    bet_type = False

headers = {
    'authority': 'sportapi.begmedia.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.betclic.fr',
    'referer': 'https://www.betclic.fr/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-client': '',
}

params = {
    'application': '2',
    'countrycode': 'fr',
    'language': 'fr',
    'sitecode': 'frfr',
}

json_data = {
    'combo_selections': [
        {
            'match_id': match_id,
            'is_live': bet_type,
            'selection_ids': [
                selection_ids,
            ],
            'is_from_mycombi': False,
        },
    ],
}


while True:
    with open(f'file_com/exit.txt', 'r') as f:
        if 'true' in f.readline():
            print("[+] Quiting odd updater")
            exit()


    while True:
        try:
            with open("file_com/latest_token.txt", "r") as f:
                latest_token = f.readline()
            headers['x-client'] = latest_token
            response = requests.post('https://sportapi.begmedia.com/api/pub/v4/selections', params=params, headers=headers, json=json_data)
            odd_data = json.loads(response.text)
            odd_data = str(odd_data["selections"][0]["odds"])
            status = json.loads(response.text)
            status = str(status["selections"][0]["status"])
        except:
            pass
        else:
            break

    with open(f"file_com/{file_name}", "w") as f:
        f.write(odd_data)
    with open(f"file_com/{file_name2}", "w") as f:
        f.write(status)

    time.sleep(0.7)
