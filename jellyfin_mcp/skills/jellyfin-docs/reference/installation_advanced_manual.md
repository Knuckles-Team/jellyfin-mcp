[Skip to main content](https://jellyfin.org/docs/general/installation/advanced/manual/#__docusaurus_skipToContent_fallback)
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
    * [Advanced Installation](https://jellyfin.org/docs/general/installation/advanced/manual/)
      * [Community Maintained Packages](https://jellyfin.org/docs/general/installation/advanced/community)
      * [Synology](https://jellyfin.org/docs/general/installation/advanced/synology)
      * [Manual Installation](https://jellyfin.org/docs/general/installation/advanced/manual)
      * [Building from source](https://jellyfin.org/docs/general/installation/advanced/source)
      * [TrueNAS SCALE](https://jellyfin.org/docs/general/installation/advanced/truenas)
      * [Kubernetes Deployment](https://jellyfin.org/docs/general/installation/advanced/kubernetes)
  * [Post-Install Setup](https://jellyfin.org/docs/general/installation/advanced/manual/)
  * [Administration](https://jellyfin.org/docs/general/installation/advanced/manual/)
  * [Server Guide](https://jellyfin.org/docs/general/installation/advanced/manual/)
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
  * Advanced Installation
  * Manual Installation


On this page
# Manual Installation
## Portable Windows Package[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-package "Direct link to Portable Windows Package")
### Portable Windows Install[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-install "Direct link to Portable Windows Install")
  1. Download and extract the latest version.
  2. Create a folder `jellyfin` at your preferred install location.
  3. Copy the extracted folder into the `jellyfin` folder and rename it to `system`.
  4. Create `jellyfin.bat` within your `jellyfin` folder containing:
     * To use the default library/data location at `%localappdata%`:
```
<--Your install path-->\jellyfin\system\jellyfin.exe

```

     * To use a custom library/data location (Path after the -d parameter):
```
<--Your install path-->\jellyfin\system\jellyfin.exe -d <--Your install path-->\jellyfin\data

```

     * To use a custom library/data location (Path after the -d parameter) and disable the auto-start of the webapp:
```
<--Your install path-->\jellyfin\system\jellyfin.exe -d <--Your install path-->\jellyfin\data -noautorunwebapp

```

  5. Run
```
jellyfin.bat

```

  6. Open your browser at `http://<--Server-IP-->:8096`.


### Portable Windows Update[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-update "Direct link to Portable Windows Update")
  1. Stop Jellyfin
  2. Rename the Jellyfin `system` folder to `system-bak`
  3. Download and extract the latest Jellyfin version
  4. Copy the extracted folder into the `jellyfin` folder and rename it to `system`
  5. Run `jellyfin.bat` to start the server again


### Portable Windows Rollback[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-rollback "Direct link to Portable Windows Rollback")
  1. Stop Jellyfin.
  2. Delete the `system` folder.
  3. Rename `system-bak` to `system`.
  4. Run `jellyfin.bat` to start the server again.


## Portable macOS package[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-macos-package "Direct link to Portable macOS package")
### Installing the Portable macOS Version[​](https://jellyfin.org/docs/general/installation/advanced/manual/#installing-the-portable-macos-version "Direct link to Installing the Portable macOS Version")
  1. Download the latest version of Jellyfin.
  2. Extract it into the Applications folder.
  3. Open Terminal and type `cd` followed with a space then drag the jellyfin folder into the terminal.
  4. Type `xattr -rd com.apple.quarantine .` to remove the quarantine flag.
  5. Type `codesign -fs - --deep jellyfin` to create an ad-hoc signature for the server.
  6. Type `./jellyfin` to run jellyfin.
  7. Open your browser at <http://localhost:8096>.


Closing the terminal window will end Jellyfin. Running Jellyfin in screen or tmux can prevent this from happening.
### Updating the Portable macOS Version[​](https://jellyfin.org/docs/general/installation/advanced/manual/#updating-the-portable-macos-version "Direct link to Updating the Portable macOS Version")
  1. Download the latest version.
  2. Stop the currently running server either via the dashboard or using `CTRL+C` in the terminal window.
  3. Extract the latest version into Applications
  4. Open Terminal and type `cd` followed with a space then drag the jellyfin folder into the terminal.
  5. Type `xattr -rd com.apple.quarantine .` to remove the quarantine flag.
  6. Type `codesign -fs - --deep jellyfin` to create an ad-hoc signature for the server.
  7. Type `./jellyfin` to run jellyfin.
  8. Open your browser at <http://localhost:8096>


### Uninstalling the Portable macOS Version[​](https://jellyfin.org/docs/general/installation/advanced/manual/#uninstalling-the-portable-macos-version "Direct link to Uninstalling the Portable macOS Version")
  1. Stop the currently running server either via the dashboard or using `CTRL+C` in the terminal window.
  2. Move `/Application/jellyfin-version` folder to the Trash. Replace version with the actual version number you are trying to delete.
  3. Delete the folder `~/.config/jellyfin/`
  4. Delete the folder `~/.local/share/jellyfin/`


### Using FFmpeg with the Portable macOS Version[​](https://jellyfin.org/docs/general/installation/advanced/manual/#using-ffmpeg-with-the-portable-macos-version "Direct link to Using FFmpeg with the Portable macOS Version")
The portable version doesn't come with FFmpeg by default. There are a few options for installing FFmpeg:
  * download jellyfin-ffmpeg from the [Jellyfin repo](https://repo.jellyfin.org/?path=/ffmpeg/macos) (recommended)
  * use the package manager homebrew by typing `brew install ffmpeg` into your Terminal ([here's how to install homebrew if you don't have it already](https://treehouse.github.io/installation-guides/mac/homebrew)
  * download the most recent [static build](https://evermeet.cx/ffmpeg/get/zip) (compiled by a third party see [evermeet.cx](https://evermeet.cx/ffmpeg/) for options and information) (Apple Silicon builds are not available from this source)
  * compile from source available from the official [website](https://ffmpeg.org/download.html)


Once downloaded, remove the quarantine flag for the `ffmpeg` and `ffprobe`.
Ensure that both `ffmpeg` and `ffprobe` are located at the same path, then execute the following command:
```
cd /path/to/ffmpeg/folder
xattr -rd com.apple.quarantine .

```

## Portable Linux install[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-linux-install "Direct link to Portable Linux install")
Generic `amd64`, `arm64`, and `armhf` Linux builds in TAR archive format are available [in the main download repository](https://repo.jellyfin.org/?path=/server/).
### Base Installation Process[​](https://jellyfin.org/docs/general/installation/advanced/manual/#base-installation-process "Direct link to Base Installation Process")
Create a directory in `/opt` for jellyfin and its files, and enter that directory.
```
sudo mkdir /opt/jellyfin
cd /opt/jellyfin

```

Download the latest generic Linux build for your architecture. The rest of these instructions assume version 10.10.7 is being installed (i.e. `jellyfin_10.10.7-amd64.tar.gz`). Download the generic build, then extract the archive:
```
sudo wget https://repo.jellyfin.org/files/server/linux/latest-stable/amd64/jellyfin_10.10.7-amd64.tar.gz
sudo tar xvzf jellyfin_10.10.7-amd64.tar.gz

```

Create four sub-directories for Jellyfin data.
```
sudo mkdir data cache config log

```

###  `FFmpeg` Installation[​](https://jellyfin.org/docs/general/installation/advanced/manual/#ffmpeg-installation "Direct link to ffmpeg-installation")
If you are not running a Debian derivative, install `ffmpeg` through your OS's package manager, and skip this section.
Not being able to use `jellyfin-ffmpeg` will most likely break hardware acceleration and tonemapping.
If you are running Debian or a derivative, you should [download](https://repo.jellyfin.org/?path=/ffmpeg/debian/) and install an `ffmpeg` `.deb` package built specifically for Jellyfin.
If you run into any dependency errors, run this and it will install them and `jellyfin-ffmpeg`.
```
sudo apt install -f

```

### Running Jellyfin[​](https://jellyfin.org/docs/general/installation/advanced/manual/#running-jellyfin "Direct link to Running Jellyfin")
Due to the number of [command line options](https://jellyfin.org/docs/general/administration/configuration/#command-line-options) that must be passed on to the Jellyfin binary, it is easiest to create a small script to run Jellyfin.
```
sudoedit jellyfin.sh

```

Then paste the following commands, optionally changing arguments as needed for custom deployments.
```
#!/bin/bash
JELLYFINDIR="/opt/jellyfin"
FFMPEGDIR="/usr/share/jellyfin-ffmpeg"

$JELLYFINDIR/jellyfin/jellyfin \
 -d $JELLYFINDIR/data \
 -C $JELLYFINDIR/cache \
 -c $JELLYFINDIR/config \
 -l $JELLYFINDIR/log \
 --ffmpeg $FFMPEGDIR/ffmpeg

```

Assuming you desire Jellyfin to run as a non-root user, `chmod` all files and directories to your normal login user and group. Also make the startup script above executable.
```
USER=$(id --name --user)
GROUP=$(id --name --group)
sudo chown -R $USER:$GROUP *
sudo chmod u+x jellyfin.sh

```

Finally, you can run it. You will see lots of log information when run, this is normal. Setup is as usual in the web browser.
```
./jellyfin.sh

```

#### Starting Jellyfin on boot (optional)[​](https://jellyfin.org/docs/general/installation/advanced/manual/#starting-jellyfin-on-boot-optional "Direct link to Starting Jellyfin on boot \(optional\)")
Create a `systemd` unit file.
```
cd /etc/systemd/system
sudo nano jellyfin.service

```

Then paste the following contents, replacing `youruser` with your username.
```
[Unit]
Description=Jellyfin
After=network.target

[Service]
Type=simple
User=youruser
Restart=always
ExecStart=/opt/jellyfin/jellyfin.sh

[Install]
WantedBy=multi-user.target

```

Apply the correct permissions to the file, enable the service to start on boot, then start it.
```
sudo chmod 644 jellyfin.service
sudo systemctl daemon-reload
sudo systemctl enable jellyfin.service
sudo systemctl start jellyfin.service

```

## Portable .NET DLL[​](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-net-dll "Direct link to Portable .NET DLL")
Platform-agnostic .NET Core DLL builds in TAR archive format are available from the [portable downloads section](https://jellyfin.org/downloads/dotnet).
These builds use the binary `jellyfin.dll` and must be loaded with `dotnet`.
## Debian (using extrepo)[​](https://jellyfin.org/docs/general/installation/advanced/manual/#debian-using-extrepo "Direct link to Debian \(using extrepo\)")
extrepo is only supported on Debian currently. The advantage of extrepo is that it is packaged in Debian. So you don’t have to execute the `curl | sudo bash` combo from the previous Automatic section. The risk with that command is that it relies on the security of the webserver. extrepo avoids this by having the Jellyfin repo information including the GPG key in its [extrepo-data](https://salsa.debian.org/extrepo-team/extrepo-data/-/blob/master/repos/debian/jellyfin.yaml?ref_type=heads). extrepo-data is verified with GPG by the extrepo tool. So there is a chain of trust from Debian all the way to the Jellyfin repo information.
```
sudo apt install extrepo
sudo extrepo enable jellyfin

```

Now you can continue at step 5. of the [Repository (Manual) section](https://jellyfin.org/docs/general/installation/advanced/manual/#official-linux-repository-manual).
## Official Linux Repository (Manual)[​](https://jellyfin.org/docs/general/installation/advanced/manual/#official-linux-repository-manual "Direct link to Official Linux Repository \(Manual\)")
If you would prefer to install everything manually, the full steps are as follows:
  1. Install `curl` and `gnupg` if you haven't already:
```
sudo apt install curl gnupg

```

  2. On Ubuntu (and derivatives) only, enable the Universe repository to obtain all the FFmpeg dependencies:
```
sudo add-apt-repository universe

```

If the above command fails you will need to install the following package `software-properties-common`. This can be achieved with the following command `sudo apt-get install software-properties-common`
On Debian, you can also enable the `non-free` components of your base repositories for additional FFmpeg dependencies, but this is optional.
  3. Download the GPG signing key (signed by the Jellyfin Team) and install it:
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.jellyfin.org/jellyfin_team.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/jellyfin.gpg

```

  4. Add a repository configuration at `/etc/apt/sources.list.d/jellyfin.sources`:
```
export VERSION_OS="$( awk -F'=' '/^ID=/{ print $NF }' /etc/os-release )"
export VERSION_CODENAME="$( awk -F'=' '/^VERSION_CODENAME=/{ print $NF }' /etc/os-release )"
export DPKG_ARCHITECTURE="$( dpkg --print-architecture )"
cat <<EOF | sudo tee /etc/apt/sources.list.d/jellyfin.sources
Types: deb
URIs: https://repo.jellyfin.org/${VERSION_OS}
Suites: ${VERSION_CODENAME}
Components: main
Architectures: ${DPKG_ARCHITECTURE}
Signed-By: /etc/apt/keyrings/jellyfin.gpg
EOF

```

The supported values for the above variables are:
     * `${VERSION_OS}`: One of `debian` or `ubuntu`; if it is not, use the closest one for your distribution.
     * `${VERSION_CODENAME}`: One of our supported [Debian](https://github.com/jellyfin/jellyfin-repo-helper-scripts/blob/master/install-debuntu.sh#L7) or [Ubuntu](https://github.com/jellyfin/jellyfin-repo-helper-scripts/blob/master/install-debuntu.sh#L8) release codenames. These can change as new releases come out and old releases are dropped, so check the script to be sure yours is supported.
     * `${DPKG_ARCHITECTURE}`: One of our [supported architectures](https://github.com/jellyfin/jellyfin-repo-helper-scripts/blob/master/install-debuntu.sh#L6). Microsoft does not provide a .NET for 32-bit x86 Linux systems, and hence Jellyfin is **not** supported on the `i386` architecture.
  5. Update your APT repositories:
```
sudo apt update

```

  6. Install the Jellyfin metapackage, which will automatically fetch the various sub-packages:
```
sudo apt install jellyfin

```

If you want to be explicit, instead of the metapackage, you can install the sub-packages individually:
```
sudo apt install jellyfin-server jellyfin-web

```

The `jellyfin-server` package will automatically select the right `jellyfin-ffmpeg` package for you as well.
  7. Manage the Jellyfin system service:
```
sudo systemctl {action} jellyfin
sudo service jellyfin {action}

```



##  `.deb` Packages (Very Manual)[​](https://jellyfin.org/docs/general/installation/advanced/manual/#deb-packages-very-manual "Direct link to deb-packages-very-manual")
Raw `.deb` packages, including old versions, source packages, and `dpkg` meta files, are available [in the main download repository](https://repo.jellyfin.org/?path=/server/).
The repository is the preferred way to obtain Jellyfin on Debian and Ubuntu systems, as this ensures you get automatic updates and that all dependencies are properly resolved. Use these steps only if you really know what you're doing.
  1. On Ubuntu (and derivatives) only, enable the Universe repository to obtain all the FFmpeg dependencies:
```
sudo add-apt-repository universe

```

If the above command fails you will need to install the following package `software-properties-common`. This can be achieved with the following command `sudo apt-get install software-properties-common`
On Debian, you can also enable the `non-free` components of your base repositories for additional FFmpeg dependencies, but this is optional.
  2. Download the desired `jellyfin-server`, `jellyfin-web`, and `jellyfin-ffmpeg` `.deb` packages from the repository; `jellyfin` is a metapackage and is not required.
  3. Install the downloaded `.deb` packages with `apt` to handle dependency resolution:
```
sudo apt install ./jellyfin-server_*.deb ./jellyfin-web_*.deb ./jellyfin-ffmpeg_*.deb

```

  4. Manage the Jellyfin system service:
```
sudo systemctl {action} jellyfin
sudo service jellyfin {action}

```



[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/installation/advanced/manual.md)
[Previous Synology](https://jellyfin.org/docs/general/installation/advanced/synology)[Next Building from source](https://jellyfin.org/docs/general/installation/advanced/source)
  * [Portable Windows Package](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-package)
    * [Portable Windows Install](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-install)
    * [Portable Windows Update](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-update)
    * [Portable Windows Rollback](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-windows-rollback)
  * [Portable macOS package](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-macos-package)
    * [Installing the Portable macOS Version](https://jellyfin.org/docs/general/installation/advanced/manual/#installing-the-portable-macos-version)
    * [Updating the Portable macOS Version](https://jellyfin.org/docs/general/installation/advanced/manual/#updating-the-portable-macos-version)
    * [Uninstalling the Portable macOS Version](https://jellyfin.org/docs/general/installation/advanced/manual/#uninstalling-the-portable-macos-version)
    * [Using FFmpeg with the Portable macOS Version](https://jellyfin.org/docs/general/installation/advanced/manual/#using-ffmpeg-with-the-portable-macos-version)
  * [Portable Linux install](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-linux-install)
    * [Base Installation Process](https://jellyfin.org/docs/general/installation/advanced/manual/#base-installation-process)
    * [`FFmpeg` Installation](https://jellyfin.org/docs/general/installation/advanced/manual/#ffmpeg-installation)
    * [Running Jellyfin](https://jellyfin.org/docs/general/installation/advanced/manual/#running-jellyfin)
  * [Portable .NET DLL](https://jellyfin.org/docs/general/installation/advanced/manual/#portable-net-dll)
  * [Debian (using extrepo)](https://jellyfin.org/docs/general/installation/advanced/manual/#debian-using-extrepo)
  * [Official Linux Repository (Manual)](https://jellyfin.org/docs/general/installation/advanced/manual/#official-linux-repository-manual)
  * [`.deb` Packages (Very Manual)](https://jellyfin.org/docs/general/installation/advanced/manual/#deb-packages-very-manual)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
