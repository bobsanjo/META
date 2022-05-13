---
permalink: /docs/guides/using_conda/
title: "Installing Python and MetaBuild with Conda"
---

## Installing Conda

The Conda package manager can be installed locally at any desired location on your system. 

- If on mac (also works for M1), run the [install_conda.sh](https://git.corp.adobe.com/meta-samples/conda_setup/blob/main/install_conda.sh) script (no sudo needed)
    ```
    bash ./install_conda.sh /path/to/install
    ```
- If on windows , run the [install_conda.ps1](https://git.corp.adobe.com/meta-samples/conda_setup/blob/main/install_conda.ps1) script (no admin access needed)
    ```
    powershell ./install_conda.ps1 \path\to\install
    ```

## Activating Conda

Here, I assume that you installed conda in `~/.miniconda3` for mac and `C:/miniconda3 `for windows.

After conda is installed, depending on what os and terminal you have, add these to that 
- Mac add to ~/.bash_profile and ~/.zshrc for bash and zsh, respectively.
  ```terminal
  source ~/.miniconda3/bin/activate
  ```
- windows powershell, add to $PROFILE (do `echo $PROFILE` in powershell to see where this file should be)
  ```terminal
  & C:\miniconda3\shell\condabin\conda-hook.ps1
  ```
- windows git bash, add to ~/.bash_profile
  ```terminal
  source /c/miniconda3/etc/profile.d/conda.sh
  ```

## Installing python and MetaBuild with Conda

To install python and MetaBuild with Conda, you need a conda `.yaml` file. You can start from [this example](https://git.corp.adobe.com/meta-samples/conda_setup/blob/main/example-env.yaml). In this file you can specify the version of MetaBuild and python to be installed in your conda virtual environment. You can also add more packages to the env if you need them. See a list of available package [here](https://anaconda.org/conda-forge/repo).

Then you need to run
```terminal
conda env update --file /path/to/env/file.yaml [--prefix /path/to/virtual/env]
```

If you pass the `--prefix` flag, conda will setup the virtual env at `/path/to/virtual/env` and to activate it you need to run `conda activate /path/to/virtual/env`. If you don't use that argument, conda will setup the env within its distribution, and to activate the you just type `conda activate env-name` (where env name is the entry you specify [here](https://git.corp.adobe.com/meta-samples/conda_setup/blob/main/example-env.yaml#L1)).

When you activate the env, both python and MetaBuild will be available to you.
