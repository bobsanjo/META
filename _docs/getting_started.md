---
permalink: /docs/getting_started/
title: "Getting started with MetaBuild"
toc: true
---

## Install MetaBuild

Follow the [MetaBuild install guide]({{ site.baseurl }}{% link _docs/install_metabuild.md %}).

## Follow the tutorial

You can find the tutorial [here]({{ site.baseurl }}{% link _docs/tutorial/main.md %}).

## Clone a sample project

We can either use `git clone` to clone one of the sample projects, or we could use the builtin `metabuild clone` command to automatically clone the projects using just the name:

### Using `git clone`

- [Umbrella project](https://git.corp.adobe.com/meta-samples/UmbrellaSample) sample:

    ```shell
    git clone git@git.corp.adobe.com:meta-samples/UmbrellaSample.git
    ```

- [Product project](https://git.corp.adobe.com/meta-samples/ProductSample) sample:

    ```shell
    git clone git@git.corp.adobe.com:meta-samples/ProductSample.git
    ```

- [LibraryA](https://git.corp.adobe.com/meta-samples/LibraryA) sample

    ```shell
    git clone git@git.corp.adobe.com:meta-samples/LibraryA.git
    ```

- [LibraryB](https://git.corp.adobe.com/meta-samples/LibraryB) sample

    ```shell
    git clone git@git.corp.adobe.com:meta-samples/LibraryB.git
    ```

### Using `metabuild clone`

- [Umbrella project](https://git.corp.adobe.com/meta-samples/UmbrellaSample) sample:

    ```shell
    metabuild pm clone @samples/UmbrellaSample
    ```

- [Product project](https://git.corp.adobe.com/meta-samples/ProductSample) sample:

    ```shell
    metabuild pm clone @samples/ProductSample
    ```

- [LibraryA](https://git.corp.adobe.com/meta-samples/LibraryA) sample

    ```shell
    metabuild pm clone @samples/LibraryA
    ```

- [LibraryB](https://git.corp.adobe.com/meta-samples/LibraryB) sample

    ```shell
    metabuild pm clone @samples/LibraryB
    ```

## Prepare the project

Change current directory to the project that was just cloned in previous step.

```shell
cd [project_name]
```

Prepare the Xcode / Visual Studio project.

```shell
metabuild prepare
```

Open the generated project and build using Xcode or Visual Studio.
