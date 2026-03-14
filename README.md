# Setting Up OAuth Client ID for Desktop App

TODO: Add detailed instructions with screenshots.

-   https://console.cloud.google.com/
-   APIs & Services -> Credentials
-   Create Credentials -> OAuth client ID
-   Desktop App

# Setup Python Environment

## Windows

```
setup.bat
```

## macOS/Linux

```
./setup.sh
```

# Usage

```
python main.py
```

# Limitations

-   Quota limits from YouTube Data API v3 apply.
-   Must have "Manage your YouTube account" permission for playlists.
-   Must have a Google Console project with YouTube Data API v3 enabled.
-   If running on remote server, ensure proper credential setup locally and securely transfer credentials to server.
