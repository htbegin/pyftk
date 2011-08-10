#!/bin/bash

find ftk/ -name "*.py" | xargs \
sed -i \
	-e 's/from\s\+ctypes\s\+import\s\+\*/import ctypes/g' \
	-e 's/\(^\|[^.]\)\<\(c_bool\|c_char\|c_wchar\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(c_byte\|c_ubyte\|c_short\|c_ushort\|c_int\|c_uint\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(c_size_t\|c_ssize_t\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(c_long\|c_ulong\|c_longlong\|c_ulonglong\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(c_float\|c_double\|c_longdouble\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(c_char_p\|c_wchar_p\|c_void_p\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(addressof\|alignment\|byref\|cast\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(create_string_buffer\|create_unicode_buffer\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(memset\|pointer\|resize\|sizeof\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(POINTER\|CFUNCTYPE\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(Structure\|Union\)\>/\1ctypes.\2/g' \
	-e 's/\(^\|[^.]\)\<\(cdll\)\>/\1ctypes.\2/g'
