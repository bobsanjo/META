---
permalink: /docs/internals/profiling/
title: "Profiling"
---

# High level tracing

MetaBuild comes with a profiler. If you run any MetaBuild command with the additional argument `--trace /path/to/trace/file.json`, MetaBuild will write a chrome trace file. This file can be opened with google chrome, and shows how much time MetaBuild spent doing what.

You can learn more about this feature by following this example.

Clone a repository that can be built with MetaBuild, e.g., `https://git.corp.adobe.com/meta-specs/pybind11`.
```
git clone https://git.corp.adobe.com/meta-specs/pybind11
```

Cd into the repo, and run a MetaBuild command with the trace option, e.g.,
```
metabuild prepare --trace prepare_trace.json
```

Open google chrome and type `chrome://tracing` in the address bar. Chrome will show you this window ![](https://git.corp.adobe.com/storage/user/30871/files/6d2e2780-082b-11ec-88c0-c632241e1476)

Then click on `Load` and open the trace file that MetaBuild wrote. You should get a trace record like below. You can zoom into sections, and click on a task to see full details about it. ![](https://git.corp.adobe.com/storage/user/30871/files/60f69a00-082c-11ec-8f5a-978f976e56aa)

## cProfile

MetaBuild also integrates python's `cProfile`. This can be activated via the `--profile` command line argument. Note that the output of `cProfile` is much more detailed and less human readable than the high level tracing above. This will record all the actions that MetaBuild main thread and the background threads perform.