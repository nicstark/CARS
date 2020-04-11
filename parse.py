import os
import sys
import os.path
from bs4 import BeautifulSoup, SoupStrainer
import lxml
from lxml import etree
import re
import pandas as pd
from io import StringIO, BytesIO
import mwparserfromhell
import linecache

myDict = {}

root_path = "C:/Users/eufou/Desktop/CARS/"



cars = {};

class FlowException(Exception):
    pass

def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]


def filterNumber(n):
	if(len(n)==N):
		return True
	else:
		return False

def purify(numbers, productionbackup):
    if len(numbers[0]) == 2:
        numbers.remove(numbers[0])

    for i in numbers:
        if len(i) < 2:
            # print(i)
            numbers.remove(i)
        elif int(len(i)) > 8:
            numbers.remove(i)
        elif int(len(i)) == 3:
            numbers.remove(i)
        elif int(len(i)) > 2 and int(i[0]) > 3:
            numbers.remove(i)

    # if len(numbers) == 2 and len(numbers[1]) == 2:
    #     numbers.remove(numbers[])
    if len(numbers) == 2 and len(numbers[0]) == 2 and len(numbers[1]) == 2:
        # print(productionbackup)
        # print(numbers)
        numbers.remove(numbers[1])
        numbers.remove(numbers[0])
    if len(numbers) == 3 and len(numbers[1]) == 2 and len(numbers[2]) == 2:
        # print(productionbackup)
        # print(numbers)
        numbers.remove(numbers[2])
    if len(numbers) == 3 and len(numbers[1]) == 2:
        # print(productionbackup)
        # print(numbers)
        numbers.remove(numbers[1])
    return numbers

