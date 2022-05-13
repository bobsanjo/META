---
permalink: /docs/faq/common_errors/
title: "Common Errors"
---

### Error: MetaException: Unknown attribute name.

This could be due to a typo in your MetaBuild files (using a wrong argument to a MetaBuild function). It could also be due to using an old version of MetaBuild that does not support the MetaBuild files you are trying to run.

You can specify a minimum MetaBuild version. So if you are trying to build a project with old MetaBuild version, a descriptive message will be printed. See [checking MetaBuild version]({{ site.baseurl }}{% link _docs/guides/checking_metabuild_version.md %}).


### I get `CERTIFICATE_VERIFY_FAILED`

Some Python versions come with a broken SSL implementation and require a separate step to upgrade the SSL certificates. Running `pip3 install --upgrade certifi` should fix the issue.

If you use the Python3 that comes on MacOS 10.5 (Catalina), use the methods described in  [Install MetaBuild]({{ site.baseurl }}{% link _docs/install_metabuild.md %}) to install a fully functional distribution of Python.

For more info check out this [blog post](https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/).

### Windows long path support

Windows might enforce a maximum path length limitation which is likely to cause issues with MetaBuild. To lift this restriction and enable support for long paths you need to
  1. [Enable the support within windows registry](https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/)
  2. If you install python via the official installers (and not with virtual env tools such as conda or pyenv), [at install time, ensure that support for long paths is enabled](https://stackoverflow.com/questions/51019926/python-installer-for-windows-disable-path-length-limit-option-not-available).


### Git authentication issues

This can often manifest itself in MetaBuild asking for a ssh passphrase or errors like 
```
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
```

Since MetaBuild runs git commands to download dependencies/specs the environment must be setup to support them. For Git authentication through ssh key to work seamlessly and not have it ask for the passphrase for every git operation that MetaBuild does (every dependency of the project being compiled) either __use an ssh key with no passphrase__ or __setup the ssh-agent must be with your key__:

1. running MetaBuild from CMD

   run `start-ssh-agent`, this will ask for the passphrase and cache it

2. running Metabuild from Bash (or windows Git Bash)

   run `eval "$(ssh-agent -s)"` followed by `ssh-add ~/.ssh/id_rsa` to enter the passphrase


### Accessing MetaBuild cache with older versions of git

If a repository is accessed and modified via git (especially the ones checked in MetaBuild cache with the new partial clone feature), then it might not be accessible via an older version of git. Therefore, in MetaBuild before we perform any git operation in cache we ensure that the git that you are using to modify the cache is either the same version or newer than what was used last time. If you try to access the cache with a version older version than the one used before, you see a message like

```
Error: MetaException: Last git version used in metabuild cache is 2.24.3, however, you are trying to access the cache with an older git version (2.24.2), this is not supported.
```

If you see this message, it means that multiple gits live in your system, and they are being used interchangeably. It could be due to a miss-configured system (e.g., you have installed multiple versions, some in virtual envs). Or it could be due to xcode putting its own `git` in priority in the path when running MetaBuild genrules.

The proper solution depends on the context:
  - Lock the path to git exactly via the config `git.path` so always the same version is used.
  - If you really intend to use different versions of git, configure the MetaBuild cache path (`cache.path`) to be different for each one.

*Note*: On macos `/usr/bin/git` just calls `xcrun git ...` internally, so the version of git is determined by the currently selected version of xcode. So even if you lock the path and change xcode version with `xcode-select` you can get conflicts. When locking the path to git, use a git other than `/usr/bin/git`.

You can temporarily disable this check by setting the config `cache.validate_git_version` to false.

### I experience unnecessary rebuilds after running metabuild prepare.

We take special care to make sure the generated projects are identical between different runs of prepare. For example, we issue all targets in a stable order and all the generated properties are predictable and stable across different runs. The IDE should be able to reuse everything from previous runs.
If you experience a different behavior then it is a bug and we could look into it. Please log a bug in JIRA if you can reproduce it.

Some things that are expected to cause a rebuild of a target:
  1. changing flags or preprocessor macros
  2. changing dependencies
  3. changing a precompiled header
  4. changes in included files
  5. genrules that are generating files and NOT using the provided update_file method that prevents timestamp changes

### MetaBuild project has broken git links on external drive

MetaBuild manages Git dependencies in the project-specific output folder as _linked Git worktrees_ to a single _main Git worktree_ in a global cache. The default global cache location is **machine-specific**: `~/.adobe_meta_cache`. If you run `git status` in one of these _linked Git worktrees_, you will likely get: `fatal: not a git repository: /Users/<user>/.adobe_meta_cache/git/adobe/<org>/<repo>/worktrees/<worktree>`.

The solution is to also store the global cache on the external drive. MetaBuild's `cache.dir` setting can be used to configure the global cache location. Pass the `--user` argument to save this setting in `META.user.yaml`, which should be in your `.gitignore`:

```sh
metabuild config set cache.dir <external_drive/path/to/cache> --user
```
