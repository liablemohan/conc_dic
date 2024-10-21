import sys, re

fr1 = open(sys.argv[1], 'r')
fr2 = open(sys.argv[2], 'r')
doc1 = list(fr1)
doc2 = list(fr2)
ans=open(sys.argv[3],'w+')

c1 = 0
c2 = 0
for i in range(len(doc2)):
    lst = doc2[c2].split(',')
    #print(lst)
    if lst[0].startswith('(') and  lst[0].endswith(')'):
        print(',,,,,,,,,', doc2[c2].strip())
        #print('&&&&&&&&&&&&&&&&&&&&&&&&&')
        c2 += 1
    elif lst[0] == '.':
        print(',,,,,,,,,', doc2[c2].strip())
        #print('===========================')
        c2 += 1

    else:
        print(doc1[c1].strip(), doc2[c2].strip())
        c1 += 1
        c2 += 1

