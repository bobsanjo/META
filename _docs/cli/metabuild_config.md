---
permalink: /docs/cli/metabuild_config/
title: "metabuild config"
---

Configure options are used during the MetaBuild workflows. Options can be communicated to MetaBuild using YAML configuration files, the [META.lock]({{ site.baseurl }}{% link _docs/guides/config_files.md %}) file, or using command line arguments.

## YAML Config Files

MetaBuild has a set of [YAML config files]({{ site.baseurl }}{% link _docs/guides/config_files.md %}) at different locations. They can be edited by hand, but the `metabuild config` command makes it easy to interact with these config files.

```shell
metabuild config [--meta PROJECT] [--global|--project|--user|--cache] {get,set,reset,dump,locations,which} ...
```

**Refer to the [`default_config.yaml`](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/config/default_config.yaml#L2) file for reference on the possible options.**

| Command | Description |
|---------|-------------|
| `metabuild config get <key>` | Reads and prints the setting with the name `key`. |
| `metabuild config set <key> <value>` | Changes the the value of the setting `key` to value `value`. |
| `metabuild config reset <key>` |  Removes the value of the setting `key`. |
| `metabuild config dump` | List all available settings. |
| `metabuild config locations` | List all known locations of the configuration files. |

| Argument | Description |
|----------|-------------|
| `--meta <PROJECT>`, `-m <PROJECT>` | Sets the meta project to use for project and user properties. Defaults to the meta project in the current directory. |
| `--global`  | Loads/Stores the property from/to the global config. |
| `--project` | Loads/Stores the property from/to the project config. |
| `--user`    | Loads/Stores the property from/to the user config. |
| `--cache`   | Loads/Stores the property from/to the cache config. |


## Command Line Args

Configs can also be passed to MetaBuild during the `metabuild prepare` command. These will override the values specified in the files. For example,
```
metabuild prepare --define msvs.version=15
```
Any config passed during prepare will be save by MetaBuild, and will used during next phases (e.g., build).

Note that certain configs might **also** be overridable during other phases. For example
```
metabuild build --define msvs.builder=incredibuild
```
However, these overrides will not be stored, and will be used only during this phase.

### Defining lists of values
`--define` can also specify a list, for example:
```
metabuild prepare --define dva.params=--params,"code_sign_identity=None,debug_mode",--apps,"PremierePro,AfterEffects",--loglevel,INFO
```
This defined the `dva.params` parameter with the value `--params,"code_sign_identity=None,debug_mode",--apps,"PremierePro,AfterEffects",--loglevel,INFO` which represents a list:
```
[
  --params,
  "code_sign_identity=None,debug_mode",
  --apps,
  "PremierePro,AfterEffects",
  --loglevel,
  INFO
]
```
The rules are:
- elements in the list are separated by comma,
- if the value itself contains a comma, it needs to be quoted to avoid splitting it up.
