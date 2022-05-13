---
permalink: /docs/cli/metabuild_graph/
title: "metabuild graph"
---

Generates a .dot file or .dgml file graph using the dependencies from the current project.

```
metabuild graph [--format {dot,dgml}] GRAPH_FILE
```

`.dot` files are in [GraphViz](https://graphviz.org/doc/info/command.html) format; use the `dot` tool to render them. 

`.dgml` files can be interactively viewed and manipulated in Visual Studio; be sure to install "Tools > Get tools and features... > Individual Component > Code tools > DGML Editor"
