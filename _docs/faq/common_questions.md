---
permalink: /docs/faq/common_questions/
title: "Common Questions"
---

### I see an error message printed by MetaBuild, the message is not informative enough. How can I request a more informative message?

Please create a [JIRA](https://jira.corp.adobe.com/projects/METAB/issues) ticket and communicate it via a message to the [`#metabuild`](https://adobe.slack.com/archives/CP416U06M) with the JIRA link.

We will prioritize accordingly and address it according to the MetaBuild team's resources. 
Typically, by adding a section under [Common Errors]({{ site.baseurl }}{% link _docs/faq/common_errors.md %}), elaborating on potential reasons for the error to happen, and what are the solutions. We then create a link from the exception raise in MetaBuild to the in the docs.

If you would like to contribute in expanding the error message (this can help getting addressed sooner for all MetaBuild users to benefit), you can place a PR on the MetaBuild docs repo under [Common Errors]({{ site.baseurl }}{% link _docs/faq/common_errors.md %}) (see [How can I contribute to MetaBuild docs](#How-can-I-contribute-to-MetaBuild-docs)).


### How can I contribute to MetaBuild docs

Fork and clone the [meta-build.git.corp.adobe.com ](git@git.corp.adobe.com:meta-build/meta-build.git) repository. Then follow [serving the local webpage]({{ site.baseurl }}{% link _docs/internals/docs.md %}#serving-the-local-webpage) to serve the website locally on your machine (so that you can verify your edits). Make your desired changes, and then place a PR using your fork.


### How do I integrate a new third party lib to my app / library?

Read the tutorial on how to use an already existing external library [here]({{ site.baseurl }}{% link _docs/tutorial/existing_project.md %}). The most recommended way is using [project_link()]({{ site.baseurl }}{% link _docs/api/project_link.md %}).

If the project does not have MetaBuild spec files, they have to be created first. See the [tutorial]({{ site.baseurl }}{% link _docs/tutorial/creating_project.md %}) on how do this.

#### Some common mistakes when using external libraries are:

1. You should never use ‘..’ in your #include. If you need to do that, something is wrong or you must have a strong explanation.
2. You have added the source files or include paths of another lib directly to your own library/app. Instead you need to add a separate cxx_library that exports the correct public include directory. If the third party lib is not something you own iit would be best to create a shared spec in here — https://git.corp.adobe.com/meta-specs/ to host the META.py for that library.
3. You checked in external code inside a third-party folder. Make a clone of their repo and add it to https://git.corp.adobe.com/meta-archives/ instead, and use git_checkout (expanded further in the tutorial).

### Can my spec override properties on my dependency’s?

For example, if inside my spec i have a `project_link()` and I want to add some xcode_flags to that project. Can I do that?

First, there are [`universe_flags`]({{ site.baseurl }}{% link _docs/guides/global_flags.md %}). This are meant for flags that should be used uniformly for all the targets. Both for the targets in the [`root project`]({{ site.baseurl }}{% link _docs/guides/root_target.md %}) and all its dependencies, e.g. C++ version. In this case, we only process `universe_flags` of project A when A is the root project. If A is not the root project (and is a dependency) these flags are ignored. Each root project has to define its own `universe_flags`. For example, see how the C++ version is set in the [Lagrange repository](https://git.corp.adobe.com/lagrange/lagrange-lib/blob/v5.8.0/META/META.py#L51-L65).

In addition to `universe_flags` MetaBuild has a default project found under the [`metabuild/builtin`](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.20/metabuild/builtin) folder. Every target also inherits the flags from these projects. Some of these flags can be configured via the [MetaBuild config mechanism]({{ site.baseurl }}{% link _docs/guides/config_files.md %}). For example, the [DEPLOYMENT_TARGET](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.20/metabuild/builtin/xcode.meta.py#L320) in xcode is hooked to an [option](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.20/metabuild/builtin/xcode.meta.py#L18-L26) and can be set via the config [`[xcode]deployment_target=...`](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.20/metabuild/builtin/xcode.meta.py#L20). See an example usage here in the [Lagrange repository](https://git.corp.adobe.com/lagrange/lagrange-lib/blob/v5.8.0/META/META.lock#L10) (configs can be appended with platform name to only be applied to that platform).

Projects must not try to set the flags that need to be universal (uniform across all targets) for specific targets. Because they way properties can be overridden is `defaults -> universe_flags -> target`. If a target hard codes things like signing credentials, the root projects cannot change them anymore via the config values.

If a project wants to allow its dependees to modify some of the specific target's properties (e.g., `xcode_flags`, `preferred_linkage`, etc.), they should use options. Then the root project (dependee) can communicate with the dependcy, by changing the value of that option via configs. For example, see [Overriding the linkage using options]({{ site.baseurl }}{% link _docs/guides/dlls.md %}#overriding-the-linkage-using-options)
