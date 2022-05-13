---
permalink: /docs/cli/metabuild_scm/
title: "metabuild scm"
---

Command used to invoke git commands on all repositories managed by MB.

```
    list                List all the remote SCM repos.
    status              Status of all the remote SCM repos.
    clone               Clone repo using MetaBuild cache.
    each                Run a SCM command in all of the repos.
```

## Checking status of all repos

```shell
> metabuild scm status
```

## Running git command across all GIT repos

```shell
> metabuild scm each git status
> metabuild scm each git add .
> metabuild scm each git checkout -b branch_name
> metabuild scm each git commit -m "message"
> metabuild scm each git push origin branch_name
```

## Cloning a repository using MB

```shell
> metabuild scm clone git@git... --commit main ./repo
```

Clones a GIT repo using the internal MB caching system. This way the repo can share the history with all the other GIT repos in the system.

> Note that MB uses `git worktree` commands to manage multiple instances of the same repo on disk. A limitation of this command is that a specific branch can only be checked out into a single location on disk. The workaround is to use the commit hash instead of the branch name and create a new branch after the checkout is complete using git commands.
