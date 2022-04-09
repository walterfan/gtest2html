#!/usr/bin/env python3
###########################################################################################################
# This tool is for test case summary and result report  --  Walter Fan on 9/1/17
###########################################################################################################
import os
import markdown
import codecs
import sys
import argparse
import re
import json
import logging

import xml.etree.ElementTree as ET

DEFAULT_MD = "ut-report.md"
DEFAULT_HTML = "ut-report.html"
DEFAULT_XML = "ut-report.xml"
DEFAULT_JSON = "ut-cases.json"

verbose_flag = True    
log_file = 'testcases.log' 
total_case_count = 0
 
# add log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


ENABLE_EXTEND_ATTRIBUTES = False

class TestSuite:
    def __init__(self, json_file):
        
        self.read(json_file)

    def read(self, json_file):
        
        json_data=open(json_file)
        self.test_data = json.load(json_data)
        self.test_suites = self.test_data['testsuites']

    def list_to_string(self, the_list):
        output = ""
        for item in the_list:
            output = output + "* %s " % item
        return output

    def dump_to_markdown(self, mdfile, test_results):
        global total_case_count
        for test_suite in self.test_suites:   
            print(("test sute: %s " % test_suite['name']))

            test_suite_result = test_results.get_test_suite_result(test_suite['name'])
            
            mdfile.write("\n# Test suite:  %s\n\n" % test_suite['name'])
            if(test_suite_result):
                mdfile.write("* %s\n\n" % test_suite_result["info"])
            else:
                logger.error("cannot find test suite: " + test_suite['name'])
            
            print("ENABLE_EXTEND_ATTRIBUTES=", ENABLE_EXTEND_ATTRIBUTES)

            if ENABLE_EXTEND_ATTRIBUTES:
                mdfile.write("| # | suite | case | time | result | given | when | then | checkpoints |\n")
                mdfile.write("|---|---|---|---|---|---|---|---|---|\n")
            else:
                mdfile.write("| # | suite | case | time | result |\n")
                mdfile.write("|---|---|---|---|---|\n")

            for test_case in test_suite['testcases']:
                total_case_count = total_case_count + 1
                case_full_name = test_suite['name'] + '.' + test_case['name']
                test_case_result = test_results.get_test_case_status(case_full_name)
                if(not test_case_result):
                    logger.error("cannot find test case:" + case_full_name)

                if ENABLE_EXTEND_ATTRIBUTES:
                    mdfile.write("| %d | %s | %s | %s | %s | %s | %s | %s | %s |\n" 
                        % (total_case_count, 
                        test_case['suite'],
                        test_case['name'],
                        test_case['time'],
                        test_case['result'],
                        test_case['given'],
                        test_case['when'],
                        test_case['then'],
                        self.list_to_string(test_case['checkpoints'])))
                else:
                    mdfile.write("| %d | %s | %s | %s | %s |\n" 
                        % (total_case_count,
                        test_case['suite'],
                        test_case['name'],
                        test_case['time'],
                        test_case['result']))

