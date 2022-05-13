---
permalink: /docs/api/meta_tool/
title: "meta_tool()"
---

```python
meta_tool(...)
```

Inherits all attributes from [MetaNode]({{ site.baseurl }}{% link _docs/api/meta_node.md %}).

A meta_tool() enables you to install packages via MetaBuild.


| Attribute | Type | Description |
|-----------|------|-------------|
|name (required)|string|The name of this node|
|check|string|bash script that checks if the tool is installed.|
|which|string|name of an executable that can be used to check if the tool is installed. MB will run this using the 'which' command.|
|brew|string|name of the package to install via homebrew on macos.|
|msys|string|name of the package to install via msys on windows.|
|apt|string|name of the package to install via apt on Ubuntu.|


MetaBuild uses MSYS2, Cmd, Brew, and Apt on Windows, Mac, and Ubuntu, respectively. By default MetaBuild installs the package manager, for its own use only, in its global cache folder. If you want MetaBuild to use your own installed package manager, it can be done by one of the following commands (depending on the platform).
```
metabuild config set --global brew.path "/path/to/Homebrew"
metabuild config set --global msys.path "/path/to/MSYS2"
metabuild config set --global apt.path "/path/to/Apt"
```
You can read more about [MetaBuild configs]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) here.
