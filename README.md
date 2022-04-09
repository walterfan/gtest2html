# gtest2html

A python script to convert google test report from xml to markdown or html files

# Usage

* Convert xml to markdown

```
./gtest2html.py  -i example/ut-report.xml -o -ut-report.md
```

* Convert xml to html

```
./gtest2html.py -i example/ut-report.xml -o ut-report.html
```

* gtest demo

```
./gtest2html.py -c test
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
./bld/gtest_demo --gtest_filter="testcase*" --gtest_output="xml:ut-report.xml"
```