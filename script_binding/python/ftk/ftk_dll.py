#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import ctypes
from ctypes.util import find_library
import sys

import ftk_constants

# Private version checking declared before ftk_version can be
# imported.
class _FtkVersion(ctypes.Structure):
    _fields_ = [('major', ctypes.c_ubyte),
                ('minor', ctypes.c_ubyte),
                ('patch', ctypes.c_ubyte)]

    def __repr__(self):
        return '%d.%d.%d' % \
            (self.major, self.minor, self.patch)

def _version_parts(v):
    '''Return a tuple (major, minor, patch) for `v`, which can be
    an _FtkVersion, string or tuple.'''
    if hasattr(v, 'major') and hasattr(v, 'minor') and hasattr(v, 'patch'):
        return v.major, v.minor, v.patch
    elif type(v) == tuple:
        return v
    elif type(v) == str:
        return tuple([int(i) for i in v.split('.')])
    else:
        raise TypeError

def _version_string(v):
    return '%d.%d.%d' % _version_parts(v)

def _platform_library_name(library):
    if sys.platform[:5] == 'linux':
        return 'lib%s.so' % library
    elif sys.platform == 'darwin':
        return '%s.framework' % library
    elif sys.platform == 'windows':
        return '%s.dll' % library
    return library

class FtkDLL:
    def __init__(self, library_name, version_function_name):
        self.library_name = library_name
        library = find_library(library_name)
        if not library:
            raise ImportError, 'Dynamic library "%s" was not found' % \
                _platform_library_name(library_name)
        self._dll = getattr(ctypes.cdll, library)
        
        # Get the version of the DLL we're using
        if version_function_name:
            try:
                version_function = getattr(self._dll, version_function_name)
                version_function.restype = ctypes.POINTER(_FtkVersion)
                self._version = _version_parts(version_function().contents)
            except AttributeError:
                self._version = (0, 0, 0)
        else:
            self._version = (0, 0, 0)

    def version_compatible(self, v):
        '''Returns True if `v` is equal to or earlier than the loaded library
        version.'''
        v = _version_parts(v)
        for i in range(3):
            if self._version[i] < v[i]:
                return False
        return True

    def assert_version_compatible(self, name, since):
        '''Raises an exception if `since` is later than the loaded library.'''
        if not version_compatible(since):
            import ftk_error
            raise ftk_error.FtkNotImplementedError, \
                '%s requires ftk version %s; currently using version %s' % \
                (name, _version_string(since), _version_string(self._version))

    def private_function(self, name, **kwargs):
        '''Construct a wrapper function for ctypes with internal documentation
        and no argument names.'''
        kwargs['doc'] = 'Private wrapper for %s' % name
        kwargs['args'] = []
        return self.function(name, **kwargs)

    def function(self, name, doc, args=[], arg_types=[], 
                 return_type=None, 
                 dereference_return=False, 
                 require_return=False,
                 check_return=False,
                 since=None):
        '''Construct a wrapper function for ctypes.

        :Parameters:
            `name`
                The name of the function as it appears in the shared library.
            `doc`
                Docstring to associate with the wrapper function.
            `args`
                List of strings giving the argument names.
            `arg_types`
                List of ctypes classes giving the argument types.
            `return_type`
                The ctypes class giving the wrapped function's native
                return type.
            `dereference_return`
                If True, the return value is assumed to be a ctypes.pointer and
                will be dereferenced via ``.contents`` before being
                returned to the user application.
            `require_return`
                Used in conjunction with `dereference_return`; if True, an
                exception will be raised if the result is NULL; if False
                None will be returned when the result is NULL.
            `check_return`
                If True, an FtkError exception will be raised if
                the reuslt is not RET_OK.
            `since`
                Tuple (major, minor, patch) or string 'x.y.z' of the first
                version of ftk in which this function appears.  If the
                loaded version predates it, a placeholder function that
                raises `FtkNotImplementedError` will be returned instead.
                Set to None if the function is in all versions of ftk.

        '''
        # Check for version compatibility first
        if since and not self.version_compatible(since):
            def _f(*args, **kwargs):
                import ftk_error
                raise ftk_error.FtkNotImplementedError, \
                      '%s requires %s %s; currently using version %s' % \
                      (name, self.library_name, _version_string(since), 
                       _version_string(self._version))
            if args:
                _f._args = args
            _f.__doc__ = doc
            try:
                _f.func_name = name
            except TypeError: # read-only in Python 2.3
                pass
            return _f

        # Ok, get function from ctypes
        func = getattr(self._dll, name)
        func.argtypes = arg_types
        func.restype = return_type
        if dereference_return:
            if require_return:
                # Construct a function which dereferences the ctypes.pointer result,
                # or raises an exception if NULL is returned.
                def _f(*args, **kwargs):
                    result = func(*args, **kwargs)
                    if result:
                        return result.contents
                    import ftk_error
                    raise ftk_error.FtkError(ftk_constants.RET_FAIL)
            else:
                # Construct a function which dereferences the ctypes.pointer result,
                # or returns None if NULL is returned.
                def _f(*args, **kwargs):
                    result = func(*args, **kwargs)
                    if result:
                        return result.contents
                    return None
        elif check_return:
            # Construct a function which returns None, but raises an exception
            # if the C function returns a failure code.
            def _f(*args, **kwargs):
                result = func(*args, **kwargs)
                if result != ftk_constants.RET_OK:
                    import ftk_error
                    raise ftk_error.FtkError(result)
                return None
        else:
            # Construct a function which returns the C function's return
            # value.
            def _f(*args, **kwargs):
                return func(*args, **kwargs)
        if args:
            _f._args = args
        _f.__doc__ = doc
        try:
            _f.func_name = name
        except TypeError: # read-only in Python 2.3
            pass
        return _f

# Shortcuts to the ftk core library
_dll = FtkDLL('ftk', '')
version_compatible = _dll.version_compatible
assert_version_compatible = _dll.assert_version_compatible
private_function = _dll.private_function
function = _dll.function
