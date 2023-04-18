import json
import time
from aiohttp import BodyPartReader
from lcu_driver import Connector

connector = Connector()

@connector.ready
async def connect(conn):
    summoner_name = input("Nick: ")
    summoner = await conn.request('get', f"/lol-summoner/v1/summoners?name={summoner_name}")
    summoner = await summoner.json()
    try:
        summoner_id = summoner['accountId']
        summoner_puid = summoner['puuid']
    except:
        print(summoner)
        print("Summoner not found")
        exit(0)
    response = await conn.request('get', f"/lol-match-history/v1/products/lol/{summoner_puid}/matches")
    response = await response.json()
    game_id = response['games']['games'][1]['gameId']
    while True:
        report_data = {
            "comment": "he literally trolls the game, how is he even allowed to play",
            "gameId": game_id,
            "offenses": "Negative Attitude, Verbal Abuse, Intentional Feeding",
            "reportedSummonerId": summoner_id
        }
        response = await conn.request('post', "/lol-end-of-game/v2/player-complaints", data=report_data)
        response = await response.json()
        try:
            if response['httpStatus'] == 403:
                print(f"failed to report {summoner_name}")
            else:
                print(f"Player {summoner_name} is reported.")
        except:
            print(f"Player {summoner_name} is reported.")
        wait_time = 60 * 60 + 1
        for i in range(wait_time):
            print("\033c", end="")
            time.sleep(1)
            print(f"\n\nWaiting 1 hours...: {i // 60} min {i % 60} sec")

connector.start()
