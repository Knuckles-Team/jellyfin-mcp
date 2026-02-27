[Skip to main content](https://jellyfin.org/docs/general/clients/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/clients/)
  * [Administration](https://jellyfin.org/docs/general/clients/)
  * [Server Guide](https://jellyfin.org/docs/general/clients/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
    * [Codec Support](https://jellyfin.org/docs/general/clients/codec-support)
    * [CSS Customization](https://jellyfin.org/docs/general/clients/css-customization)
    * [Jellyfin Vue](https://jellyfin.org/docs/general/clients/jellyfin-vue)
    * [Kodi](https://jellyfin.org/docs/general/clients/kodi)
    * [Mopidy](https://jellyfin.org/docs/general/clients/mopidy)
    * [Jellyfin Web Configuration](https://jellyfin.org/docs/general/clients/web-config)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * Clients


On this page
# Clients
Clients connect your devices to your Jellyfin server and let you view your content on any supported device.
If you are interested in helping out, please see our [contribution guide](https://jellyfin.org/docs/general/contributing) and feel free to [contact us](https://jellyfin.org/contact) for more information!
## Client List[​](https://jellyfin.org/docs/general/clients/#client-list "Direct link to Client List")
A list of all Jellyfin clients can be found on the main [Clients page](https://jellyfin.org/downloads/clients).
Some clients that are no longer maintained can be found in the [jellyfin-archive organization on GitHub](https://github.com/jellyfin-archive).
Do you have a client that interfaces with Jellyfin and want to see it listed on the Clients page? Please verify it meets the requirements below and [submit a pull request](https://github.com/jellyfin/jellyfin.org/edit/master/src/data/clients.ts)!
### Requirements for Inclusion in All Clients[​](https://jellyfin.org/docs/general/clients/#requirements-for-inclusion-in-all-clients "Direct link to Requirements for Inclusion in All Clients")
Clients must meet the following guidelines for inclusion in the list of all clients:
  * Must be aligned with the [Jellyfin Community Standards](https://jellyfin.org/docs/general/community-standards).
    * In particular, the client must **NOT** engage in, encourage, or facilitate piracy.
    * The developer must be in good community standing in accordance to the Community Standards.
  * Must adhere to the [Jellyfin Branding Guidelines](https://jellyfin.org/docs/general/contributing/branding), including usage of the Jellyfin name, trademarks and icons.
    * This includes usage of the Jellyfin name or `org.jellyfin` namespace that could hinder the ability to publish an official client to a store in the future.
  * Must include first rate support for Jellyfin servers. (i.e. Support for Jellyfin should be a primary function or at the same level of integration of any other supported services.)
  * Must **NOT** be specific to or intended to promote a specific hosted Jellyfin server instance.
  * Must have clear licensing and be void of any known issues related to attribution, copyright, or license violations.


The final decision for inclusion is at the discretion of the Jellyfin Contributor Team following the decision-making guidelines in the [Jellyfin Constitution](https://github.com/jellyfin/jellyfin-meta/blob/master/policies-and-procedures/jellyfin-constitution.md).
### Requirements for Inclusion as a Recommended Client[​](https://jellyfin.org/docs/general/clients/#requirements-for-inclusion-as-a-recommended-client "Direct link to Requirements for Inclusion as a Recommended Client")
  * The client must be a first-party client (meaning published and maintained by the Jellyfin team with source freely licensed and available in the [Jellyfin GitHub organization](https://github.com/jellyfin)).
**OR**
  * The client must fill a significant void in the current first-party client offerings. Must be a high-quality client on a popular platform.


### Removal from the clients list[​](https://jellyfin.org/docs/general/clients/#removal-from-the-clients-list "Direct link to Removal from the clients list")
We strive to maintain an up-to-date and accurate client list; however, we do not wish to remove clients without just cause. To ensure the integrity and relevance of the client list, we will conduct regular maintenance. The Jellyfin team reserves the right to remove any listed client at any time.
Typically, a client will be removed if any of the following criteria are met:
  * The client no longer fulfills the inclusion criteria outlined above.
  * The client is no longer maintained or does not support the latest stable version of the Jellyfin server.
  * The client is malfunctioning (key features are not operating correctly).


In general, the team will attempt to contact the maintainers of a listed client prior to removal. However, if this is not feasible (e.g., the maintainers cannot be reached), the team may proceed with removal without prior notice.
Additionally, there are situations where contacting maintainers is unnecessary, such as in cases of malware distribution or violations of community guidelines. In these instances, clients will be removed from the list without notification.
## Supported Browsers[​](https://jellyfin.org/docs/general/clients/#supported-browsers "Direct link to Supported Browsers")
Our goal is to provide support for the two most recent versions of these browsers.
  * Firefox
  * Firefox ESR
  * Chrome
  * Chrome for Android
  * Safari for MacOS and iOS
  * Edge


Older browsers may be supported as a result of the needs of specific web-based clients, but full functionality is not guaranteed on their desktop version.
## Additional Client Documentation[​](https://jellyfin.org/docs/general/clients/#additional-client-documentation "Direct link to Additional Client Documentation")
## [📄️ Codec Support The goal is to Direct Play all media. This means the container, video, audio and subtitles are all compatible with the client. If the media is incompatible for any reason, Jellyfin will use FFmpeg to convert the media to a format that the client can process. Direct Stream will occur if the audio, container or subtitles happen to not be supported. If the video codec is unsupported, this will result in video transcoding. Subtitles can be tricky because they can cause Direct Stream (subtitles are remuxed) or video transcoding (burning in subtitles) to occur. This is the most intensive CPU component of transcoding. Decoding is less intensive than encoding.](https://jellyfin.org/docs/general/clients/codec-support)## [📄️ CSS Customization In Dashboard > General, the "Custom CSS" field can be used to override current CSS in Jellyfin's stylesheet.](https://jellyfin.org/docs/general/clients/css-customization)## [📄️ Jellyfin Vue Jellyfin Vue is an experimental, alternative browser-based web client for Jellyfin written using Vue.js.](https://jellyfin.org/docs/general/clients/jellyfin-vue)## [📄️ Kodi Add-on Repository](https://jellyfin.org/docs/general/clients/kodi)## [📄️ Mopidy The Mopidy Jellyfin extension is available to install from PyPi using pip.](https://jellyfin.org/docs/general/clients/mopidy)## [📄️ Jellyfin Web Configuration Editing](https://jellyfin.org/docs/general/clients/web-config)
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/clients/index.mdx)
[Previous Managing Users](https://jellyfin.org/docs/general/server/users/adding-managing-users)[Next Codec Support](https://jellyfin.org/docs/general/clients/codec-support)
  * [Client List](https://jellyfin.org/docs/general/clients/#client-list)
    * [Requirements for Inclusion in All Clients](https://jellyfin.org/docs/general/clients/#requirements-for-inclusion-in-all-clients)
    * [Requirements for Inclusion as a Recommended Client](https://jellyfin.org/docs/general/clients/#requirements-for-inclusion-as-a-recommended-client)
    * [Removal from the clients list](https://jellyfin.org/docs/general/clients/#removal-from-the-clients-list)
  * [Supported Browsers](https://jellyfin.org/docs/general/clients/#supported-browsers)
  * [Additional Client Documentation](https://jellyfin.org/docs/general/clients/#additional-client-documentation)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
