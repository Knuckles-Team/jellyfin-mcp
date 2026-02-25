[Skip to main content](https://jellyfin.org/docs/general/installation/advanced/synology/#__docusaurus_skipToContent_fallback)
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
    * [Advanced Installation](https://jellyfin.org/docs/general/installation/advanced/synology/)
      * [Community Maintained Packages](https://jellyfin.org/docs/general/installation/advanced/community)
      * [Synology](https://jellyfin.org/docs/general/installation/advanced/synology)
      * [Manual Installation](https://jellyfin.org/docs/general/installation/advanced/manual)
      * [Building from source](https://jellyfin.org/docs/general/installation/advanced/source)
      * [TrueNAS SCALE](https://jellyfin.org/docs/general/installation/advanced/truenas)
      * [Kubernetes Deployment](https://jellyfin.org/docs/general/installation/advanced/kubernetes)
  * [Post-Install Setup](https://jellyfin.org/docs/general/installation/advanced/synology/)
  * [Administration](https://jellyfin.org/docs/general/installation/advanced/synology/)
  * [Server Guide](https://jellyfin.org/docs/general/installation/advanced/synology/)
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
  * Synology


On this page
# Installation on Synology
Many pre-built NAS devices are underpowered. We generally do not recommend running Jellyfin on those devices. See: [Hardware Selection](https://jellyfin.org/docs/general/administration/hardware-selection) for more information.
For [Synology](https://www.synology.com/en-us/dsm), Jellyfin is installed using Docker. In this guide, the Synology Container Manager will be used to install Jellyfin.
## Prerequisites[​](https://jellyfin.org/docs/general/installation/advanced/synology/#prerequisites "Direct link to Prerequisites")
Everything is done through the Synology web interface. This guide assumes you have already set up your Synology NAS and have access to the web interface. And your Synology NAS is running DSM 7.0 or newer. Install the "Container Manager" package from the Synology Package Center. Open the Package Center and search for "Container Manager" to find the package. For further information read this [guide](https://kb.synology.com/en-global/DSM/help/DSM/PkgManApp/install_buy?version=7).
The creation and initialization of a volume will not be touched in this guide. Further information is provided by [Synology](https://kb.synology.com/en-global/DSM/help/DSM/StorageManager/volume_create_volume?version=7)
## Installation[​](https://jellyfin.org/docs/general/installation/advanced/synology/#installation "Direct link to Installation")
The installation is done with the Synology Container Manager. If you don't see the icon in the main menu after the installation of `Container Manager`, it can be found by clicking the top left corner of the main menu.
### Downloading the Jellyfin Image[​](https://jellyfin.org/docs/general/installation/advanced/synology/#downloading-the-jellyfin-image "Direct link to Downloading the Jellyfin Image")
Navigate to the "Registry" tab and search for "Jellyfin". You should see the official jellyfin/jellyfin image. Click on it and then click "Download".
![Downloading the Image](https://jellyfin.org/assets/images/install-synology-0-97c909d74d308a9d6811bd630528f577.png)
A new window will open and a Jellyfin version can be selected for installation. The latest version is recommended. Click `Apply` after selection a version.
![Downloading the Image](https://jellyfin.org/assets/images/install-synology-1-e4b2ef30abf77106bf76ff4d43416092.png)
After the image is downloaded, it can be found in the `Image` tab.
### Creating the Container[​](https://jellyfin.org/docs/general/installation/advanced/synology/#creating-the-container "Direct link to Creating the Container")
Navigate to the `Container` tab and click `Create`. Select the `Jellyfin` image and give the container a name. This is mainly for identification purposes and can be set to anything desired. `auto-restart` can be enabled to automatically start Jellyfin when the NAS boots. Resource limits can also be set for the container. It is recommended that all CPU resources and at least 4GB of ram be allocated to the Jellyfin container. Click `Next` to proceed to the next step. ![Creating the Container](https://jellyfin.org/assets/images/install-synology-2-d1fa42c5c52fbd6f1c3048c0f0bcbc16.png)
#### Network and Port Settings[​](https://jellyfin.org/docs/general/installation/advanced/synology/#network-and-port-settings "Direct link to Network and Port Settings")
For the [Network Settings](https://jellyfin.org/docs/general/post-install/networking/dlna#general) and [Port Settings](https://jellyfin.org/docs/general/post-install/networking/#port-bindings) please refer their respected guides.
#### Volume Settings[​](https://jellyfin.org/docs/general/installation/advanced/synology/#volume-settings "Direct link to Volume Settings")
This setting maps, directories on the host within the container. Use this setting to allow Jellyfin access to media and a place to store application data. To add a volume, click "Add Folder" and select the folder desired. The mount point is set in the middle column and the directory will be accessible at this path within the container. For media files, `/media` can be used, and for config files, `/config` can be used.
#### Example[​](https://jellyfin.org/docs/general/installation/advanced/synology/#example "Direct link to Example")
Your settings should look like this: ![Advanced Settings](https://jellyfin.org/assets/images/install-synology-3-40f0d860b472dd20ebd81fb266efd912.png) ![Advanced Settings](https://jellyfin.org/assets/images/install-synology-4-0ab060e18fd687ba7c582cd978ac062d.png) Click `Next` to proceed to the next step.
Settings can be reviewed on this screen. Check the `Run this container after the wizard is finished` checkbox and click `Apply` if everything looks correct. The container should now be shown in the `Container` tab. Browse to `http://SERVER_IP:8096` in a browser on a other device to finish setting up the Jellyfin server. If a different port was used, replace `8096` with the port used instead.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/installation/advanced/synology.md)
[Previous Community Maintained Packages](https://jellyfin.org/docs/general/installation/advanced/community)[Next Manual Installation](https://jellyfin.org/docs/general/installation/advanced/manual)
  * [Prerequisites](https://jellyfin.org/docs/general/installation/advanced/synology/#prerequisites)
  * [Installation](https://jellyfin.org/docs/general/installation/advanced/synology/#installation)
    * [Downloading the Jellyfin Image](https://jellyfin.org/docs/general/installation/advanced/synology/#downloading-the-jellyfin-image)
    * [Creating the Container](https://jellyfin.org/docs/general/installation/advanced/synology/#creating-the-container)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
