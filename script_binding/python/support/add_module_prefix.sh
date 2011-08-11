#!/bin/bash

pushd ftk/ >/dev/null
all_module=$(ls -1 *.py | cut -d "." -f 1)
popd >/dev/null

for m in $all_module
do
	if test "$m" != "__init__" and test "$m" != "template"
	then
		git mv ftk/$m.py ftk/ftk_$m.py
	fi
done

#sed -i -e 's/ftk\.\([a-z_]\+\)/ftk_\1/g' ftk/widget.py
