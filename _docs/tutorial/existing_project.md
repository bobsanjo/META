---
permalink: /docs/tutorial/existing_project/
title: "Using a MetaBuild project"
toc: true
---

Before you begin the tutorial, make sure to follow the [MetaBuild install guide]({{ site.baseurl }}{% link _docs/install_metabuild.md %}).

A MetaBuild project consists of a `META.py` file along with optional `*.meta.py` additional files. These files are usually stored either in the root folder of a repository or in a `META` folder. We will also refer to these `.py` files as _recipes_ or _specs_.

The specs are either stored in the same repository that hosts the C++ source code (e.g., [here](https://git.corp.adobe.com/adobe-research/lerida/tree/master/META)) or in a dedicated repository only for the specs (e.g., [here](https://git.corp.adobe.com/meta-specs/CLI11)). The former scenario is preferable in most cases, and the latter is only used for external libraries.

## Building an existing project

To build a project that uses MetaBuild, first you need to generate the project. Change directory into the project's directory and run
```
metabuild prepare
```
This will generate the project for the default platform for the host (e.g., for windows default platform is win32) and default generator (e.g., for the ios platform default generator is xcode). If you want to generate the project for a different platform, see [the docs for `metabuild prepare`]({{ site.baseurl }}{% link _docs/cli/metabuild_prepare.md %}). You can also run `metabuild prepare --help`.

To compile the project, you have two options. Either open the project that MetaBuild generated in the previous step, and run build from there or use MetaBuild to build the project
```sh
metabuild build
```
See [the docs for `metabuild build`]({{ site.baseurl }}{% link _docs/cli/metabuild_build.md %}) or run `metabuild build --help` to see different options accepted by the build command.

Some projects get a set of options. These options can be set by passing `-doptionname=value` to MetaBuild. Alternatively, they can be set within a MetaBuild config file. See [MetaBuild config]({{ site.baseurl }}{% link _docs/guides/config_files.md %}) for more details on how to pass configs to MetaBuild.

**Note:** By default, MetaBuild will only generate files or build targets within the `group(name='main')` node (e.g., [here](https://git.corp.adobe.com/adobe-research/lerida/blob/f926907ccce72316f1fb67e60977c66b95af4fea/META/META.py#L102)), and their dependencies. To generate the project a different target and its dependencies use the `--target name` argument for MetaBuild prepare. Note that names passed to `--target` have to follow the MetaBuild naming convention (e.g., `:my_target` or `myproj//:mytarget`. Read more about [Target references]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}). Similarly, `metabuild build` will build the root target specified in the prepare phase and all its dependencies. To build a different target, use the `--build-target <target_ref>` argument.

### Example

You can build [projA](https://git.corp.adobe.com/meta-samples/tutorial_examples/blob/main/projA) with MetaBuild as an example. The META.py file of this repo has more comments explaining the commands in details. Here, we will repeat the content of repo so that you don't have to keep switching tabs between git.corp and the tutorials.

### Project structure

```
projA/
    projA_lib.hxx
    projA_lib.cxx
    main.cxx
    META.py
```

### projA_lib.hxx

```cpp
#pragma once
namespace projA {
void print_the_secret_of_the_universe();
}
```

### projA_lib.cxx
```cpp
#include "projA_lib.hxx"
#include <cstdio>

namespace projA {
void print_the_secret_of_the_universe() {
    printf("%d \n", 5);
}
}
```

### main.cxx
```cpp
#include "projA_lib.hxx"
int main() {
    projA::print_the_secret_of_the_universe();
    return 0;
}
```

### META.py
```py
# Follow https://git.corp.adobe.com/meta-samples/test_project/blob/master/META/META.py for basics
set_project_name("projA")

# typing `metabuild build --target :lib` or `metabuild build projA//:lib will build this.
cxx_library(
    name = "lib",
    srcs = "projA_lib.cxx",
)

# typing `metabuild build --target  :exec` or `metabuild build projA//:lib will build this.
cxx_binary(
    name = "exec",
    srcs = "main.cxx",
    # :lib is short for projA//:lib
    deps = ":lib"
)

# typing `metabuild build` will build dependencies of main (and their dependencies).
group("main",
    deps = [
        # :exec is short for projA//:exec
        ":exec"
    ]
)

# To build either use `metabuild build`
# or use `metabuild prepare` and then open the resulting xcode/msvs file.
```

## Linking to an existing project

Using other MetaBuild projects in your project is done via the `project_link()` command. In the end of the day, you should tell MetaBuild the name of that project and where its META.py file resides. However, there is a lot of flexibility in doing this, you can use the reference link from the [metabuild package management repo](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs), a link to a git repo, or even a link in your local disk. See [projB](https://git.corp.adobe.com/meta-samples/tutorial_examples/blob/main/projB) for a detailed explanation. They are also repeated here with detailed comments.

### Project structure

```
projB/
    main.cxx
    META.py
    META.lock
```

### META.py


```py
set_project_name("projB")
```

If we are using a library that is already listed in [MetaBuild package management repository](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs) you just publish a project_link() command. This is the recommended way to include libraries. Since it prevents clashes in projects
using the same library from different places. The version of the library you are using should be specified in the META.lock file. MetaBuild tries to analyze the lock file of your library and the lock files of all dependencies to prevent or warn about clashes. The first time you run `metabuild prepare`, MetaBuild will create a META.lock file. Replace the versions in that file with the correct values and check it in. To find the available versions, you need to look into the directory corresponding to the project in meta-libs. For projects that have an entry like [this](https://git.corp.adobe.com/meta-build/meta-libs/blob/main/libs/CLI11/META.py) in the meta-libs repo, the version will be tags in the repo that the `git_tags()` command addresses. For libs that are specified like [this](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs/acp-local-test), the available versions are those that have an explicit .py file.
```py
project_link("CLI11")
```

Sometimes your dependency is in active development and you have not added where its META.py file resides or its versioning convention to to [meta-libs](https://git.corp.adobe.com/meta-build/meta-libs). In this case, you can just tell MetaBuild explicitly which repo and commit to use.
```py
## Inside META.py
project_link("console")
```
```ini
## Inside META.lock
[console]
repo = git@git.corp.adobe.com:euclid/console.git
commit = 9e5f1e494c162d1cbd84976bafbd87127f6c82a8
# optional, tells MetaBuild to not look for submodules when checking the repo out to save some time
submodules = false
```

When you are locally debugging, you can even pass the location of a file on your disk like this.
```py
# project_link("console", root = "pass/to/folder/that/contains/console's/META.py")
```

Now let's create our executable that uses both the console and the CLI11 libraries.
```py
cxx_binary(
    name = "exec",
    srcs = "main.cxx",
    deps = [
```
The target names are found in the META.py file of CLI11. CLI11 was used from the meta-libs unified links. Therefore, to find its META.py I first look in [meta-libs/libs/CLI11/META.py](https://git.corp.adobe.com/meta-build/meta-libs/blob/main/libs/CLI11/META.py). It has the following entry  `git_tags(repo = "git@git.corp.adobe.com:meta-specs/CLI11.git", prefix = "v")`, which tells me that the META.py file of CLI11 is in [this](git@git.corp.adobe.com:meta-specs/CLI11.git) repo. When the `git_tags()` command is used, the versions that the `META.lock` file accept are the tags of the `git@git.corp.adobe.com:meta-specs/CLI11.git` repo that have a prefix
v and follow the semver convention. In the end, I have to look in `meta-specs/CLI11.git` to find the META.py file and the target names. Note that when referencing a different project we have to use the full target names.
```py
        "CLI11//:CLI11",
```

For console, I used an explicit location for the META.py file instead of using the links inside `meta-libs`. I specifically said that the META.py file is in [here](https://git.corp.adobe.com/euclid/console/blob/master/), where I can also find the target names.
```py
        "console//:lib_console",
    ]
)
```

And here is our usual main group that specifies the default target.
```py
group("main",
    deps = [
        ":exec"
    ]
)
```

### META.lock
```
[projB//:console_git]
commit = 9e5f1e494c162d1cbd84976bafbd87127f6c82a8

[CLI11]
version = 1.9.0
```

### main.cxx

Some basic usage of both console and CLI11 for illustrative purposes.

```cpp
#include <console/Console.h>
#include <console/LogService.h>
#include <console/LogFilters.h>
#include <console/LogSinks.h>
#include <CLI/CLI.hpp>

#include <string>

int main(int argc, char *argv[]) {
    CLI::App app{argv[0]};
    class {
    public:
        std::string something = "something";
    } args;
    app.option_defaults()->always_capture_default();
    app.add_option("something,--something", args.something);

    CLI11_PARSE(app, argc, argv)


    console::LogFilterContextAndSeverityPtr filter(new console::LogFilterContextAndSeverity(console::LogSeverity::Performance));
    console::LogService::add_output_port("std::cout_output", filter, console::LogFilterStdOutPtr(new console::LogFilterStdOut()));
    console::couti << "Something is entered: " << args.something;

    return 0;
}
```
