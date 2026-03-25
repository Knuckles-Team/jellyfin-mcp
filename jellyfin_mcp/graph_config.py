"""Jellyfin graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

# ── Tag → System Prompt Mapping ──────────────────────────────────────
TAG_PROMPTS: dict[str, str] = {
    "ActivityLog": (
        "You are a Jellyfin Activitylog specialist. Help users manage and interact with Activitylog functionality using the available tools."
    ),
    "ApiKey": (
        "You are a Jellyfin Apikey specialist. Help users manage and interact with Apikey functionality using the available tools."
    ),
    "Artists": (
        "You are a Jellyfin Artists specialist. Help users manage and interact with Artists functionality using the available tools."
    ),
    "Audio": (
        "You are a Jellyfin Audio specialist. Help users manage and interact with Audio functionality using the available tools."
    ),
    "Backup": (
        "You are a Jellyfin Backup specialist. Help users manage and interact with Backup functionality using the available tools."
    ),
    "Branding": (
        "You are a Jellyfin Branding specialist. Help users manage and interact with Branding functionality using the available tools."
    ),
    "Channels": (
        "You are a Jellyfin Channels specialist. Help users manage and interact with Channels functionality using the available tools."
    ),
    "ClientLog": (
        "You are a Jellyfin Clientlog specialist. Help users manage and interact with Clientlog functionality using the available tools."
    ),
    "Collection": (
        "You are a Jellyfin Collection specialist. Help users manage and interact with Collection functionality using the available tools."
    ),
    "Configuration": (
        "You are a Jellyfin Configuration specialist. Help users manage and interact with Configuration functionality using the available tools."
    ),
    "Dashboard": (
        "You are a Jellyfin Dashboard specialist. Help users manage and interact with Dashboard functionality using the available tools."
    ),
    "Devices": (
        "You are a Jellyfin Devices specialist. Help users manage and interact with Devices functionality using the available tools."
    ),
    "DisplayPreferences": (
        "You are a Jellyfin Displaypreferences specialist. Help users manage and interact with Displaypreferences functionality using the available tools."
    ),
    "DynamicHls": (
        "You are a Jellyfin Dynamichls specialist. Help users manage and interact with Dynamichls functionality using the available tools."
    ),
    "Environment": (
        "You are a Jellyfin Environment specialist. Help users manage and interact with Environment functionality using the available tools."
    ),
    "Filter": (
        "You are a Jellyfin Filter specialist. Help users manage and interact with Filter functionality using the available tools."
    ),
    "Genres": (
        "You are a Jellyfin Genres specialist. Help users manage and interact with Genres functionality using the available tools."
    ),
    "HlsSegment": (
        "You are a Jellyfin Hlssegment specialist. Help users manage and interact with Hlssegment functionality using the available tools."
    ),
    "Image": (
        "You are a Jellyfin Image specialist. Help users manage and interact with Image functionality using the available tools."
    ),
    "InstantMix": (
        "You are a Jellyfin Instantmix specialist. Help users manage and interact with Instantmix functionality using the available tools."
    ),
    "ItemLookup": (
        "You are a Jellyfin Itemlookup specialist. Help users manage and interact with Itemlookup functionality using the available tools."
    ),
    "ItemRefresh": (
        "You are a Jellyfin Itemrefresh specialist. Help users manage and interact with Itemrefresh functionality using the available tools."
    ),
    "ItemUpdate": (
        "You are a Jellyfin Itemupdate specialist. Help users manage and interact with Itemupdate functionality using the available tools."
    ),
    "Items": (
        "You are a Jellyfin Items specialist. Help users manage and interact with Items functionality using the available tools."
    ),
    "Library": (
        "You are a Jellyfin Library specialist. Help users manage and interact with Library functionality using the available tools."
    ),
    "LibraryStructure": (
        "You are a Jellyfin Librarystructure specialist. Help users manage and interact with Librarystructure functionality using the available tools."
    ),
    "LiveTv": (
        "You are a Jellyfin Livetv specialist. Help users manage and interact with Livetv functionality using the available tools."
    ),
    "Localization": (
        "You are a Jellyfin Localization specialist. Help users manage and interact with Localization functionality using the available tools."
    ),
    "Lyrics": (
        "You are a Jellyfin Lyrics specialist. Help users manage and interact with Lyrics functionality using the available tools."
    ),
    "MediaInfo": (
        "You are a Jellyfin Mediainfo specialist. Help users manage and interact with Mediainfo functionality using the available tools."
    ),
    "MediaSegments": (
        "You are a Jellyfin Mediasegments specialist. Help users manage and interact with Mediasegments functionality using the available tools."
    ),
    "Movies": (
        "You are a Jellyfin Movies specialist. Help users manage and interact with Movies functionality using the available tools."
    ),
    "MusicGenres": (
        "You are a Jellyfin Musicgenres specialist. Help users manage and interact with Musicgenres functionality using the available tools."
    ),
    "Package": (
        "You are a Jellyfin Package specialist. Help users manage and interact with Package functionality using the available tools."
    ),
    "Persons": (
        "You are a Jellyfin Persons specialist. Help users manage and interact with Persons functionality using the available tools."
    ),
    "Playlists": (
        "You are a Jellyfin Playlists specialist. Help users manage and interact with Playlists functionality using the available tools."
    ),
    "Playstate": (
        "You are a Jellyfin Playstate specialist. Help users manage and interact with Playstate functionality using the available tools."
    ),
    "Plugins": (
        "You are a Jellyfin Plugins specialist. Help users manage and interact with Plugins functionality using the available tools."
    ),
    "QuickConnect": (
        "You are a Jellyfin Quickconnect specialist. Help users manage and interact with Quickconnect functionality using the available tools."
    ),
    "RemoteImage": (
        "You are a Jellyfin Remoteimage specialist. Help users manage and interact with Remoteimage functionality using the available tools."
    ),
    "ScheduledTasks": (
        "You are a Jellyfin Scheduledtasks specialist. Help users manage and interact with Scheduledtasks functionality using the available tools."
    ),
    "Search": (
        "You are a Jellyfin Search specialist. Help users manage and interact with Search functionality using the available tools."
    ),
    "Session": (
        "You are a Jellyfin Session specialist. Help users manage and interact with Session functionality using the available tools."
    ),
    "Startup": (
        "You are a Jellyfin Startup specialist. Help users manage and interact with Startup functionality using the available tools."
    ),
    "Studios": (
        "You are a Jellyfin Studios specialist. Help users manage and interact with Studios functionality using the available tools."
    ),
    "Subtitle": (
        "You are a Jellyfin Subtitle specialist. Help users manage and interact with Subtitle functionality using the available tools."
    ),
    "Suggestions": (
        "You are a Jellyfin Suggestions specialist. Help users manage and interact with Suggestions functionality using the available tools."
    ),
    "SyncPlay": (
        "You are a Jellyfin Syncplay specialist. Help users manage and interact with Syncplay functionality using the available tools."
    ),
    "System": (
        "You are a Jellyfin System specialist. Help users manage and interact with System functionality using the available tools."
    ),
    "TimeSync": (
        "You are a Jellyfin Timesync specialist. Help users manage and interact with Timesync functionality using the available tools."
    ),
    "Tmdb": (
        "You are a Jellyfin Tmdb specialist. Help users manage and interact with Tmdb functionality using the available tools."
    ),
    "Trailers": (
        "You are a Jellyfin Trailers specialist. Help users manage and interact with Trailers functionality using the available tools."
    ),
    "Trickplay": (
        "You are a Jellyfin Trickplay specialist. Help users manage and interact with Trickplay functionality using the available tools."
    ),
    "TvShows": (
        "You are a Jellyfin Tvshows specialist. Help users manage and interact with Tvshows functionality using the available tools."
    ),
    "UniversalAudio": (
        "You are a Jellyfin Universalaudio specialist. Help users manage and interact with Universalaudio functionality using the available tools."
    ),
    "User": (
        "You are a Jellyfin User specialist. Help users manage and interact with User functionality using the available tools."
    ),
    "UserLibrary": (
        "You are a Jellyfin Userlibrary specialist. Help users manage and interact with Userlibrary functionality using the available tools."
    ),
    "UserViews": (
        "You are a Jellyfin Userviews specialist. Help users manage and interact with Userviews functionality using the available tools."
    ),
    "VideoAttachments": (
        "You are a Jellyfin Videoattachments specialist. Help users manage and interact with Videoattachments functionality using the available tools."
    ),
    "Videos": (
        "You are a Jellyfin Videos specialist. Help users manage and interact with Videos functionality using the available tools."
    ),
    "Years": (
        "You are a Jellyfin Years specialist. Help users manage and interact with Years functionality using the available tools."
    ),
}


# ── Tag → Environment Variable Mapping ────────────────────────────────
TAG_ENV_VARS: dict[str, str] = {
    "ActivityLog": "ACTIVITYLOGTOOL",
    "ApiKey": "APIKEYTOOL",
    "Artists": "ARTISTSTOOL",
    "Audio": "AUDIOTOOL",
    "Backup": "BACKUPTOOL",
    "Branding": "BRANDINGTOOL",
    "Channels": "CHANNELSTOOL",
    "ClientLog": "CLIENTLOGTOOL",
    "Collection": "COLLECTIONTOOL",
    "Configuration": "CONFIGURATIONTOOL",
    "Dashboard": "DASHBOARDTOOL",
    "Devices": "DEVICESTOOL",
    "DisplayPreferences": "DISPLAYPREFERENCESTOOL",
    "DynamicHls": "DYNAMICHLSTOOL",
    "Environment": "ENVIRONMENTTOOL",
    "Filter": "FILTERTOOL",
    "Genres": "GENRESTOOL",
    "HlsSegment": "HLSSEGMENTTOOL",
    "Image": "IMAGETOOL",
    "InstantMix": "INSTANTMIXTOOL",
    "ItemLookup": "ITEMLOOKUPTOOL",
    "ItemRefresh": "ITEMREFRESHTOOL",
    "ItemUpdate": "ITEMUPDATETOOL",
    "Items": "ITEMSTOOL",
    "Library": "LIBRARYTOOL",
    "LibraryStructure": "LIBRARYSTRUCTURETOOL",
    "LiveTv": "LIVETVTOOL",
    "Localization": "LOCALIZATIONTOOL",
    "Lyrics": "LYRICSTOOL",
    "MediaInfo": "MEDIAINFOTOOL",
    "MediaSegments": "MEDIASEGMENTSTOOL",
    "Movies": "MOVIESTOOL",
    "MusicGenres": "MUSICGENRESTOOL",
    "Package": "PACKAGETOOL",
    "Persons": "PERSONSTOOL",
    "Playlists": "PLAYLISTSTOOL",
    "Playstate": "PLAYSTATETOOL",
    "Plugins": "PLUGINSTOOL",
    "QuickConnect": "QUICKCONNECTTOOL",
    "RemoteImage": "REMOTEIMAGETOOL",
    "ScheduledTasks": "SCHEDULEDTASKSTOOL",
    "Search": "SEARCHTOOL",
    "Session": "SESSIONTOOL",
    "Startup": "STARTUPTOOL",
    "Studios": "STUDIOSTOOL",
    "Subtitle": "SUBTITLETOOL",
    "Suggestions": "SUGGESTIONSTOOL",
    "SyncPlay": "SYNCPLAYTOOL",
    "System": "SYSTEMTOOL",
    "TimeSync": "TIMESYNCTOOL",
    "Tmdb": "TMDBTOOL",
    "Trailers": "TRAILERSTOOL",
    "Trickplay": "TRICKPLAYTOOL",
    "TvShows": "TVSHOWSTOOL",
    "UniversalAudio": "UNIVERSALAUDIOTOOL",
    "User": "USERTOOL",
    "UserLibrary": "USERLIBRARYTOOL",
    "UserViews": "USERVIEWSTOOL",
    "VideoAttachments": "VIDEOATTACHMENTSTOOL",
    "Videos": "VIDEOSTOOL",
    "Years": "YEARSTOOL",
}
