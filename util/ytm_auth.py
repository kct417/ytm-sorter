import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from util.ytm_log import setup_logger

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CREDENTIALS = "credentials/client_secret.json"
TOKEN = "credentials/token.json"

logger = setup_logger(__name__)


def authenticate_youtube():
    if not os.path.exists(TOKEN):
        raise RuntimeError("token.json not found. Generate it once locally.")

    try:
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

        # If expired, refresh silently
        if creds.expired:
            if creds.refresh_token:
                logger.info("Access token expired. Refreshing...")
                creds.refresh(Request())

                # Save updated token
                with open(TOKEN, "w") as token:
                    token.write(creds.to_json())
            else:
                raise RuntimeError("No refresh token available. Regenerate token.json.")

    except Exception as error:
        # If any error occurs, prompt for authentication
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
        creds = flow.run_local_server()

        with open(TOKEN, "w") as f:
            f.write(creds.to_json())

        logger.error(f"Authentication failed: {error}")
        raise

    youtube = build("youtube", "v3", credentials=creds)
    logger.info("YouTube authentication successful.")
    return youtube
