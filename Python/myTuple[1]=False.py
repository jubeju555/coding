from collections import _odict_values


phoneext={'david':1410,'brad':1137}
phoneext
{'brad': 1137, 'david': 1410}
phoneext.keys()
dict_keys(['brad', 'david'])
list(phoneext.keys())
['brad', 'david']
phoneext.values()
_odict_values([1137, 1410])
list(phoneext.values())
[1137, 1410]
phoneext.items()
dict_items([('brad', 1137), ('david', 1410)])
list(phoneext.items())
[('brad', 1137), ('david', 1410)]
phoneext.get("kent")
phoneext.get("kent","NO ENTRY")
'NO ENTRY'
