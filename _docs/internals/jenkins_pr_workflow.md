---
permalink: /docs/internals/jenkins_pr_workflow/
title: "Jenkins PR workflow"
toc: true
---

Here you can find some information and tips regarding MetaBuild Jenkins workflow and automatic versioning.

## Accessing the Jobs

### PR jobs

Every PR commit kicks off a Jenkins job that you can access by clicking on the `Details` at the bottom of the PR page on github.

![](https://git.corp.adobe.com/storage/user/30871/files/294f3d80-8821-11ec-94ba-48ad853e77db)

When your PR is merged into main, another Jenkins job is kicked off based on the new `main` branch. This job can be accessed by going to the commit history of the [main](https://git.corp.adobe.com/meta-build/meta-build/commits/main) branch. Then click on the icon under the merged PR (it is either a green checkmark, a red cross or a yellow circle). Then click on the `Details` link.

### `main` branch job

![](https://git.corp.adobe.com/storage/user/30871/files/e3df4000-8821-11ec-8413-d00d173d20fe)

The Job description lives in the [Jenkinsfile](https://git.corp.adobe.com/meta-build/meta-build/blob/0.1.629/Jenkinsfile) that uses the [torq-shared-pipeline](https://git.corp.adobe.com/torq/torq-shared-pipeline) groovy library (we are interested to use [meta-build-jenkins](https://git.corp.adobe.com/meta-build/meta-build-jenkins), which is used for all specs in [meta-specs](https://git.corp.adobe.com/meta-specs/), library instead for consistency).

## Important Info on the Job Page

You can find the following helpful info

- The `pipeline` tab. The following is for the main branch Jenkins jobs. The PR jobs have a subset of these steps.
  - Python Linter: this is the [linting checks]({{ site.baseurl }}{% link _docs/internals/contribute.md %}#linting).
  - Testing Linux, Windows, MacOS: the unit tests.
  - Version: this is where Jenkins creates a new `tag` (version) on the MetaBuild github repo and bumps the `latest` tag. __Until the main pipeline is launched ans reaches this stage, no new tag will be pushed, neither will `latest` be updated__.
  - Push MB and deps to artifactory: pushes the wheel for MB and its dependencies to [MetaBuild's pypi repository](https://artifactory.corp.adobe.com/artifactory/api/pypi/pypi-metabuild-dev-local).
  ![](https://git.corp.adobe.com/storage/user/30871/files/cca25180-8825-11ec-814e-8bc27ba3db0f)
- The `tests` tab.
  - Shows a visually nice parsed version of the results of MetaBuild's unit tests.
  ![](https://git.corp.adobe.com/storage/user/30871/files/cf9d4200-8825-11ec-96eb-78357007dbf8)
- The `artifacts` tab.
  - `verbose_test_log.txt`: The verbose MetaBuild log for the unit tests.
  - `Test Timing`: A table summarizing the time it took to run each unit test on each builder (MacOS, Windows, Linux).
  - `Python Coverage`: Coverage report for MetaBuild unit tests.
  ![](https://git.corp.adobe.com/storage/user/30871/files/d1670580-8825-11ec-8754-6631873990fe)

## Re-launching a Jenkins job

This can be useful in multiple cases, e.g.,
  - When the last job for the main branch failed so no new version of MB is released, but you want a new one to be released anyway. You can launch a job and disable the `run the tests`.
  - When there was a builder related failure and you want to try again with another builder. You can find a list of all builders [on this page](https://torq-build.ci.corp.adobe.com/job/Meta%20Build/) on the left panel.

To re-launch a job, follow these steps. 
  - Go to the Job's page (see [accessing the job](#accessing-the-jobs)).
  - Then click on the arrow icon to go the classic view instead of blue ocean.
    ![](https://git.corp.adobe.com/storage/user/30871/files/cd39e880-8823-11ec-9995-563dcad13402)
  - Go to the main page of the Jobs for the PR branch or the main branch.
    ![](https://git.corp.adobe.com/storage/user/30871/files/cdd27f00-8823-11ec-9423-5f95044dde73)
  - Click on `Build with Parameters`
    ![](https://git.corp.adobe.com/storage/user/30871/files/cf03ac00-8823-11ec-8c44-0a9a1bff7dfe)
  - Specify the parameters and press build. Using the parameters you can enable or disable parts of the pipeline. You can also select what machine(s) to use to run the pipeline.
    ![](https://git.corp.adobe.com/storage/user/30871/files/cf9c4280-8823-11ec-8e19-5f794ad52984)

## Mapping commits and versions

- To see the first version that contains a change introduced by a PR, go to the omit history of the [main](https://git.corp.adobe.com/meta-build/meta-build/commits/main). Click on the commit that corresponds to the merged PR, and then on the top left you can see the first version that contains this change.
  ![](https://git.corp.adobe.com/storage/user/30871/files/eb531900-8822-11ec-8e5a-edcd8dc0d51b)
- To see the commit history for a specific version use the following link pattern (replace `<version>` with the actual version.)
  - `https://git.corp.adobe.com/meta-build/meta-build/commits/<version>`
  - For example `https://git.corp.adobe.com/meta-build/meta-build/commits/0.1.629`

## Common Builder Issues 

Sometimes MetaBuild unit tests fail because of builder specific issues. Here are some of the common issues that can happen from time to time.

### Windows UWP

- Installation of MetaBuild test apps (`metabuild.build.test.app`) is failing
  - MetaBuild runs some executables for UWP during its unit tests. They have to be installed as Windows apps and they are all called `metabuild.build.test.app`. Sometimes they can get into a bad state (installed by a user other that `torqbld`), and would need to be uninstalled for all users with administrator privileges. In this case run this in an administrator powershell terminal
    ```
    Get-AppxPackage -AllUsers -Name metabuild.build.test.app | remove-appxpackage -AllUsers
    ```
- Running the MetaBuild test apps is failing
  - The executables run via `cdb.exe`. This needs a recent version of cdb. Make sure at cdb's version is `>=10.0.16299.15`. See [installing CDB]({{ site.baseurl }}{% link _docs/guides/install_cdb_on_windows.md %}).
  - Some tests check for the existence or non-existence of files in the installed app bundle. Sometimes the app bundle folder under `C:\Program Files\WindowsApps\metabuild.build.test.app...` gets in a bad permission state and will not be deleted, even when the app is uninstalled. In this case these tests will start failing, since the content of that folder is not correct anymore. Unfortunately, the folder cannot be automatically deleted that easily since the permission of `WindowsApps` folder is System. For now, we have worked around it by disabling any check that requires a file to `not exist`. [METAB-695](https://jira.corp.adobe.com/browse/METAB-695).
    ![](https://git.corp.adobe.com/storage/user/30871/files/6bde4c00-88ed-11ec-891d-12a13a22e0a8)
- `ilc.exe` cannot be found
  - This error might need reinstalling or repairing the Visual Studio installation on the builder. See more details on the [UXP docs](https://developers.corp.adobe.com/uxp/docs/jenkins/gotchas.md#windows-build-error).

### Apple

  - IOS signing issues
    - MetaBuild uses the same builders as UXP. The instructions for setting up the IOS signing workflow can be found in the [UXP docs](https://developers.corp.adobe.com/uxp/docs/jenkins/build_ios.md).
  - Xcode helper process not having enough privileges. Some unit tests use Xcode's test scheme. They fail if it is not setup correctly.
    - go to System Preferences / Security & Privacy / Select Privacy tab
    - Pick Accessibility from the list on the left
    - Look for Xcode Helper in the list on the right and make sure it is checked.
