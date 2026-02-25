[Skip to main content](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/)
    * [Setup Wizard Walkthrough](https://jellyfin.org/docs/general/post-install/setup-wizard)
    * [Networking](https://jellyfin.org/docs/general/post-install/networking/)
      * [Tailscale](https://jellyfin.org/docs/general/post-install/networking/tailscale)
      * [Reverse Proxy](https://jellyfin.org/docs/general/post-install/networking/reverse-proxy/)
      * [Advanced Networking](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/)
        * [fail2ban](https://jellyfin.org/docs/general/post-install/networking/advanced/fail2ban)
        * [IPBan](https://jellyfin.org/docs/general/post-install/networking/advanced/ipban)
        * [Let's Encrypt](https://jellyfin.org/docs/general/post-install/networking/advanced/letsencrypt)
        * [Monitoring](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring)
      * [DLNA](https://jellyfin.org/docs/general/post-install/networking/dlna)
    * [Transcoding](https://jellyfin.org/docs/general/post-install/transcoding/)
  * [Administration](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/)
  * [Server Guide](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * Post-Install Setup
  * [Networking](https://jellyfin.org/docs/general/post-install/networking/)
  * Advanced Networking
  * Monitoring


On this page
# Monitoring
Jellyfin has two monitoring and metrics endpoints built-in: a basic health check endpoint and a Prometheus-compatible metrics endpoint.
## Health check endpoint[​](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/#health-check-endpoint "Direct link to Health check endpoint")
The health endpoint will not function as expected while the server is still starting up. Monitoring/ Watchdog programs could therefore kill the server when its running migrations.
Jellyfin exposes the `/health` endpoint designated for checking the status of the underlying service. Currently this will verify HTTP and database connectivity and return a `200 OK` response if successful. You can see this for yourself by using `curl`:
```
curl -i http://myserver:8096/health

```

The `-i` option tells `curl` to also print the HTTP response code and headers.
## Prometheus metrics[​](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/#prometheus-metrics "Direct link to Prometheus metrics")
Jellyfin can make [Prometheus](https://prometheus.io/) metrics available at `/metrics`, but this is turned off by default to avoid unintentionally leaking this information on the public internet. To enable it, you will need to edit `/etc/jellyfin/system.xml` and change this line from `false` to `true`:
```
<EnableMetrics>false</EnableMetrics>

```

If you have a [reverse proxy](https://jellyfin.org/docs/general/post-install/networking/reverse-proxy/) configured, you can configure it to block access to the `/metrics` endpoint except for your internal network.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/post-install/networking/9_advanced/monitoring.md)
[Previous Let's Encrypt](https://jellyfin.org/docs/general/post-install/networking/advanced/letsencrypt)[Next DLNA](https://jellyfin.org/docs/general/post-install/networking/dlna)
  * [Health check endpoint](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/#health-check-endpoint)
  * [Prometheus metrics](https://jellyfin.org/docs/general/post-install/networking/advanced/monitoring/#prometheus-metrics)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