class TestResults:
    def __init__(self, testResultPath):
        self.test_result_file = testResultPath
        self.test_case_results = {}
        self.test_suite_results = {}

    def get_test_result(self, case):
        case_exec_result = "pass"
        
        if len(case): 
            for grantchild in case:
                if 'failure' == grantchild.tag:
                    case_exec_result = 'failure'
                    break
        return case_exec_result

    def read_test_suites(self):
        tree = ET.parse(self.test_result_file)

        root = tree.getroot()
        for suites in root.iter("testsuites"):
            self.read_test_suite(suites)

    def read_test_suite(self, suites):
        
        for suite in suites.iter("testsuite"):
            test_suite_result = {}
            #self.test_suite_results[suite.attrib.get('name')] = "tests=%s, failures=%s, errors=%s, disabled=%s, time=%s" % (suite.attrib.get('tests'), suite.attrib.get('failures'), suite.attrib.get('errors'), suite.attrib.get('disabled'), suite.attrib.get('time'))
            test_suite_result["info"] = "tests=%s, failures=%s, errors=%s, disabled=%s, time=%s" % (suite.attrib.get('tests'), suite.attrib.get('failures'), suite.attrib.get('errors'), suite.attrib.get('disabled'), suite.attrib.get('time'))
            test_suite_result["testcases"] = {}
            
            for case in suite.iter():
                test_case_result = {}
                
                if(not case.attrib.get('classname')):
                    continue
                
                case_exec_result =  self.get_test_result(case)
                
                case_full_name = "%s.%s" % (case.attrib.get('classname'), case.attrib.get('name'))
               
                test_case_result["suite"] = suite.attrib.get('name')
                test_case_result["case_full_name"] = case_full_name
                test_case_result["classname"] = case.attrib.get('classname')
                test_case_result["name"] = case.attrib.get('name')
                test_case_result["result"] = case_exec_result
                test_case_result["time"] = case.attrib.get('time')
                #----------------- extended fields --------------------
                test_case_result["given"] = case.attrib.get('given')
                test_case_result["when"] = case.attrib.get('when')
                test_case_result["then"] = case.attrib.get('then') 
                test_case_result["feature"] = case.attrib.get('feature') 
                test_case_result["scenario"] = case.attrib.get('scenario') 
                test_case_result["checkpoints"] = case.attrib.get('checkpoints') 
                
                
                test_suite_result["testcases"][case_full_name]=test_case_result
                
                self.test_case_results[case_full_name] = case_exec_result
                
                
                logger.info("test case: %s, status=%s, time=%s" % (case_full_name, case.attrib.get('status'), case.attrib.get('time')))
            print("append test suite name: %s" % suite.attrib.get('name'))
            self.test_suite_results[suite.attrib.get('name')] = test_suite_result
            
            logger.info("finish test sute: %s " % suite.attrib.get('name'))

    def get_test_case_status(self, case_full_name):
        return self.test_case_results.get(case_full_name)
    
    def get_test_case_info(self, suite_name, case_name):
        test_cases = self.test_suite_results.get(suite_name)
        return test_cases.get(case_name)

    def get_test_suite_result(self, suite_name):
        return self.test_suite_results.get(suite_name)


    def dump_to_markdown(self, mdfile):
        global total_case_count
        for test_suite_name, test_suite_result in self.test_suite_results.items():
            print("dump test_suite_name=%s" % test_suite_name) 
            mdfile.write("\n# Test suite:  %s\n\n" % test_suite_name)
            if(test_suite_result):
                mdfile.write("* %s\n\n" % test_suite_result["info"])
            else:
                logger.error("cannot find test suite: " + test_suite['name'])
                continue
            

            if ENABLE_EXTEND_ATTRIBUTES:
                mdfile.write("| # | suite | case | time | result | given | when | then | checkpoints |\n")
                mdfile.write("|---|---|---|---|---|---|---|---|---|\n")
            else:
                mdfile.write("| # | suite | case | time | result |\n")
                mdfile.write("|---|---|---|---|---|\n")

            for case_full_name, test_case_result in test_suite_result['testcases'].items():
                total_case_count = total_case_count + 1
                

                if ENABLE_EXTEND_ATTRIBUTES:
                    mdfile.write("| %d | %s | %s | %s | %s | %s | %s | %s | %s |\n" 
                        % (total_case_count, 
                        test_case_result['suite'],
                        test_case_result['name'],
                        test_case_result['time'],
                        test_case_result['result'],
                        test_case_result['given'],
                        test_case_result['when'],
                        test_case_result['then'],
                        self.list_to_string(test_case_result['checkpoints'])))
                else:
                    mdfile.write("| %d | %s | %s | %s | %s |\n" 
                        % (total_case_count,
                        test_case_result['suite'],
                        test_case_result['name'],
                        test_case_result['time'],
                        test_case_result['result']))    

