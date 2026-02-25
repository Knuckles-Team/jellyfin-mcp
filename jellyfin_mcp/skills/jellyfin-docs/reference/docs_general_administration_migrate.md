[Skip to main content](https://jellyfin.org/docs/general/administration/migrate/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/administration/migrate/)
  * [Administration](https://jellyfin.org/docs/general/administration/migrate/)
    * [Backup and Restore](https://jellyfin.org/docs/general/administration/backup-and-restore)
    * [Configuration](https://jellyfin.org/docs/general/administration/configuration)
    * [Hardware Selection](https://jellyfin.org/docs/general/administration/hardware-selection)
    * [Migrating](https://jellyfin.org/docs/general/administration/migrate)
    * [Storage](https://jellyfin.org/docs/general/administration/storage)
    * [Troubleshooting](https://jellyfin.org/docs/general/administration/troubleshooting)
  * [Server Guide](https://jellyfin.org/docs/general/administration/migrate/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * Administration
  * Migrating


On this page
# Migrating
This page covers migrations of Jellyfin as well as migrations to Jellyfin.
Jellyfins internal databases cannot be copied or adjusted easily. Depending on your case there may be ways to work around this, for example by just migrating parts of the data, or because it's possible maintain the same file paths.
## Watched Status Migration[​](https://jellyfin.org/docs/general/administration/migrate/#watched-status-migration "Direct link to Watched Status Migration")
There are third-party scripts available that will use the API to copy watched status and users from one instance to another. This can be done from Plex, Emby or another Jellyfin instance.
[Emby/Jellyfin to Jellyfin migration](https://github.com/CobayeGunther/Emby2Jelly)
[Plex to Jellyfin migration](https://github.com/wilmardo/migrate-plex-to-jellyfin)
## Migrating Linux install to Docker[​](https://jellyfin.org/docs/general/administration/migrate/#migrating-linux-install-to-docker "Direct link to Migrating Linux install to Docker")
It's possible to use the data of a local install in the official docker image by mapping files and folders to the same locations and configuring the image accordingly. It's possible to do this via the command line or by using Docker environment variables. To read more, see the [Configuration](https://jellyfin.org/docs/general/administration/configuration) page.
You need to have exactly matching paths for your files inside the docker container! This means that if your media is stored at `/media/raid/` this path needs to be accessible at `/media/raid/` inside the docker container too - the configurations below do include examples.
To guarantee proper permissions, get the `uid` and `gid` of the local user Jellyfin runs as (on a default install this is the `jellyfin` system user). You can do this by running the following command:
```
   id jellyfin

```

You need to replace the `<uid>:<gid>` placeholder below with the correct values.
To properly map the folders for your install, go to `Dashboard > Paths`.
### Using docker cli[​](https://jellyfin.org/docs/general/administration/migrate/#using-docker-cli "Direct link to Using docker cli")
```
docker run -d \
    --user <uid>:<gid> \
    -e JELLYFIN_CACHE_DIR=/var/cache/jellyfin \
    -e JELLYFIN_CONFIG_DIR=/etc/jellyfin \
    -e JELLYFIN_DATA_DIR=/var/lib/jellyfin \
    -e JELLYFIN_LOG_DIR=/var/log/jellyfin \
    --mount type=bind,source=/etc/jellyfin,target=/etc/jellyfin \
    --mount type=bind,source=/var/cache/jellyfin,target=/var/cache/jellyfin \
    --mount type=bind,source=/var/lib/jellyfin,target=/var/lib/jellyfin \
    --mount type=bind,source=/var/log/jellyfin,target=/var/log/jellyfin \
    --mount type=bind,source=</path/to/media>,target=</path/to/media> \
    --net=host \
    --restart=unless-stopped \
    jellyfin/jellyfin

```

### Using docker-compose yaml[​](https://jellyfin.org/docs/general/administration/migrate/#using-docker-compose-yaml "Direct link to Using docker-compose yaml")
```
services:
  jellyfin:
    image: jellyfin/jellyfin
    user: <uid>:<gid>
    network_mode: 'host'
    restart: 'unless-stopped'
    environment:
      - JELLYFIN_CACHE_DIR=/var/cache/jellyfin
      - JELLYFIN_CONFIG_DIR=/etc/jellyfin
      - JELLYFIN_DATA_DIR=/var/lib/jellyfin
      - JELLYFIN_LOG_DIR=/var/log/jellyfin
    volumes:
      - /etc/jellyfin:/etc/jellyfin
      - /var/cache/jellyfin:/var/cache/jellyfin
      - /var/lib/jellyfin:/var/lib/jellyfin
      - /var/log/jellyfin:/var/log/jellyfin
      - <path-to-media>:<path-to-media>

```

## Migrating From Emby 3.5.2 to Jellyfin[​](https://jellyfin.org/docs/general/administration/migrate/#migrating-from-emby-352-to-jellyfin "Direct link to Migrating From Emby 3.5.2 to Jellyfin")
Direct database migration from Emby (of any version) to Jellyfin is NOT SUPPORTED. We have found many subtle bugs due to the inconsistent database schemas that result from trying to do this, and strongly recommend that all Jellyfin users migrating from Emby start with a fresh database and library scan.
The original procedure is provided below for reference however we cannot support it nor guarantee that a system upgraded in this way will work properly, if at all. If anyone is interested in writing a database migration script which will correct the deficiencies in the existing database and properly import them into Jellyfin, [we would welcome it however](https://jellyfin.org/docs/general/contributing)!
While it is technically possible to migrate existing configuration of Emby version 3.5.2 or earlier, due to subtle and weird bugs reported after such attempts we do not recommend this migration. Emby versions 3.5.3 or 3.6+ cannot be migrated. Thus, we recommend creating a new Jellyfin configuration and rebuilding your library instead.
Windows users may take advantage of the `install-jellyfin.ps1` script in the [Jellyfin repository](https://github.com/jellyfin/jellyfin) which includes an automatic upgrade option.
This procedure is written for Debian-based Linux distributions, but can be translated to other platforms by following the same general principles.
  1. Upgrade to Emby version 3.5.2, so that the database schema is fully up-to-date and consistent. While this is not required, it can help reduce the possibility of obscure bugs in the database.
  2. Stop the `emby-server` daemon:
```
sudo service emby-server stop

```

  3. Move your existing Emby data directory out of the way:
```
sudo mv /var/lib/emby /var/lib/emby.backup

```

  4. Remove or purge the `emby-server` package:
```
sudo apt purge emby-server

```

  5. Install the `jellyfin` package using the [installation instructions](https://jellyfin.org/docs/general/installation).
  6. Stop the `jellyfin` daemon:
```
sudo service jellyfin stop

```

  7. Copy over all the data files from the Emby backup data directory:
```
sudo cp -a /var/lib/emby.backup/* /var/lib/jellyfin/

```

  8. Correct ownership on the new data directory:
```
sudo chown -R jellyfin:jellyfin /var/lib/jellyfin

```

  9. Mark Startup Wizard as completed - if not marked as completed then it can be a security risk especially if remote access is enabled:
```
sudo sed -i '/IsStartupWizardCompleted/s/false/true/' /etc/jellyfin/system.xml

```

  10. Start the `jellyfin` daemon:


```
sudo service jellyfin start

```

[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/administration/migrate.md)
[Previous Hardware Selection](https://jellyfin.org/docs/general/administration/hardware-selection)[Next Storage](https://jellyfin.org/docs/general/administration/storage)
  * [Watched Status Migration](https://jellyfin.org/docs/general/administration/migrate/#watched-status-migration)
  * [Migrating Linux install to Docker](https://jellyfin.org/docs/general/administration/migrate/#migrating-linux-install-to-docker)
    * [Using docker cli](https://jellyfin.org/docs/general/administration/migrate/#using-docker-cli)
    * [Using docker-compose yaml](https://jellyfin.org/docs/general/administration/migrate/#using-docker-compose-yaml)
  * [Migrating From Emby 3.5.2 to Jellyfin](https://jellyfin.org/docs/general/administration/migrate/#migrating-from-emby-352-to-jellyfin)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
