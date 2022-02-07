# RefinedFeedback
Compile
```
$ javac src/RefinedRegexFeedback.java
```
Example usage. Pattern expected as cmd line argument, student output
expected on  `stdin`.
```
$ regex="hello.*world"
$ cmd="cat student_output.txt | java RefinedRegexFeedback \"$regex\""; eval $cmd
```
