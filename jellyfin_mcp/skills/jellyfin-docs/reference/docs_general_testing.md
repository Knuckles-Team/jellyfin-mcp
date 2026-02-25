[Skip to main content](https://jellyfin.org/docs/general/testing/#__docusaurus_skipToContent_fallback)
[![Jellyfin Logo](https://jellyfin.org/images/logo.svg)](https://jellyfin.org/)
[Blog](https://jellyfin.org/posts)[Downloads](https://jellyfin.org/downloads)[Contribute](https://jellyfin.org/contribute)[Documentation](https://jellyfin.org/docs/)[Contact](https://jellyfin.org/contact)[Forum](https://forum.jellyfin.org)
`ctrl``K`
  * [Introduction](https://jellyfin.org/docs/)
  * [Getting Help](https://jellyfin.org/docs/general/getting-help)
  * [Quick Start](https://jellyfin.org/docs/general/quick-start)
  * [Installation](https://jellyfin.org/docs/general/installation/)
  * [Post-Install Setup](https://jellyfin.org/docs/general/testing/)
  * [Administration](https://jellyfin.org/docs/general/testing/)
  * [Server Guide](https://jellyfin.org/docs/general/testing/)
  * [Clients](https://jellyfin.org/docs/general/clients/)
  * [About Jellyfin](https://jellyfin.org/docs/general/about)
  * [Community Standards](https://jellyfin.org/docs/general/community-standards/)
  * [FAQ](https://jellyfin.org/docs/general/faq)
  * [Contributing](https://jellyfin.org/docs/general/contributing/)
  * [Style Guides](https://jellyfin.org/docs/general/style-guides/)
  * [Testing](https://jellyfin.org/docs/general/testing/)
    * [Upgrades & Downgrades](https://jellyfin.org/docs/general/testing/upgrades)
    * [Testing Jellyfin Server](https://jellyfin.org/docs/general/testing/server/)
    * [Testing Jellyfin Web Clients](https://jellyfin.org/docs/general/testing/web/)
  * [API Documentation](https://api.jellyfin.org)


  * [](https://jellyfin.org/)
  * Testing


On this page
# Testing Jellyfin
In addition to contributing code, testing is also very important for Jellyfin.
## Testing Basics[​](https://jellyfin.org/docs/general/testing/#testing-basics "Direct link to Testing Basics")
Please keep the following things in mind:
  1. Make regular backups. Changes from testing might be irreversible.
  2. Keep everything local. It is generally not a good idea to expose testing environments to the wider internet.
  3. Expect things to break, especially with non-release versions.


## The Testing Process[​](https://jellyfin.org/docs/general/testing/#the-testing-process "Direct link to The Testing Process")
Below is a quick overview of the testing process:
  1. Get a copy of the software to be tested.
  2. Setup the testing environment. (Install software and dependencies)
  3. Perform test(s).
  4. Document and report findings.


## What To Test[​](https://jellyfin.org/docs/general/testing/#what-to-test "Direct link to What To Test")
There are 2 types of items that need to be tested on Jellyfin:
  1. Testing for general bugs. This means trying to find new, previously unknown bugs.
  2. Reproduction of unconfirmed issues. This means trying to reproduce issues someone else has reported.


### Testing for General Bugs[​](https://jellyfin.org/docs/general/testing/#testing-for-general-bugs "Direct link to Testing for General Bugs")
To test for general bugs, use Jellyfin normally, or try to come up with edge cases that you think might break Jellyfin and / or edge cases that have broken other pieces of software before. If you have successfully broken Jellyfin, congratulations! You might have found a previously unknown bug.
### Reproducing Unconfirmed Issues[​](https://jellyfin.org/docs/general/testing/#reproducing-unconfirmed-issues "Direct link to Reproducing Unconfirmed Issues")
To test for unconfirmed issues, start by browsing the GitHub Issue Tracker. Any issue that hasn't been labeled `confirmed` means that it hasn't been confirmed yet. Testing issues that have been marked `confirmed` but hasn't been tested since the last major release would also be helpful. Find an issue that you have the necessary hardware / software to reproduce, and have fun!
## Reporting Test Findings[​](https://jellyfin.org/docs/general/testing/#reporting-test-findings "Direct link to Reporting Test Findings")
To report test findings, start by going to the GitHub Issue Tracker of the respective component. What you would do next depends entirely on what is being tested.
### Reporting General Bugs[​](https://jellyfin.org/docs/general/testing/#reporting-general-bugs "Direct link to Reporting General Bugs")
Start by searching the issue tracker for similar issues. If you believe an issue is a duplicate to an open issue, comment your findings there. Otherwise, open a new issue report following the template of the specific repo. Please remember to follow **ALL** instructions on the template to avoid problems with other people. After you have submitted the report, the Jellyfin Triage Team will tell you what to do next.
### Successful Reproduction of Unconfirmed Issue[​](https://jellyfin.org/docs/general/testing/#successful-reproduction-of-unconfirmed-issue "Direct link to Successful Reproduction of Unconfirmed Issue")
If you have successfully reproduced an unconfirmed issue, please comment your findings, along with reproduction steps you have taken and exact details of your setup. They should be as detailed as possible. Once the Jellyfin Triage Team reviews your report, the issue may be marked confirmed if no further info is required.
### Unsuccessful Reproduction of Unconfirmed Issue[​](https://jellyfin.org/docs/general/testing/#unsuccessful-reproduction-of-unconfirmed-issue "Direct link to Unsuccessful Reproduction of Unconfirmed Issue")
If you have attempted to reproduce an unconfirmed issue but failed to do so, also comment on the original issue. The Jellyfin Triage Team might close the issue or ask for further feedback from another user.
[](https://github.com/jellyfin/jellyfin.org/edit/master/docs/general/testing/index.md)
[Previous JavaScript](https://jellyfin.org/docs/general/style-guides/javascript)[Next Upgrades & Downgrades](https://jellyfin.org/docs/general/testing/upgrades)
  * [Testing Basics](https://jellyfin.org/docs/general/testing/#testing-basics)
  * [The Testing Process](https://jellyfin.org/docs/general/testing/#the-testing-process)
  * [What To Test](https://jellyfin.org/docs/general/testing/#what-to-test)
    * [Testing for General Bugs](https://jellyfin.org/docs/general/testing/#testing-for-general-bugs)
    * [Reproducing Unconfirmed Issues](https://jellyfin.org/docs/general/testing/#reproducing-unconfirmed-issues)
  * [Reporting Test Findings](https://jellyfin.org/docs/general/testing/#reporting-test-findings)
    * [Reporting General Bugs](https://jellyfin.org/docs/general/testing/#reporting-general-bugs)
    * [Successful Reproduction of Unconfirmed Issue](https://jellyfin.org/docs/general/testing/#successful-reproduction-of-unconfirmed-issue)
    * [Unsuccessful Reproduction of Unconfirmed Issue](https://jellyfin.org/docs/general/testing/#unsuccessful-reproduction-of-unconfirmed-issue)


[Documentation](https://jellyfin.org/docs)·[Feature Requests](https://features.jellyfin.org)·[Contribute](https://jellyfin.org/contribute)·[Status](https://status.jellyfin.org)·[Contact](https://jellyfin.org/contact)
![Jellyfin Logo](https://jellyfin.org/images/logo.svg)
[ ![Current Release](https://img.shields.io/github/release/jellyfin/jellyfin.svg) ](https://github.com/jellyfin/jellyfin/releases/latest)
Site content is licensed [CC-BY-ND-4.0](http://creativecommons.org/licenses/by-nd/4.0/)
