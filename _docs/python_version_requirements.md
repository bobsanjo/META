---
permalink: /docs/python_version_requirements/
title: "Python Version Requirements"
---

Supporting old python versions places extra workload on MetaBuild development. Especially, when it comes to dealing with issues of older python versions, and testing. Given that updating to newer versions of python is a much easier task, we have decided to adopt a python version support strategy. We will drop support for older python versions and switch to latest stable python in a pre-defined schedule. 

Please ensure to upgrade the version of the python that you use in your build infrastructure and CI to the minimum supported version by the dates indicated below.

| Date Range| Supported Versions of Python |
|-----------|---------|
|2021-08 - 2023-01     | >= 3.8  |
|2023-01 - ...   | >= 3.10 |

Note that there are many easy ways to manage versions of python. For example, [conda]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}).

> Some users need to build native python modules (dlls that can be loaded by python) that need linking against the python library with separate version requirements. In this case, you should keep the python(s) used for linking separate from the python that drives the build toolchain and CI in which MetaBuild is installed. In addition to decoupling requirements, this will also allow you to build your native module for different python versions at no extra cost. For example, the [stager](https://git.corp.adobe.com/euclid/stager/blob/release/1.1.1/META/META.lock#L138-L142) application uses a dedicate python to link their native module against.
