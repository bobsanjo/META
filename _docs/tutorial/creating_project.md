---
permalink: /docs/tutorial/creating_project/
title: "Creating a new MetaBuild project"
toc: true
---

**Note:** If you are already familiar with MetaBuild projects and need to update third party library in `meta-specs`, we have a [more dedicated guide]({{ site.baseurl }}{% link _docs/guides/thirdparty_libraries.md %}).
{: .notice--warning}

## High level picture

We covered how to use an existing project in the Section [Using existing MetaBuild projects]({{ site.baseurl }}{% link _docs/tutorial/existing_project.md %}). Here, we will cover how to create a new one.

Each project might have a few components. Let's see how to deal with each.
- __Source code__:
  For internal Adobe projects, they are already hosted in git.corp. For external projects, however, some orgs explicitly require using a repository inside git.corp. Therefore, if you are using a repository __outside__ git.corp, you need to mirror it inside git.corp. If a well known mirror already exists, use that (e.g., [photoshop's boost](https://git.corp.adobe.com/thirdparty/boost)). If a mirror does not exist, create one inside the [meta-archives](https://git.corp.adobe.com/meta-archives) org. You can find more about creating a mirror in the [misc. guides]({{ site.baseurl }}{% link _docs/guides/thirdparty_libraries.md %}#mirroring-an-external-git-repository) section of the tutorials.
- __Artifacts__:
  Projects can have artifacts. Be kind to the people that will contribute to your code and use git repositories for code and not large files. Large files or things that don't need to be version controlled should be stored in artifactory. If you are writing META.py specs for an internal Adobe repository, the artifacts should go into your own artifact repository. If the project is external, and does not have its own artifactory repo, use the [meta-archives](https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/) artifactory repository. You might need to ask for __write__ permission on the #metabuild slack channel to do so. Note that, delete or overwrite permissions are not granted, to prevent accidental deletion of files. You can use MetaBuild to [upload files to artifactory]({{ site.baseurl }}{% link _docs/cli/metabuild_http.md %}).
- __Metabuild specs__:
  This is the `META.py` file (and potentially additional `*.meta.py` files) that describe how your project should be built. For Adobe repositories, the META.py file should either go in the root of the repo, or in  a top level `META` folder. For external repos, the `META.py` files goes within a repository inside the [meta-specs](https://git.corp.adobe.com/meta-specs) org.
- __Package Management__:
  Any project that a customer project links to, needs to know where to find its own meta specs (Meta.py file). [meta-libs](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs) is a centralized repository that holds a mapping between (name + version) of projects to the location where their META.py file is stored.

Now you should know the importance of each of these locations.


The use of all these different locations might be daunting at first look. But the pain and sorrow it saves is incomparable to this minor discomfort.
  - [meta-archives](https://git.corp.adobe.com/meta-archives) org for mirroring external repos that already don't have a mirror.
  - [meta-archives](https://artifactory.corp.adobe.com/artifactory/generic-metabuild-release/) artifact repo for external projects that don't have their own artifact repo.
  - [meta-specs](https://git.corp.adobe.com/meta-specs) org for placing meta specs of external repositories that are only mirrored in git.corp.
  - [meta-libs](https://git.corp.adobe.com/meta-build/meta-libs/tree/main/libs) repository which holds a 'name' <-> 'where to find the meta specs for each version' mapping. If a project is listed in meta-libs, using it elsewhere is as easy as just typing `project_link('thatprojectsname')` + putting a version for it in the `META.lock` file.

## Field experience

Let's now get our hands dirty and write meta specs for an external repository. For example, [draco](https://github.com/google/draco) mesh compression library. You can already find the specs [here](https://git.corp.adobe.com/meta-specs/draco). I will repeat them here in this doc with more comments to get into detail of what each command is doing.

You can further find all sorts of examples here: https://git.corp.adobe.com/meta-specs

```py
set_project_name("draco")
set_output_directory("dist")
```

Now we specify the dependencies of draco project. googletest is needed for the `draco//:tests` target. Since googletest is already in meta-libs repo, we don't specify a link. Also note that MetaBuild is smart, and if you don't ask it to build the tests target, it will not bring in googletests.
```py
project_link("googletest")
```

We need to grab the source code. Since draco lives in a repository in github, and Shayan at the time of writing this did not find a mirror in git.corp, he mirrored it in `git@git.corp.adobe.com:meta-archives`. And now this line tells MetaBuild to clone this repository. We specify the tag or commit sha1 at which the draco repository should be checked out in the META.lock file. Note that when we specify the version of the external library like this, there should be a one to one correspondence between the branches of the meta-specs repo and the versions of the external lib that we wanna support. This means that multiple branches of the spec repo have to be maintained. It is also possible to handle multiple versions of the external repo, in a single set of META.py-META.lock files. In this case, only one branch of the spec repo needs to be active. We describe this more advanced case in the [misc. guides]({{ site.baseurl }}{% link _docs/guides/thirdparty_libraries.md %}#handling-multiple-versions-of-an-external-repo-in-a-single-spec-file) section.
```py
git_checkout(
    # From now on you can refer to the path that this repo is cloned at as
    # $(location :draco_git)
    name = "draco_git",
    repo = "git@git.corp.adobe.com:meta-archives/draco.git",
)
```

The actual draco spec does not need to download anything from artifactory, but for illustrative purposes, we download some files from artifactory here. Note that unlike the photoshop artifactory tool, you do not need to associate a platform to your artifacts. MetaBuild smartly downloads only the artifacts that it needs.
```py
http_archive(
    name="FBX_win_archive", # some unique name within this project
    urls="Link to download this",
)
```
See docs on [http_archive]({{ site.baseurl }}{% link _docs/api/http_archive.md %}) for more details. Note that http_archive expects an archive file (zip, tar, etc). And then it will extract this archive, and the path to the extracted content is available as `$(location :unique_target_name)`. [Autodesk FBX]((https://git.corp.adobe.com/meta-specs/FBX/blob/master/META.py)) is a project that actually uses this the `http_archive` command, since it is only provided as a closed source SDK.


Draco cmake uses generated files. You probably have seen them, files like `config.h.in`, that CMake magically uses to generate a config.h file. Metabuild has the [`genrule`]({{ site.baseurl }}{% link _docs/api/genrule.md %}) command to achieve the same purpose.
```py
def _generate_features(input):
    update_file(input.gen_srcs[0], "// AUTOGENERATED TO MAKE DRACO HAPPY \n")
    update_file(input.gen_srcs[1], "// AUTOGENERATED TO MAKE DRACO HAPPY \n")

genrule(
    name = "generated_files",
    phase = "prepare",
    gen_srcs = [
        # these will be created inside a unique folder
        "draco/draco_features.h",
        "draco/draco_test_config.h",
    ]
    py = _generate_features,
)
```

Now we specify the draco main target (`draco//:draco`) which is a library. We have to use the [`cxx_library`]({{ site.baseurl }}{% link _docs/api/cxx_library.md %}) command.
```py
cxx_library(
    name = "draco",
```

This specifies the include directories that also get inherited by customers of `draco//:draco`. Note that `$(location :generated_files)` is the path to the folder containing the files that I just generate with `gen_rule()`. And `$(location :draco_git)` is the folder where the draco repo was cloned.
```py
    public_include_directories = [
        "$(location :generated_files)",
        "$(location :draco_git)/src",
    ],
```

Now I specify the source files with the help of the [`glob()`]({{ site.baseurl }}{% link _docs/api/glob.md %}) command. Note that we can prevent the repetitive use of `$(location :draco_git)` by using the [`set_root_directory('$(location :draco_git)')`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) command. This command can be used multiple times without any side effects. Arguments passed as the `exclude` argument cannot be absolute and must to relative to the root directory. This is due to patters like `*/test/*`. In such cases, if absolute paths were allowed, the test folder could match anything in the path, so the builds can break when somebody uses a folder like `/Users/test/code/...` to checkout MB projects.
```py
    srcs = [
        cpp_glob([
            "$(location :draco_git)/src/draco/animation/**",
            "$(location :draco_git)/src/draco/attributes/**",
            "$(location :draco_git)/src/draco/compression/**",
            "$(location :draco_git)/src/draco/metadata/**",
            "$(location :draco_git)/src/draco/mesh/**",
            "$(location :draco_git)/src/draco/point_cloud/**",
            "$(location :draco_git)/src/draco/core/**",
        ], exclude=[
            "/src/draco/core/draco_test_base.h",
            "/src/draco/core/draco_test_utils.h",
            "/src/draco/core/draco_test_utils.cc",
            "/src/draco/core/draco_tests.cc",
            "/src/draco/*/**_test.cc",
        ]),
    ],
```

I need to specify preprocessor macros as well. These need to get propagated, so I use the `exported_` version. In case I need to specify flags only in certain conditions, I can use filters. The [`target`]({{ site.baseurl }}{% link _docs/api/target.md %}) object has filters for detecting the OS for example.
```py
    exported_preprocessor_macros = [
        "DRACO_MESH_COMPRESSION_SUPPORTED",
        "DRACO_NORMAL_ENCODING_SUPPORTED",
        "DRACO_STANDARD_EDGEBREAKER_SUPPORTED",
        # if a flag needs to be only available on windows or mac we can do
        # (target.win, "ONLY_FOR_WIN")
    ],
```

Here, I specify other MetaBuild targets that `draco//:draco` depends on. Since `draco//:generated_files` is not a lib, this just means that "dear MetaBuild please create the generated_files before building me". If I put other cpp library targets in here, it means that they have linkage dependency. There is also a `exported_` version of deps.
```py
    deps = [
        ":generated_files"
    ]
```

We are building draco from source, and we don't use prebuilt binaries. However, for the sake of demonstration, here is how we can associate prebuilt binaries with our target. We need to pass these libraries as `exported_linker_libraries` or `linker_libraries` arguments with the help of [user_lib]({{ site.baseurl }}{% link _docs/api/user_lib.md %}) and [system_lib]({{ site.baseurl }}{% link _docs/api/system_lib.md %}). We can use filters again to use the correct prebuilt library.
```py
    exported_linker_libraries = [
        (target.win32 & (target.debug | target.coverage), user_lib(
            lib="$(location :FBX_win_archive)/win/lib-vs2015-x64-dngit/debug/libfbxsdk.lib",
            dll="$(location :FBX_win_archive)/win/lib-vs2015-x64-dngit/debug/libfbxsdk.dll",
            symbols="$(location :FBX_win_archive)/win/lib-vs2015-x64-dngit/debug/libfbxsdk.pdb",
        )),
        (target.win32 & target.release, user_lib(
            lib="$(location :FBX_win_archive)/win/lib-vs2015-x64-dngit/release/libfbxsdk.lib",
            dll="$(location :FBX_win_archive)/win/lib-vs2015-x64-dngit/release/libfbxsdk.dll",
        )),
        (target.apple & (target.debug | target.coverage),
            user_lib("$(location :FBX_osx_archive)/osx/lib-clang/debug/libfbxsdk.dylib"),
        ),
        (target.apple & target.release,
            user_lib("$(location :FBX_osx_archive)/osx/lib-clang/release/libfbxsdk.dylib"),
        ),

        # Here is how we can link to system libraries
        (target.windows, system_lib("Shlwapi.lib"),

        # We can also link to system frameworks on mac
        (target.macos, system_lib.framework("Cocoa")),

        #  windows SDKs
        (target.windows, system_lib.sdk("CppUnitTestFramework.Universal, Version=$(UnitTestPlatformVersion)")),

        # packages installed using nuget()
        (target.windows, system_lib.nuget("Microsoft.Windows.CppWinRT")),

    ], # exported_linker_libraries
```
Here are more examples on [`system_lib.sdk("")`](https://git.corp.adobe.com/meta-build/meta-build/blob/main/tests/generator/__fixtures__/uwp_test_app/META.py#L23) and [`system_lib.nuget("")`](https://git.corp.adobe.com/meta-samples/winrt_test/blob/master/META.py#L59). If you use `nuget`, the version of the lib must go to the META.lock file ([example](https://git.corp.adobe.com/meta-samples/winrt_test/blob/master/META.lock#L1)).


The previous strategy does not apply to dynamic libraries that are hot loaded with `dlopen()`. We just copy these libraries to the executable directory (or its Frameworks directory for mac). It can be done with the [`data`]({{ site.baseurl }}{% link _docs/guides/resource_spec.md %}) argument (for an actual usage, see [here](https://git.corp.adobe.com/meta-specs/MDL-SDK/blob/main/META.py#L40)).
```py
    data = {
        # These go to Frameworks for mac. For win they just go to the executable dir
        "frameworks": [
            (target.apple ,[
                "$(location :MDL_SDK_osx_archive)/osx/lib/libmdl_sdk.so",
                "$(location :MDL_SDK_osx_archive)/osx/lib/nv_freeimage.so",
                "$(location :MDL_SDK_osx_archive)/osx/lib/dds.so",
            ]),
            (target.windows ,[
                "$(location :MDL_SDK_win_archive)/win/lib/libmdl_sdk.dll",
                "$(location :MDL_SDK_win_archive)/win/lib/nv_freeimage.dll",
                "$(location :MDL_SDK_win_archive)/win/lib/dds.dll",
            ]),
        ],

        # For test data or assets use this
        # They will go to Resources for mac. For win will just go to the executable dir.
        "resources" : [
            # blah blah
        ],
    },
```

All this time we were still within the parenthesis of the cxx_library function. So let's close it.
```py
)
```

To make sure you built the library correctly, create a small test, or directly build the tests of the said library.
```py

# create a temp directory to put the test output to
unique_folder(name = "draco_temp")

cxx_binary(
    name = "draco_tests",

    srcs = [
        "$(location :draco_git)/src/draco/core/draco_test_base.h",
        "$(location :draco_git)/src/draco/core/draco_test_utils.h",
        "$(location :draco_git)/src/draco/core/draco_test_utils.cc",
        "$(location :draco_git)/src/draco/core/draco_tests.cc",
        cpp_glob([
            "$(location :draco_git)/src/draco/*/**_test.cc",
        ], exclude = [
            "/io/file_reader_factory_test.h",
            "/io/file_reader_factory_test.cc",
        ]),
    ],
    preprocessor_macros = [
        "DRACO_TEST_DATA_DIR=\"$(location :draco_git)/testdata\"",
        "DRACO_TEST_TEMP_DIR=\"$(location :draco_temp)\"",
    ],

    deps = [
        ":draco",
        "googletest//:gtest",
        "googletest//:gmock",
    ],
)
```

Finally, we specify the main group. If you run MetaBuild build in the draco repo itself, it will try to build the targets in here. If you are just linking to draco, linking to `draco//:draco` is what you need. MetaBuild is smart and does not clone gtest and gmock if you are only linking to `draco//:draco` in another project down the road.
```py
group(
    name = "main",
    deps = [
        ":draco",
        ":draco_tests",
    ]
)
```
