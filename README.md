# gtest2html

progress: 90%

A python script to convert google test report from xml to markdown or html files

# Steps

* build example

```
mkdir -p example/bld
cd example/bld
cmake ..
make
```

* Generate unit test result

```
./bld/gtest_demo --gtest_output="xml:ut-report.xml"
```

* Convert xml to markdown

```
./gtest2html.py --markdown_file=-ut-report.md --xml_file=ut-report.xml
```

* Convert xml to html

```
./gtest2html.py --xml_file=ut-report.xml --html_file=ut-report.xml
```
