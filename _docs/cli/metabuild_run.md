---
permalink: /docs/cli/metabuild_run/
title: "metabuild run"
---

Runs nodes like `genrule` that are designed to run during the `prepare` phase. This is useful when a script is used to generated files.

When using `metabuild run` only a subset of the `prepare` sequence is invoked, so it should be faster to use `metabuild run` instead of using the full `metabuild prepare`.

For example:

  metabuild run --target :generate_files
