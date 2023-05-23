# PMD Data Clumps

This project should parse a projects classes, interfaces, methods and fields. This should increase the speed of: https://github.com/FireboltCasters/data-clumps which uses AntLR4 in web. This could be extracted to a server which then calls this jar and gives the parsed output back to [data-clumps](https://github.com/FireboltCasters/data-clumps).

## Setup

For example our <Path_to_Project> is: /Users/nbaumgartner/Desktop/javaAnalyzeProject

```
make setup
make build
make run DIRECTORY=<Path_to_Project>
```

## Roadmap:

- [x] Implement Basic parser for classes, interfaces, methods and fields
- [ ] Handle unresolved imports
  - Check ToDos in pmd-java-custom/src/main/java/net/sourceforce/pmd/examples/java/rules/MyRule.java
    - *CodePiece --> no dots --> replace * by packagename 
    - *org.flywaydb.core.api.configuration.FluentConfiguration --> technically we only need to remove the *
    - *CodePiece.InnerClass --> ?