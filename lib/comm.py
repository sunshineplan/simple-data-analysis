#!/usr/bin/python3
# coding:utf-8

def precheck(list_data):
    data=[i.strip() for i in list_data]     #remove backspace
    data=[i for i in data if i!='']         #remove empty string
    output=sort_data(data)
    return output

def sort_data(list_data):
    #output=sorted(list_data, key=lambda item:(int(item.partition(' ')[0]) if item[0].isdigit() else float('inf'), item))
    output=sorted(list_data)
    return output
