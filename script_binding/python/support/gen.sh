#!/bin/bash

if test $# -lt 1
then
	exit 1
fi

header="../../src/ftk_$1.h"
if test $# -ge 2 && test ${2:0:1} != "-"
then
	py="ftk/ftk_$2.py"
	shift
else
	py="ftk/ftk_$1.py"
fi

if test -f "$header" && test -f "$py"
then
	shift
	./support/code_gen.py -i $header $@ >> $py
	exit 0
else
	exit 1
fi
