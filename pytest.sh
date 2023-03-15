#! /usr/bin/bash

# remove any old files from previous tests
rm -f cov.xml
rm -f .coverage
rm -f junit.xml

# the 4 options passed to pytest below do the following:
# only measure coverage of files in src/
# print report to terminal
# save report in XML format to cov.xml
# save report in JUnit-XML format to junit.xml
pytest --cov=src/ --cov-report term-missing --cov-report xml:cov.xml --junitxml=junit.xml

# install genbadge if it's not already installed
x=$(pip list | grep genbadge)
exit_code=$?

if [ $exit_code -ne 0 ]
then
    echo "genbadge is not installed. Installing it now ..."
    pip install genbadge[tests,coverage]
else
    echo "genbadge is already installed."
fi 

# make the tests and coverage badges
genbadge tests --input-file junit.xml -v
genbadge coverage --input-file cov.xml -v
