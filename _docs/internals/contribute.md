---
permalink: /docs/internals/contribute/
title: "Contribute"
toc: true
---

 GIT: [meta-build/meta-build](https://git.corp.adobe.com/meta-build/meta-build)

Read more about [internals of `MetaBuild`](architecture.md).

If you don't have Python3 available on your machine,
[download and install Python3]({{ site.baseurl }}{% link _docs/install_metabuild.md %}).

## Setup

### Clone the repository

```shell
git clone git@git.corp.adobe.com:meta-build/meta-build.git
cd meta-build
```

### On MacOS

```shell
source tools/setup.sh
```

### On Windows

```shell
call tools/setup.cmd
```

### Open the project in VSCode

```shell
code -n .
```

There are a couple of useful targets available via the checked-in [launch.json](https://git.corp.adobe.com/meta-build/meta-build/blob/main/.vscode/launch.json#L6) file for [VSCode](https://code.visualstudio.com/).

The targets should show up in the **Debug** tab in `VSCode`. Make sure to configure the default interpreter in `VSCode` to use `python3`.

Do not directly modify files under `.vscode`. You can use the [workspace file]({{ site.baseurl }}{% link _docs/internals/vscode_tips.md %}#Multi-folder-workspace) to make custom modifications.

If you use the workspace feature you need to use the following instead.

```shell
code -n -g metabuild.code-workspace
```

## Running the tests

There's a global "Run MetaBuild Test Suite" target in `VSCode` that can be used to invoke all the tests.

The Python `unittest` framework is also integrated with the `Test` tab in VSCode. You can see all the tests and even individually invoke tests as needed from the `Test` panel.

To run the tests from the command line make sure that the venv is created and activated. If you have already ran `setup.cmd/sh`, simply run
```
source .venv/bin/activate # mac
call .venv/scripts/activate # win
```

### Running from command line

```shell
# make sure the venv is created and activated
python ./tests/main.py
```

### Running a test directory from command line

```shell
# make sure the venv is created and activated
python ./tests/main.py api
```

### Running a single test class or test function from command line

```shell
# make sure the venv is created and activated
python ./tests/main.py --no-discover api.test_loader[.TestLoaderAPIs[.test_load]]
```


### Running MetaBuild in Python debugger

To run a local version of metabuild run `pip install -e .` from the root of the cloned repository. Check that Metabuild
runs from cloned sources by running `metabuild version` in a separate cmd.

To run MetaBuild on a project from VSCode in python debugger, you can use a [workspace file]({{ site.baseurl }}{% link _docs/internals/vscode_tips.md %}#Multi-folder-workspace) file. Add an extra entry in the under "launch". Pass the directory where the `META.py` file resides to MetaBuild with the command line argument `--meta`, or use the VSCode `"cwd"` argument.

__Note__: In order to avoid the Git passphrase issues mentioned in [Common Errors / Git Authentication]({{ site.baseurl }}{% link _docs/faq/common_errors.md %}#git-authentication-issues) you must set the env variable `SSH_AUTH_SOCK`
to point to the path of the ssh agent generated (pid) file, e.g., `C:/Users/your_username/AppData/Local/Temp/ssh-XZMyJgs568Hd/agent.xxxx`,
or run `start-ssh-agent` in a CMD prompt and start VSCode from that same console with `code -n .`.

## Windows extras

If you are running the uwp tests in MetaBuild repo, you need [`windows sdk 10.0.16299.0` or higher](https://git.corp.adobe.com/meta-build/meta-build/blob/0.1.501/metabuild/test/MetaTestCase.py#L104), and [CDB]({{ site.baseurl }}{% link _docs/guides/install_cdb_on_windows.md %})

## Linting

MetaBuild the following linting tools and enforces them in Jenkins:
- pylint: general checks for errors and inconsistencies
- mypy: type checker
- isort: formats the import statements at the top of files.
- black: code formatter

All these tools are configured via the file `pyproject.toml` and run on your code during the `lint` phase on Jenkins. To fix complaints issued by these tools:
- pylint and mypy: fix the error mentioned by the tool.
- isort: Either run isort on the file by opening the file on vscode > right click > press sort imports, or run `python tools/isort.py` to run it on all files.
- black: Either run isort on the file by opening the file on vscode > ctrl(cmd on mac)+shift+p > press format document, or run `python tools/black.py` to run it on all files.

You can run the checks locally too via the following scripts
```
python tools/lint.py [all,black,isort,mypy,pylint] [--check]
```

Note that sometimes you might wish to disable isort or black for a portion of the file, you can use
```py
# isort: off
### code not affected by isort
# isort: on

# fmt: off
### code not affected by black
# fmt: on
```

## Placing a PR in MetaBuild repo

When placing a PR in the MetaBuild repo please use the [PR template](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.29/.github/PULL_REQUEST_TEMPLATE.md). Do not delete the template. The info from the template is used to automatically update the MetaBuild [changelog]({{ site.baseurl }}{% link _docs/changelog/0.2.md %}).

If your PR is not related to a JIRA link, you can skip the JIRA related parts in the checklist.

If you want to message to the reviewer that the PR still has remaining tasks, add them under the `##Code` section of checklist.

When merging the PR, only squash is allowed. Use the first part of the template (everything above `Checklist before Merging PR`) as the commit message.