---
permalink: /docs/becoming_a_user/
title: "Becoming a MetaBuild User"
---

If you are interested in using MetaBuild you can start by following the [MetaBuild Tutorial]({{ site.baseurl }}{% link _docs/tutorial/main.md %}).

If you need support or have questions, you can reach out in the #metabuild channel. We can also provide more dedicated support depending on the MetaBuild teams' schedule.

Once transition is in a good state, we expect you to
  1. Dedicate an engineer in your team to be the in-house MetaBuild expert.
  2. Properly report issues you face when using MetaBuild
  3. Lock the MetaBuild version in your codebase
  4. Stay up to date with recent versions of MetaBuild. We have created the MetaBuild stable pipeline to help you with that.
  5. Contribute to [`meta-specs`](https://git.corp.adobe.com/meta-specs) (MetaBuild specs for third party repos) and [`meta-archives`](https://git.corp.adobe.com/meta-archives)(mirror of third party repos) for your needs. See ["Specs for Third Party Libraries"]({{ site.baseurl }}{% link _docs/guides/thirdparty_libraries.md %}).
  6. Sign up for the MetaBuild stable pipeline to help us test MetaBuild more rigorously, and help yourself validating new versions of MetaBuild pretty much effortlessly.
  7. Include MetaBuild as part of your team's scope of work. Varying from training in house MetaBuild experts to contributing to MetaBuild depending on the size of your feature requests and the size of your team.

## In-house expert

With current MetaBuild staffing, the MetaBuild team cannot scale to answer every question that the developer of a team might have. So we ask each team to dedicate a person (or people) to be the expert in house of MetaBuild for the team (e.g., @ftrofin for DVA, @bgardner for photoshop) who can answer the day to day questions of team members. And that person can be in contact with the MetaBuild core team more regularly. Devs are encourage to ask questions #metabuild, but the expert in house should be the first front in answering the questions even if they are asked in #metabuild.

### Stakeholder meeting

We have a MetaBuild weekly stakeholder meeting, where (potential) users can ask questions, give status updates, and provide feedback. It is recommended to have a representative from your team to join (semi-)regularly. Please reach out to #metabuild for the invite.

## Reporting issues

If you suspect that there is a bug in MetaBuild, please use [JIRA](https://jira.corp.adobe.com/projects/METAB/issues) to report it. Note that you must include full steps on how to reproduce your issue. Also, please include the repository and `sha` (not just branch because branches can change) that needs to be checked out. Include all changes that is needed to reproduce the issue in the repo already and avoid instructions like: "checkout x, comment out y, add z, ...". 

Please note that the cases to reproduce your issue should be as simple as possible. This way the MetaBuild team can easily investigate it and see if it is indeed a bug. However, if you reproducing your issue includes checking out a whole product repo and building it, investigating would be delayed.

## Lock the MetaBuild version in your codebase

We recommend using a specific version inside your project, and updating this specific version regularly (after confirming that the new version is working for your particular project). If you need to compile an older version of a project, the recommendation is to use the version of MB that was known to work with that particular version of your project. 

To assign a MetaBuild version to each sha1 of your project, you can simply put the version in your README. Or even better, you can use a virtual environment spec file (a technique where python packages are installed locally in an isolated environment to be used only for your project, much similar to [local `node_modules`](https://docs.npmjs.com/cli/v7/configuring-npm/folders)). For example, a [pip `requirements.txt`](https://git.corp.adobe.com/structure/structure/blob/main/requirements.txt) or a [conda `.yaml` file](https://git.corp.adobe.com/euclid/stager/blob/develop/META/misc/stager.yaml). Note that you are not confined to these two methods for creating virtual environment, but these are two very common ones. You can read more about Conda [here]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}).

With this practice, if you need to build an old sha1 of your project, you simply check that out, and setup the corresponding virtual environment with its MetaBuild installation.

## Stay up to date

As a library developer at Adobe you will have to make sure your project works with the versions of MB needed by the host products that use your library. For that reason, we are going to enforce a rule of always up-to-date or as close as possible to `stable` for all projects. This is due to other projects also adopting MB, which triggers implementation of new features and requirements of using newer MB in order to support these new targets too.

To make it easy for teams to validate every new version of MetaBuild with their codebase, we have created the MetaBuild `stable` pipeline. You should sign up. Let us know in #metabuild and we will create JIRA tasks for the MetaBuild DevOps team to work with you to add your project to this pipeline.

## MetaBuild stable pipeline

We have a `stable` git tag which points to the latest MetaBuild version that has also passed through a more rigorous testing pipeline. With every new version of MetaBuild the stable pipeline is triggered. This Jenkins pipeline will use the new version of MetaBuild to place a PR on a series of repositories, a combination of products and open source projects. The pipeline then tracks the status of the PRs it has placed on the repos. If all the PRs pass, this pipeline certifies the new version of MetaBuild as `stable` and bumps the stable tag in the MetaBuild repo to match this new version. You can read more about the test pipeline for updating the `stable` tag [here](https://wiki.corp.adobe.com/display/metab/Releases).

- [MetaBuild stable pipeline source code](https://git.corp.adobe.com/meta-build/meta-build-status)
- [Example of MetaBuild stable pipeline execution](https://torq-build.ci.corp.adobe.com/blue/organizations/jenkins/Meta%20Build%2Fmeta-build-status/detail/main/335/pipeline)

### Requirements for signing up for the stable pipeline

1. Have a unified place in your codebase to mention the version of MetaBuild to be used. See [Lock the MetaBuild version in your project](#lock-the-metabuild-version-in-your-project). So that our stable pipeline can change this value in the PR it places on your repo.
2. If you have flaky tests, have a parameter (e.g. an option for MetaBuild in your lock file or an option in your Jenkinsfile) that can disable these tests. The stable pipeline can then use this parameter to disable these tests in the PR that it places on your repo. It is essential that there is no flaky tests for the purpose of MetaBuild stable pipeline.

### Current Adobe projects on MetaBuild stable pipeline

List extracted from [here](https://git.corp.adobe.com/meta-build/meta-build-status/blob/main/stage5-git-jobs.json).

- UXP, [git.corp.adobe.com/torq/torq-native](https://git.corp.adobe.com/torq/torq-native)
- XD, [git.corp.adobe.com/WebPA/sparkler-shell](https://git.corp.adobe.com/WebPA/sparkler-shell)

Note: XD and UXP are not satisfying requirement (2) above at this moment, so even though we do place PRs in their repos, ignore their failures at this moment. Once they do, we will take failures into account for bumping the stable tag.

## Include MetaBuild in your "budget"

If you have multiple feature requests for MetaBuild that are very specific to your team, and your team has a dedicated team that has the build systems under their responsibilities (e.g., DVA or Photoshop), the MetaBuild team will support you to transition to MetaBuild. However, once your transition is in a stable state, we expect you to work with MetaBuild team to manage your own feature requests. And if there are parts of MetaBuild specifically written for your team (e.g. the [mp module](https://git.corp.adobe.com/meta-build/meta-build/tree/main/metabuild/mp) for DVA), we expect you to take ownership of them.

Currently, at Adobe, budget for managing each team's build system lies in the team itself. And the MetaBuild team does not receive extra engineering resources with each new team added under its belt. Therefore, teams that do have resources for supporting the build system are expected to include "contributing to MetaBuild for their needs" in their responsibilities.

Even for smaller teams, we at least expect you to make yourself familiar with MetaBuild, and have engineers within your team that know MetaBuild well, and can answer the day to day questions of their teammates. And work with the MetaBuild team to create tickets and small reproducible examples if their team find regressions in MetaBuild.

Note that the contributions __must not be one off__ fixes. They must be in accordance with MetaBuild's ecosystem and design, and has to go through the usual Jenkins pipeline and code reviews. Otherwise, each team will end up with an incompatible instance of MetaBuild and the most significant goal of MetaBuild, sharing build specs and building from source, is thrown away!
