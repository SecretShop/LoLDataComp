from appJar import gui
# import requests
# URL = "https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/23777784?api_key=RGAPI-2552283f-0ed5-4cbd-acea-8cbad0ed02af"
# test = requests.get(URL)
# test = test.json()
# print (test)
# list1 = test.pop(0)
# print(list1)
# list2 = test.pop(0)
# print(list2)

test = gui("test")
test.setGeometry("300x300")
test.setSticky("news")
test.setExpand("both")
test.addLabel("t1","this is gonna be line one\n This is gonna be line 2\n")
test.addHorizontalSeparator(colour="black")
test.go()


