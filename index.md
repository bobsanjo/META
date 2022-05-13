---
layout: single
sidebar:
  nav: docs
---

MetaBuild is a distributed C++ package manager and project generator.

**Note:** If you see broken links or other issues in this website, please report it via [JIRA](https://jira.corp.adobe.com/projects/METAB/issues) and notify us in the #metabuild slack channel. Alternatively, you can [send us a PR]({{ site.baseurl }}{% link _docs/faq/common_questions.md %}#how-can-i-contribute-to-metabuild-docs) for the fix.
{: .notice--warning}


## Getting Started

Start from the [MetaBuild Tutorial]({{ site.baseurl }}{% link _docs/tutorial/main.md %}) page.

## Goals

1.  Written in portable Python 3.8+ code.

2.  Python based syntax for the MetaBuild files. The builder commands are as close as possible to [Buck](http://buck.build/) from Facebook.

3.  Compile all of the C++ code from source and allow sharing external C++ dependencies without duplication.

4.  Unlike [Buck](http://buck.build/), `MetaBuild` doesn't actually drive the compilation of the C++ code:
    - Generates native Xcode and Visual Studio projects.
    - Generates CMake files for Android and Linux.

5.  Supported external dependencies:
    - download via HTTP/S
    - download from Artifactory
    - download code straight out of GIT

6.  `MetaBuild` is fast:
    - cache downloads from remote
    - cache extracted dependencies
    - allow shallow git clones of external repos with lots of history
    - allow local linking of external dependencies for local development


## Links

- Public:
    - [MetaBuild website](https://git.corp.adobe.com/pages/meta-build/).
    - MetaBuild Slack Channel: #metabuild
    - [MetaBuild JIRA (near future tasks)](https://jira.corp.adobe.com/browse/METAB-722)
    - [MetaBuild JIRA (current sprint)](https://jira.corp.adobe.com/secure/RapidBoard.jspa?projectKey=METAB&rapidView=30422)
    - [MetaBuild Wiki](https://wiki.corp.adobe.com/display/metab/Welcome+to+MetaBuild): Deprecated, please prefer to use the MetaBuild website.
- Code:
    - [MetaBuild](https://git.corp.adobe.com/meta-build/meta-build) source code.
    - [meta-libs](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs) repo, package management.
    - [meta-samples](https://git.corp.adobe.com/meta-samples) org, some meta-build examples.
    - [meta-specs](https://git.corp.adobe.com/meta-specs) org, meta.py files for external repos.
    - [meta-archives](https://git.corp.adobe.com/meta-archives) org, mirror of external repos. Longterm vision is to unify it with Photoshop's [counterpart](https://git.corp.adobe.com/thirdparty/).
    - [meta-archives](https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/) artifactory repo, data storage for MetaBuild itself and the external repos in meta-specs.
- MetaBuild developers:
    - MetaBuild development Slack Channel: #metabuild-dev
    - MetaBuild development outlook group: Grp-metabuild-dev (metabuild-dev@outlook.com). Use for Canlendar invites or PTO announcements.
    - [MetaBuild notebook](https://adobe-my.sharepoint.com/personal/hoshyari_adobe_com/_layouts/15/Doc.aspx?sourcedoc={be8dd1f3-2af1-4f0e-8241-c2fe89104a0c}&action=edit&wd=target%28Links.one%7Ca75daa6b-5832-4315-8466-99aad7aa27ac%2FReadme%7Cb6e920ed-71ee-417f-bf8e-0aac09f1099f%2F%29&wdorigin=703): Internal MetaBuild developer discussions.
    - [MetaBuild Lucid Charts](https://lucid.app/folder/invitations/accept/inv_3d923a0b-da62-4ea4-b1ab-28771e5c2783): Complements the notebook. For drawings.



## Team


| Name || Position |
| -------- |----------| ---------- |
| Alexandru Chiculita || Consultant (founder and former lead) |
| Shayan Hoshyari || Lead Developer |
| Jakub Plichta || Engineering Manager |
| Randy Pun || Devops and QE |
| Terry Ridgeway || Devops and QE |
| [Open position](https://wd5.myworkday.com/adobe/d/inst/15$158872/9925$130222.htmld) || Software Development Engineer |
|| User Representatives ||
| Mike Baldus || Aero |
| Bob Gardner || Photoshop |
| Florin Trofin || DVA |
| Charles Pina, Nik Svakhin || Stager |
| Let us know about your team || ... |
|| Alumni ||
| Claudiu Milea || Software Development Engineer |
| Panneerselvam Varatharajan || Software Development Engineer |
| Sarah Wong || Software Development Engineer |
| Muddsar Jamil || Engineering Manager |
