import requests
from appJar import gui
   
def main(): 

    # This is my Riot API Auth Key so that i can access their database
    APIKey = "RGAPI-ef4a41fb-c325-4274-b3f9-38f680140986"
    # This will hold User ID
    Sum_ID = ""
    # This will hold your Region
    rgn = ""
    #Declaring the Gui's outside for reference
    menu = gui()
    login = gui()

    # This grabs Summoner info from Riot Servers
    def requestSummonerData(rgn, sumName, APIKey): 
        # These are the URL's to fetch data
        URL = "https://" + rgn + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + sumName + "?api_key=" + APIKey
        print (URL)
        # Goes to URl and fetches JSON
        response = requests.get(URL)
        # Returns back the JSON we just got.
        print (response.json())
        return response.json()

    def requestSummonerRank(rgn, sum_ID, APIKey):
        # Fetch ranked data
        URL =  "https://" + rgn + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + sum_ID + "?api_key=" + APIKey
        print(URL)
        response = requests.get(URL)
        print (response.json())
        return response.json()
        
        
    def ranked_Start(rgn, sum_ID, sumName, APIKey, sum_Rank_Out1, sum_Rank_Out2):
        # This will be the Gui for ranked data
        # Get data then make gui
        ranked = gui("Ranked data for "+sumName)
        ranked.setPadding([20,2])
        # Seperate info
        ranked.addLabel("title", "Below is "+sumName+"'s ranked info")
        ranked.addLabel("mes1", "5v5: "+sum_Rank_Out1['tier']+" "+sum_Rank_Out1['rank'])
        ranked.addLabel("mes2", "   Wins: "+(str)(sum_Rank_Out1['wins'])+"   Losses: "+(str)(sum_Rank_Out1['losses'])+"\n")
        ranked.addLabel("mes3", "3v3: "+sum_Rank_Out2['tier']+" "+sum_Rank_Out2['rank'])
        ranked.addLabel("mes4", "   Wins: "+(str)(sum_Rank_Out2['wins'])+"   Losses: "+(str)(sum_Rank_Out2['losses'])+"\n")
        ranked.go()
        
            
    def menu_Start(rgn, sum_ID, sumName, sum_lvl):
        def menu_buttons(button):
            if button == "Start":
                # Grab the Action
                user_Action = menu.getOptionBox("Actions")
                # Determine which action to do now
                if user_Action == "Lookup Rank":
                    sum_Rank = requestSummonerRank(rgn,sum_ID,APIKey)
                    sum_Rank_Out1 = sum_Rank.pop(0)
                    sum_Rank_Out2 = sum_Rank.pop(0)
                    # Create Gui with info
                    ranked_Start(rgn, sum_ID, sumName, APIKey, sum_Rank_Out1, sum_Rank_Out2)
                    
                
                
            elif button == "Exit":
                # Exit out of the entire program
                menu.stop()
            elif button == "Log Out":
                # Return user to Login Screen
                menu.stop() 
                login_Start()
                
        
        # Making the Gui
        menu = gui("Data for "+sumName)
        menu.setPadding([20,2])
        # Print the Summoner basic info to Menu box
        menu.addLabel("log-l1", "Summoner Name: "+sumName)
        menu.addLabel("log-l2", "Summoner ID: "+sum_ID)
        menu.addLabel("log-l3", "Summoner Lvl: "+sum_lvl)
        menu.addLabel("log-l4", "Choose an Action")
        menu.addLabelOptionBox("Actions",["Lookup Rank", "Check Data", "Import Data"]) 
        menu.addButtons(["Start", "Exit", "Log Out"], menu_buttons)
        menu.go()
        
        
    def login_Start():
        def login_buttons(button):
            if button == "Cancel":
                login.stop()  
            elif button == "Check":
                rgn = (str) (login.getOptionBox("Region"))
                sumName = (str) (login.getEntry("Summoner Name"))
                responseJSON  = requestSummonerData(rgn, sumName, APIKey)
                #Replace username without spaces
                sumName = sumName.replace(" ","")
                if "status" in responseJSON:
                    login.setLabel("Error","Summoner name could not be found")
                    login.setLabelBg("Error","red")
                else:
                    sum_ID = str(responseJSON['id'])
                    sum_lvl = str(responseJSON['summonerLevel'])
                    # As long as data is correct, go to next screen and close out this this one   
                    login.stop()
                    menu_Start(rgn, sum_ID, sumName, sum_lvl)
                
        #Creating the Gui        
        login = gui("Summoner Retrieval")
        login.setPadding([20,2])
        login.addLabel("title", "  Enter the Following to Login!  ")
        login.addLabelOptionBox("Region", ["na1","euw1", "eun1", "oc1"])
        login.addLabelEntry("Summoner Name")
        login.addButtons(["Check", "Cancel"], login_buttons)
        # This is here in case an error with login occurs
        login.addEmptyLabel("Error")    
        login.go()  


    # This starts the user at the login Screen
    login_Start()
    
        
        
if __name__ == '__main__':
   main()
