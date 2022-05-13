---
permalink: /docs/guides/thirdparty_libraries/
title: "Working with Third Party Libraries"
toc: true
---

This guide describes how to create or update specs for third party libraries. Before reading this section, make sure that you are have followed the [MetaBuild Tutorial]({{ site.baseurl }}{% link _docs/tutorial/main.md %}).

Third party libraries often have two parts: 
1. The source code is where the source for the library goes. If the source comes from a git repo outside Adobe, you need to mirror it to [third-party](https://git.corp.adobe.com/thirdparty/) organization ([meta-archives](https://git.corp.adobe.com/meta-archives/) is the older location).  If the source code already exists in other location in Adobe git.corp, it is better to just use that (don't create another copy).
2. The MetaBuild specs under [meta-specs](https://git.corp.adobe.com/meta-specs/) organization.

The intent of this structure is to keep our modifications to the spec repo, and keep the git history of the source code mirror as intact as possible. However, in some cases, if we make a lot of local modifications to the source code, and the third party lib is not actively released, you might see the source code living in the same folder as the code (e.g., tinyexr [tinyexr](https://git.corp.adobe.com/CTL-third-party/tinyexr)).

The process of updating a third party library is as follows:
1. If a source code mirror does not exist in git.corp, create one (needs temporary permission, ask in #metabuild).
2. If the source code exists, update it (needs temporary permission, ask in #metabuild).
3. If specs do not exist, create a repo for them (needs temporary permission, ask in #metabuild).
3. Update the specs by placing a PR (you can use a personal fork to place a PR).

Note that during this process you can always use the third party library based on your modification, before your meta-specs PR is merged, or your updates to the source code is pushed. See [debugging locally](#debugging-locally).
{: .notice--warning}


## The source code

### Creating a mirror

If the source code for the library does not exist in git.corp, first you need to create a mirror. If the source code exists, please use the existing source code, and don't create a duplicate in third-party (or meta-archives).

First,  ask in the #metabuild channel for a repository to be created in the org, and write access to be granted to you on that repo.

Then, clone the original repo on your local disk
```terminal
git clone https://github.com/CLIUtils/CLI11
```

Change directory into the repo, and push to the mirror repository with the `--mirror` flag. This will push all the branches and tags.
```terminal
git push --mirror https://git.corp.adobe.com/thirdparty/CLI11
```

### Updating the mirror

If the mirror already exists, clone the original repo on disk (if you don't have it already).
```terminal
git clone https://github.com/CLIUtils/CLI11
```

Change directory to the cloned repo
```terminal
cd CLI11
```

Add the mirror as a second remote (we call the remote meta here)
```
git remote add meta https://git.corp.adobe.com/thirdparty/CLI11
```

Push the new tags that you want to make available on the mirror (for illustrative purposes we assume we want to add the new v10.1.2 and v10.1.3 tags, and the dev/10.2 branch).
```
git push meta v10.1.2 v10.1.3 --tags
git push meta dev/10.2
```

**NOTES**:
- this time __do not__ use the mirror option. Others might have created other branches in the mirror and pushing like this can erase them.
- If you are updating the upstream branches (e.g., master), make sure not to push any user commits to them, and keep their commit history identical to the original repository.

### Making changes to source

Sometimes you need to make some changes to the original code to fix a bug or improve it. Ideally those fixes should be contributed upstream to the original project repo (make sure you get the approval from Legal first!) but sometimes you can't or you're time pressed and need those changes now.
In that case, we suggest the following:
1. Create a branch `adobe/<version>` in the mirrored repo and put the updates there.
2. In the meta-specs for the library point the `lib_version` option value associated with that version to the SHA of that branch head (instead of `main`).

---
## MetaBuild Specs

Before updating or creating specs for third party libraries, first make sure that you are familiar with how MetaBuild projects work by following the  [MetaBuild Tutorial]({{ site.baseurl }}{% link _docs/tutorial/main.md %}). 

### Writing specs

Start by using the [spec template](https://git.corp.adobe.com/meta-specs/spec-template) project, by clicking the use template button.
![](https://git.corp.adobe.com/storage/user/30871/files/e59e0a80-537d-11ec-9ec8-9b1221368d34)
To create a repo under the `meta-specs` organization.
![](https://git.corp.adobe.com/storage/user/30871/files/2a29a600-537e-11ec-94f8-0a85dd82366c).

Then you can start writing the specs. Keep in mind the following conventions:

1. In the third party project specs, we often separate the version of the library source code and the version of the spec. See the note on version and lib_version in [project_link()]({{ site.baseurl }}{% link _docs/api/project_link.md %}#note-on-lib_version) and [handling multiple versions of an external repo in a single spec file](#handling-multiple versions-of-an-external-repo-in-a-single-spec-file). For consistency, always call this option `lib_version`.
2. Place all `project_link()` and `git_checkout()`s in a `deps.meta.py` file.
3. Place all `option()`s in a `options.meta.py` file.
4. Call the final product the same as the name of the project, and either place it in a file with the same name as the project, e.g., `cxx_library(name = CLI11)`, in `CLI11.meta.py`.
5. Create an alias for the main product(s) in the META.py so your target can be used simply as `CLI11//:CLI11` instead of `CLI11//CLI11:CLI11`. See [how to create an alias]({{ site.baseurl }}{% link _docs/api/import_rules.md %}).

Also make sure to update the Jenkinsfile accordingly. If you are adding a test that is supposed to build on ios or uwp, also make sure to add a dependency to test_helper//:cli_app, see [example](https://git.corp.adobe.com/meta-specs/spdlog/blob/main/META.py#L54).


### Updating the specs


So most of the time, you might just need to find where the choices for `lib_version` is defined for the specs, e.g., [here](https://git.corp.adobe.com/meta-specs/eigen/blob/v4.0.11/META.py) for Eigen and augment it. And then also set the corresponding source code SHA1 (or  tags) of the source code repo, e.g., [here](https://git.corp.adobe.com/meta-specs/eigen/blob/v4.0.11/META.py#L57-L67) for Eigen.

For some repos, we might just be supporting a single version of the third party for the spec. In these cases, you might just need to update the version of the source code repo, in the lock file of the spec repo for example [here](https://git.corp.adobe.com/meta-specs/boringssl/blob/main/META.lock#L1-L3) for boringssl. 

In some cases, you might also need to modify the spec to adapt it to the source code changes. Some specs might have more detailed docs in the readme, such as [boringssl](https://git.corp.adobe.com/meta-specs/boringssl). Also if you find more README worthy info, please feel free to include an update to the README in your PR.

Once your modifications are done, and you verified that things work locally, place a PR for the spec job. Jenkins job should start automatically. When the PR is merged, Jenkins should push a new tag to the spec repo, which you should be able to use in your application.

## Debugging your changes locally

When you modify a spec file in a fork or on a repo on your disk, you can always ask MB to use your fork or your local repo for the third party project instead of the one in meta-specs when building your application. Simply in your [lock file, or yaml config files]({{ site.baseurl }}{% link _docs/guides/config_files.md %}) of the [root project]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}#root) (i.e., your application), place the following. Assuming the project name is `CLI11`:

```
# For using your fork
[CLI11]
repo = /link/to/your/spec/repo
commit = commit of spec repo

# For using your local folder
[CLI11]
local_link = /path/to/local/folder
```

If you have any `git_checkout` in your spec, you can also temporarily redirect it to another repo or local folder, if the `thirdparty` mirror is still not updated. Note that `CLI11//:CLI11_git` is a placeholder for the [target reference]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}) of the `git_checkout()` node. In this case, it means the `git_checkout()` lives in the META.py file of the `CLI11` spec repo, and its name is `CLI11_git`.

```
# to checkout another git repo
[CLI11//:CLI11_git]
repo = ...
commit = ...

# to use local folder
[CLI//:CLI11_git]
local_link = ...
```

## Handling multiple versions of an external repo in a single spec file

It is possible to handle multiple versions of an external library in the same spec file. The specs of the [asyncplusplus library](https://git.corp.adobe.com/meta-specs/asyncplusplus/blob/main/META.py) is an example. Here, the user will ask for this library in the following way
```
[asyncplusplus]
version = 1.0.0
lib_version = 7.65.3
```
Where `version` is the version of the specs (git tag of the `meta-specs/asyncplusplus` since the `git_tag` command is used in [`meta-libs/asyncplusplus`](https://git.corp.adobe.com/meta-build/meta-libs/blob/main/libs/asyncplusplus/META.py) ), while `lib_version` is the version of the `asyncplusplus` library. This way, if a fix is applied to the spec file, it does not have to be applied to all the tags in the spec repo. Only the development branch is updated, and a new tag is assigned.

How can we achieve this? `lib_version` is simply an [option](https://git.corp.adobe.com/meta-specs/asyncplusplus/blob/4a2711477d065cb3f022418baf58ae438f3623b9/META.py#L3) in the asyncplusplus specs. Then, based on the version, we decide [which version](https://git.corp.adobe.com/meta-specs/asyncplusplus/blob/4a2711477d065cb3f022418baf58ae438f3623b9/META.py#L14) of the `asyncplusplus` has to be checked out, using the [`commit` argument](https://git.corp.adobe.com/meta-specs/asyncplusplus/blob/4a2711477d065cb3f022418baf58ae438f3623b9/META.py#L13) to the `git_checkout` command. Finally, you should pass the `auto_lock=false` to the `META.lock` file of the specs. This should always be done if you want to specify the git sha1 of the checked-out branch in `META.py`.
```
[asyncplusplus//:asyncplusplus_git]
auto_lock = false
```
