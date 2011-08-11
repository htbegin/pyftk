#!/bin/bash

pushd ftk/ >/dev/null
all_module=$(ls -1 *.py | cut -d "." -f 1)
popd >/dev/null

for m in $all_module
do
	if test "$m" != "__init__" && test "$m" != "template" && test "${m:0:4}" != "ftk_"
	then
		git mv ftk/$m.py ftk/ftk_$m.py
	fi
done

ssed -R -i \
	-e 's/(?<!from )ftk\.([a-z_][a-z_]+)/ftk_\1/g' \
	-e 's/(?<=from )ftk\.(?!ftk_)([a-z_]+)/ftk.ftk_\1/g' \
	ftk/*.py

ssed -R -i \
	-e 's/(?<=from )ftk\.(?!ftk_)([a-z_]+)/ftk.ftk_\1/g' \
	test/*.py
