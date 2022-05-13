---
permalink: /docs/guides/invoking_alternative_msvs_builders/
title: "Invoking Alternative MSVS Builders"
---

By default the command `metabuild build` will use the [`MSBuild`](https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2019) software to build your MSVS projects. Incredibuild BuildConsole and devenv.com (command line version of visual studio) are also supported. To change the builder, you can use the following config value `msvs.builder`. Accepted values are
```
msbuild              -> use msbuild, default
devenv               -> use devenv
incredibuild         -> use incredibuild with msbuild backend
incredibuild-msbuild -> use incredibuild with msbuild backend
incredibuild-devenv  -> use incredibuild with devenv backend
```

[Passing extra args]({{ site.baseurl }}{% link _docs/cli/metabuild_build.md %}#passing-arguments-to-build) is supported all the builders. Also, you can use all the [usual methods]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) to set the values of this config.
