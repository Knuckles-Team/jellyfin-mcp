[Skip to main content](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/)
    * [Setup Wizard Walkthrough](https://jellyfin.org/docs/general/post-install/setup-wizard)
    * [Networking](https://jellyfin.org/docs/general/post-install/networking/)
    * [Transcoding](https://jellyfin.org/docs/general/post-install/transcoding/)
      * [Hardware Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/)
        * [AMD GPU](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/amd)
        * [Apple Mac](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/apple)
        * [Intel GPU](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/intel)
        * [Known Issues](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/known-issues)
        * [NVIDIA GPU](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/nvidia)
        * [Rockchip VPU](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/rockchip)
      * [Stereo Downmix](https://jellyfin.org/docs/general/post-install/transcoding/downmix)
  * [Administration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/)
  * [Server Guide](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/)
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
  * [Transcoding](https://jellyfin.org/docs/general/post-install/transcoding/)
  * Hardware Acceleration


On this page
# Hardware Acceleration
The Jellyfin server can offload on the fly video transcoding by utilizing an integrated or discrete graphics card ([GPU](https://en.wikipedia.org/wiki/Graphics_processing_unit)) suitable to accelerate this workloads very efficiently without straining your CPU.
## Supported Acceleration Methods[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#supported-acceleration-methods "Direct link to Supported Acceleration Methods")
The Jellyfin server uses a modified version of [FFmpeg](http://ffmpeg.org/) as its transcoder, namely [jellyfin-ffmpeg](https://github.com/jellyfin/jellyfin-ffmpeg). It enables the Jellyfin server to access the fixed-function video codecs, video processors and [GPGPU](https://en.wikipedia.org/wiki/General-purpose_computing_on_graphics_processing_units) computing interfaces provided by vendor of the installed GPU and the operating system.
The supported and validated video [hardware acceleration (HWA)](https://trac.ffmpeg.org/wiki/HWAccelIntro) methods are:
  * **Intel** Quick Sync Video (QSV)
  * **NVIDIA** NVDEC/NVENC (NVENC)
  * **AMD** Advanced Media Framework (AMF)
  * **Intel/AMD** Video Acceleration API (VA-API, Linux only)
  * **Apple** Video Toolbox (macOS only)
  * **Rockchip** RKMPP (Linux only)


## Full & Partial Acceleration[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#full--partial-acceleration "Direct link to Full & Partial Acceleration")
The transcoding pipeline usually has multiple stages, which can be simplified to:
  * Video Decoding
  * Video Deinterlacing (optional)
  * Video Scaling & Format conversion (optional)
  * Video HDR/DV Tone-mapping (optional)
  * Video Subtitle burn-in (optional)
  * Video Encoding
  * Zero-copy in above stages


Some of these stages cannot be GPU accelerated due to software, hardware or driver limitations.
Partial acceleration may result in higher CPU usage and lower transcoding speed.
Jellyfin supports full acceleration for:
  * Mainstream Intel and Nvidia GPUs on Windows and Linux
  * AMD Polaris and newer GPUs on Linux via VA-API and Vulkan interop
  * Older AMD GPUs on Windows
  * Rockchip VPU of RK3588/3588S
  * Intel and Apple Silicon on macOS 12 and above


Using [jellyfin-ffmpeg](https://github.com/jellyfin/jellyfin-ffmpeg/releases) with Jellyfin is highly recommended, which has a `-Jellyfin` suffix in the version string.
```
$ /usr/lib/jellyfin-ffmpeg/ffmpeg

ffmpeg version 6.0.1-Jellyfin Copyright (c) 2000-2023 the FFmpeg developers
  built with gcc 12.2.0 (crosstool-NG 1.25.0.90_cf9beb1)
...

```

Using FFmpeg binaries downloaded from somewhere else will result in partial acceleration.
Jellyfin-ffmpeg usually ships with our deb package, official Docker images and Windows installers.
The only exception is when using a portable installation or an unsupported distro, then it's required to manually download and set it in Jellyfin.
## Configure & Verify Hardware Acceleration[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#configure--verify-hardware-acceleration "Direct link to Configure & Verify Hardware Acceleration")
There are some preparations that need to be done before enabling hardware acceleration.
The specific configuration steps may vary between GPU vendors, installation methods, and operating systems.
On Linux you can check available GPU using the `lspci` command:
```
lspci -nn | grep -Ei "3d|display|vga"

```

Or using `lshw`:
```
lshw -C display

```

See the table below to pick the best hardware acceleration method for your hardware:
GPU Vendor | Windows | macOS | Linux
---|---|---|---
AMD | [AMF (Windows)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/amd#windows-setups) | [VideoToolbox](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/apple) | [VAAPI (AMD)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/amd#linux-setups)
Apple | N/A | [VideoToolbox](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/apple) | N/A
Intel | [QSV (Windows)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/intel#windows-setups) | [VideoToolbox](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/apple) | [QSV (Linux)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/intel#linux-setups)
Nvidia | [NVENC (Windows)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/nvidia#windows-setups) | N/A | [NVENC (Linux)](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/nvidia#linux-setups)
Rockchip | N/A | N/A | [RKMPP](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/rockchip)
## Remote Hardware Acceleration[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#remote-hardware-acceleration "Direct link to Remote Hardware Acceleration")
If your Jellyfin server does not support hardware acceleration, but you have another machine that does, you can leverage [rffmpeg](https://github.com/joshuaboniface/rffmpeg) to delegate the transcoding to another machine.
Currently Linux-only and requires SSH between the machines, as well as shared storage for media and the Jellyfin data directory.
## Hardware Accelerated Tone-mapping[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#hardware-accelerated-tone-mapping "Direct link to Hardware Accelerated Tone-mapping")
Jellyfin supports hardware accelerated tone-mapping of HDR10 and HLG to SDR.
Dolby Vision (P5 & P8) to SDR tone-mapping is supported in Jellyfin 10.8 and requires jellyfin-ffmpeg 5.0.1-5 or newer.
  * Intel VPP HDR10 tone-mapping is supported on Intel QSV and VA-API on Linux.
  * VPP is preferred if both tone-mapping options are enabled.
  * Rockchip RKMPP does support Dolby Vision tone-mapping Jellyfin 10.11 and later versions.


## Tips For Hardware Acceleration[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#tips-for-hardware-acceleration "Direct link to Tips For Hardware Acceleration")
  * Avoid H.264 / AVC 10-bit videos
The hardware decoding of H.264 / AVC 10-bit (High 10 profile) video is not supported by any Intel, NVIDIA and AMD GPU. It is only supported by Apple Silicon and Rockchip. Jellyfin will fall back to software decoding for it when there is no hardware decoder available. Consider upgrading such video to H.265 / HEVC 10-bit (Main 10 profile).
  * iGPU / APU Prefer dual-channel memory
Integrated GPUs take up a portion of system memory as their video memory, which means using dual-channel memory can double the video memory bandwidth. This can be useful while computing intensive workloads such as hardware HDR/DV tone-mapping.
  * Use SSD or RamDisk for caching
On modern GPUs the peak throughput of video transcoding can be limited by the I/O speed of your hard drives. In this case, an SSD or RamDisk can be used for caching the transcoded temporary video segments.
  * Tune encoder presets to trade off quality for speed
Hardware encoder presets can greatly affect encoding speed. You can lower this preset in the Jellyfin dashboard to sacrifice encoding quality to maximize speed, or raise the preset to optimize encoding quality on an overkill GPU.


## Raspberry Pi Hardware Acceleration Support Deprecation[​](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#raspberry-pi-hardware-acceleration-support-deprecation "Direct link to Raspberry Pi Hardware Acceleration Support Deprecation")
Jellyfin previously supported hardware acceleration on Raspberry Pi via `OpenMAX OMX` in Jellyfin 10.8, with partial support for Raspberry Pi via `V4L2` in 10.9. However, the support never reached the level of maturity seen with other acceleration methods. Many operations fell back to the already underperforming CPU, due to the lacking of full hardware acceleration. The situation worsened with the release of the latest generation of Raspberry Pi 5, which lacks hardware encoders entirely, rendering further development of hardware acceleration on this platform impractical.
As a result, we have to deprecate `V4L2` support for Raspberry Pi, unfortunately. While it may continue to work for now, future updates to the Linux kernel or FFmpeg could break this support, and it's unlikely that we'll address any resulting issues. This decision may be reversed if future Raspberry Pi models reintroduce hardware encoders.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/post-install/transcoding/hardware-acceleration/index.md)
[Previous Transcoding](https://jellyfin.org/docs/general/post-install/transcoding/)[Next AMD GPU](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/amd)
  * [Supported Acceleration Methods](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#supported-acceleration-methods)
  * [Full & Partial Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#full--partial-acceleration)
  * [Configure & Verify Hardware Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#configure--verify-hardware-acceleration)
  * [Remote Hardware Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#remote-hardware-acceleration)
  * [Hardware Accelerated Tone-mapping](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#hardware-accelerated-tone-mapping)
  * [Tips For Hardware Acceleration](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#tips-for-hardware-acceleration)
  * [Raspberry Pi Hardware Acceleration Support Deprecation](https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/#raspberry-pi-hardware-acceleration-support-deprecation)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
