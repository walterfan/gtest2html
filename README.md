# gtest2html

A python script to convert google test report from xml to markdown or html files

# prerequisite

```
apt install -y doxygen graphviz plantuml libjsoncpp-dev libgtest-dev

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


# Generate HTML report 

python3 is required, run `pip3 install -r requirements.txt` first

* Convert xml to markdown

```
./gtest2html.py  -i example/ut-report.xml -o ut-report.md
```

* Convert xml to restructuredText

```
./gtest2html.py  --input=example/ut-report.xml --output=-ut-report.rst
```

* Convert xml to html

```
./gtest2html.py -i example/ut-report.xml -o ut-report.html
```

* gtest demo

```
./gtest2html.py -c test
```

# Generate doxygen document

* Integrate https://github.com/kracejic/EmptyDoxygenCMake

steps

```
cd bld
cmake ..
make doc

```
