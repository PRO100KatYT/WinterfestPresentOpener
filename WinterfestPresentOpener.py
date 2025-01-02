version = "1.0.4"
print(f"Winterfest Present Opener v{version} by PRO100KatYT\n")

try:
    import json
    import requests
    import os
    from datetime import datetime
    import threading
    import time
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.\n")
    exit()

# All links centralized in one place
class links:
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    presentList = "https://pastebin.com/raw/J9xa9MKg"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId=athena"
    tokenUrl = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token"
    deviceAuthUrl = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/deviceAuthorization"
    deviceAuthFetchUrl = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"

# Global variables
class vars:
    headers = accountId = displayName = deviceId = secret = ""
    presentsCount = presentsOpened = 0

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"Error: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Get the text from a request and check for errors.
def requestText(request, bCheckForErrors = True):
    requestText = json.loads(request.text)
    if (bCheckForErrors and ("errorMessage" in requestText)): customError(requestText['errorMessage'])
    return requestText

# Load or save login info to auth.json
def loadAuth():
    authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
    if os.path.exists(authPath):
        with open(authPath, "r") as authFile:
            return json.load(authFile)
    return None

def saveAuth(data):
    authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
    with open(authPath, "w") as authFile:
        json.dump(data, authFile, indent=2)

class Auth:
    @staticmethod
    def get_new_access_token(account_id, device_id, secret):
        headers = {
            "Authorization": "basic OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
        }

        body = {
            "grant_type": "device_auth",
            "account_id": account_id,
            "device_id": device_id,
            "secret": secret,
        }

        response = requests.post(links.tokenUrl, headers=headers, data=body)

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            customError("Failed to get a new access token.\n")

    @staticmethod
    def authenticate():
        # Check if auth.json exists and load credentials
        authData = loadAuth()
        if authData:
            vars.accountId = authData["accountId"]
            vars.displayName = authData["displayName"]
            vars.deviceId = authData["deviceId"]
            vars.secret = authData["secret"]
            access_token = Auth.get_new_access_token(vars.accountId, vars.deviceId, vars.secret)
            vars.headers = {
                "User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit",
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json",
                "X-EpicGames-Language": "en",
                "Accept-Language": "en",
            }
            print(f"Logged in as {vars.displayName}\n")
            return

        print("Starting the login process...\n")
        auth_placeholder = "basic OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
        
        # Step 1: Get client credentials
        client_response = session.post(
            links.tokenUrl,
            headers={"Authorization": auth_placeholder},
            data={"grant_type": "client_credentials"}
        )

        if client_response.status_code != 200:
            customError("Failed to fetch client credentials.\n")
        
        client_credentials = client_response.json()["access_token"]

        # Step 2: Get device authorization
        device_response = session.post(
            links.deviceAuthUrl,
            headers={"Authorization": f"Bearer {client_credentials}"},
            data={}
        )

        if device_response.status_code != 200:
            customError("Failed to fetch device authorization.\n")

        device_data = device_response.json()
        device_code = device_data["device_code"]
        verification_url = device_data["verification_uri_complete"]

        print(f"Please authorize the application by visiting the following URL:\n{verification_url}\n")
        print("Waiting for device code verification...\n")

        # Step 3: Poll for access token
        access_token = None
        while not access_token:
            time.sleep(5)  # Retry every 5 seconds
            token_response = session.post(
                links.tokenUrl,
                headers={"Authorization": auth_placeholder},
                data={"grant_type": "device_code", "device_code": device_code}
            )

            if token_response.status_code == 200:
                token_json = token_response.json()
                access_token = token_json["access_token"]
                vars.accountId = token_json["account_id"]
                vars.displayName = token_json["displayName"]
            elif token_response.status_code != 400:
                customError(f"Failed to fetch access token: {token_response.text}")

        # Step 4: Fetch device authentication info
        device_auth_response = session.post(
            links.deviceAuthFetchUrl.format(vars.accountId),
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if device_auth_response.status_code == 200:
            device_auth_data = device_auth_response.json()
            vars.deviceId = device_auth_data.get("deviceId")
            vars.secret = device_auth_data.get("secret")

            # Save login data and device auth info to auth.json
            saveAuth({
                "accountId": vars.accountId,
                "displayName": vars.displayName,
                "deviceId": vars.deviceId,
                "secret": vars.secret
            })

            print(f"Logged in as {vars.displayName} and device auth info saved.\n")
        else:
            customError("Failed to fetch device authentication info.\n")

        access_token = Auth.get_new_access_token(vars.accountId, vars.deviceId, vars.secret)
        vars.headers = {
            "User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit",
            "Authorization": f"bearer {access_token}",
            "Content-Type": "application/json",
            "X-EpicGames-Language": "en",
            "Accept-Language": "en",
        }

# Main program logic
def main():
    # Get the presents JSON and check if the event is live
    presentsJson = session.get(links.presentList).json()  # Ensure this fetches the present list
    date = datetime.now()
    if presentsJson["startTimestamp"] > date.timestamp():
        customError(presentsJson["beforeEventMessage"])
    if presentsJson["endTimestamp"] < date.timestamp():
        customError(presentsJson["afterEventMessage"])
    if presentsJson["alert"]:
        print(presentsJson["alert"])
    if presentsJson["error"]:
        customError(presentsJson["error"])

    Auth.authenticate()

    # Fetch the Winterfest event graph and process presents
    vars.presentsCount = len(presentsJson['presents'][0]) + len(presentsJson['presents'][1])

    print(f"Opening available Winterfest {presentsJson['year']} presents...\n")
    vars.presentsOpened = 0

    # Get the Winterfest event graph guid from the athena profile.
    rewardGraphId = ""
    reqGetAthena = requestText(session.post(links.profileRequest.format(vars.accountId, "ClientQuestLogin"), headers = vars.headers, data = "{}"))
    for item in reqGetAthena['profileChanges'][0]['profile']['items']:
        if reqGetAthena['profileChanges'][0]['profile']['items'][item]["templateId"].lower() == presentsJson["rewardGraphTemplateId"].lower(): rewardGraphId = item
    if not rewardGraphId: customError(f"Could not find the Winterfest Reward Graph on {vars.displayName}'s account. ({presentsJson['rewardGraphTemplateId']})")

    def openPresent(node):
        session.post(links.profileRequest.format(vars.accountId, "UnlockRewardNode"), headers=vars.headers,json={"nodeId": node, "rewardGraphId": rewardGraphId})
        vars.presentsOpened += 1
        print(f"Progress: {round((vars.presentsOpened / vars.presentsCount) * 100)}%")

    threads = [threading.Thread(target=openPresent, args=(node,)) for node in presentsJson["presents"][0]]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for node in presentsJson["presents"][1]:
        openPresent(node)

    print(f"\nSuccessfully opened all available Winterfest {presentsJson['year']} presents as {vars.displayName}!\n")

# Start the program
if __name__ == "__main__":
    main()

input("Press ENTER to close the program.\n")
exit()
