import os
import tempfile
import hashlib
# test.server_test
tfn=hashlib.md5("haha".encode("utf8")).hexdigest()
tp = tempfile.gettempdir().replace('\\', '/')
name = tp+'/'+tfn

print(name)
f=open(name,"w+")
print("你好世界",file=f)

# print(tp+'/'+tfn)
if os.path.exists(name):
    print("yes")

f.close()

rdf=open(name)
print(rdf.readline())
