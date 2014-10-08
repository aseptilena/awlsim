from __future__ import division, absolute_import, print_function, unicode_literals

import awlsim.cython_helper as __cython

if __cython.shouldUseCython():
	try:
		from awlsim_cython.common.all_modules import *	#<no-cython-patch
	except ImportError as e:
		__cython.cythonImportError("common", str(e))
if not __cython.shouldUseCython():
	from awlsim.common.all_modules import *			#<no-cython-patch