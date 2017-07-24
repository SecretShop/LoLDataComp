import requests
import sqlite3
import os.path
import time
from appJar import gui
   
def main(): 

    # This is my Riot API Auth Key so that i can access their database
    APIKey = "RGAPI-b6b4b44d-3145-45cf-816f-2218f20948b2"
    # This will hold Summoner ID
    sum_ID = ""
    # This will hold Account ID
    act_ID = ""
    # This will hold your Region
    rgn = ""
    # This will hold the Champs Dictionary for reference
    champ_dict = {}
    #Declaring the Gui's outside for reference
    menu = gui()
    login = gui()

    
    # Grabs The Champ Id's and names so that other parts of the program can use this.
    # Returns a Dict named Champs for reference
    def requestChampData(rgn,APIKey):
        URL = "https://" + rgn + ".api.riotgames.com/lol/static-data/v3/champions?locale=en_US&tags=keys&dataById=true&api_key=" + APIKey
        conn = sqlite3.connect('Ranked_Data.db')
        c = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS CHAMPS
            (ID INT PRIMARY KEY     NOT NULL,
            NAME      STR     NOT NULL);''')
        response = requests.get(URL)
        response = response.json()
        for id,v in response['data'].items():
            name = v['name']
            conn.execute("INSERT OR REPLACE INTO CHAMPS (ID,NAME) \
                VALUES (?,?)",(id, name))
            champ_dict.update({id : name})
        conn.commit()
        conn.close()
        return champ_dict
    
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
        
    def viewRankedData(rgn, sum_ID, APIKey, sumName):
        # Check if ranked database has been created
        isData = os.path.isfile("Ranked_Data.db")
        if isData == False:
            error_msg = "NO DATABASE"
            return error_msg
        else:
            # Open a seperate Gui with Ranked data
            conn = sqlite3.connect('Ranked_Data.db')
            c = conn.cursor()
                
            showData = gui("{}'s Ranked Statistics".format(sumName))
            query_Temp = 'SELECT GAMEID, CHAMP, TIME FROM {}'.format(sumName)
            c.execute(query_Temp)
            stuff = c.fetchall()
            
            showData.setGeometry("500x500")
            showData.addScrolledTextArea("a1")
            for k in range(len(stuff)-1,0,-1):
                champName = stuff[k][1]
                query_Temp = "SELECT NAME FROM CHAMPS WHERE ID='{}'".format(champName)
                c.execute(query_Temp)
                champName = c.fetchone()[0]
                day = time.strftime('%m/%d/%Y %H:%M', time.gmtime(stuff[k][2]/1000.0))
                showData.setTextArea("a1","\n{})       {}        {}".format(day, stuff[k][0], champName))    
            showData.setTextArea("a1","\n   DATE PLAYED             GAME ID              CHAMP")
            showData.setTextArea("a1","Total games: {}".format(len(stuff)))
            conn.close()
            showData.go()
                
            
    def importRankedData(rgn, act_ID, APIKey, sumName):
        # Import all ranked data into database
        URL = "https://" + rgn + ".api.riotgames.com/lol/match/v3/matchlists/by-account/"+ act_ID + "?season=9&api_key=" + APIKey
        print(URL)
        ranked_data = requests.get(URL)
        ranked_data = ranked_data.json()
        conn = sqlite3.connect('Ranked_Data.db')
        c = conn.cursor()
        
        createTblQuery = "CREATE TABLE IF NOT EXISTS {} \
            (ID         INT     PRIMARY KEY, \
            GAMEID      INT     NOT NULL, \
            CHAMP       INT     NOT NULL, \
            QUEUE       INT     NOT NULL, \
            TIME        INT     NOT NULL);".format(sumName)
        conn.execute(createTblQuery)
        matches = ranked_data['matches']
        
        for k in range(len(matches),0,-1):
            list1 = matches.pop(0)
            # print("Game ID "+(str)(k)+": "+(str)(list1["gameId"]))
            gameId_Temp = list1["gameId"]
            champion_Temp = list1['champion']
            queue_Temp = list1['queue']
            time_Temp = list1['timestamp']
            query_Temp = "INSERT OR REPLACE INTO {} (ID,GAMEID,CHAMP,QUEUE,TIME) \
                VALUES (?,?,?,?,?)".format(sumName)
            conn.execute(query_Temp,(k,gameId_Temp, champion_Temp, queue_Temp,time_Temp))
                
        conn.commit()   
        print ("Table created successfully")      
        conn.close()
        error_msg = "Completed"
        return error_msg
            
        
    def ranked_Start(rgn, sum_ID, sumName, APIKey, sum_Rank):
        # This will be the Gui for ranked data
        # Get data then make gui
        ranked = gui("Ranked data for "+sumName)
        ranked.setPadding([20,2])
        ranked.addLabel("title", "Below is "+sumName+"'s ranked info")
        print(sum_Rank)
        # Seperate info
        for k in range(0,len(sum_Rank)):
            sum_Rank_Out = sum_Rank.pop(0)
            ranked.addLabel("mesA"+(str)(k), sum_Rank_Out['queueType']+": "+sum_Rank_Out['tier']+" "+sum_Rank_Out['rank'])
            ranked.addLabel("mesB"+(str)(k), "   Wins: "+(str)(sum_Rank_Out['wins'])+"   Losses: "+(str)(sum_Rank_Out['losses'])+"\n")
        
        # ranked.addLabel("mes3", "3v3: "+sum_Rank_Out2['tier']+" "+sum_Rank_Out2['rank'])
        #ranked.addLabel("mes4", "   Wins: "+(str)(sum_Rank_Out2['wins'])+"   Losses: "+(str)(sum_Rank_Out2['losses'])+"\n")
        ranked.go()
        
            
    def menu_Start(rgn, sum_ID, sumName, sum_lvl, act_ID):
        def menu_buttons(button):
            if button == "Start":
                # Grab the Action
                user_Action = menu.getOptionBox("Actions")
                # Determine which action to do now
                if user_Action == "Lookup Rank":
                    sum_Rank = requestSummonerRank(rgn,sum_ID,APIKey)
                    # Create Gui with info
                    ranked_Start(rgn, sum_ID, sumName, APIKey, sum_Rank)
                    
                elif user_Action == "View Ranked Data":
                    error_msg = viewRankedData(rgn, sum_ID, APIKey, sumName)
                    if error_msg == "NO DATABASE":
                        menu.setLabel("Error","Database has not been created")
                        menu.setLabelBg("Error","red")
                    else:
                        print("showing Ranked Data")
                elif user_Action == "Import Ranked Data":
                    error_msg = importRankedData(rgn, act_ID, APIKey, sumName)
                    if error_msg == "Completed":
                        menu.setLabel("Error","Ranked Info Updated!")
                        menu.setLabelBg("Error","green")
                    
                    
                
                
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
        menu.addLabelOptionBox("Actions",["Lookup Rank", "View Ranked Data", "Import Ranked Data"]) 
        menu.addButtons(["Start", "Exit", "Log Out"], menu_buttons)
        menu.addLabel("Error")
        # Check if Table Exists prior to user asking
        conn = sqlite3.connect('Ranked_Data.db')
        c = conn.cursor()
        query_Temp = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(sumName)
        c.execute(query_Temp)
        if len(c.fetchall())==0 :
            menu.setLabel("Error","Import Ranked Data")
            menu.setLabelBg("Error", "orange")
        else:
            menu.setLabel("Error","Summoner Data Exists")
            menu.setLabelBg("Error", "grey")
        conn.close()
        menu.go()
            
        
        
    def login_Start():
        def login_buttons(button):
            if button == "Quit":
                login.stop()  
            elif button == "Check":
                rgn = (str) (login.getOptionBox("Region"))
                sumName = (str) (login.getEntry("Summoner Name"))
                responseJSON  = requestSummonerData(rgn, sumName, APIKey)
                #Replace username without spaces
                sumName = sumName.replace(" ","")
                if "status" in responseJSON:
                    if responseJSON['status']['status_code'] == 403:
                        login.setLabel("Error","Please Update APIKey")
                        login.setLabelBg("Error","yellow")
                    if responseJSON['status']['status_code'] == 500:
                        login.setLabel("Error","Error with Riot 's Servers")
                        login.setLabelBg("Error","Orange")
                    elif responseJSON['status']['status_code'] == 404:
                        login.setLabel("Error","Summoner name could not be found")
                        login.setLabelBg("Error","red")
                else:
                    sum_ID = str(responseJSON['id'])
                    act_ID = str(responseJSON['accountId'])
                    sum_lvl = str(responseJSON['summonerLevel'])
                    # Champ Database will update every time you login to ensure it is up to date
                    champ_dict = requestChampData(rgn, APIKey)
                    # As long as data is correct, go to next screen and close out this this one   
                    login.stop()
                    menu_Start(rgn, sum_ID, sumName, sum_lvl, act_ID)
                
        #Creating the Gui        
        login = gui("Summoner Retrieval")
        login.setPadding([20,2])
        login.addLabel("title", "  Enter the Following to Login!  ")
        login.addLabelOptionBox("Region", ["na1","euw1", "eun1", "oc1"])
        login.addLabelEntry("Summoner Name")
        login.addButtons(["Check", "Quit"], login_buttons)
        # This is here in case an error with login occurs
        login.addEmptyLabel("Error")    
        login.go()  


    # This starts the user at the login Screen
    login_Start()
    
        
        
if __name__ == '__main__':
   main()
