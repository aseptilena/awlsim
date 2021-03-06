Awlsim - S7 compatible Soft-PLC
===============================

Awlsim is a free Step 7 compatible AWL/STL Soft-PLC written in Python.

The latest version of awlsim can be downloaded from the [official awlsim site](https://bues.ch/a/awlsim).


Awlsim - Soft-PLC
-----------------

Awlsim is a free Step 7 compatible AWL/STL Soft-PLC written in Python. Depending on the host machine and the Python interpreter used, it achieves good performance of several thousand to millions of AWL/STL instructions per second. German and English S7 AWL/STL mnemonics are supported.

AWL/STL programs on PLCs are used for automation of industrial processes. However Awlsim is very flexible, so it can be used for other purposes beyond industrial applications, too. Awlsim aims to be compatible with the industry standard S7 software on the AWL/STL level.

Awlsim can emulate CPUs with two and four accumulator registers (S7-3xx and S7-4xx). Compatibility to S7 hardware is a task taken seriously by the awlsim project. We want to be as close as possible to the real PLC hardware with our AWL/STL code execution. For this reason awlsim ships an extensive selftest suite. Missing features and differences between awlsim and Step 7 are documented in the COMPATIBILITY.md and TODO.md files.


License / Copyright
-------------------

Copyright (C) Michael Büsch / et al.

Awlsim is Open Source Free Software licensed under the GNU General Public License v2+. That means it's available in full source code and you are encouraged to improve it and contribute your changes back to the community. Awlsim is free of charge, too. 
