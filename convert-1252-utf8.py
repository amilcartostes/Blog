
import chardet

with open('olddb.json', encoding='windows-1252') as file:
    content = file.read()
    print(content)

with open('db.json', 'wb') as file1:
   file1.write(content.encode('utf-8'))

with open('db.json', 'rb') as file2:
    content = file2.read()
    encoding = chardet.detect(content)
    print(encoding)

with open('olddb.json', 'rb') as file3:
    content = file3.read()
    encoding = chardet.detect(content)
    print(encoding)