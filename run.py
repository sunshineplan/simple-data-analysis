#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time

from flask import Flask, jsonify, render_template, request

from core import chk_consecutive, chk_duplicates, compare, diff
from util import precheck, print_result

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analysis', methods=['POST'])
def sda():
    func = request.form.get('func')
    source = request.form.get('source')
    if source == 'Data1' or source == 'Data2':
        if source == 'Data1':
            data = request.form.get('data1').splitlines()
        else:
            data = request.form.get('data2').splitlines()
        if data == []:
            return jsonify(f'{source} is empty.\nPlease enter something...')
    elif source == 'Data1,Data2':
        data1 = request.form.get('data1').splitlines()
        data2 = request.form.get('data2').splitlines()
        if data1 == []:
            return jsonify('Data1 is empty.\nPlease enter something...')
        elif data2 == []:
            return jsonify('Data2 is empty.\nPlease enter something...')
    result = []
    if func == 'chk_duplicates':
        start_time = time()
        r1 = chk_duplicates(data)
        elapsed_time = time()-start_time
        if r1 == []:
            result.append(f'{source} contains no duplicate values.\n')
            result.append(f'Duration for process: {elapsed_time:.3f} sec.')
        else:
            result += print_result([f'{i[0]}\t\tappears {i[1]} time(s)' for i in r1],
                                   f'Duplicate values found in {source}', elapsed_time=elapsed_time)
    elif func == 'rm_duplicates':
        result = precheck(list(set(data)))
    elif func == 'chk_consecutive':
        try:
            start_time = time()
            r1 = chk_consecutive(data)
            tmp = chk_duplicates(data)
            elapsed_time = time()-start_time
        except ValueError:
            result.append(
                f'[Error]{source} contains non-numeric value. Please check and try again!')
        else:
            if tmp != []:
                result.append(
                    f'[Warning]Duplicate values found in {source}.\nYou can "Check Duplicates ({source})" to check it.\n')
            if r1 == []:
                result.append(
                    f'{source} contains consecutive natural numbers.\n')
                result.append(f'Duration for process: {elapsed_time:.3f} sec.')
            else:
                result += print_result(r1, f'{source} is not consecutive',
                                       'The following numbers are missing:', elapsed_time=elapsed_time)
    elif func == 'compare':
        mode = request.form.get('mode')
        ignore_duplicates = request.form.get('ignore_duplicates')
        if ignore_duplicates == 'true':
            data1 = list(set(data1))
            data2 = list(set(data2))
        if mode == 'comm':
            start_time = time()
            r1 = compare(data1, data2, mode='comm')
            elapsed_time = time()-start_time
            if r1 == []:
                result.append('Two data contain no common values.\n')
                result.append(f'Duration for process: {elapsed_time:.3f} sec.')
            else:
                result += print_result(r1, 'Common values found between two data.',
                                       elapsed_time=elapsed_time)
        elif mode == 'diff':
            start_time = time()
            r1 = compare(data1, data2)
            r2 = compare(data2, data1)
            elapsed_time = time()-start_time
            if r1 + r2 == []:
                result.append('Data1 is same as Data2.\n')
                result.append(f'Duration for process: {elapsed_time:.3f} sec.')
            elif r1 == []:
                result.append('Data2 completely contains Data1.\n')
                result += print_result(r2, 'Data2 is more than Data1',
                                       elapsed_time=elapsed_time)
            elif r2 == []:
                result.append('Data1 completely contains Data2.\n')
                result += print_result(r1, 'Data1 is more than Data2',
                                       elapsed_time=elapsed_time)
            else:
                result.append('Two files have inconsistent content.\n')
                result += print_result(r1, 'Data1 is more than Data2')
                result.append('')
                result += print_result(r2, 'Data2 is more than Data1',
                                       elapsed_time=elapsed_time)
    elif func == 'diff':
        result = diff(data1, data2)
    output = '\n'.join(result)
    return jsonify(output)


if __name__ == '__main__':
    app.run()
