[Skip to main content](https://jellyfin.org/docs/general/server/plugins/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/server/plugins/)
  * [Administration](https://jellyfin.org/docs/general/server/plugins/)
  * [Server Guide](https://jellyfin.org/docs/general/server/plugins/)
    * [Devices](https://jellyfin.org/docs/general/server/devices)
    * [Libraries](https://jellyfin.org/docs/general/server/libraries)
    * [Live Broadcast](https://jellyfin.org/docs/general/server/live-tv/)
    * [Media](https://jellyfin.org/docs/general/server/plugins/)
    * [Metadata](https://jellyfin.org/docs/general/server/metadata/)
    * [Webhook Plugin for Notifications](https://jellyfin.org/docs/general/server/notifications)
    * [Plugins](https://jellyfin.org/docs/general/server/plugins/)
      * [Open Subtitles](https://jellyfin.org/docs/general/server/plugins/open-subtitles)
      * [TVHeadend](https://jellyfin.org/docs/general/server/plugins/tvheadend)
    * [Quick Connect](https://jellyfin.org/docs/general/server/quick-connect)
    * [Settings](https://jellyfin.org/docs/general/server/settings)
    * [Tasks](https://jellyfin.org/docs/general/server/tasks)
    * [Users](https://jellyfin.org/docs/general/server/users/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * Server Guide
  * Plugins


On this page
# Plugins
Jellyfin has a collection of optional plugins that can be installed to provide additional features. To create a plugin, see the [plugin template](https://github.com/jellyfin/jellyfin-plugin-template) repository.
## Installing[​](https://jellyfin.org/docs/general/server/plugins/#installing "Direct link to Installing")
### Catalog[​](https://jellyfin.org/docs/general/server/plugins/#catalog "Direct link to Catalog")
Many plugins are available in a repository hosted on our servers, which can be easily installed using the plugin catalog in the settings. At the moment many of these are still being updated frequently so the version number may not be accurate. There are several different categories that can indicate what kind of functionality the plugins may provide.
The _plugins folder_ is located in different locations depending on your install:
  * `%UserProfile%\AppData\Local\jellyfin\plugins` for direct installs
  * `%ProgramData%\Jellyfin\Server\plugins` for tray installs


After that start Jellyfin back up, and reinstall each plugin you want to update using the above method from the catalog. Plugin settings should be retained if you do not delete the `.xml` files from the `<direct or tray path>\plugins\configurations` folder.
**Authentication:** Add new authentication providers, such as LDAP.
**Channels:** Allow streaming remote audio or video content.
**General:** Plugins that serve general purposes, such as sync with Trakt.tv, or Kodi.
**Live TV:** Plugins that help with connecting to tuners, such as NextPVR, or TVHeadend.
**Metadata:** Scrape metadata from a new source or modify existing metadata.
**Notifications:** Allow notifications to connect to many different services, including Gotify and Slack.
### Manual[​](https://jellyfin.org/docs/general/server/plugins/#manual "Direct link to Manual")
All plugins hosted on the repository can be built from source and manually added to your server as well. They just need to be placed in the plugin directory, which is something like `/var/lib/jellyfin/plugins/` on most Linux distributions. Once the server is restarted any additions should automatically show up in your list of installed plugins. If you can't see the new plugin there may be a file permission issue.
## List[​](https://jellyfin.org/docs/general/server/plugins/#list "Direct link to List")
### Official Plugins[​](https://jellyfin.org/docs/general/server/plugins/#official-plugins "Direct link to Official Plugins")
#### Metadata Plugins[​](https://jellyfin.org/docs/general/server/plugins/#metadata-plugins "Direct link to Metadata Plugins")
Manage your Anime in Jellyfin with several different metadata providers and options for organizing your collection.
##### Anilist[​](https://jellyfin.org/docs/general/server/plugins/#anilist "Direct link to Anilist")
![Anilist Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-anilist.svg) ![Anilist Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-anilist.svg) ![Anilist License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-anilist.svg)
Provides metadata support from [Anilist](https://anilist.co/).
**Link:**
  * [Github](https://github.com/jellyfin/jellyfin-plugin-anilist)


##### Anidb[​](https://jellyfin.org/docs/general/server/plugins/#anidb "Direct link to Anidb")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-anidb.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-anidb.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-anidb.svg)
Provides metadata support from [Anidb](https://anidb.net/).
**Link:**
  * [Github](https://github.com/jellyfin/jellyfin-plugin-anidb)


##### Anisearch[​](https://jellyfin.org/docs/general/server/plugins/#anisearch "Direct link to Anisearch")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-anisearch.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-anisearch.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-anisearch.svg)
Provides metadata support from [Anisearch](https://www.anisearch.com/).
**Link:**
  * [Github](https://github.com/jellyfin/jellyfin-plugin-anisearch)


##### Bookshelf[​](https://jellyfin.org/docs/general/server/plugins/#bookshelf "Direct link to Bookshelf")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-bookshelf.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-bookshelf.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-bookshelf.svg)
Supports several different metadata providers and options for organizing your collection.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-bookshelf)


##### Kitsu[​](https://jellyfin.org/docs/general/server/plugins/#kitsu "Direct link to Kitsu")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-kitsu.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-kitsu.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-kitsu.svg)
Provides metadata support from [Kitsu](https://kitsu.app/).
  * [Github](https://github.com/jellyfin/jellyfin-plugin-kitsu)


#### Fanart[​](https://jellyfin.org/docs/general/server/plugins/#fanart "Direct link to Fanart")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-fanart.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-fanart.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-fanart.svg)
Scrape poster images for movies, shows, and artists in your library from [fanart.tv](https://fanart.tv).
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-fanart)


#### Kodi Sync Queue[​](https://jellyfin.org/docs/general/server/plugins/#kodi-sync-queue "Direct link to Kodi Sync Queue")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-kodisyncqueue.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-kodisyncqueue.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-kodisyncqueue.svg)
Helps keep Jellyfin for Kodi in sync with the library without needing to run periodic full scans.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-kodisyncqueue)


#### Local Intros[​](https://jellyfin.org/docs/general/server/plugins/#local-intros "Direct link to Local Intros")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-intros.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-intros.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-intros.svg)
Use pre-roll intro videos from local storage.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-intros)


#### LDAP[​](https://jellyfin.org/docs/general/server/plugins/#ldap "Direct link to LDAP")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-ldapauth.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-ldapauth.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-ldapauth.svg)
Authenticate your Jellyfin users against an LDAP database, and optionally create users who do not yet exist automatically. Allows the administrator to customize most aspects of the LDAP authentication process, including customizable search attributes, username attribute, and a search filter for administrative users (set on user creation). The user, via the "Manual Login" process, can enter any valid attribute value, which will be mapped back to the specified username attribute automatically as well.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-ldapauth)


#### NextPVR[​](https://jellyfin.org/docs/general/server/plugins/#nextpvr "Direct link to NextPVR")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-nextpvr.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-nextpvr.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-nextpvr.svg)
Provides access to Live TV, Program Guide, and Recordings from [NextPVR](https://www.nextpvr.com/).
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-nextpvr)


####  [Open Subtitles](https://jellyfin.org/docs/general/server/plugins/open-subtitles)[​](https://jellyfin.org/docs/general/server/plugins/#open-subtitles "Direct link to open-subtitles")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-opensubtitles.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-opensubtitles.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-opensubtitles.svg)
Download subtitles from the internet to use with your media files from [Open Subtitles](https://www.opensubtitles.org/). You can configure the languages it downloads on a per-library basis.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-opensubtitles)


#### Subtitle Extract[​](https://jellyfin.org/docs/general/server/plugins/#subtitle-extract "Direct link to Subtitle Extract")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-subtitleextract.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-subtitleextract.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-subtitleextract.svg)
Plugin to automatically extract embedded subtitles in media. This avoids delayed subtitles during streaming if the client does not support direct play and requests subtitles.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-subtitleextract)


#### Playback Reporting[​](https://jellyfin.org/docs/general/server/plugins/#playback-reporting "Direct link to Playback Reporting")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-playbackreporting.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-playbackreporting.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-playbackreporting.svg)
Collect and show user playback statistics, such as total time watched, media watched, time of day watched, and time of week watched. Can keep information for as long as you want or can cull older information automatically. Also allows you to manually query the data collected so you can generate your own reports.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-playbackreporting)


#### Reports[​](https://jellyfin.org/docs/general/server/plugins/#reports "Direct link to Reports")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-reports.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-reports.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-reports.svg)
Generate reports of your media library.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-reports)


#### TMDb Box Sets[​](https://jellyfin.org/docs/general/server/plugins/#tmdb-box-sets "Direct link to TMDb Box Sets")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-tmdbboxsets.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-tmdbboxsets.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-tmdbboxsets.svg)
Automatically create movie box sets based on TMDb collections. Configurable minimum number of films to be considered a boxset. Boxsets are created as collections and includes a scheduled task to ensure that new media is automatically put into boxsets.
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-tmdbboxsets)


#### Trakt[​](https://jellyfin.org/docs/general/server/plugins/#trakt "Direct link to Trakt")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-trakt.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-trakt.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-trakt.svg)
Record your watched media with [Trakt](https://trakt.tv).
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-trakt)


#### TVHeadend[​](https://jellyfin.org/docs/general/server/plugins/#tvheadend "Direct link to TVHeadend")
![Language](https://img.shields.io/github/languages/top/jellyfin/jellyfin-plugin-tvheadend.svg) ![Contributors](https://img.shields.io/github/contributors/jellyfin/jellyfin-plugin-tvheadend.svg) ![License](https://img.shields.io/github/license/jellyfin/jellyfin-plugin-tvheadend.svg)
Manage TVHeadEnd directly from Jellyfin by visiting the [TVHeadEnd plugin support page](https://jellyfin.org/docs/general/server/plugins/tvheadend).
**Links:**
  * [GitHub](https://github.com/jellyfin/jellyfin-plugin-tvheadend)


### 3rd-Party Plugins[​](https://jellyfin.org/docs/general/server/plugins/#3rd-party-plugins "Direct link to 3rd-Party Plugins")
#### Ani-Sync[​](https://jellyfin.org/docs/general/server/plugins/#ani-sync "Direct link to Ani-Sync")
Ani-Sync lets you synchronize/scrobble your Jellyfin Anime watch progress to popular services like MyAnimeList, AniList, Kitsu.
**Links:**
  * [GitHub](https://github.com/vosmiic/jellyfin-ani-sync)


#### Kinopoisk metadata plugin[​](https://jellyfin.org/docs/general/server/plugins/#kinopoisk-metadata-plugin "Direct link to Kinopoisk metadata plugin")
Fetches metadata from <https://kinopoisk.ru>. This site is popular in the Russian-speaking community and contains almost no English-language information. Can provide movies and series rating, description, actors and staff, trailers and so on.
**Links:**
  * [GitHub](https://github.com/LinFor/jellyfin-plugin-kinopoisk)


#### Last.FM[​](https://jellyfin.org/docs/general/server/plugins/#lastfm "Direct link to Last.FM")
Enables audio scrobbling to Last.FM as well as a metadata fetcher source.
**Links:**
  * [GitHub](https://github.com/jesseward/jellyfin-plugin-lastfm)


#### Merge Versions[​](https://jellyfin.org/docs/general/server/plugins/#merge-versions "Direct link to Merge Versions")
Automatically group every repeated movie.
**Links:**
  * [GitHub](https://github.com/danieladov/jellyfin-plugin-mergeversions)


#### Shokofin[​](https://jellyfin.org/docs/general/server/plugins/#shokofin "Direct link to Shokofin")
A plugin to integrate your Shoko database with the Jellyfin media server.
**Links:**
  * [GitHub](https://github.com/ShokoAnime/Shokofin)


#### Skin Manager[​](https://jellyfin.org/docs/general/server/plugins/#skin-manager "Direct link to Skin Manager")
Download and manage the most popular skins.
**Links:**
  * [GitHub](https://github.com/danieladov/jellyfin-plugin-skin-manager)


#### Themerr[​](https://jellyfin.org/docs/general/server/plugins/#themerr "Direct link to Themerr")
Plugin for Jellyfin that adds theme songs to movies and tv shows using ThemerrDB.
**Links:**
  * [GitHub](https://github.com/LizardByte/themerr-jellyfin)


#### YouTube Metadata[​](https://jellyfin.org/docs/general/server/plugins/#youtube-metadata "Direct link to YouTube Metadata")
Downloads metadata of YouTube videos with a YouTube API key.
**Links:**
  * [GitHub](https://github.com/ankenyr/jellyfin-youtube-metadata-plugin)


#### TubeArchivistMetadata[​](https://jellyfin.org/docs/general/server/plugins/#tubearchivistmetadata "Direct link to TubeArchivistMetadata")
A plugin to integrate your TubeArchivist library with Jellyfin, providing metadata and organizing media.
**Links:**
  * [GitHub](https://github.com/tubearchivist/tubearchivist-jf-plugin)


#### AudioMuse-AI[​](https://jellyfin.org/docs/general/server/plugins/#audiomuse-ai "Direct link to AudioMuse-AI")
Enhance Jellyfin with sonic analysis and smart song clustering, replacing InstantMix with sonically similar music suggestions.
**Links:**
  * [GitHub](https://github.com/NeptuneHub/audiomuse-ai-plugin)


#### WizdomSubs Downloader[​](https://jellyfin.org/docs/general/server/plugins/#wizdomsubs-downloader "Direct link to WizdomSubs Downloader")
Downloads Hebrew subtitles from WizdomSubs for your media files. This plugin provides automatic subtitle downloading for Hebrew-speaking users.
**Links:**
  * [GitHub](https://github.com/DeDuplicate/Jellyfin_wizdomsubs_downloader)


## Repositories[​](https://jellyfin.org/docs/general/server/plugins/#repositories "Direct link to Repositories")
### Official Jellyfin Plugin Repositories[​](https://jellyfin.org/docs/general/server/plugins/#official-jellyfin-plugin-repositories "Direct link to Official Jellyfin Plugin Repositories")
### Jellyfin
Official
Repository URL
```
https://repo.jellyfin.org/files/plugin/manifest.json
```

### Jellyfin Unstable
OfficialUnstable
Repository URL
```
https://repo.jellyfin.org/files/plugin-unstable/manifest.json
```

### 3rd-Party Plugin Repositories[​](https://jellyfin.org/docs/general/server/plugins/#3rd-party-plugin-repositories "Direct link to 3rd-Party Plugin Repositories")
### 9p4's Single-Sign-On (SSO) Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/9p4/jellyfin-plugin-sso/manifest-release/manifest.json
```

#### Includes
  * [9p4's Single Sign On Plugin](https://github.com/9p4/jellyfin-plugin-sso)


### Ani-Sync Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/vosmiic/jellyfin-ani-sync/master/manifest.json
```

#### Includes
  * [Ani-Sync](https://github.com/vosmiic/jellyfin-ani-sync)


### danieladov's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/danieladov/JellyfinPluginManifest/master/manifest.json
```

#### Includes
  * [Merge Versions](https://github.com/danieladov/jellyfin-plugin-mergeversions)
  * [Skin Manager](https://github.com/danieladov/jellyfin-plugin-skin-manager)
  * [Theme Songs](https://github.com/danieladov/jellyfin-plugin-themesongs)


### dkanada's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/dkanada/jellyfin-plugin-intros/master/manifest.json
```

#### Includes
  * [Intros](https://github.com/dkanada/jellyfin-plugin-intros)


### k-matti's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/k-matti/jellyfin-plugin-repository/master/manifest.json
```

#### Includes
  * [SMS Notifications](https://github.com/k-matti/jellyfin-plugin-sms)
  * [NapiSub](https://github.com/k-matti/jellyfin-plugin-napi)


### LinFor's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/LinFor/jellyfin-plugin-kinopoisk/master/dist/manifest.json
```

#### Includes
  * [Kinopoisk metadata plugin](https://github.com/LinFor/jellyfin-plugin-kinopoisk)


### LizardByte's Repo
Third Party
Repository URL
```
https://app.lizardbyte.dev/jellyfin-plugin-repo/manifest.json
```

#### Includes
  * [Themerr](https://github.com/LizardByte/themerr-jellyfin)


### ShokoAnime's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/ShokoAnime/Shokofin/metadata/stable/manifest.json
```

#### Includes
  * [Shokofin](https://github.com/ShokoAnime/Shokofin)


### TubeArchivist's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/tubearchivist/tubearchivist-jf-plugin/master/manifest.json
```

#### Includes
  * [TubeArchivistMetadata](https://github.com/tubearchivist/tubearchivist-jf-plugin)


### AudioMuse-AI's Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/neptunehub/audiomuse-ai-plugin/master/manifest.json
```

#### Includes
  * [AudioMuse-AI](https://github.com/neptunehub/audiomuse-ai-plugin)


### DeDuplicate's WizdomSubs Downloader Repo
Third Party
Repository URL
```
https://raw.githubusercontent.com/DeDuplicate/Jellyfin_wizdomsubs_downloader/refs/heads/main/manifest.json
```

#### Includes
  * [WizdomSubs Downloader](https://github.com/DeDuplicate/Jellyfin_wizdomsubs_downloader)


[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/server/plugins/index.mdx)
[Previous Webhook Plugin for Notifications](https://jellyfin.org/docs/general/server/notifications)[Next Open Subtitles](https://jellyfin.org/docs/general/server/plugins/open-subtitles)
  * [Installing](https://jellyfin.org/docs/general/server/plugins/#installing)
    * [Catalog](https://jellyfin.org/docs/general/server/plugins/#catalog)
    * [Manual](https://jellyfin.org/docs/general/server/plugins/#manual)
  * [List](https://jellyfin.org/docs/general/server/plugins/#list)
    * [Official Plugins](https://jellyfin.org/docs/general/server/plugins/#official-plugins)
    * [3rd-Party Plugins](https://jellyfin.org/docs/general/server/plugins/#3rd-party-plugins)
  * [Repositories](https://jellyfin.org/docs/general/server/plugins/#repositories)
    * [Official Jellyfin Plugin Repositories](https://jellyfin.org/docs/general/server/plugins/#official-jellyfin-plugin-repositories)
    * [3rd-Party Plugin Repositories](https://jellyfin.org/docs/general/server/plugins/#3rd-party-plugin-repositories)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
