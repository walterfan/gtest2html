# gtest2html

A python script to convert google test report from xml to markdown or html files

# Usage



* Convert xml to markdown

```
./gtest2html.py  --input=example/ut-report.xml --output=-ut-report.md
```

* Convert xml to html

```
./gtest2html.py --input=example/ut-report.xml --output=ut-report.html
```

# Example

* build example

```
mkdir -p bld
cd bld
cmake ..
make
cd ..
```

* Generate unit test result

```
./bld/gtest_demo --gtest_output="xml:ut-report.xml"
```