# PMD Data Clumps

This project should parse a projects classes, interfaces, methods and fields. This should increase the speed of: https://github.com/FireboltCasters/data-clumps which uses AntLR4 in web. This could be extracted to a server which then calls this jar and gives the parsed output back to [data-clumps](https://github.com/FireboltCasters/data-clumps). Since the speed up in parsing is significant we then only pass the parsed files to the next python programm.

### Speed comparison - Parsing files

| Project | Files | Time [data-clumps](https://github.com/FireboltCasters/data-clumps) | Time this | Speed increase this vs. [data-clumps](https://github.com/FireboltCasters/data-clumps) |
| --- | --- | --- | --- | --- |
| Eclipse JDT Core 3.1 | 20.436 | 2.310s (38m 30s) | 47s (0m 47s) | 98% |
| ArgoUML-0.26Beta | 2.214 | 98s (1m 38s) | 23s (0m 23s) | 76% |
| Apache | 654 | 12s (0m 12s) | 8s (0m 8s) | 33% |

This shows a significant speed increase by using this project for parsing files.

### Speed comparison - detecting data clumps

| Project | Files | Time [data-clumps](https://github.com/FireboltCasters/data-clumps) | Time this | Speed increase this vs. [data-clumps](https://github.com/FireboltCasters/data-clumps) |
| --- | --- | --- | --- | --- |
| Eclipse JDT Core 3.1 | 20.436 | 2.310s (38m 30s) | 5415 (90m 15s) | -42% |

This shows that the detection by using NodeJS is faster than using Python. This is because of the usage of the AST which is faster in NodeJS than in Python.

Therefore a mix between PMD and NodeJS is here: [data-clumps-doctor](https://github.com/NilsBaumgartner1994/data-clumps-doctor)

## Requirements

openjdk version "19.0.1" 2022-10-18
OpenJDK Runtime Environment (build 19.0.1+10-21)
OpenJDK 64-Bit Server VM (build 19.0.1+10-21, mixed mode, sharing)

Python3

## Usage

### 1. Parsing your project

For example our <Path_to_Project> is: /Users/nbaumgartner/Desktop/javaAnalyzeProject

```
make setup
make build
make run DIRECTORY=<Path_to_Project> OUTPUT_FOLDER<Output_Folder>
```

```
python3 data-clumps.py detect --config ./detector-options.json --source /ArgoUML_src/src/argouml-app/src
```
