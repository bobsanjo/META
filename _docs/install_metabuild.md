---
permalink: /docs/install_metabuild/
title: "Install MetaBuild"
toc: true
---


> For minimum python version restrictions, please see the [Python Version Requirements]({{ site.baseurl }}{% link _docs/python_version_requirements.md %}) page.

## Install Python

Here, we offer several methods to install python. We recommend using `conda` as it is the most versatile method, and does not need any `sudo` or `administrator` access to your machine.

Note that Xcode 11 or higher and recent versions of MSVS come with their bundled Python3. These distributions of Python could be incomplete. Do not use them to run MetaBuild.

### Conda (Windows, Linux, and Mac)

See [Using Conda]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}). Conda can install both python and MetaBuild at the same time.

### Using Homebrew (only Mac)


1. Install Homebrew - [brew.sh](https://brew.sh/)
2. Run `brew install python`

### Using Global Installer

- Windows:
  - download and install latest Python3 from [python.org](https://www.python.org/downloads/).
- MacOS:
  - Download and install latest Python3 from [python.org](https://www.python.org/downloads/)
  - Run `pip3 install --upgrade certifi` 

**NOTE** Please use 64bit version of Python for Windows. MetaBuild is only supported on 64bit.
{: .notice--warning}

## Install MetaBuild

Jenkins Page: [![Build Status](https://torq.ci.corp.adobe.com:12001/job/Meta%20Build/job/meta-build/job/main/badge/icon)](https://torq.ci.corp.adobe.com:12001/job/Meta%20Build/job/meta-build/job/main/)

If you used the guides on [Conda]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}) it will install both Python and MetaBuild for you and you don't need any additional step. Otherwise, you can use one of the following approaches to install MetaBuild.

### Installing in a virtual environment

You should always install MetaBuild in a virtual env. Installing python packages that have executable entry points with `pip` globally is fragile and thus not supported by MetaBuild team. First create a python virtual env and activate it:

- Mac and Linux
  ```sh
  python3 -m venv .venv
  . .venv/bin/activate
  ```
- Windows (powershell)
  ```
  py -3 -m venv .venv
  & .venv/scripts/activate.ps1
  ```
- Windows (cmd)
  ```
  py -3 -m venv .venv
  call .venv/scripts/activate
  ```

Note that `.venv` is simply a path to create the virtual environment at. You can replace it with any other path. Once the virtual env is activated, all the installed python packages will go to `.venv/` instead of getting installed globally. Also, the executable `python` will now refer to `python3`.

To disable the virtual env, simply type `deactivate`, or just open a new terminal window. If you open a new tab, and want to reenable the virtual env, simply repeat the `activate` part of the previous steps again.

Now you can install MetaBuild.
```sh
pip install -U git+ssh://git@git.corp.adobe.com/meta-build/meta-build.git@latest
```

Many repositories usually abstract this step in a `setup.sh/ps1` script. For example, [MetaBuild](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.62/tools/setup.sh) itself.

## Other Notes

### Check MetaBuild has been installed
```
metabuild --help
```

### Check the version of MetaBuild

```shell
metabuild version
```

### Specifying MetaBuild version

You can change the `latest` keyword in the MetaBuild installation lines with the version you want to use. Check the [Jenkins Page](#Install-MetaBuild) above to get the latest passing version number. `latest` is simply a git tag pointing to the latest MetaBuild version. We also have a `stable` git tag which points to the latest MetaBuild version that has also passed through a more rigorous testing pipeline. You can read more about the stable tag and the stable pipeline [here]({{ site.baseurl }}{% link _docs/versioning.md %}).
### Installing from artifactory instead of git.corp

Metabuild is also available as a PIP wheel, along with all of its dependencies, from the Corporate Artifactory.

```terminal
pip install metabuild --index-url=https://<UserName>:<Artifacotry_API_Key>@artifactory.corp.adobe.com/artifactory/api/pypi/pypi-metabuild-dev-local/simple
```
If you define your `ARTIFACTORY_API_KEY` as a variable in your Terminal, then you can avoid specifying the username, too. adding `metabuild==version` will install that specific version and all of its dependencies. For example: 

```terminal
pip install -v metabuild==0.1.420 --index-url=https://:${ARTIFACTORY_API_KEY}@artifactory.corp.adobe.com/artifactory/api/pypi/pypi-metabuild-dev-local/simple
```

Also, a good reference is this [DVA Wiki page](https://wiki.corp.adobe.com/display/dvadevops/Working+with+Python+packages) on using internal PIP Packages. The wiki also explains how you can setup PIP so that you don't need to include the index-url argument.
