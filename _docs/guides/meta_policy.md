---
permalink: /docs/guides/meta_policy/
title: "MetaPolicy Guide"
---

## Meta Policy
   Concepts discussed in this page are implemented using [meta_policy api]({{ site.baseurl }}{% link _docs/api/meta_policy.md %}). Please refer `meta_policy` API if you have more ideas to extend our implementation in your project.
   Please note that, if you change the url in `meta_policy` callbacks, changed urls will go through validations required for safe mode or internal url mode based on user configurations.

## Safe Mode

Safe mode is a sandboxing system for specifications built with MetaBuild.

When enabled, several builtin features in MetaBuild either get disabled or change behavior:

1. No tool will install out of box. If any tools are necessary during the build, the user must configure the required tools ahead of time and provide the paths to MetaBuild using the configuration system. All builtin tools have the option to change the install path using the `tool_name.path` config property.

2. The specifications can continue to download source code and/or binaries from remote, but only from pre-approved URLs.

Safe mode can be enabled using the MetaBuild configuration system by using the `mb.safe_mode = True` option. At the moment, safe mode is NOT enabled by default. The default state might change in a future version once the implementation becomes more stable. Any change in default values require proper colaboration with the users to ensure backwards compatibility for all the teams.

### Error conditions in safe mode

###### Fail to configure the required tool used in the build system will raise one of following exception based on the error condition:
   
* When required tool is not configured in safe mode:
>Tool installation is not available when mb.safe_mode=True. You must:
>1. install the tool manually and
>2. provide installed path using the command: 
>metabuild config set --global tool.path install_path configuration property.
>Please refer https://git.corp.adobe.com/pages/meta-build/docs/cli/metabuild_config on how to work with metabuild config.

* If required tool path is configured and it's main executable not found:
>Main executable 'tool exe path' is not found for the tool: tool name

* If required tool path is configured and if tool version is different at configured path:
>Executable at 'executable_path' with version: 'installed_version' does not match requested version: 'configured_version'.

* If configured tool path doest exist:
>Configured tool install path configured_path does not exist

###### Using un-approved host URL will raise following exception and abort the build:
>Access to public URL is not allowed when mb.enable_internal_url_policy is True.

## Internal mode
* Enable internal mode using `mb.enable_internal_url_policy = True`.
* This mode is not enabled by default. 
* When enabled, metaspecs running for current build will have access only to approved URL hosts.

### Error condition in internal mode
If the metaspec make a request to download the source code or tools other than approved host names, build will be aborted with following error condition:
> Access to public URL is not allowed when mb.enable_internal_url_policy is True.

### default host names
metabuild considers following names as default approved host names:

Default approved Host names

| URL |
| ----------- |
| git.corp.adobe.com |
| artifactory.corp.adobe.com |
| artifactory-no1.corp.adobe.com |
| codex.corp.adobe.com |
| gerrit.allegorithmic.com |
| gerrit-3di.allegorithmic.com |
| gerrit-3di.corp.adobe.com |
| gerrit |
   
use `mb.additional_approved_host_names = list of comma separated additional approved host names` if you would like to add more approved domains.
For any valid reason, if you want to change the default approved host names, use `mb.default_approved_host_names = list of comma separated approved host names`.
Please ensure to provide regular expression for the host names, for ex, `git.corp.adobe.com` is listed as `^git.corp.adobe.com$`.

## configure installed tool path
Use `path` property of specific tool to configure installed path.

| tool | property | 
| ------ | ------ |
| android | android.path |
| cmake | cmake.path |
| nodejs | nodejs.path |
| nuget | nuget.path |
| vswhere | vswhere.path |

If you want to configure tool path based on it's version, use `tool_name.path_<version_string_dots_replaced_with_underscore_platform>`.
For ex, in order to configure paths for nodejs version `10.15.3` and `12.16.2`, you can use 
- `nodejs.path_10_15_3_win32="nodejs version 10.15.3 install location on the machine"`
- `nodejs.path_12_16_2_win32="nodejs version 12.16.2 install location on the machine"`