class TestCaseSummarizer:
    def __init__(self, caseDefinitionPath, caseResultFile):
        self.case_path = caseDefinitionPath
        self.testSuites = []
        self.test_case_results = TestResults(caseResultFile)

    def read_case_file(self, json_file):
        print(("read %s " % json_file))
        self.testSuites.append(TestSuite(json_file))
        
    def read_test_results(self):
        self.test_case_results.read_test_suites()

    def json_to_markdown(self, filename):
        with open(filename, "a") as mdfile:
            for testSuite in self.testSuites:
                testSuite.dump_to_markdown(mdfile, self.test_case_results)
                
    def xml_to_markdown(self, filename):
        with open(filename, "a") as mdfile:
            self.test_case_results.dump_to_markdown(mdfile)

    def read_case_files(self):
        regex = re.compile(".*\.json$")
        for root, dirs, names in os.walk(self.case_path):

            for dirname in dirs:
                result = regex.match(dirname)
                if result:
                    self.read_case_file(os.path.join(root, dirname))
            for filename in names:
                #print(os.path.join(root, filename))
                result = regex.match(filename)    
                if result:
                    self.read_case_file(os.path.join(root, filename))

    
    def dump_to_html(self, filename):

        input_file = codecs.open(markdown_file, mode="r", encoding="utf-8")
        text = input_file.read()

        html = markdown.markdown(text, extensions=['markdown.extensions.tables'])

        output_file = codecs.open(html_file, "w", 
                          encoding="utf-8", 
                          errors="xmlcharrefreplace")
        output_file.write(html)
    

def read_test_cases(json_file, markdown_file, xml_file):
    summarizer =  TestCaseSummarizer(".", xml_file)
    summarizer.read_case_file(json_file)
    summarizer.read_test_results()
    summarizer.json_to_markdown(markdown_file)
        

def write_test_cases(xml_file, markdown_file, html_file):
    summarizer =  TestCaseSummarizer(".", xml_file)
        
    summarizer.read_test_results()
    summarizer.xml_to_markdown(markdown_file)

    if(html_file):
        summarizer.dump_to_html(html_file)

def usage():
    print("Usage: ./gtest2html.py -i={} -o={}]".format(DEFAULT_XML, DEFAULT_MD))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', action='store', dest='command', default="convert", help='specify a command')
    parser.add_argument('-t', action='store', dest='testcase', help='specify a test case')
    parser.add_argument('-i', action='store', dest='input', help='specify a input file')
    parser.add_argument('--input', action='store', dest='input', help='specify a input file')
    parser.add_argument('-o', action='store', dest='output', help='specify a output file')
    parser.add_argument('--output', action='store', dest='output', help='specify a output file')
    args = parser.parse_args()

    if args.command == "convert" and args.input and args.output:
        input_file = args.input
        output_file = args.output
        print("input: {}, output: {}".format(input_file, output_file))
        json_file = None
        xml_file = None
        markdown_file = None
        html_file = None
        

        if input_file.endswith(".xml"):
            xml_file=input_file
        elif input_file.endswith(".json"):
            json_file=input_file
        else:
            usage()

        if output_file.endswith(".md"):
            markdown_file = output_file
        elif output_file.endswith(".html"):
            html_file = output_file
            markdown_file = html_file[:-5] + ".md"
        else:
            usage()


        
        if markdown_file and os.path.isfile(markdown_file):
            os.remove(markdown_file)
        if html_file and os.path.isfile(html_file):
            os.remove(html_file)
        

        if json_file:
            read_test_cases(json_file, markdown_file, xml_file)
        else:
            print("convert {} to {} or {}".format(xml_file, markdown_file, html_file))
            write_test_cases(xml_file, markdown_file, html_file)

    elif args.command == "test" or args.testcase:
        testcases = "*"
        if not args.testcase:
            testcases = args.testcase
        cmd = './bld/gtest_demo --gtest_filter="{}" --gtest_output="xml:ut-report.xml"'.format(testcases)
        print(cmd)
        os.system(cmd)
    else:
        usage()