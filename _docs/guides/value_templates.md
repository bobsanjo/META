---
permalink: /docs/guides/value_templates/
title: "Value Templates"
---

All string values in MetaBuild are evaluated against a simple templating engine.

The template engine replaces the `$(...)` pattern with the resulting variables or macro value.

For example, the location of a file inside a GIT repo can be extracted using:

```python
"$(location :git_repo)/file1.cpp"
```

**Note** In order to escape the `$()` patterns, double the dollar sign ie. `$$(...)` or place your text within the function `escaped_value(value : string)`.
{: .notice--info}

## Builtin template macros:

| Macro | Description |
|------|-------------|
| `$(project_root <project_name>)` | Returns the root directory of the specified target project. |
| `$(location <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the output location of the specified target and resolves any lazy values it if needed (e.g. git checkout or http download).|
| `$(future_location <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the directory of the specified target without resolving any lazy values. |
| `$(generated_files <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the list of the files that a node generates (e.g., output of `genrule` or export header for `cxx_library`). |
| `$(generated_location <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the directory where the `generated_files` of a node go (some nodes such as `cxx_library` can have a distinct `generated_location` from `location`). |
| `$(exe <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the path to the binary created by a `CxxNode`. |
| `$(app <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | For targets that create bundles (e.g., .app or .framework on MacOS) returns the path to the bundle, otherwise, reverts to `$(exe ...)`|
| `$(option <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns to the value of an [`option`]({{ site.baseurl }}{% link _docs/api/option.md %}) node. |
| `$(pkg <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Used on UWP to get the absolute path to the pkg of the specified target project. |
| `$(upload_url <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns upload url of the specified `http_upload` node target. |
| `$(resolve <`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>)` | Returns the absolute location of the specified file reference. Useful when defining values for properties that are not `file_refs`. For example, when adding a preprocessor macro that should contain the full path of a relative file.|
| `$(uri <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | Returns the codex uri associated with a `code_query()` node. |
| `$(http URL)` | Resolves to the content of a text file downloaded from the URL. |
| `$(xcode_tool name)` | Returns the absolute location of the xcode tool with the given name. Internally calls `xcodebuild -find`.|
| `$(module.name <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | |
| `$(project.name <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` |  |
| `$(target.name <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | |
| `$(target.file <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | |
| `$(target.dir <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` | |

**Note** To query the location where the META.py file of a project is located, you must use `$(project_root ...)`.
{: .notice--info}

```py
project_link('boost')
# $(project_root boost) -> valid, project_root expects a project name
# $(location boost)     -> invalid, location expects a target reference (target_ref)
```

## Builtin template variables:

| Name | Description |
|------|-------------|
| `$(project_root)` | Same as its macro counterpart but for the current project. |
| `$(location <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>)` |Same as its macro counterpart but for the current node. |
| `$(generated_location)` | Same as its macro counterpart but for the current node. |
| `$(generated_files)` | Same as its macro counterpart but for the current node. |
| `$(midl_location)` | Same as its macro counterpart but for the current node. |
| `$(python)` | Returns the absolute path to the python `executable` in which metabuild is installed. |
| `$(mb_cache_path)` | Returns the absolute path to the MetaBuild cache. The default path is `~/.adobe_meta_cache`. |
| `$(emsdk_tools_path)` | Returns the PATH environment variable from the emsdk environment used by MetaBuild. |
| `$(msvs_install_dir)` | Returns the the absolute path to the MSVS install directory. |
| `$(msvs_vc_install_dir)` | Returns the absolute path to the MSVS VC compiler tools directory. |
| `$(config.platform)` | Returns the current platform. |
| `$(config.flavors)` | Returns the current flavor (if any). |
| `$(config.type)` | Returns the current configuration type (`Debug`, `Release`, `Coverage`) |
| `$(config.arch)` | Current build architecture. `x64`, `arm64`, `arm32`, `x86` or `universal` |
| `$(config.file)` | |
| `$(config.dir)` | |
| `$(config.cpu_arch)` | Current CPU architecture `x64`, `arm64`, `arm32`, `x86`. Note that for a xcode universal project cpu_arch might not have been resolved depending on the sharing value of node within which you are using this template value. See [SharedNode]({{ site.baseurl }}{% link _docs/api/shared_node.md %}). Sharing should include per cpu arch. |
