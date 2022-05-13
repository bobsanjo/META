---
permalink: /docs/internals/architecture/
title: "Architecture Overview"
toc: true
---

MetaBuild is designed to be both a library and a command line tool.

All the command line commands are stored in the [metabuild/commands](https://git.corp.adobe.com/meta-build/meta-build/tree/main/metabuild/commands) subfolder.

## MetaUniverse

[meta.core.MetaUniverse](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/core/MetaUniverse.py)

The ``MetaUniverse`` object is the root object that needs to be created in order to bootstrap MetaBuild. The object
holds information about everything needed to prepare the projects:

- Global target configuration (platform, flavors and build configuration)
- Holds a reference to the root `MetaProject` selected via the "--meta" command line argument.
- Holds a reference to the target `MetaNode` selected via the "--target" command line argument.
- Holds references to all the `MetaProject`_ objects that are loaded during the generation of the project.
- The output directory.
- The type of generator and an actual instance of the `Generator`_ object.
- An instance of the `Cache`_ object.

**Note:** During the regular execution of the ``metabuild`` a single ``MetaUniverse`` object is created. However, it is important to understand that the ``MetaUniverse`` is **not** a singleton. Other projects can embed the ``metabuild`` as a library and can simultaneously use multiple ``MetaUniverse`` objects.
{: .notice--info}

Note that by default no META files are loaded by the MetaUniverse. Loading of other META files happens
automatically on demand as the resources are requested by the dependency tree.

## MetaProject

[meta.core.MetaProject](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/core/MetaProject.py)

By default there's a single `MetaProject`. This project is created by loading the initial META file
referenced by the main ``--meta`` file references via the command line arguments.

The META files are just regular *Python* files that have a a few more global methods injected into the global space.

For a complete list of the methods check [Py Methods]({{ site.baseurl }}{% link
_docs/guides/py_method.md %}).

## MetaModule

[meta.core.MetaModule](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/core/MetaModule.py)

TBD

## MetaNode

[meta.core.MetaNode](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/nodes/MetaNode.py>)

TBD

## Cache

[meta.utils.Cache](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/utils/Cache.py)

MetaBuild uses a local cache that is shared across all projects.

By default the store is created at ``~/.adobe_meta_cache``.

The Cache deals with multiple types of shared data:

- Global configuration settings like the Artifactory key.
  The [`metabuild config`]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) command can
  be used to read and write the settings in the cache.
  
- GIT repositories are checked out as bare repos. When a project embeds a GIT repo, a new
  [`git worktree`](https://git-scm.com/docs/git-worktree) is created inside the project, but all the
  checkouts share the same common ".git" folder. This model improves checkout times and reduces space
  by sharing the GIT history across all repos.

- HTTP downloads from Artifactory are stored in the cached.

The `Cache` object uses a `StateFile` to store all the metadata,
the default location of the DB is `~/.adobe_meta_cache/status.sqlite.db`.

## StateFile

[meta.utils.StateFile](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/utils/StateFile.py)

Wrapper over Sqlite DB API to make it easy to read/write JSON based values in a DB file.

## Generator

[meta.generator.Generator](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/generator/Generator.py)

Base class used to generate projects.
