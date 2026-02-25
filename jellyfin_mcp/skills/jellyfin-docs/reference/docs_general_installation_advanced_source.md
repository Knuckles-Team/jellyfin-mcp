[Skip to main content](https://jellyfin.org/docs/general/installation/advanced/source/#__docusaurus_skipToContent_fallback)
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
    * [Advanced Installation](https://jellyfin.org/docs/general/installation/advanced/source/)
      * [Community Maintained Packages](https://jellyfin.org/docs/general/installation/advanced/community)
      * [Synology](https://jellyfin.org/docs/general/installation/advanced/synology)
      * [Manual Installation](https://jellyfin.org/docs/general/installation/advanced/manual)
      * [Building from source](https://jellyfin.org/docs/general/installation/advanced/source)
      * [TrueNAS SCALE](https://jellyfin.org/docs/general/installation/advanced/truenas)
      * [Kubernetes Deployment](https://jellyfin.org/docs/general/installation/advanced/kubernetes)
  * [Post-Install Setup](https://jellyfin.org/docs/general/installation/advanced/source/)
  * [Administration](https://jellyfin.org/docs/general/installation/advanced/source/)
  * [Server Guide](https://jellyfin.org/docs/general/installation/advanced/source/)
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
  * Building from source


On this page
# Building from source
As an alternative to using binary packages, you can build Jellyfin from source.
Jellyfin supports several methods of building for different platforms and instructions for all supported platforms are below.
All package builds begin with these two steps:
  1. Clone the repository.
```
git clone https://github.com/jellyfin/jellyfin-packaging.git
cd jellyfin-packaging

```

  2. Initialize the submodules.
```
git submodule update --init

```



## Container image[​](https://jellyfin.org/docs/general/installation/advanced/source/#container-image "Direct link to Container image")
  1. Build the container image using Docker or Podman.
```
docker build -t $USERNAME/jellyfin --file docker/Dockerfile .

```

or
```
podman build -t $USERNAME/jellyfin --file docker/Dockerfile .

```

or use provided Python build script:
```
./build.py auto docker

```

Replace "auto" with your own Jellyfin version tag if you want to.
  2. Run Jellyfin in a new container using Docker or Podman from the built container image.
```
docker run -d -p 8096:8096 $USERNAME/jellyfin

```

or
```
podman run -d -p 8096:8096 $USERNAME/jellyfin

```



## Linux or MacOS[​](https://jellyfin.org/docs/general/installation/advanced/source/#linux-or-macos "Direct link to Linux or MacOS")
  1. Use the included `build` script to perform builds.
```
./build --help
./build --list-platforms
./build <platform> all

```

  2. The resulting archives can be found at `../bin/<platform>`.


This will very likely be split out into a separate repository at some point in the future.
## Windows[​](https://jellyfin.org/docs/general/installation/advanced/source/#windows "Direct link to Windows")
  1. Install dotnet SDK 8.0 from [Microsoft's Website](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) and [install Git for Windows](https://gitforwindows.org/). You must be on Powershell 3 or higher.
  2. From Powershell set the execution policy to unrestricted.
```
set-executionpolicy unrestricted

```

  3. If you are building a version of Jellyfin newer than 10.6.4, you will need to download the build script from a separate repository.
```
git clone https://github.com/jellyfin/jellyfin-server-windows.git windows

```

  4. Run the Jellyfin build script.
```
windows\build-jellyfin.ps1 -verbose

```

     * The `-WindowsVersion` and `-Architecture` flags can optimize the build for your current environment; the default is generic Windows x64.
     * The `-InstallLocation` flag lets you select where the compiled binaries go; the default is `$Env:AppData\Jellyfin-Server\`.
     * The `-InstallFFMPEG` flag will automatically pull the stable `ffmpeg` binaries appropriate to your architecture (x86/x64 only for now) from [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases) and place them in your Jellyfin directory.
     * The `-InstallNSSM` flag will automatically pull the stable `nssm` binary appropriate to your architecture (x86/x64 only for now) from [NSSM's Website](https://nssm.cc/) and place it in your Jellyfin directory.
  5. (Optional) Use [NSSM](https://nssm.cc) to configure Jellyfin to run as a service.
  6. Jellyfin is now available in the default directory, or whichever directory you chose.
     * Start it from PowerShell.
```
&"$env:APPDATA\Jellyfin-Server\jellyfin.exe"

```

     * Start it from CMD.
```
%APPDATA%\Jellyfin-Server\jellyfin.exe

```



This will very likely be split out into a separate repository at some point in the future.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/installation/advanced/source.md)
[Previous Manual Installation](https://jellyfin.org/docs/general/installation/advanced/manual)[Next TrueNAS SCALE](https://jellyfin.org/docs/general/installation/advanced/truenas)
  * [Container image](https://jellyfin.org/docs/general/installation/advanced/source/#container-image)
  * [Linux or MacOS](https://jellyfin.org/docs/general/installation/advanced/source/#linux-or-macos)
  * [Windows](https://jellyfin.org/docs/general/installation/advanced/source/#windows)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
