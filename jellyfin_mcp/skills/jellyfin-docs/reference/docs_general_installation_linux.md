[Skip to main content](https://jellyfin.org/docs/general/installation/linux/#__docusaurus_skipToContent_fallback)
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
    * [Advanced Installation](https://jellyfin.org/docs/general/installation/linux/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/installation/linux/)
  * [Administration](https://jellyfin.org/docs/general/installation/linux/)
  * [Server Guide](https://jellyfin.org/docs/general/installation/linux/)
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
  * Linux


On this page
# Linux
## Debian / Ubuntu and derivatives[​](https://jellyfin.org/docs/general/installation/linux/#debian--ubuntu-and-derivatives "Direct link to Debian / Ubuntu and derivatives")
To simplify deployment and help automate this for as many users as possible, we provide a BASH script to handle repo installation as well as installing Jellyfin on Debian / Ubuntu and derivatives. All you need to do is run this command on your system (requires `curl`, or substitute `curl` with `wget -O-`):
```
curl https://repo.jellyfin.org/install-debuntu.sh | sudo bash

```

You can verify the script download integrity with (requires `sha256sum`):
```
diff <( curl -s https://repo.jellyfin.org/install-debuntu.sh -o install-debuntu.sh; sha256sum install-debuntu.sh ) <( curl -s https://repo.jellyfin.org/install-debuntu.sh.sha256sum )

```

An empty output means everything is correct. Then you can inspect the script to see what it does (optional but recommended) and execute it with:
```
less install-debuntu.sh
sudo bash install-debuntu.sh

```

The script tries to handle as many common derivatives as possible, including, at least, Linux Mint (Ubuntu and Debian editions), Raspbian/Raspberry Pi OS, and KDE Neon. We welcome PRs [to the script](https://github.com/jellyfin/jellyfin-repo-helper-scripts/blob/master/install-debuntu.sh) for any other common derivatives.
## Other Distributions[​](https://jellyfin.org/docs/general/installation/linux/#other-distributions "Direct link to Other Distributions")
For other distributions, [containers](https://jellyfin.org/docs/general/installation/container) are the recommended way to install Jellyfin. There are also [community-maintained packages](https://jellyfin.org/docs/general/installation/advanced/community) provided by 3rd parties if you would like to use them instead.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/installation/linux.md)
[Previous macOS](https://jellyfin.org/docs/general/installation/macos)[Next Container](https://jellyfin.org/docs/general/installation/container)
  * [Debian / Ubuntu and derivatives](https://jellyfin.org/docs/general/installation/linux/#debian--ubuntu-and-derivatives)
  * [Other Distributions](https://jellyfin.org/docs/general/installation/linux/#other-distributions)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