Following metaspec will use these configured nodejs paths: 

#### META.py

```python

nodejs(
    name = "nodejs_10_15_3",
    version = "10.15.3"
)

nodejs(
    name = "nodejs_12_16_2",
    version = "12.16.2"
)

nodejs_modules(
    name = "nodejs_module_install_10_15",
    packager = "yarn",
    package_json = "package.json",
    modules_folder = "node_modules_10_15",
    deps = [
        ":nodejs_10_15_3"
    ]
)

nodejs_modules(
    name = "nodejs_module_install_12_16",
    packager = "yarn",
    package_json = "package.json",
    modules_folder = "node_modules_12_16",
    deps = [
        ":nodejs_12_16_2"
    ]
)

group(
   name = "main",
   deps = [
       ":nodejs_module_install_10_15",
       ":nodejs_module_install_12_16"
   ])
```

If you are using one version of nodejs across all your metaspecs, following will work too.
- `nodejs.path="nodejs install location on the machine"`

If you want to use specific version of the tool, you can configure using `tool_name.version`, this config is useful for the tools which are requested without explicitly mentioning the version (android, cmake, ninja, vswhere and nuget).

### available tool versions
you should be able to query list of available versions which could be used in metabuild with following command:
- metabuild android versions
- metabuild cmake versions
- metabuild nodejs versions
- metabuild ninja versions

## Tool installer download
metabuild will download tool installers hosted at https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/. If you are missing a tool here, please post the request at #metabuild slack channel.

### configuring URL for a tool download

Use `url` property of specific tool to configure download url. Configured url will be used when tool need to be downloaded 

| tool | property | 
| ------ | ------ |
| android | android.url |
| cmake | cmake.url |
| nodejs | nodejs.url |
| nuget | nuget.url |
| vswhere | vswhere.url |

If you want to configure version specific url, use `tool_name.url_<version_string_dots_replaced_with_underscore>_platform`. 
For ex, in order to configure urls for nodejs version `10.15.3` and `12.16.2`, you can  use
- `nodejs.url_10_15_3_win32 = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-win-x64.zip"`
- `nodejs.url_12_16_2_win32 = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v12.16.2/node-v12.16.2-win-x64.zip"`
- `nodejs.url_10_15_3_macos = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-darwin-x64.tar.xz"`
- `nodejs.url_12_16_2_macos = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v12.16.2/node-v12.16.2-darwin-x64.tar.xz"`
- `nodejs.url_10_15_3_linux = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-linux-x64.tar.xz"`
- `nodejs.url_12_16_2_linux = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v12.16.2/node-v12.16.2-linux-x64.tar.xz"`

or if metaspec uses only nodejs version#10.15.3, following will work
- `nodejs.url_win32 = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-win-x64.zip"`
- `nodejs.url_macos = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-darwin-x64.tar.xz"`
- `nodejs.url_linux = "https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/nodejs/v10.15.3/node-v10.15.3-linux-x64.tar.xz"`

### download tool from public url
We do not recommend this option for build machines, it's recommended only for experiments performed on the developer machines.
If the tool is not available as part of internal hosting (https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/tools/), you may want to experiment new versions from publicly hosted installers, in such cases, you can use following configurations to use new version:
- `tool_name.use_public_binaries` = True
- `tool_name.url` = "public installer url to new version"
Please note `tool_name.use_public_binaries` will override `mb.enable_internal_url_policy` but it cannot override `mb.safe_mode`; Tool install will fail and abort the build if these options are used in safe mode.

If you want to provide public access only to specific version of tool, you can use 
- `tool_name.use_public_binaries_<version_string_dot_replaced_with_underscore>` = True
- `tool_name.url_<version_string_dot_replaced_with_underscore>` = "public installer url to new version"
