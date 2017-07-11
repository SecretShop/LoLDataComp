#This tutorial was built by me, Farzain! You can ask me questions or troll me on Twitter (@farzatv)

#First we need to import requests. Installing this is a bit tricky. I included a step by step process on how to get requests in readme.txt which is included in the file along with this program.
import requests
from appJar import gui

def requestSummonerData(region, summonerName, APIKey):

    #Here is how I make my URL.  There are many ways to create these.
    
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    print (URL)
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    #Here I return the JSON we just got.
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    print (URL)
    response = requests.get(URL)
    return response.json()
    
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        sumName = app.getEntry("SummonerName")
        Rgn = app.getEntry("Region")
        print("Name: ", sumName, "Region: ", Rgn)
    
    
def main():

    # Create a Gui
    app = gui()
    # App labels and stuffs
    app.addLabel("title", "League of Lag")
    # Entry stuff
    app.addLabelEntry("Region")
    app.addLabelEntry("SummonerName")
    app.addButtons(["Submit", "Cancel"], press)
    # Start the Gui
    app.go()
	
    #defining my Auth Key so i don't have to paste it.
    APIKey = "RGAPI-2552283f-0ed5-4cbd-acea-8cbad0ed02af"
	
	
    print ("\nEnter your region to get started (NA or EU)")
    print ("Type in one of the following regions or else the program wont work correctly:\n")
	

    #I first ask the user for three things, their region, summoner name, and API Key.
    #These are the only three things I need from them in order to get create my URL and grab their ID.

    region = (str)(input('Type in one of the regions above: '))
    summonerName = (str)(input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))

    #I send these three pieces off to my requestData function which will create the URL and give me back a JSON that has the ID for that specific summoner.
    #Once again, what requestData returns is a JSON.
    responseJSON  = requestSummonerData(region, summonerName, APIKey)
    
    ID = responseJSON[summonerName]['id']
    ID = str(ID)
    print (ID)
    responseJSON2 = requestRankedData(region, ID, APIKey)
    print (responseJSON2[ID][0]['tier'])
    print (responseJSON2[ID][0]['entries'][0]['division'])
    print (responseJSON2[ID][0]['entries'][0]['leaguePoints'])

#This starts my program!
if __name__ == "__main__":
    main()

