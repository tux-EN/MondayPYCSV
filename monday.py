import requests as rq 
import pandas as pd 
import json
import os

#Monday board exporter by Joshua Gest
#This is a rough script that will export a board from monday.com using their API v2 and dump it to a CSV File.


#Declare Constants
apiKey = input("Please Input your Monday.com v2 API Key: ")
apiURL = "https://api.monday.com/v2"
apiVer = "2024-01" #need to update query to newest API
headers = {"Authorization" : apiKey,"API-Version" : apiVer}
path = './export/' #this can be changed to any path you like

#Defines post query to monday API
#Current query lacks Pagination(500 item limit) and does not pull mirror columns(can do this with newest API)
query = '{boards(ids: INSERT BOARD ID HERE ) {items_page (limit: 500) {items {name column_values {column { title} text}}}}}' #Input your board ID where it says
data = {'query' : query}
print("Querying Monday API V2 please wait...")
#Execute GraphQL query and defines the output as jsonData.
try:
    r = rq.post(url=apiURL, json=data, headers=headers)
    jsonData = r.json()
except rq.exceptions.RequestException as e:
    print(e)
    quit() #Kills program if postquery failes for any reason
print("Query successful...")

#Intialize Dictionary
print("Initalizing dictionary...")
itm=jsonData['data']['boards'][0]['items_page']['items']


# Initialize an empty DataFrame
print("Creating dataframe...")
dfColumns = ["Store"]  # Columns for the DataFrame
dfData = []

# loop through items and extract data from the trainwreck JSON export that monday spits out
for item in itm:
    rowData = {
        "Store": item["name"]
    }
    for columnValue in item["column_values"]:
        columnTitle = columnValue["column"]["title"]
        text = columnValue["text"]
        rowData[columnTitle] = text
    dfData.append(rowData)

# Create the dataframe using the cleaned up data.
df = pd.DataFrame(dfData)
print("Dataframe created sucessfully....")


#Checks if export directory exists and creates it if not
print("Checking if export directory exists...")
if os.path.isdir(path):
    print("Export directory exists... proceeding...")
else:
    print("Export directory is not present... Creating directory...")
    os.makedirs(path)
    print("Directory created....")



# Export Data Frame to comma delim CSV file
print("Exporting Dataframe to CSV")
df.to_csv('./export/export.csv', sep=',', encoding='utf-8', index=False)
print("Saved to export.csv inside export directory")
#Below function will print the dataframe to the console. it will be a mess. you will need to comment the above 3 lines and uncomment the below line.
#print(df)