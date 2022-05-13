---
permalink: /docs/guides/config_files/
title: "Using MetaBuild Config Files"
---

## YAML Config Files

MetaBuild has a set of YAML config files at different locations. They can be edited by hand, but the `metabuild config` command makes it easy to interact with these config files. See [metabuild config]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) for how to use metabuild config command.

There are multiple locations that MetaBuild uses as possible configuration files.

**Note** Use `metabuild config locations` to check the locations of the configuration files on your computer.
{: .notice--info}

1. Internal defaults: [`meta/utils/default_config.yaml`](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/config/default_config.yaml#L2).
2. Global
    - MacOS: `~/Library/Application Support/metabuild/config.yaml` (`~` on MacOS is `/Users/[user]`)
    - Win32: `~\AppData\Roaming\metabuild\config.yaml` (`~` on Windows is `C:\Users\[user]`)
    - Linux: `~/.config/metabuild/config.yaml`
3. Project lock and config files:
    - `[root_project]/META.lock` project lock file in INI format
    - `[root_project]/META.yaml` project lock file in YAML format
    - NOTE: See [META.lock and META.yaml](#metalock-and-metayaml) section below
3. User - `[root_project]/META.user.yaml`
    - This is a local override for the lock file so users can override settings in `META.lock` or `META.yaml` without checking them in.
    - This file should be added to your `.gitignore` file to avoid users pushing it into the repo.

## MetaBuild Lock Files

The lock file is supposed to be pushed into the GIT repo. Here are some important notes:
- The lock file is what makes the builds reproducible across time and space (different machines).
- If MetaBuild has to take a decision it will always store the result of that decision inside the `META.lock` file.
- The format of the lock file is user friendly, so you can always update the lock file by hand with the correct values as needed.
- If you change values in the lock file then `metabuild prepare` will update the referenced projects to match the requested versions & commits.

The order of priority for the properties (from highest to lowest):
- `--defines` in the command line
- `META.user.yaml` local override file
- `META.lock` lock file
- `META.yaml` lock file

Properties from lock files are inherited through a chain of projects (added with [`project_link()`]({{ site.baseurl }}{% link _docs/api/project_link.md %})) such that they are propagated from a project to the project that requested it in the chain. When multiple projects in the link set the same property higher level projects have priority and can override properties of linked projects.

Some properties must be in the root project by design and are not inherited from other projects, for example [xcode] properties for iOS code signing.

## META.lock and META.yaml

Both of these files are considered "lock" files but they are slightly different:
- `META.yaml` file is intended for the user to store "read-only" config properties, that should be read by MetaBuild but not modified. This file is NOT read by MetaBuild when a reference to a remote project is used (only for the local project).
- `META.lock` file is in INI format and is what MetaBuild will use to write config properties back to when it "locks" components in the build tree to a specific version (if it's not already specified in META.yaml or META.lock). The config properties in this file are read when MetaBuild reads a remote project.

The YAML format has the advantage of supporting comments but at the time MetaBuild was developed we couldn't find a parser that will round trip the comments properly.
The INI format doesn't support comments (although extensions exists that do implement it) so MetaBuild started using this format for the META.lock file when writing back the properties.

To avoid confusion and inconsistencies there are future plans to consolidate the META.lock and META.yaml files into a single file META.lock.yaml (see https://jira.corp.adobe.com/browse/METAB-543).

## META.lock file

Config values can be set in the META.lock file using the following syntax: to set the value of a `a.b` property you can use
```ini
[a]
b = value
```
in the META.lock file. These values can be overridden either temporarily from the [command line]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) using `--define a.b=value` syntax or from the `META.user.yaml` local override file:
```yaml
a
  b: value
```
INI files don't support comments so if you attempt to place comments in the META.lock like this:
```ini
[a]
# This is b
b = value
```
those comments will be lost when MetaBuild re-writes the file. Instead you can do this:
```ini
[a]
comment1 = This is b
b = value
```

## META.yaml file

To set the `a.b` property in the META.yaml file you can use the normal YAML syntax. If your value looks like a number, you may need to wrap it in quotes.
```yaml
a:
  b: value
```


