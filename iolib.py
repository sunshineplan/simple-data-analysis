#!/usr/bin/python3

def file2list(filename):
    file=open(filename)
    data=file.readlines()
    file.close()
    count=0
    for line in data:
        line=line.strip('\n')#删除\n
        line=line.strip()#删除空格
        data[count]=line
        count+=1
    output=[a for a in data if a!='']#删除空值
    output.sort()
    return output

def list2file(l,filename):
    file=open(filename,'w')
    for line in l:
        file.write(str(line)+'\n')
    file.close()
    return 0
