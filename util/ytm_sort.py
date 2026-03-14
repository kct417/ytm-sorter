from copy import deepcopy

from util.ytm_log import setup_logger

logger = setup_logger(__name__)


def get_playlists(youtube):
    playlists = []
    next_page_token = None
    while True:
        try:
            result = (
                youtube
                    .playlists()
                    .list(
                        part="snippet",
                        mine=True,
                        maxResults=50,
                        pageToken=next_page_token
                    )
                    .execute()
            )
        except Exception as error:
            logger.error(f"Failed to fetch playlists: {error}")
            break

        playlists.extend(result["items"])
        next_page_token = result.get("nextPageToken")
        if not next_page_token:
            break
    return playlists


def get_playlist_items(youtube, playlist_id):
    items = []
    next_page_token = None
    while True:
        try:
            result = (
                youtube
                    .playlistItems()
                    .list(
                        part="snippet",
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=next_page_token,
                    )
                    .execute()
            )
        except Exception as error:
            logger.error(f"Failed to fetch items for playlist {playlist_id}: {error}")
            break

        items.extend(result["items"])
        next_page_token = result.get("nextPageToken")
        if not next_page_token:
            break
    return items


def sort_playlist_by_artist(items):
    def sort_key(item):
        artist = (
            item["snippet"]["videoOwnerChannelTitle"] or item["snippet"]["channelTitle"]
        )
        title = item["snippet"]["title"]

        if artist == item["snippet"]["channelTitle"]:
            logger.warning(
                f"Missing artist for item '{title}', using channel title instead."
            )

        return (artist.lower(), title.lower())

    return sorted(items, key=sort_key)


def sort_playlist_by_title(items):
    def sort_key(item):
        title = item["snippet"]["title"]
        return title.lower()

    return sorted(items, key=sort_key)


def reorder_playlist_items(youtube, playlist_id, sort_function):
    playlist_items = get_playlist_items(youtube, playlist_id)
    sorted_items = sort_function(playlist_items)

    if all(
        playlist_items[i]["id"] == sorted_items[i]["id"]
        for i in range(len(playlist_items))
    ):
        logger.info("Playlist is already sorted. Skipping.")
        return

    for i, sorted_item in enumerate(sorted_items):
        current_item = playlist_items[i]
        if sorted_item["id"] != current_item["id"]:
            try:
                # Find the original index of the item to be moved
                original_index = next(
                    i
                    for i, item in enumerate(playlist_items)
                    if item["id"] == sorted_item["id"]
                )
            except StopIteration:
                logger.error(
                    f"Could not find item ID {sorted_item['id']} in current playlist."
                )
                break

            # Create a new snippet with the updated position
            snippet = deepcopy(sorted_item["snippet"])
            snippet["position"] = i

            try:
                youtube.playlistItems().update(
                    part="snippet", body={"id": sorted_item["id"], "snippet": snippet}
                ).execute()
            except Exception as error:
                logger.error(
                    f"Failed to update item '{snippet['title']}' to position {i}: {error}"
                )
                break

            try:
                moved_item = playlist_items.pop(original_index)
                playlist_items.insert(i, moved_item)
            except Exception as error:
                logger.error(
                    f"Failed to reorder local list after moving item '{snippet['title']}': {error}"
                )
                break

            logger.info(f"{i + 1}. Moved '{snippet['title']}' to position {i}")


def sort_playlist(youtube, playlist, sort_function=sort_playlist_by_artist):
    playlist_id = playlist["id"]
    title = playlist["snippet"]["title"]
    logger.info(f"{title} (ID: {playlist_id})")

    try:
        reorder_playlist_items(youtube, playlist_id, sort_function)
    except Exception as error:
        logger.error(f"Error sorting playlist {playlist_id}: {error}")


def sort_all_playlists(youtube, playlists, sort_function=sort_playlist_by_artist):
    logger.info(f"Found {len(playlists)} playlists.")

    for playlist in playlists:
        sort_playlist(youtube, playlist, sort_function)

    logger.info(f"Finished sorting all playlists.")


def display_items(youtube, playlist):
    playlist_id = playlist["id"]
    items = get_playlist_items(youtube, playlist_id)
    if not items:
        logger.info(f"No items found in playlist {playlist['snippet']['title']}.")
        return

    logger.info(f"Items in playlist {playlist['snippet']['title']}:")
    for item in items:
        title = item["snippet"]["title"]
        artist = (
            item["snippet"]["videoOwnerChannelTitle"] or item["snippet"]["channelTitle"]
        )
        logger.info(f"{title} by {artist} (ID: {item['id']})")
