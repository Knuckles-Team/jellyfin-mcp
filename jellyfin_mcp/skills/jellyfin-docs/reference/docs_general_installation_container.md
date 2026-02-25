[Skip to main content](https://jellyfin.org/docs/general/installation/container/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
    * [Windows](https://jellyfin.org/docs/general/installation/windows)
    * [macOS](https://jellyfin.org/docs/general/installation/macos)
    * [Linux](https://jellyfin.org/docs/general/installation/linux)
    * [Container](https://jellyfin.org/docs/general/installation/container)
    * [Advanced Installation](https://jellyfin.org/docs/general/installation/container/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/installation/container/)
  * [Administration](https://jellyfin.org/docs/general/installation/container/)
  * [Server Guide](https://jellyfin.org/docs/general/installation/container/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * Container


On this page
# Container
## Container images[​](https://jellyfin.org/docs/general/installation/container/#container-images "Direct link to Container images")
Official container image: `jellyfin/jellyfin` [![jellyfin Docker Pull Count](https://img.shields.io/docker/pulls/jellyfin/jellyfin.svg)](https://hub.docker.com/r/jellyfin/jellyfin).
This image is also published on the GitHub Container Registry: `ghcr.io/jellyfin/jellyfin`.
LinuxServer.io image: `linuxserver/jellyfin` [![linuxserver jellyfin Docker Pull Count](https://img.shields.io/docker/pulls/linuxserver/jellyfin.svg)](https://hub.docker.com/r/linuxserver/jellyfin).
hotio image: `ghcr.io/hotio/jellyfin`.
Jellyfin distributes official container images on [Docker Hub](https://hub.docker.com/r/jellyfin/jellyfin/) and the [GitHub Container Registry](https://ghcr.io/jellyfin/jellyfin) for multiple architectures. These images are based on Debian and [built directly from the Jellyfin source code](https://github.com/jellyfin/jellyfin-packaging/blob/master/docker/Dockerfile).
Several tags are available tracking different builds and [version](https://jellyfin.org/docs/general/contributing/release-procedure/#versioning) levels.
  * `latest` always tracks the latest stable release, including through major and minor version bumps
  * `X` (e.g. `10`) tracks the major version, e.g. the latest 10.Y.Z
  * `X.Y` (e.g. `10.11`) tracks the minor version, e.g. the latest 10.11.Z
  * `X.Y.Z` (e.g. `10.11.0`) tracks a specific release
  * `X.Y.Z.YYYYMMDD-HHMMSS` (e.g. `10.11.0.20251020-004604`) tracks a specific packaging build


Additionally, there are several third parties providing unofficial container images, including the [LinuxServer.io](https://www.linuxserver.io/) ([Dockerfile](https://github.com/linuxserver/docker-jellyfin/blob/master/Dockerfile)) project and [hotio](https://github.com/hotio) ([Dockerfile](https://github.com/hotio/jellyfin/blob/release/linux-amd64.Dockerfile)), which offer images based on Ubuntu and the official Jellyfin Ubuntu binary packages.
## Installation Instructions[​](https://jellyfin.org/docs/general/installation/container/#installation-instructions "Direct link to Installation Instructions")
Replace `uid:gid` if you want to run jellyfin as a specific user/group. Exclude the `user` argument entirely if you want to use the default user.
  * Docker
  * Docker Compose
  * Podman


[Docker](https://www.docker.com/) allows you to run containers on Linux, Windows and MacOS.
If you wish to use Windows or macOS, please install Jellyfin natively instead. [Windows](https://jellyfin.org/docs/general/installation/windows) [macOS](https://jellyfin.org/docs/general/installation/macos).
While it is possible to run Jellyfin in Docker on a Windows or macOS host, it is NOT supported. Some features are known to be broken when running in Docker on platforms other than Linux, Notably:
  * Hardware Accelerated Transcoding
  * [Scanning on macOS in Docker](https://github.com/jellyfin/jellyfin/issues/13093)


You WILL NOT receive any support for running Jellyfin in Docker on platforms other than Linux.
The basic steps to create and run a Jellyfin container using Docker are as follows.
  1. Follow the [official installation guide to install Docker](https://docs.docker.com/engine/install).
  2. Download the latest container image.
```
docker pull jellyfin/jellyfin

```

  3. Create persistent storage for configuration and cache data.
Either create two directories on the host and use bind mounts:
```
mkdir /path/to/config
mkdir /path/to/cache

```

Or create two persistent volumes:
```
docker volume create jellyfin-config
docker volume create jellyfin-cache

```

  4. Create and run a container in one of the following ways.


The default network mode for Docker is bridge mode. Bridge mode will be used if host mode is omitted. Using host networking (`--net=host`) is optional but required in order to use DLNA.
**Using Docker command line interface:**
```
docker run -d \
 --name jellyfin \
 --user uid:gid \
 -p 8096:8096/tcp \
 -p 7359:7359/udp \
 --volume /path/to/config:/config \ # Alternatively --volume jellyfin-config:/config
 --volume /path/to/cache:/cache \ # Alternatively --volume jellyfin-cache:/cache
 --mount type=bind,source=/path/to/media,target=/media \
 --restart=unless-stopped \
 jellyfin/jellyfin

```

Bind Mounts are needed to pass folders from the host OS to the container OS whereas volumes are maintained by Docker and can be considered easier to backup and control by external programs. For a simple setup, it's considered easier to use Bind Mounts instead of volumes. Multiple media libraries can be bind mounted if needed:
```
--mount type=bind,source=/path/to/media1,target=/media1
--mount type=bind,source=/path/to/media2,target=/media2,readonly
...etc

```

Custom [server-side system fonts](https://jellyfin.org/docs/general/administration/configuration/#server-side-system-fonts) directory can be optionally bind mounted in order to use these fonts during transcoding with subtitle burn-in:
```
--mount type=bind,source=/path/to/fonts,target=/usr/local/share/fonts/custom,readonly

```

A directory of [fallback fonts](https://jellyfin.org/docs/general/administration/configuration/#fallback-fonts) can be mounted as well. In this case, you will have to set the directory of fallback fonts to `/fallback_fonts` in Jellyfin server settings panel:
```
--mount type=bind,source=/path/to/fallback/fonts,target=/fallback_fonts,readonly

```

If you wish to use Windows or macOS, please install Jellyfin natively instead. [Windows](https://jellyfin.org/docs/general/installation/windows) [macOS](https://jellyfin.org/docs/general/installation/macos).
While it is possible to run Jellyfin in Docker on a Windows or macOS host, it is NOT supported. Some features are known to be broken when running in Docker on platforms other than Linux, Notably:
  * Hardware Accelerated Transcoding
  * [Scanning on macOS in Docker](https://github.com/jellyfin/jellyfin/issues/13093)


You WILL NOT receive any support for running Jellyfin in Docker on platforms other than Linux.
Create a `docker-compose.yml` file like the following.
```
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    # Optional - specify the uid and gid you would like Jellyfin to use instead of root
    user: uid:gid
    ports:
      - 8096:8096/tcp
      - 7359:7359/udp
    volumes:
      - /path/to/config:/config
      - /path/to/cache:/cache
      - type: bind
        source: /path/to/media
        target: /media
      - type: bind
        source: /path/to/media2
        target: /media2
        read_only: true
      # Optional - extra fonts to be used during transcoding with subtitle burn-in
      - type: bind
        source: /path/to/fonts
        target: /usr/local/share/fonts/custom
        read_only: true
    restart: 'unless-stopped'
    # Optional - alternative address used for autodiscovery
    environment:
      - JELLYFIN_PublishedServerUrl=http://example.com
    # Optional - may be necessary for docker healthcheck to pass if running in host network mode
    extra_hosts:
      - 'host.docker.internal:host-gateway'

```

Then while in the same folder as the `docker-compose.yml` run:
```
docker compose up

```

To run the container in background add `-d` to the above command.
You can learn more about using Docker by [reading the official Docker documentation](https://docs.docker.com/).
[Podman](https://podman.io) allows you to run rootless containers. Steps to run Jellyfin using Podman are similar to the Docker steps.
  1. Install Podman:
```
sudo dnf install -y podman

```

  2. Create and run a Jellyfin container:
```
podman run \
 --detach \
 --label "io.containers.autoupdate=registry" \
 --name myjellyfin \
 --publish 8096:8096/tcp \
 --publish 7359:7359/udp \
 --rm \
 --user $(id -u):$(id -g) \
 --userns keep-id \
 --volume jellyfin-cache:/cache:Z \
 --volume jellyfin-config:/config:Z \
 --mount type=bind,source=/path/to/media,destination=/media,ro=true,relabel=private \
 docker.io/jellyfin/jellyfin:latest

```

  3. Open the necessary ports in your machine's firewall if you wish to permit access to the Jellyfin server from outside the host. This is not done automatically when using rootless Podman. If your distribution uses `firewalld`, the following commands save and load a new firewall rule opening the HTTP port `8096` for TCP connections. Additionally port 7359 UDP needs to be opened for auto discovery.
```
sudo firewall-cmd --add-port=8096/tcp --permanent
sudo firewall-cmd --add-port=7359/udp --permanent
sudo firewall-cmd --reload

```



Podman doesn't require root access to run containers, although there are some details to be mindful of; see [the relevant documentation](https://docs.podman.io/en/latest/markdown/podman.1.html#rootless-mode). For security, the Jellyfin container should be run using rootless Podman. Furthermore, it is safer to run as a non-root user within the container. The `--user` option will run with the provided user id and group id _inside_ the container. The `--userns keep-id` flag ensures that current user's id is mapped to the non-root user's id inside the container. This ensures that the permissions for directories bind-mounted inside the container are mapped correctly between the user running Podman and the user running Jellyfin inside the container.
Keep in mind that the `--label "io.containers.autoupdate=image"` flag will allow the container to be automatically updated via `podman auto-update`, and a [backup](https://jellyfin.org/docs/general/administration/backup-and-restore) will be required to restore a previous version.
The `z` (shared volume) or `Z` (private volume) volume option and `relabel=shared` or `relabel=private` mount option tell Podman to relabel files inside the volumes as appropriate, for systems running SELinux.
Replace `jellyfin-config` and `jellyfin-cache` with `/path/to/config` and `/path/to/cache` if you wish to use bind mounts.
This example mounts your media library read-only by setting `ro=true`; set this to `ro=false` if you wish to give Jellyfin write access to your media.
Managing via systemd
To run as a systemd service see [podman-systemd.unit](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
As always it is recommended to run the container rootless. Therefore we want to manage the container with the `systemd --user` flag.
  1. Create a new user that the rootless container will run under.
`useradd jellyfin`
This allows users who are not logged in to run long-running services.
`loginctl enable-linger jellyfin`
Open an interactive shell session.
`machinectl shell jellyfin@`
  2. Install `.config/containers/systemd/jellyfin.container`
> Contents of `~/.config/containers/systemd/jellyfin.container`
```
[Container]
Image=docker.io/jellyfin/jellyfin:latest
AutoUpdate=registry
PublishPort=8096:8096/tcp
UserNS=keep-id
Volume=jellyfin-config:/config:Z
Volume=jellyfin-cache:/cache:Z
Volume=jellyfin-media:/media:Z

[Service]
# Inform systemd of additional exit status
SuccessExitStatus=0 143

[Install]
# Start by default on boot
WantedBy=default.target

```

  3. Reload daemon and start the service.
`systemctl --user daemon-reload`
`systemctl --user start jellyfin`
  4. To enable Podman auto-updates, enable the necessary systemd timer.
`systemctl --user enable --now podman-auto-update.timer`
  5. Optionally check logs for errors
`journalctl --user -u jellyfin`
  6. `exit` the current session.


Using hardware acceleration
To use hardware acceleration, you need to allow the container to access the render device. If you are using container-selinux-2.226 or later, you have to set the `container_use_dri_devices` flag in selinux or the container will not be able to use it:
`sudo setsebool -P container_use_dri_devices 1`
On older versions of container-selinux, you have to disable the selinux confinement for the container by adding `--security-opt label=disable` to the podman command.
Then, you need to mount the render device inside the container:
`--device /dev/dri/:/dev/dri/`
Finally, you need to set the `--device` flag for the container to use the render device:
`--device /dev/dri/`
Podman run example:
```
   podman run \
    --detach \
    --label "io.containers.autoupdate=registry" \
    --name myjellyfin \
    --publish 8096:8096/tcp \
    --device /dev/dri/:/dev/dri/ \
    # --security-opt label=disable # Only needed for older versions of container-selinux < 2.226
    --rm \
    --user $(id -u):$(id -g) \
    --userns keep-id \
    --volume jellyfin-cache:/cache:Z \
    --volume jellyfin-config:/config:Z \
    --mount type=bind,source=/path/to/media,destination=/media,ro=true,relabel=private \
    docker.io/jellyfin/jellyfin:latest

```

systemd example:
```
[Unit]
Description=jellyfin

[Container]
Image=docker.io/jellyfin/jellyfin:latest
AutoUpdate=registry
PublishPort=8096:8096/tcp
UserNS=keep-id
#SecurityLabelDisable=true # Only needed for older versions of container-selinux < 2.226
AddDevice=/dev/dri/:/dev/dri/
Volume=jellyfin-config:/config:Z
Volume=jellyfin-cache:/cache:Z
Volume=jellyfin-media:/media:Z

[Service]
# Inform systemd of additional exit status
SuccessExitStatus=0 143

[Install]
# Start by default on boot
WantedBy=default.target

```

Vendor-specific configuration
Additional configuration steps may be required depending on your GPU vendor. Check the [Hardware Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration) section.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/installation/container.md)
[Previous Linux](https://jellyfin.org/docs/general/installation/linux)[Next Community Maintained Packages](https://jellyfin.org/docs/general/installation/advanced/community)
  * [Container images](https://jellyfin.org/docs/general/installation/container/#container-images)
  * [Installation Instructions](https://jellyfin.org/docs/general/installation/container/#installation-instructions)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