def generationParse(template):
    try:
        # print(str(template.get("name").value))
        generation = str(template.get("name").value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
        generation = re.sub('<br>', ' ', generation)
        generation = generation.split('<ref>')[0].lstrip()
        # print(generation)
    except Exception as e:
        pass

def productionParse(template):
    try:
        # print('a')
        production = str(template.get('production').value.lstrip().rstrip().encode('ascii', 'ignore'))
        # print(1)
        productionbackup = str(template.get('production').value.lstrip().rstrip().encode('ascii', 'ignore'))
        # print(2)
        if production:
            try:
                production = production.replace('present', '2020')
            except Exception as e:
                # print(production)
                print('replace present', e)
            try:
                production = production.replace('-', '')
            except Exception as e:
                # print(production)
                print('replace present', e)
            try:
                production = production.replace('&ndash', '')
            except Exception as e:
                # print(production)
                print('replace ndash', e)
            try:
                production = production.replace('&ndash;', '')
            except Exception as e:
                # print(production)
                print('replace ndash', e)

            try:
                production = re.findall(r'[0-9]+', production)

                production = purify(production, productionbackup)

            except Exception as e:
                print('split', e)
                pass


            if len(production) == 2 and all(len(flag) == 4 for flag in production):
                # print(productionbackup)
                # print(production)
                newproduction = str(production[0]) + str(production[1])
                production = [newproduction]
                cars[make][model][generation] = {'production': production}
            elif all(len(flag) == 8 for flag in production):
                cars[make][model][generation] = {'production': production}
            elif len(production) == 1 and all(len(flag) == 4 for flag in production):
                cars[make][model][generation] = {'production': production}

            # else:
                # print(productionbackup)
                # print(production)

    except Exception as e:
        print('function', e , '\n', production)
        return

def assemblyParse(template):
    try:
        assembly = str(template.get('assembly').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if assembly:
            cars[make][model][generation] = {'assembly': assembly}
            # print(assembly)
    except Exception as e:
        print(assembly)
        print('assembly error', e)
        pass

def manufacturerParse(template):
    try:
        manufacturer = str(template.get('manufacturer').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if manufacturer:
            # print(make)
            # print(man)
            # manufacturer = re.search(r'\[\[(.*)\]\]', manufacturer)
            # manufacturer = manufacturer.split(']]')
            char_list = ['\[', '\]', '\|', '\<br\>', '\<br\/\>', '\<br \/\>', '\{\{', '\}\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']

            manufacturer = re.sub("|".join(char_list), " ", manufacturer)
            manufacturer = re.sub(r'\s+', ' ', manufacturer).rstrip().lstrip()
            manufacturer.split('.')[0]
            manufacturer.split('#')[0]
            # manufacturer = manufacturer.split('<br')
            # for item in manufacturer:
            #     item = str(item).replace(r'\[\[', '')
            #     print(item)
            cars[make][model][generation] = {'manufacturer': manufacturer}
            # print(manufacturer)
    except Exception as e:
        # print('manu error', e)
        pass

def bodystyleParse(template):
    try:
        bodystyle = str(template.get('body_style').value.lstrip().rstrip().encode('ascii', 'ignore'))
        bodystylebackup = str(template.get('body_style').value.lstrip().rstrip().encode('ascii', 'ignore'))

        newbodystyle = []
        if 'ubl ' in bodystyle or 'list' in bodystyle or '{ubl' in bodystyle or 'unbulleted' in bodystyle:
            bodystyle = bodystyle.split('|')[1:]
            for item in bodystyle:
                if '[[' in item:
                    item = item.split('[[')
                    paraname = item[0].lstrip()
                    # print(bodystyle)
                    paravalue = item[1].replace(']', '').replace('\n*', '').split('|')
                    newItem = { paraname : paravalue}
                    newbodystyle.append(newItem)
                else:
                    item = item.split('<')[0]
                    try:
                        item = item.replace(')', '')
                    except:
                        pass
                    try:
                        item = item.replace(']', '')
                    except:
                        pass
                    try:
                        item = item.replace('}', '')
                    except:
                        pass
                    # print(item)
                    newbodystyle.append(item)
                    # pass
        else:
            bodystyle = re.split('<br>|<br/>|<br />', bodystyle)
            for item in bodystyle:
                item = item.replace('two', '2')
                item = item.replace('four', '4')
                try:
                    item = item.split('<')[0]
                except:
                    pass
                # print(bodystyle[2:6])
                item = re.findall(r'\[\[(.*?)\]\]', item)
                for subitem in item:
                    subitem = subitem.split('|')
                    for subsub in subitem:
                        newbodystyle.append(subsub)
        # print(newbodystyle)
        cars[make][model][generation] = {'bodystyle': newbodystyle}

    except Exception as e:
        print(e, 'bodystyle', bodystyle)
        # print(item)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def classParse(template):
    try:
        classy = str(template.get('class').value.lstrip().rstrip().encode('ascii', 'ignore'))
        classybackup = str(template.get('class').value.lstrip().rstrip().encode('ascii', 'ignore'))
        classy = classy.replace('#', ' ')
        classy = re.findall(r'\[\[(.*?)\]\]', classy)

            # print(classy.group(1))
        for classes in classy:
            try:
                classes = classes.split('|')
                cars[make][model][generation] = {'class': classes}
            except:
                cars[make][model][generation] = {'class': classes}

    except Exception as e:
        print(e, 'class', classy)
        # print(item)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def modelyearsParse(template):
    try:
        modelyears = str(template.get('model_years').value.lstrip().rstrip().encode('ascii', 'ignore'))
        modelyearsbackup = str(template.get('model_years').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if modelyears:
            modelyears = re.split('<br>|<br/>|<br />', modelyears)
            newmodelyears = []
            for item in modelyears:
                paraname = None
                easyvalue = None
                easyname = None
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = item.split('|')[1:]
                    for subitem in item:
                        subitem = subitem.lstrip().rstrip()

                        try:
                            subitem = subitem.replace('-', '')
                        except:
                            pass
                        try:
                            subitem = subitem.replace('}', '')
                        except:
                            pass
                        try:
                            subitem = subitem.replace('[', '')
                        except:
                            pass
                        try:
                            subitem = subitem.replace(']', '')
                        except:
                            pass
                        try:
                            subitem = subitem.replace('&ndash;', '')

                        except:
                            pass

                        try:
                            subitem = subitem.replace('present', '2020')
                        except:
                            pass

                        try:
                            subitem = subitem.replace('Present', '2020')
                        except:
                            pass

                        if len(subitem) is 8 or  len(subitem) is 6 or len(subitem) is 4:
                            newmodelyears.append(int(subitem))
                        else:
                            newItem = []
                            paraname = re.search(r'\((.*?)\)', subitem)
                            subitem = subitem.split('<')[0]
                            if paraname:
                                # print(subitem)
                                paraname = str(paraname.group(0))[1:-1]
                                value = subitem.split(' ')[0].strip(',')
                                try:
                                    newItem  =  {paraname : int(value)}
                                    newmodelyears.append(newItem)
                                except:
                                    pass
                                # print(newItem)
                            else:
                                if ':' in subitem:
                                    easyname = subitem.split(':')[0]
                                    easyvalue = subitem.split(':')[1]
                                    newItem  =  {easyname : int(easyvalue)}
                                    newmodelyears.append(newItem)

                                elif len(subitem.strip()) is 8 or  len(subitem.strip()) is 6 or len(subitem.strip()) is 4:
                                    newmodelyears.append(int(subitem.strip()))
                                else:
                                    print(subitem)
                else:
                    item = item.lstrip().rstrip()

                    try:
                        item = item.replace('-', '')
                    except:
                        pass
                    try:
                        item = item.replace('&ndash;', '')

                    except:
                        pass

                    try:
                        item = item.replace('present', '2020')
                    except:
                        pass
                    try:
                        item = item.replace('Present', '2020')
                    except:
                        pass

                    if len(item) is 8 or  len(item) is 6 or len(item) is 4:
                        newmodelyears.append(int(item))
                        # print(item)
                    else:
                        newItem = []
                        paraname = re.search(r'\((.*?)\)', item)
                        item = item.split('<')[0]
                        if paraname:
                            paraname = str(paraname.group(0))[1:-1]
                            value = item.split(' ')[0].strip(',')
                            newItem  =  {paraname : int(value)}
                            newmodelyears.append(newItem)
                            # print(newItem)
                        else:
                            if ':' in item:
                                easyname = item.split(':')[0]
                                easyvalue = item.split(':')[1]
                                newItem  =  {easyname : int(easyvalue)}
                                newmodelyears.append(newItem)
                            else:
                                item = item.lstrip().rstrip()
                                if len(item) is 8 or  len(item) is 6 or len(item) is 4:
                                    newmodelyears.append(int(item))
                                else:
                                    if 'and' in item:
                                        item = item.split('and')
                                        for subitem in item:
                                            # print(subitem.strip())
                                            newmodelyears.append(subitem.strip())
                                    elif ',' in item:
                                        item = item.split(',')
                                        for subitem in item:
                                            # print(subitem.strip())
                                            newmodelyears.append(subitem.strip())
                                    else:
                                        if '.5' in item:
                                            item = item.replace('.5', '')
                                            newmodelyears.append(item)
                                        elif len(item.replace(' ', '')) is 8:
                                            newmodelyears.append(item)
                                        else:
                                            paravalue = re.search(r'[0-9]{8}', item)
                                            if paravalue:
                                                newItem  =  {item[8:] : int(paravalue.group(0))}
                                                newmodelyears.append(newItem)
                                            else:
                                                newmodelyears.append(2020)


            modelyears = newmodelyears
            cars[make][model][generation] = {'model_years': modelyears}

    except Exception as e:
        print(e, 'model_years', modelyears)
        print(item)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def designerParse(template):
    try:
        designer = str(template.get('designer').value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
        # print(designer)

        if designer:
            cars[make][model][generation] = {'designer': designer}
            # print(designer)
    except Exception as e:
        # print('designer error', e)
        pass

def engineParse(template):
    try:
        engine = str(template.get('engine').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if engine:
            engine = re.sub("|".join(char_list), "", engine).rstrip('\r\n')
            cars[make][model][generation] = {'engine': engine}
            # print(engine)
    except Exception as e:
        # print('engine', e)
        pass

def transmissionParse(template):
    try:
        transmission = str(template.get('transmission').value.lstrip().rstrip().encode('ascii', 'ignore'))

        if transmission:
            transmission = re.sub("|".join(char_list), "", transmission).rstrip('\r\n')
            cars[make][model][generation] = {'transmission': transmission}
            # print(transmission)
    except Exception as e:
        # print('transmission', e)
        pass

def wheelbaseParse(template):
    try:
        wheelbase = str(template.get('wheelbase').value.lstrip().rstrip().encode('ascii', 'ignore'))
        wheelbasebackup = str(template.get('wheelbase').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if wheelbase:
            wheelbase = re.split('<br>|<br/>|<br />', wheelbase)
            newwheelbase = []
            for item in wheelbase:
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = re.split(r'(\s\|\s)', item)
                    # print(item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                    for subitem in item:
                        cvtcheck = [':', 'Convert', 'convert', 'cvt']
                        if any(x in subitem for x in cvtcheck):
                            subitem = re.sub(r'\'', ' ', subitem)
                            subitem = subitem.split('<')[0]

                            newItem = []
                            paraname = re.search(r'\((.*?)\)', subitem)
                            if paraname:
                                paraname = str(paraname.group(0))[1:-1]
                                value = subitem.split('|')[1]
                                if float(value) > 1000:
                                    value = round(float(value)*0.039370, 1)
                                newItem  =  {paraname : value}
                                newwheelbase.append(newItem)
                                # print(newItem)
                            else:
                                # subitem = re.split(r'[\:(\n)]', subitem)
                                if '*' in subitem:
                                    # print(make)
                                    subitem = subitem.split('*')[1:]
                                    for subsub in subitem:
                                        subsub = subsub.split(':')
                                        plainlistname = subsub[0].rstrip().lstrip()
                                        plainlistvalue = subsub[1].split('|')[1]
                                        newItem  =  {plainlistname : plainlistvalue}
                                        newwheelbase.append(newItem)
                                        # print(newItem)

                                else:
                                    if ':' in subitem:
                                        subitem = subitem.split(':')
                                        easyname = subitem[0]
                                        easyvalue = subitem[1].split('|')[1]
                                        newItem = {easyname : easyvalue}
                                        newwheelbase.append(newItem)
                                        # print(newItem)

                                    else:
                                        subitem = subitem.rstrip().split('}} ')
                                        lastname = subitem[1]
                                        lastvalue = subitem[0].split('|')[1]
                                        newItem = {lastname : lastvalue}
                                        newwheelbase.append(newItem)
                                        # print(newItem)

                elif '|' in str(item):
                    item = re.split('\|', item)
                    if ':' in item[0]:
                        item[0] = re.split(':', item[0])[0]
                        newItem = {}
                        if float(item[1]) > 1000:
                            item[1] = round(float(item[1])*0.039370, 1)
                        newItem[item[0]] = item[1]
                        newwheelbase.append(newItem)
                    elif '}}' in item[-1]:
                        modelindicator = re.search(r'\((.*?)\)', item[-1])
                        if modelindicator:
                            modelindicator = str(modelindicator.group(0))[1:-1]
                            newItem = {}
                            item[1] = item[1].split('-')[0]
                            if float(item[1]) > 1000:
                                item[1] = round(float(item[1])*0.039370, 1)
                            newItem[modelindicator] = item[1]
                            newwheelbase.append(newItem)
                        else:
                            if float(item[1]) > 1000:
                                item[1] = round(float(item[1])*0.039370, 1)
                            item = item[1]
                            newwheelbase.append(item)

                    else:
                        pass
                else:
                    item = item.replace('&nbsp;', ' ')
                    if ':' in item:
                        item = item.split(':')
                        modelname = item[0].lstrip()
                        modelvalue = item[1].lstrip().split(' ')[0]
                        # print(modelvalue)
                        if float(modelvalue) > 1000:
                            modelvalue = round(float(modelvalue)*0.039370, 1)
                        newItem = {modelname : modelvalue}
                        newwheelbase.append(newItem)


                    else:
                        if '(' in item:
                            parans = re.findall(r'\((.*?\))', item)
                            # print(parans)
                            for paran in parans:
                                modelname = None
                                modelvalue = None
                                if 'mm' in paran:
                                    continue
                                else:
                                    modelname = str(paran).strip(')')
                                    # modelvalue = re.sub(r'\((.*?)\)', '', item)
                                    item = wheelbasebackup.split(',')
                                    if len(item) is 3:
                                        newwheelbase = []
                                        for subitem in item:
                                            newItem = {}
                                            subitem = subitem.split('<br/>')
                                            modelname = subitem[1].split(' ')[0]
                                            modelvalue = subitem[0].split('|')[1]
                                            if float(modelvalue) > 1000:
                                                modelvalue = round(float(modelvalue)*0.039370, 1)
                                            newItem = {modelname : modelvalue}
                                            newwheelbase.append(newItem)
                                        item = newwheelbase
                                        # print(item)

                                    else:
                                        # print(modelname)
                                        # item = item[0].replace(r'\((.*?\s?.*?\))', '')
                                        item = re.sub(r'\((.*?\s?.*?\))', '', item[0])
                                        modelvalue = item.split(' ')[0]
                                        newItem = {modelname : modelvalue}
                                        newwheelbase.append(newItem)

                if type(item) is str:
                    item = re.sub(r'\((.*?\s?.*?\))', '', item)
                    item = item.split('<')[0]
                    # print(item)
                    # item = re.sub(r'\<(.*?\s?.*?)\>', '', item)
                    item = item.lstrip().split(' ')
                    if len(item) is 4:
                        modelname = item[3]
                        modelvalue = item[0]
                        if float(modelvalue) > 1000:
                            modelvalue = round(float(modelvalue)*0.039370, 1)
                        newItem = {modelname : modelvalue}
                        newwheelbase.append(newItem)

                    else:
                        newItem = item[0]
                        newwheelbase.append(newItem)


                # print(item)
            # print(newwheelbase)

            cars[make][model][generation] = {'wheelbase': newwheelbase}

    except Exception as e:
        print('wheelbase', wheelbase, e)

def lengthParse(template):
    try:
        length = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
        lengthbackup = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if length:
            length = re.split('<br>|<br/>|<br />', length)
            newlength = []
            for item in length:
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = re.split(r'(\s\|\s)', item)
                    # print(item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                    for subitem in item:
                        cvtcheck = [':', 'Convert', 'convert', 'cvt']
                        if any(x in subitem for x in cvtcheck):
                            subitem = re.sub(r'\'', ' ', subitem)
                            subitem = subitem.split('<')[0]
                            newItem = {}
                            if ':' in subitem:
                                # print(subitem)
                                subitem = subitem.split(':')
                                easyname = subitem[0]
                                easyname = easyname.replace('{{ubl\n|' , '').lstrip()
                                try:
                                    easyvalue = subitem[1].split('|')[1]
                                except:
                                    easyvalue = re.search(r'\((.*?\s?.*?)\)', subitem[1])
                                    easyvalue = str(easyvalue.group(0))[1:-1]
                                    easyvalue = easyvalue.split(' ')[0]
                                    # newItem = {easyname : easyvalue}
                                newItem = {easyname : easyvalue}
                                newlength.append(newItem)
                                # print(newItem)

                            else:
                                if 'ubl' in subitem:
                                    subitem = subitem.split('|')
                                    subitem[1] = subitem[1].split(' ')[0]
                                    # easyname = subitem[1]
                                    newItem = {subitem[1] : subitem[2]}
                                    newlength.append(newItem)
                                    # print(newItem)
                                else:
                                    # print(subitem)
                                    easyname = re.search(r'\((.*?\s?.*?)\)', subitem)
                                    if easyname:
                                        easyname = str(easyname.group(0))[1:-1]
                                        subitem = subitem.split(' ')[0]
                                        easyvalue = subitem.split('|')[1]
                                        if '+' in easyvalue:
                                            easyvalue = easyvalue.split('+')[0]
                                        newItem = {easyname : easyvalue}
                                        newlength.append(newItem)
                                    else:
                                        # subitem = subitem.split(' ')
                                        subitem = subitem.split('|')
                                        easyname = subitem[0].split(' ')[0]
                                        easyvalue = subitem[1]
                                        newItem = {easyname : easyvalue}
                                        newlength.append(newItem)

                else:
                    item = item.split('<')[0]
                    if ':' in item:
                        item = item.split(':')
                        easyname = item[0]
                        if '|' in item[1]:
                            easyvalue = item[1].split('|')[1]
                        else:
                            # print(item)
                            easyvalue = item[1].split(' ')[1]
                        easyvalue = easyvalue.replace('in', '')
                        if float(easyvalue) > 1000:
                            easyvalue = round(float(easyvalue)*0.039370, 1)
                        newItem = {easyname : easyvalue}
                        newlength.append(newItem)
                    else:
                        if '&nbsp;' in item:
                            item = item.replace('&nbsp;', ' ')
                            # easyname = re.search(r'\((.*?)\)', item)
                            easyname = item.count('(')
                            item = item.split(' ')
                            easyvalue = item[0]
                            if float(easyvalue) > 1000:
                                easyvalue = round(float(easyvalue)*0.039370, 1)
                            # print(easyname.groups())
                            if easyname is 2:
                                easyname = item[0][1:-1]
                                easyvalue = item[1]
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                newItem = {easyname : easyvalue}
                                newlength.append(newItem)
                            else:
                                newItem = easyvalue
                                newlength.append(newItem)

                        else:
                            if '|' in item:
                                easyvalue = item.split('|')[1]
                                easyvalue = easyvalue.split('-')[0]
                                easyvalue = easyvalue.split('+')[0]
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                if '(' in item:
                                    easyname = re.search(r'\((.*?)\)', item)
                                    try:
                                        easyname = easyname.group(0)[1:-1]
                                    except:
                                        item = item.split('(')
                                        easyname = item[1]
                                        easyvalue = item[0].split('|')[1]
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        # print(item)
                                    newItem = {easyname : easyvalue}
                                    newlength.append(newItem)
                                else:
                                    newItem = easyvalue
                                    newlength.append(newItem)
                            else:
                                item = item.split(' ')
                                easyvalue = item[0]
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                try:
                                    easyname = item[4][1:-1]
                                    newItem = {easyname : easyvalue}
                                    newlength.append(newItem)
                                except:
                                    newItem = easyvalue
                                    newlength.append(newItem)

                length = newlength
                # print(length)


            cars[make][model][generation] = {'length': newlength}

    except Exception as e:
        print(e, 'length', length)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def widthParse(template):
    try:
        width = str(template.get('width').value.lstrip().rstrip().encode('ascii', 'ignore'))
        widthbackup = str(template.get('width').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if width:
            width = re.split('<br>|<br/>|<br />', width)
            newwidth = []
            for item in width:
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = re.split(r'(\s\|\s)', item)
                    # print(item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                    for subitem in item:
                        cvtcheck = [':', 'Convert', 'convert', 'cvt']
                        if any(x in subitem for x in cvtcheck):
                            subitem = re.sub(r'\'', ' ', subitem)
                            subitem = subitem.split('<')[0]
                            newItem = {}
                            if ':' in subitem:
                                # print(subitem)
                                subitem = subitem.split(':')
                                easyname = subitem[0]
                                easyname = easyname.replace('{{ubl\n|' , '').lstrip()
                                try:
                                    easyvalue = subitem[1].split('|')[1]
                                except:
                                    easyvalue = re.search(r'\((.*?\s?.*?)\)', subitem[1])
                                    easyvalue = str(easyvalue.group(0))[1:-1]
                                    easyvalue = easyvalue.split(' ')[0]
                                    # newItem = {easyname : easyvalue}
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                newItem = {easyname : easyvalue}
                                newwidth.append(newItem)
                                # print(newItem)

                            else:
                                if 'ubl' in subitem:
                                    subitem = subitem.split('|')
                                    subitem[1] = subitem[1].split(' ')[0]
                                    easyvalue = subitem[2]
                                    easyvalue = easyvalue.replace(',','')
                                    easyvalue = easyvalue.replace('mm','')
                                    if float(easyvalue) > 1000:
                                        easyvalue = round(float(easyvalue)*0.039370, 1)
                                    newItem = {subitem[1] : easyvalue}
                                    newwidth.append(newItem)
                                    # print(newItem)
                                else:
                                    # print(subitem)
                                    easyname = re.search(r'\((.*?\s?.*?)\)', subitem)
                                    if easyname:
                                        easyname = str(easyname.group(0))[1:-1]
                                        subitem = subitem.split(' ')[0]
                                        easyvalue = subitem.split('|')[1]
                                        if '+' in easyvalue:
                                            easyvalue = easyvalue.split('+')[0]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        newItem = {easyname : easyvalue}
                                        newwidth.append(newItem)
                                    else:
                                        # subitem = subitem.split(' ')
                                        subitem = subitem.split('|')
                                        easyname = subitem[0].split(' ')[0]
                                        easyvalue = subitem[1]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        newItem = {easyname : easyvalue}
                                        newwidth.append(newItem)

                else:
                    item = item.split('<')[0]
                    if ':' in item:
                        item = item.split(':')
                        easyname = item[0]
                        if '|' in item[1]:
                            easyvalue = item[1].split('|')[1]
                        else:
                            # print(item)
                            easyvalue = item[1].split(' ')[1]
                        easyvalue = easyvalue.replace('in', '')
                        easyvalue = easyvalue.replace(',','')
                        easyvalue = easyvalue.replace('mm','')
                        if float(easyvalue) > 1000:
                            easyvalue = round(float(easyvalue)*0.039370, 1)
                        newItem = {easyname : easyvalue}
                        newwidth.append(newItem)
                    else:
                        if '&nbsp;' in item:
                            item = item.replace('&nbsp;', ' ')
                            # easyname = re.search(r'\((.*?)\)', item)
                            easyname = item.count('(')
                            item = item.split(' ')
                            easyvalue = item[0]
                            easyvalue = easyvalue.replace(',','')
                            easyvalue = easyvalue.replace('mm','')
                            if float(easyvalue) > 1000:
                                easyvalue = round(float(easyvalue)*0.039370, 1)
                            # print(easyname.groups())
                            if easyname is 2:
                                easyname = item[0][1:-1]
                                easyvalue = item[1]
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                newItem = {easyname : easyvalue}
                                newwidth.append(newItem)
                            else:
                                newwidth.append(easyvalue)

                        else:
                            if '|' in item:
                                easyvalue = item.split('|')[1]
                                easyvalue = easyvalue.split('-')[0]
                                easyvalue = easyvalue.split('+')[0]
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                if '(' in item:
                                    easyname = re.search(r'\((.*?)\)', item)
                                    try:
                                        easyname = easyname.group(0)[1:-1]
                                    except:
                                        item = item.split('(')
                                        easyname = item[1]
                                        easyvalue = item[0].split('|')[1]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        # print(item)
                                    newItem = {easyname : easyvalue}
                                    newwidth.append(newItem)
                                else:
                                    newwidth.append(easyvalue)
                            else:
                                item = item.split(' ')
                                easyvalue = item[0]
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                try:
                                    easyname = item[4][1:-1]
                                    newItem = {easyname : easyvalue}
                                    newwidth.append(newItem)
                                except:
                                    newwidth.append(easyvalue)

                width = newwidth

            cars[make][model][generation] = {'width': newwidth}

    except Exception as e:
        print(e, 'width', width)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def heightParse(template):
    try:
        height = str(template.get('height').value.lstrip().rstrip().encode('ascii', 'ignore'))
        heightbackup = str(template.get('height').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if height:
            height = re.split('<br>|<br/>|<br />', height)
            newheight = []
            for item in height:
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = re.split(r'(\s\|\s)', item)
                    # print(item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                    for subitem in item:
                        subitem = subitem.replace('&nbsp;', ' ')

                        cvtcheck = [':', 'Convert', 'convert', 'cvt']
                        if any(x in subitem for x in cvtcheck):
                            subitem = re.sub(r'\'', ' ', subitem)
                            subitem = subitem.split('<')[0]
                            newItem = {}
                            if ':' in subitem:
                                # print(subitem)
                                subitem = subitem.split(':')
                                easyname = subitem[0]
                                easyname = easyname.replace('{{ubl\n|' , '').lstrip()
                                try:
                                    easyvalue = subitem[1].split('|')[1]
                                except:
                                    easyvalue = re.search(r'\((.*?\s?.*?)\)', subitem[1])
                                    easyvalue = str(easyvalue.group(0))[1:-1]
                                    easyvalue = easyvalue.split(' ')[0]
                                    # newItem = {easyname : easyvalue}
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                newItem = {easyname : easyvalue}
                                newheight.append(newItem)
                                # print(newItem)

                            else:
                                if 'ubl' in subitem:
                                    subitem = subitem.split('|')
                                    subitem[1] = subitem[1].split(' ')[0]
                                    easyvalue = subitem[2]
                                    easyvalue = easyvalue.replace(',','')
                                    easyvalue = easyvalue.replace('mm','')
                                    if float(easyvalue) > 1000:
                                        easyvalue = round(float(easyvalue)*0.039370, 1)
                                    newItem = {subitem[1] : easyvalue}
                                    newheight.append(newItem)
                                    # print(newItem)
                                else:
                                    # print(subitem)
                                    easyname = re.search(r'\((.*?\s?.*?)\)', subitem)
                                    if easyname:
                                        easyname = str(easyname.group(0))[1:-1]
                                        subitem = subitem.split(' ')[0]
                                        easyvalue = subitem.split('|')[1]
                                        if '+' in easyvalue:
                                            easyvalue = easyvalue.split('+')[0]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        newItem = {easyname : easyvalue}
                                        newheight.append(newItem)
                                    else:
                                        # subitem = subitem.split(' ')
                                        subitem = subitem.split('|')
                                        easyname = subitem[0].split(' ')[0]
                                        easyvalue = subitem[1]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        newItem = {easyname : easyvalue}
                                        newheight.append(newItem)

                else:
                    item = item.replace('&nbsp;', ' ')

                    item = item.split('<')[0]
                    if ':' in item:
                        item = item.split(':')
                        easyname = item[0]
                        if '|' in item[1]:
                            easyvalue = item[1].split('|')[1]
                        else:
                            # print(item)


                            easyvalue = item[1].split(' ')[1]
                        easyvalue = easyvalue.replace('in', '')
                        easyvalue = easyvalue.replace(',','')
                        easyvalue = easyvalue.replace('mm','')
                        if float(easyvalue) > 1000:
                            easyvalue = round(float(easyvalue)*0.039370, 1)
                        newItem = {easyname : easyvalue}
                        newheight.append(newItem)
                    else:
                        if '&nbsp;' in item:
                            item = item.replace('&nbsp;', ' ')
                            # easyname = re.search(r'\((.*?)\)', item)
                            easyname = item.count('(')
                            item = item.split(' ')
                            easyvalue = item[0]
                            easyvalue = easyvalue.replace(',','')
                            easyvalue = easyvalue.replace('mm','')
                            if float(easyvalue) > 1000:
                                easyvalue = round(float(easyvalue)*0.039370, 1)
                            # print(easyname.groups())
                            if easyname is 2:
                                easyname = item[0][1:-1]
                                easyvalue = item[1]
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                newItem = {easyname : easyvalue}
                                newheight.append(newItem)
                            else:
                                newheight.append(easyvalue)

                        else:
                            if '|' in item:
                                easyvalue = item.split('|')[1]
                                easyvalue = easyvalue.split('-')[0]
                                easyvalue = easyvalue.split('+')[0]
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                if '(' in item:
                                    easyname = re.search(r'\((.*?)\)', item)
                                    try:
                                        easyname = easyname.group(0)[1:-1]
                                    except:
                                        item = item.split('(')
                                        easyname = item[1]
                                        easyvalue = item[0].split('|')[1]
                                        easyvalue = easyvalue.replace(',','')
                                        easyvalue = easyvalue.replace('mm','')
                                        if float(easyvalue) > 1000:
                                            easyvalue = round(float(easyvalue)*0.039370, 1)
                                        # print(item)
                                    newItem = {easyname : easyvalue}
                                    newheight.append(newItem)
                                else:
                                    newheight.append(easyvalue)
                            else:
                                item = item.split(' ')
                                easyvalue = item[0]
                                easyvalue = easyvalue.replace(',','')
                                easyvalue = easyvalue.replace('mm','')
                                if float(easyvalue) > 1000:
                                    easyvalue = round(float(easyvalue)*0.039370, 1)
                                try:
                                    easyname = item[4][1:-1]
                                    newItem = {easyname : easyvalue}
                                    newheight.append(newItem)
                                except:
                                    newheight.append(easyvalue)

                height = newheight

            # print(newheight)

            cars[make][model][generation] = {'height': newheight}

    except Exception as e:
        print(e, 'height', height)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def weightParse(template):
    try:
        weight = str(template.get('weight').value.lstrip().rstrip().encode('ascii', 'ignore'))
        weightbackup = str(template.get('weight').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if weight:

            # print(weight)
            weight = re.split('<br>|<br/>|<br />', weight)
            newweight = []
            for item in weight:
                newItem = {}
                easyname = None
                easyvalue = None
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = re.split(r'(\s\|\s)', item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                    for subitem in item:
                        newItem = {}
                        easyname = None
                        easyvalue = None
                        subitem = subitem.replace('&nbsp;', ' ')

                        cvtcheck = [':', 'Convert', 'convert', 'cvt']
                        if any(x in subitem for x in cvtcheck):
                            subitem = re.sub(r'\'', ' ', subitem)
                            subitem = subitem.split('<')[0]
                            if '| ' in subitem:
                                subsub = subitem.split('| ')
                                for subsubsub in subsub:
                                    if ':' in subsubsub:
                                        # print(subitem, '\n')
                                        subsubsub = subsubsub.split(':')
                                        easyname = subsubsub[0]
                                        easyname = easyname.replace('{{ubl\n|' , '').lstrip()
                                        easyvalue = subsubsub[1]
                                        # print(easyvalue)
                                        easyvalue = easyvalue.split('|')
                                        if 'lb' in easyvalue[2]:
                                            easyvalue = easyvalue[1]
                                        else:
                                            easyvalue = round(float(easyvalue[1])/0.45359237, 0)
                                        newItem = {easyname : easyvalue}
                                        newweight.append(newItem)
                            else:
                                if ':' in subitem:
                                    subitem = subitem.split(':')
                                    easyname = subitem[0]
                                    easyname = easyname.replace('{{ubl\n|' , '').lstrip()
                                    easyvalue = subitem[1]
                                    # print(easyvalue)
                                    easyvalue = easyvalue.split('|')
                                    if 'lb' in easyvalue[2]:
                                        easyvalue = easyvalue[1]
                                    else:
                                        easyvalue = round(float(easyvalue[1])/0.45359237, 0)
                                    newItem = {easyname : easyvalue}
                                    newweight.append(newItem)
                                else:
                                    easyvalue = re.search(r'\{(.*?)\}', subitem)
                                    easyvalue = easyvalue.group(1).split('|')
                                    if 'kg' in easyvalue[2]:
                                        easyvalue = int(round(float(easyvalue[1])/0.45359237))
                                    elif 'lb' in easyvalue[2]:
                                        easyvalue = easyvalue[1]
                                    else:
                                        easyvalue = str(easyvalue[1].replace(',','')) + '-' + str(easyvalue[3].replace(',',''))
                                    easyname = re.search(r'\((.*?)\)', subitem)
                                    if easyname:
                                        easyname = easyname.group(1)
                                        newItem = {easyname : easyvalue}
                                        newweight.append(newItem)
                                        # print(newItem)

                                    else:
                                        newweight.append(easyvalue)
                                        # print(easyvalue)
                        else:
                            if '*' in subitem:
                                easyvalue = subitem.split('\n')
                                for subsub in easyvalue:
                                    if '*' in subsub:
                                        easyvalue = subsub.replace(',', '')[1:]
                                        easyvalue = easyvalue.split(' ')
                                        try:
                                            easyname = re.search(r'\((.*?)\)', easyvalue[2])
                                            easyvalue = easyvalue[0]
                                            easyname = easyname.group(1)
                                            newItem = {easyname : easyvalue}
                                            newweight.append(newItem)
                                        except:
                                            newweight.append(easyvalue)
                                    else:
                                        # print(subsub)
                                        pass
                            else:
                                # print(subitem)
                                pass
                else:
                    item = item.split('<')[0]
                    cvtcheck = [':', 'Convert', 'convert', 'cvt']
                    if any(x in item for x in cvtcheck):
                        if '-' in item:
                            try:
                                easyname = re.search(r'\((.*?)\)', item)
                                easyname = easyname.group(1)
                                easyvalue = item.split('(')[0]
                                if '-' in easyvalue:
                                    easyvalue1 = easyvalue.split('|')[1]
                                    easyvalue2 = easyvalue.split('|')[3]
                                    if 'kg' in easyvalue.split('|')[4]:
                                        easyvalue1 = int(round(float(easyvalue1)/0.45359237))
                                        easyvalue2 = int(round(float(easyvalue2)/0.45359237))
                                        easyvalue = str(easyvalue1) + str(easyvalue2)
                                        newweight.append({easyname : easyvalue})
                                        # print(newweight)
                                    else:
                                        easyvalue = str(easyvalue1) + str(easyvalue2)
                                        newweight.append({easyname : easyvalue})
                                        # print(newweight)
                                else:
                                    easyvalue = easyvalue.split('|')[1]
                                    newweight.append(easyvalue)
                                    # print(easyvalue)


                                # print(easyname, easyvalue)
                            except:
                                # print(item)
                                if 'door' in item:
                                    item = item.lstrip()
                                    item = item.split(' ')
                                    # print(item)
                                    if len(item) is 3:
                                        easyname = item[0]
                                        easyvalue = item[2].split('|')
                                        easyvalue = easyvalue[1]
                                    else:
                                        easyname = item[0]
                                        easyvalue = item[1].split('|')
                                        easyvalue = easyvalue[1]

                                    # print(eas)

                                    newItem = {easyname: easyvalue}
                                    newweight.append(newItem)
                                    # print(newItem)
                                else:
                                    item = item.replace('|-|', '-')
                                    item = item.replace(',', '')
                                    if '| - |' in item or '} - {' in item:
                                        item = item.split(' - ')
                                        item[0] = item[0].split('|')
                                        item[1] = item[1].split('|')
                                        easyvalue1 = int(round(float(item[0][1])/0.45359237))
                                        easyvalue2 = int(round(float(item[1][1])/0.45359237))
                                        easyvalue = str(easyvalue1).lstrip() + str(easyvalue2).rstrip()
                                        newweight.append(easyvalue.strip())
                                        # print(easyvalue)


                                    elif '-' in item:
                                        item = item.split('|')
                                        if 'kg' in item[2]:
                                            item[1] = item[1].split('-')
                                            easyvalue1 = int(round(float(item[1][0])/0.45359237))
                                            easyvalue2 = int(round(float(item[1][1])/0.45359237))
                                            easyvalue = str(easyvalue1).lstrip() + str(easyvalue2).lstrip().rstrip()
                                            newweight.append(easyvalue)
                                            # print(easyvalue)
                                        else:
                                            easyvalue = item[1].replace('-', '').strip()
                                            newweight.append(easyvalue.strip())
                                            # print(easyvalue)
                                    else:
                                        # print(item)
                                        pass
                        else:
                            if ':' in item:
                                # item = re.sub(' +', '', item)
                                item = item.split(':')
                                if 'convert' in item[1] or 'Convert' in item[1]:
                                    easyname = item[0]
                                    easyname = easyname.replace('&nbsp;', '')
                                    easyname = easyname.replace('\n', '')
                                    easyvalue = item[1].split('|')[1]
                                    newItem = {easyname:easyvalue}
                                    newweight.append(newItem)
                                else:
                                    easyname = item[0]
                                    easyname = easyname.replace('&nbsp;', '')
                                    easyname = easyname.replace('\n', '')
                                    print(item)
                                    easyvalue = item[1].split(' ')
                                    easyvalue = list(filter(None, easyvalue))
                                    print(easyvalue)
                                    easyvalue = easyvalue[0]
                                    newItem = {easyname:easyvalue}
                                    newweight.append(newItem)
                                    print(newItem)
                            # else:


                                # pass
                    else:
                        item = item.replace('&nbsp;', ' ')
                        item = item.replace('&ndash;', ' - ')
                        item = item.replace(',','')
                        try:
                            easyname = re.search(r'\'\'\'(.*?)\'\'\'', item)
                            easyname = easyname.group(1)
                            easyvalue = item.lstrip().split(' ')[1]
                            newItem = {easyname : easyvalue}
                            newweight.append(newItem)

                        except:
                            paran = re.findall(r'\((.*?)\)', item)
                            # print(paran)

                            if len(paran) > 1:
                                easyname = paran[1]
                                easyvalue = paran[0].split(' ')[0]
                                easyvalue = int(round(float(easyvalue)/0.45359237, 0))
                                newItem = {easyname : easyvalue}
                                newweight.append(newItem)
                            elif len(paran) is 1:
                                paran = paran[0]
                                if '-' in paran:
                                    if 'kg' in paran:
                                        # print(paran)
                                        paran = paran.replace('kg', '')
                                        paran = paran.replace(',', '')
                                        paran = paran.replace(' - ', '')
                                        paran = paran.replace('-', ' ')
                                        paran = paran.lstrip().rstrip()
                                        paran = paran.split(' ')
                                        for subparan in paran:
                                            subparan = int(round(float(subparan)/0.45359237))
                                        paran = str(paran[0]) + str(paran[1])
                                        newweight.append(paran)
                                        # print(paran)
                                    else:
                                        paran = paran.replace('lb', '')
                                        paran = paran.replace('-', ' ')
                                        paran = paran.lstrip().rstrip()
                                        paran = paran.split(' ')                                        # paran = paran[0]
                                        for subparan in paran:
                                            subparan = int(round(float(subparan)/0.45359237))
                                        paran = str(paran[0]) + str(paran[1])
                                        newweight.append(paran)
                                else:
                                    paran = paran.split(' ')
                                    if 'kg' in paran[1]:
                                        if len(paran[0]) is 8:
                                            paran1 = paran[0][:4]
                                            paran1 = int(round(float(paran1)/0.45359237))
                                            paran2 = paran[0][4:]
                                            paran2 = int(round(float(paran2)/0.45359237))
                                            paran = str(paran1) + str(paran2)
                                            newweight.append(paran)
                                        else:
                                            paran = int(round(float(paran[0])/0.45359237))
                                            newweight.append(paran)
                                    else:
                                        paran = paran[0]
                                        newweight.append(paran)

                            else:
                                item = item.replace('-', ' ')
                                item = item.replace('lbs.', '')
                                item = item.replace('lb', '')
                                ''.join(item.split())
                                item = item.split(' ')
                                if len(item) is 1:
                                    newweight.append(item[0])
                                else:
                                    item = str(item[0]) + str(item[1])
                                    newweight.append(item)

                weight = newweight

            # print(weightbackup)
            # print(newweight)

            cars[make][model][generation] = {'weight': newweight}

    except Exception as e:
        print(e, 'weight', weight)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

for filename in os.listdir(root_path):
    make = str(filename.split('.')[0].encode('ascii', 'ignore'))
    # print(make)
    cars[make] = {}
    if filename.endswith(".xml"):
    # if filename.endswith("esla.xml"):

        with open (root_path + filename, 'r') as vehicles_file:


            mainsoup = BeautifulSoup(vehicles_file,features="lxml")
            pages = mainsoup.find_all('page')
            for page in pages:
                model = str(page.find('title').get_text().encode('ascii', 'ignore'))
                # print(title)
                # print(title)
                cars[make][model] = {}
                texts = page.find_all('text')

                for text in texts:
                    try:
                        wikicode = mwparserfromhell.parse(text.get_text().encode('ascii', 'ignore'))
                        templates = wikicode.filter_templates(recursive = True)


                        for template in templates:

                            # if 'Infobox automobile' or 'Infobox electric' or 'Infobox racing' in template.name:
                            namecheck = ['Infobox automobile', 'Infobox electric', 'Infobox racing']
                            if any(x in template.name for x in namecheck):

                                electric = None
                                generation = None
                                production = None
                                designer= None
                                engine= None
                                engines= None
                                transmission= None
                                transmissions= None
                                assembly = None
                                wheelbase = None
                                length = None
                                lengthbackup = None
                                width = None
                                widthbackup = None
                                char_list = ['\[', '\]', '\&nbsp\;L', '\/\>', '\}', '\{', 'unbulleted list', '\&nbsp\;']

                                if 'electric' in template.name:
                                    electric = True
                                else:
                                    electric = False


                                # generationParse(template)
                                #
                                # productionParse(template)
                                #
                                # modelyearsParse(template)
                                #
                                # assemblyParse(template)
                                #
                                # designerParse(template)
                                #
                                # classParse(template)
                                #
                                # bodystyleParse(template)
                                #
                                # manufacturerParse(template)
                                #
                                # engineParse(template)
                                #
                                # transmissionParse(template)
                                #
                                # wheelbaseParse(template)
                                #
                                # lengthParse(template)
                                #
                                # widthParse(template)
                                #
                                # heightParse(template)
                                #
                                weightParse(template)

                    except Exception as e:
                        # print(e)
                        continue



#EXPORT_________________________________________
#
# dir = ('C:/Users/eufou/Desktop/CARS/parsed')
# if not os.path.exists(dir):
#     os.mkdir(dir)
#
# for key in myDict:
#     subdir = (dir +"/" + key)
#     if not os.path.exists(subdir):
#         os.mkdir(subdir)
#
# def jsonOutput(subdir,filename,data):
#     if data:
#         with open(os.path.join(dir + subdir, filename + '.txt'), mode='w') as outfile:
#             json.dump(data, outfile)
#     else:
#         pass


#EXPORT ACTIVITY____________________
#
# def exporter():
#
#
#
#     #EXPORT PHONE__________
#         phoneHolder = []
#         for entry in myDict['Phone']:
#             try:
#                 if int(entry['Date']) > int(file[0]['Start']) and int(entry['Date']) < int(file[-1]['End']):
#                     phoneHolder.append(entry)
#             except Exception as e:
#                 print("Phone ", e)
#                 continue
#         jsonOutput('/Phone', filename, phoneHolder)
#


# fileParse()
# print(len(cars))
# print(vehicles)

# exporter()
