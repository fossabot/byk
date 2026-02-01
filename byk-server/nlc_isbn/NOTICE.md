Notice
======

This module contains code migrated from [https://github.com/DoiiarX/NLCISBNPlugin]. The original code is licensed under
the Apache License, Version 2.0.

Modifications and Overall Distribution: As part of [byk], this module is redistributed under the GNU GPLv3 license,
as permitted by the compatibility between Apache 2.0 and GPLv3.

Original Copyright 2025 DoiiarX <doiiars AT qq.com>
Modified by Andrija Junzki <andrija.junzki AT gmail.com> 2025

## Data Optimization
The original hard-coded dictionary in [`data_wrapper.py`](https://github.com/DoiiarX/NLCISBNPlugin/blob/main/src/data_wrapper.py) 
has been converted to a gzip-compressed JSON format (`clc.json.gz`) to improve loading efficiency and  reduce package 
size.
