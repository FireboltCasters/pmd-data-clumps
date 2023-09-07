# PMD Data Clumps

This project should parse a projects classes, interfaces, methods and fields. This should increase the speed of: https://github.com/FireboltCasters/data-clumps which uses AntLR4 in web. This could be extracted to a server which then calls this jar and gives the parsed output back to [data-clumps](https://github.com/FireboltCasters/data-clumps). Since the speed up in parsing is significant we then only pass the parsed files to the next python programm.

### Speed comparison

| Project | Files | Time [data-clumps](https://github.com/FireboltCasters/data-clumps) | Time this | Speed increase this vs. [data-clumps](https://github.com/FireboltCasters/data-clumps) |
| --- | --- | --- | --- | --- |
| Eclipse JDT Core 3.1 | 20.436 | 2.910s (48m 30s) | 47s (0m 47s) | 98% |
| ArgoUML-0.26Beta | 2.214 | 98s (1m 38s) | 23s (0m 23s) | 76% |
| Apache | 654 | 12s (0m 12s) | 8s (0m 8s) | 33% |

This shows a significant speed increase by using this project.

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

python3 data-clumps.py detect --config ./detector-options.json --source /Users/nbaumgartner/Desktop/LCSD-Paper/Data_for_Paper/ArgoUML_src/src/argouml-app/src

### 2. Analysing the parsed files

Optional: Install requirements.txt ```pip install -r requirements.txt```

```

```

## Contribution

Edit:
- 1_astGenerate/pmd-java-custom/src/main/java/net/sourceforge/pmd/examples/java/rules/MyRule.java


## Roadmap:
- [ ] Check for further adaptions
