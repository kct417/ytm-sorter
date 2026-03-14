from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CREDENTIALS = "credentials/client_secret.json"

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS,
        SCOPES
    )

    creds = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent"
    )

    with open("credentials/token.json", "w") as f:
        f.write(creds.to_json())

def main():
    generate_token()

if __name__ == "__main__":
    main()
