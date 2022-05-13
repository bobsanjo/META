---
permalink: /docs/guides/msvs_idl_resources/
title: "MSVS IDL Resources"
---

If you have a library that uses [IDL Resources](https://docs.microsoft.com/en-us/windows/win32/com/idl-files), you have to set the property [`msvs_generator = True`]({{ site.baseurl }}{% link _docs/api/cxx_node.md %}) when creating your library. Also, the location of the generated files from the IDL resources are available with the macro `$(midl_location)`.

MetaBuild by default does not enforce build dependency between static libraries, so that they can be built in parallel as much as possible. IDL files, however, have to be compiled with the MIDL compiler before the library is used by its dependencies. The `msvs_generator = True` property asks MetaBuild to enforce the dependency in such cases.

In the following example, first A will be built and then B. However, if `msvs_generator = True` is not specified, both will be built in parallel, and B can error out due to not finding the compile IDL resources of A. 
```py
cxx_library(
    name = 'A',
    srcs = ['x.idl'],
    msvs_generator = True,
    # (*) if you need others that depend on this to see the generated
    # header files.
    public_include_directories = ['$(midl_location)'],
)

cxx_library(
    name = 'B',
    deps = [':A'],
    # Alternative to using (*)
    include_directories = ['$(midl_location :A)'],
)
```

Only use `msvs_generator = True` if it's truly needed. It affects the build performance by preventing parallelization of the targets that depend on it.
