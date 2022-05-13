---
permalink: /docs/guides/syncing/
title: "Working with multiple GITs"
---

## Syncing Rules

1. The root repository is always the responsibility of the developer.
    - MetaBuild never uses a different version of the root project, nor tries to update it any way.
    - The only file that MetaBuild changes in the root repo is the `META.lock`. Even in that case, the changes are always additive and it never removes nor changes existing values.

2. Local changes are always preserved! MetaBuild never overwrite any of the local changes. This is very important for MetaBuild.

    > The `--overwrite` flag can be used to turn this rule off. This flag forces MetaBuild to overwrite local changes in order to satisfy rule 3 below.

3. MetaBuild always **tries** to keep your build up-to-date with all the requirements. No other flags are needed to do that.

    > For example, if you update a commit in the `META.lock`, then MetaBuild will have to checkout the updated repositories. However, it will never break rule #2 above.
    > A warning is issued when such cases are detected. The build will continue regardless, just that MetaBuild will use the unmodified local changes instead of pulling the required version.

4. The `META.lock` is supposed to be pushed into the GIT repo.
    - The lockfile is what makes the builds reproducible across time and space (different machines).
    - If MetaBuild has to take a decision it will always store the result of that decision inside the `META.lock`
    - The format of the `META.lock` file is user friendly, so you can always update the `META.lock` file by hand with the correct values as needed.

## Changing the META.lock file

If you change values in the `META.lock` file, then `metabuild prepare` will update the referenced projects to match the requested versions & commits.

For example, if you switch from `sqlite.v1` to `sqlite.v2`, then MetaBuild will update the local "sqlite" checkout to match the new version requested via `META.lock`.

However, because you can have some local changes done to the "sqlite" repository, there are a couple of cases that MetaBuild handles:

- **Uncommitted local changes**: If the "sqlite" GIT repo has local changes, then it will warn about the local changes and bail the update of the GIT repo. Note that this is just a warning in the console, so MetaBuild will continue to use the local checkout as if the checkout was successful. As a result, the new `sqlite` version from the META.lock file is ignored and the local version is used instead.

    > MetaBuild runs `git status` inside the "sqlite" GIT folder to detect local changes. If `git status` reports any change then it is considered a local change.

- **Committed changes**: MetaBuild compares the current GIT commit of the local checkout to the SHA of the commit that MetaBuild used during the previous successful checkout of `sqlite`.

    a) If the commits do NOT match, MetaBuild will warn about the mismatch and ignore the update request. The results are the same as *case 1* above.

    b) If the commits match, then it means the developer didn't change the local `sqlite` GIT repo at all since the last checkout. In this case MetaBuild will checkout the required commit as specified by the `META.lock` file.

    > MetaBuild keeps record of all the checked out versions using the `dist/status.sqlite.db` database.

- **Forced overwrite**: If you don't need to preserve the local changes, then you can add `--overwrite` to the prepare command. In this case MetaBuild will **clean any local changes**. This is useful when you need to get a pristine build without any local changes inside the dependencies.

    > Note that MetaBuild NEVER changes the root repository, so the root is never overwritten. There's no file that could tell MetaBuild to pick a different version for the root project, so it will never decide to use a different one.

## Multiple GIT repositories

When working with MetaBuild there are multiple types of GIT repos:

1. The root repository. This is the one you manually check out before running the `metabuild prepare` command.
2. All the repos added with `git_checkout()` go inside `dist/git`
3. All projects added using `project_link()`go inside `dist/projects`

Note that *(2)* and *(3)* above are just regular local GIT checkouts. However, the changes in these repos are never reported when using `git status` inside the root folder. You have to manually switch over inside each of these repos and run `git status` for each GIT repo. That's because the entire `dist` folder is added to the `.gitignore` of the root repository.

### `metabuild scm status`
Prints the full status of the local repositories.

MetaBuild runs `git status` on all repos and reports back the results for the changed repos.

> All the `metabuild scm` commands include the root repository even if it is not managed by MetaBuild. As a result, you don't have to make a separate call to `git status` inside the root project.

### `metabuild scm list`
Prints a list of all the GIT directories used by MetaBuild during status.

### `metabuild scm each git [command]`
Runs the specified command inside all repos that had local changes.

### `metabuild scm each --all git [command]`
Runs the specified command inside all repos known to MetaBuild.


## Saving local work

In order to save your local changes, you would have to create a branch, stage the changes, commit and then push. You can do the same on all repos at once using the `metabuild scm each git` command

| Command | Description |
|---------|-------------|
| `metabuild scm each git checkout -b my_feature_branch_name` | Creates a new `my_feature_branch_name` branch in all repos. |
| `metabuild scm each git add .` | Stages all of the changed files. |
| `metabuild scm status` | Check that no unwanted files are added to the repos. You may need to manually switch to those directories and manage each repo by hand. |
| `metabuild scm each git commit -m 'This is a fix.'` | Commit the changes using the specified message. |
| `metabuild scm each git push origin my_feature_branch_name` | Pushes the `my_feature_branch_name` branch to remote repos. |

In the end, open PRs for all the changed repositories by hand using the GitHub interface.

## Future workflows

Working with multiple GIT repositories is a bit more complicated then it could be. The following commands make the daily workflows a bit easier when using MetaBuild.

> The following workflows **are not yet supported**. The commands will be available in a future version of MetaBuild. Feedback on the implementation details of these workflows is welcome via [METAB-119](https://jira.corp.adobe.com/browse/METAB-119).

### `metabuild scm save`

[METAB-127](https://jira.corp.adobe.com/browse/METAB-127) Saves a complete snapshot of the local changes.

### `metabuild scm load [snapshot_link]`

[METAB-128](https://jira.corp.adobe.com/browse/METAB-128) Restores the state of a saved snapshot.

### Example

Possible implementation of these commands:

```bash
> metabuild scm save
Saved your changes to `https://git.corp.adobe.com/gist/123123/v1`
```

Then on the other machine you would run the following command to restore the previous snapshot.

```bash
> metabuild scm load https://git.corp.adobe.com/gist/123123/v1
```

### `metabuild scm pull-request`

[METAB-129](https://jira.corp.adobe.com/browse/METAB-129) Prepares all the required PRs with GitHub.



## Preventing network access

By default MetaBuild always tries to get the most up-to-date dependencies of your specification. When this is not needed, the `--cached` flag can be used to make MetaBuild skip fetching updated GIT repos from remote.

In general, a GIT branch has two possible meanings:
1) the commit that the branch points to inside the local cached repo
2) the commit that the branch points to on the remote GitHub hosted repository

When the `--cached` argument is used, it simply tells MetaBuild that the **local** branch that was already on the machine is good enough to be used in the build.

Here are some use-cases:

1. If you work without internet connection or without a VPN connection to Adobe.
2. If you want to speed up `metabuild prepare` by avoiding any remote checks.

Note that when MetaBuild needs to use a repository and that repo does not have a local cached version, then it will still have to fetch the repo from remote even if you've used the `--cached` flag. Otherwise, an entire repository would be missing and MetaBuild wouldn't know how to fix it.

