---
permalink: /docs/internals/docs/
title: "Documentation"
toc: true
---

## Edit directly on GitHub

You can send a PR directly from your browser. Each page has a link on the bottom called "Edit this page on GitHub". Click that link and use GitHub's Edit button on the upper right corner. Changes to the main branch are automatically republished by GitHub.

## Local setup

GIT: [meta-build/meta-build.git.corp.adobe.com](https://git.corp.adobe.com/meta-build/meta-build.git.corp.adobe.com)

The documentation is using GitHub Pages via `jekyll` site generator.

### Clone the repo

```shell
git clone git@git.corp.adobe.com:meta-build/meta-build.git.corp.adobe.com.git
cd meta-build.git.corp.adobe.com
```

### Serving the local webpage

You have two choices to serve the webpage locally, depending on whether you install the Jekyll site generator locally or via docker. Using docker can be very slow due to the poor performance of docker accessing files on your native os. But on windows, setting up the docker workflow is easier than native Jekyll install.

#### Local Jekyll install (Mac and Linux)

1. Install the conda package manager. Do not worry, this package manager will be installed locally and will not mess up with your global system setup. You can follow the sections [using conda]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}#installing-conda) and [activating conda]({{ site.baseurl }}{% link _docs/guides/using_conda.md %}#activating-conda).
2. You only need to do this step once. If you have done this step before jump to 3. In a terminal with conda activated, create a new env for Jekyll, and install Jekyll inside it.
   ```terminal
    conda create -n jekyll
    conda activate jekyll
    conda install -c conda-forge rb-jekyll 
   ```
3. Activate the jekyll env
    ```terminal
    conda activate jekyll
    ```
    now  you should see the lower left of your terminal saying `(jekyll)`.
4. Serve the website.
    ```terminal
    bundle exec jekyll serve
    ```

#### Use Jekyll within Docker (Windows)

- Install Docker
- Install python `invoke` package (`pip install invoke`)
- Run `invoke serve`

## Download a static set of html files of website

Jekyll does not directly generate a website that can be viewed without any webserver. However, you can acheive by `wget`. First, serve the website locally. Then, call

```
wget --mirror --convert-links http://127.0.0.1:4000/
```

This needs wget. You can install it via conda (or brew, or apt).
