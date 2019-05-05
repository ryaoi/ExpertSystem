# ExpertSystem
AST + backward-chaining to solve expert system.

```
usage: ExpertSystem.py [-h] [-v] input_file
ExpertSystem.py: error: the following arguments are required: input_file
```

Example of input file:
```
A + B => C
A + B + C => D

=CAB

?BD
```

Example for AST visualizer:
```
python3 genastdot.py example_easy.txt > ast.dot && dot -Tpng -o ast.png ast.dot
```
