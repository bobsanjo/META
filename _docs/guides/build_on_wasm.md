---
permalink: /docs/guides/build_on_wasm/
title: "Build on WASM"
---

WebAssembly (Wasm) is a binary format for executing code on the web. Metabuild supports the Wasm platform through the Emscripten SDK (Emsdk) and generates a cmake build.
To support Wasm in MetaBuild a new target filter can be used in the build files (i.e. `META.py`): `target.wasm`.

To build a project on Wasm run:

`metabuild prepare --platform wasm`

`metabuild build --platform wasm`


If a version of Emsdk is not specified in the build file (or through metabuild defines i.e. `--define emsdk.version=2.0.14`) a default one is used. 
A specific version of Emsdk can be specified by using the following defines:

- an Emsdk repository

`repository: https://github.com/emscripten-core/emsdk.git`

- a commit in the Emsdk repository

`commit: 2b720e547355182d0b78d59d269bd17561dfac2e`

- a specific Emsdk

`version: 2.0.14`


__Note__: Currently you have to specify both commit and version (take the version from tags of https://git.corp.adobe.com/meta-archives/emsdk and its associated commit).  [METAB-728](https://jira.corp.adobe.com/browse/METAB-728) tracks the feature to only require version and make commit optional. In this case an Emsdk version should already have been installed
and activated in the repository (see <https://emscripten.org/docs/getting_started/downloads.html>)

Usually on Wasm the compiler can generate .js, .wasm  and/or .html files depending on config.
Emscripten provides various options for connecting "normal" JavaScript and compiled code (see <https://emscripten.org/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html#interacting-with-code>)
A sample for using the two main tools for binding C++ and JS code (Embind and WebIDL) can be found in the meta-build repo: meta-build/tests/generator/__fixtures__/emscripten_app/
