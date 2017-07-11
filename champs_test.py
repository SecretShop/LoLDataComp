import sqlite3
import requests

URL = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/37952182?season=8&api_key=RGAPI-be1dbe4c-f01a-4ecb-b133-c7875512dd1b"
test = requests.get(URL)
test = test.json()
# print (test)

conn = sqlite3.connect('champs2.db')
print ("Opened database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS RANKED
    (ID INT PRIMARY KEY     NOT NULL,
    GAMEID      INT     NOT NULL,
    CHAMP       INT     NOT NULL,
    QUEUE       INT);''')

matches = test['matches']
print("Start of Game ID List\n")
for k in range(len(matches),0,-1):
    list1 = matches.pop(0)
    print("Game ID "+(str)(k)+": "+(str)(list1["gameId"]))
    gameId_Temp = list1["gameId"]
    champion_Temp = list1['champion']
    queue_Temp = list1['queue']
    conn.execute("INSERT OR REPLACE INTO RANKED (ID,GAMEID,CHAMP,QUEUE) \
        VALUES (?,?,?,?)",(k, gameId_Temp, champion_Temp, queue_Temp))
        
conn.commit()   
print ("Table created successfully")      
print("\n That is all!")
conn.close()
