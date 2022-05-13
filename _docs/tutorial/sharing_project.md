---
permalink: /docs/tutorial/sharing_project/
title: "Sharing a MetaBuild project with other MetaBuild projects"
toc: true
---

## Allow other projects using your project

Now you have written your MetaBuild project, and you would like to share it with others. Your new project can now be consumed in the same way other projects are consumed, as described in the [using an existing project tutorial]({{ site.baseurl }}{% link _docs/tutorial/existing_project.md %}). So no new machinery comes to play. Nevertheless, here, we go over the process again for completeness of the tutorial.

- Make sure that the `META.py` of your MetaBuild project is in the root directory of your repository, or at `META/META.py`. See for example the [euclid_ml](https://git.corp.adobe.com/euclid/ml/blob/08b86f4e26548cddf1ac45e70968f5f51d46c40d/META/META.py) project.
  - See [File structure for specs]({{ site.baseurl }}{% link _docs/guides/spec_file_structure.md %}) for more information regarding MetaBuild file structure and projects.
- Then other MetaBuild projects can simply consume your project in the process mentioned in [existing project tutorial]({{ site.baseurl }}{% link _docs/tutorial/existing_project.md %}). For example, the `euclid_ml` project is consumed in the [stager application](https://git.corp.adobe.com/euclid/stager/tree/792ff56e19acddce6dcffe9e2a248e45c15c5926/META). Here is a simplified version of what is happening there.
  - Usage of `ml` project is requested via a `project_link()` call [here](https://git.corp.adobe.com/euclid/stager/blob/792ff56e19acddce6dcffe9e2a248e45c15c5926/META/deps.meta.py#L10). By convention we put all the project links inside a `deps.meta.py` file so it is easy to see all dependencies.
  - Some target or targets in stager use a target from `euclid_ml`, [example](https://git.corp.adobe.com/euclid/stager/blob/792ff56e19acddce6dcffe9e2a248e45c15c5926/META/components/lantern_api.meta.py#L23).
  - `stager` tells MetaBuild how to retreive `euclid_ml` in the META.lock file, [here](https://git.corp.adobe.com/euclid/stager/blob/792ff56e19acddce6dcffe9e2a248e45c15c5926/META/META.lock#L77-L79). To see the details on how to tell MB where to retreive projects from see the docs for [project_link()]({{ site.baseurl }}{% link _docs/api/project_link.md %}). The typical ways are [`version=...`]({{ site.baseurl }}{% link _docs/api/project_link.md %}#version-is-used-or-if-simply-nothing-is-supplied), [`local_link=...`]({{ site.baseurl }}{% link _docs/api/project_link.md %}#local_link-is-used), and [`repo=... commit=...`]({{ site.baseurl }}{% link _docs/api/project_link.md %}#repo-and-commit-are-used). Note that no matter how many `project_link()`s to a project exists (e.g. diamond shaped deps), MetaBuild ensures only a single project is used everywhere in the dependency graph! And that the [root project]({{ site.baseurl }}{% link _docs/guides/root_target.md %}) can override where this project is coming from. This is the main goal of MetaBuild, it makes building everythign with the same version of a project easy. Also if a project referenced with `project_link()` is not used (reached by main target), MetaBuild will skip it.

Sometimes you may wish to give your users an option to consume your project as prebuilt to reduce build time. We have covered all the pieces needed to do that in these tutorials. See [Using prebuilts to save time]({{ site.baseurl }}{% link _docs/guides/build_result_caching.md %}) to see how these building blocks can be assembled together to achieve that.

## Upload build results to artifactory

If you want to upload the build result of you project to artifactory (e.g., apps want to have workable builds, or libraries might want to ship prebuilds to consumers that don't use MetaBuild), MetaBuild gives some functionality to do that as part of the build system. See the guide on [creating release bundles and uploading them]({{ site.baseurl }}{% link _docs/guides/creating_bundles_and_uploading.md %}).

__Note__: If project B wants to optionally consume project A as prebuilts to save time, and both have MetaBuild specs, the recommendation is to use the mechanism described in [Using prebuilts to save time]({{ site.baseurl }}{% link _docs/guides/build_result_caching.md %}) in which upload to artifactory happens at project B, and not project A. However, the guides also describe how to simply consume bundles that A provides.