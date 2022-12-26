version = "1.0.0"
print(f"Winterfest Present Opener v{version} by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from datetime import datetime
    import webbrowser
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId=34a02cf8f4414e29b15921876da36f9a&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D34a02cf8f4414e29b15921876da36f9a%2526responseType%253Dcode"
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    presentList = "https://pastebin.com/raw/J9xa9MKg"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId=athena"

# Global variables
class vars: accessToken = displayName = headers = accountId = ""

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"Error: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Loop input until the response is one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if response in values: break
        response = input("You provided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request, bCheckForErrors = True):
    requestText = json.loads(request.text)
    if (bCheckForErrors and ("errorMessage" in requestText)): customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqTokenText(loginLink, altLoginLink, authHeader):
    count = 0
    while True:
        count += 1
        if count > 1: loginLink = altLoginLink
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didn't open it, copy this link to your browser: {(loginLink)}\n")
        reqToken = json.loads(session.post(links.getOAuth.format("token"), headers={"Authorization": f"basic {authHeader}"}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")}).text)
        if not "errorMessage" in reqToken: break
        else: input(f"\n{reqToken['errorMessage']}.\nPress ENTER to open the website again and get the code.\n")
    return reqToken

# Authentication
def auth():
    # Create and/or read the auth.json file.
    authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
    if not os.path.exists(authPath):
        isLoggedIn = validInput("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
        input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
        if isLoggedIn == "1": loginLink = links.loginLink1
        else: loginLink = links.loginLink2
        reqToken = reqTokenText(loginLink, links.loginLink1, "MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=")
        refreshToken, vars.accountId, expirationDate = [reqToken["refresh_token"], reqToken["account_id"], reqToken["refresh_expires_at"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": vars.accountId, "refresh_expires_at": expirationDate}, authFile, indent = 2)
        print("\nThe auth.json file was generated successfully.\n")

    # Log in to an account.
    authJson = json.loads(open(authPath, "r").read())
    expirationDate, refreshToken = [authJson["refresh_expires_at"], authJson["refreshToken"]]
    if expirationDate < datetime.now().isoformat(): customError("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one. If this problem persists try to log in using the device auth type.")
    vars.accountId = authJson["accountId"]
    reqRefreshToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), True)
    with open(authPath, "r") as getAuthFile: authFile = json.loads(getAuthFile.read())
    authFile['refreshToken'], authFile['refresh_expires_at'] = [reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]]
    with open(authPath, "w") as getAuthFile: json.dump(authFile, getAuthFile, indent = 2)
    reqExchange = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
    reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
    vars.accessToken, vars.displayName = [reqToken['access_token'], reqToken['displayName']]
    vars.headers = {"User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit", "Authorization": f"bearer {vars.accessToken}", "Content-Type": "application/json", "X-EpicGames-Language": "en", "Accept-Language": "en", "X-EpicGames-ProfileRevisions": json.dumps([{"profileId":"athena","clientCommandRevision":-1}])}
    print(f"Logged in as {vars.displayName}.\n")

# The main part of the program
def main():
    # Get the presents json and check if the event is currently live.
    presentsJson = requestText(session.get(links.presentList))
    if not presentsJson: customError("Could not get to the presents json information.")
    date = datetime.now()
    if presentsJson["startTimestamp"] > date.timestamp(): customError(presentsJson["beforeEventMessage"])
    if presentsJson["endTimestamp"] < date.timestamp(): customError(presentsJson["afterEventMessage"])
    if presentsJson["alert"]: print(presentsJson["alert"])
    if presentsJson["error"]: customError(presentsJson["error"])
    
    auth()

    profileRevision = 0 
    
    # Get the Winterfest event graph guid from the athena profile.
    rewardGraphId = ""
    reqGetAthena = requestText(session.post(links.profileRequest.format(vars.accountId, "ClientQuestLogin"), headers = vars.headers, data = "{}"))
    profileRevision = reqGetAthena['profileCommandRevision']
    for item in reqGetAthena['profileChanges'][0]['profile']['items']:
        if reqGetAthena['profileChanges'][0]['profile']['items'][item]["templateId"].lower() == presentsJson["rewardGraphTemplateId"]: rewardGraphId = item
    if not rewardGraphId: customError(f"Could not find the Winterfest Reward Graph on {vars.displayName}'s account. ({presentsJson['rewardGraphTemplateId']})")

    # Open Winterfest presents.
    print("Opening available Winterfest presents...\n")
    for node in presentsJson["presents"]:
        vars.headers["X-EpicGames-ProfileRevisions"] = json.dumps([{"profileId":"athena","clientCommandRevision":profileRevision}])
        reqOpenPresent = requestText(session.post(links.profileRequest.format(vars.accountId, "UnlockRewardNode"), headers = vars.headers, json = {"nodeId": node, "rewardGraphId": rewardGraphId}))
        profileRevision = reqOpenPresent['profileCommandRevision']
        print(f"Progress: {round(presentsJson['presents'].index(node)/len(presentsJson['presents'])*100)}%")

    print(f"Progress: 100%\n\nSuccessfully opened all currently available Winterfest {presentsJson['year']} presents as {vars.displayName}!\n")

# Start the program
if __name__ == "__main__": main()

input("Press ENTER to close the program.\n")
exit()