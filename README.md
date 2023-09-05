# PMD Data Clumps

This project should parse a projects classes, interfaces, methods and fields. This should increase the speed of: https://github.com/FireboltCasters/data-clumps which uses AntLR4 in web. This could be extracted to a server which then calls this jar and gives the parsed output back to [data-clumps](https://github.com/FireboltCasters/data-clumps). Since the speed up in parsing is significant we then only pass the parsed files to the next python programm.

### Speed comparison

| Project | Files | Time [data-clumps](https://github.com/FireboltCasters/data-clumps) | Time this | Speed increase this vs. [data-clumps](https://github.com/FireboltCasters/data-clumps) |
| --- | --- | --- | --- | --- |
| Eclipse JDT Core 3.1 | 20.436 | 2.910s (48m 30s) | 47s (0m 47s) | 98% |
| ArgoUML-0.26Beta | 2.214 | 98s (1m 38s) | 9s (0m 9s) | 91% |
| Apache | 654 | 12s (0m 12s) | 6s (0m 6s) | 50% |

This shows a significant speed increase by using this project.


## Usage

### 1. Parsing your project

For example our <Path_to_Project> is: /Users/nbaumgartner/Desktop/javaAnalyzeProject

```
make setup
make build
make run DIRECTORY=<Path_to_Project> OUTPUT_FOLDER<Output_Folder>
```

### 2. Analysing the parsed files

```

```

## Roadmap:
- [ ] Check for further adaptions
