import os
import sys
import os.path
import json
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
        generation = None
        # print(str(template.get("name").value))
        generation = str(template.get("name").value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
        generation = re.sub('<br>', ' ', generation)
        generation = generation.split('<ref>')[0].lstrip()

        return generation
    except Exception as e:
        pass
        # print(e, 'generation', generation)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

def productionParse(template):
    try:
        production = None
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
                # print('replace present', e)
                pass
            try:
                production = production.replace('-', '')
            except Exception as e:
                # print(production)
                # print('replace present', e)
                pass
            try:
                production = production.replace('&ndash', '')
            except Exception as e:
                # print(production)
                # print('replace ndash', e)
                pass
            try:
                production = production.replace('&ndash;', '')
            except Exception as e:
                # print(production)
                # print('replace ndash', e)
                pass

            try:
                production = re.findall(r'[0-9]+', production)

                production = purify(production, productionbackup)

            except Exception as e:
                # print('split', e)
                pass


            if len(production) == 2 and all(len(flag) == 4 for flag in production):
                # print(productionbackup)
                # print(production)
                newproduction = str(production[0]) + str(production[1])
                production = [newproduction]
            elif all(len(flag) == 8 for flag in production):
                # cars[make][model][generation] = {'production': production}
                production = production
            elif len(production) == 1 and all(len(flag) == 4 for flag in production):
                # cars[make][model][generation] = {'production': production}
                production = production

            else:
                production = None
                # print(productionbackup)
                # print(production)

        return production
    except Exception as e:
        # print('function', e , '\n', production)
        return

    # print(production)

def assemblyParse(template):
    assembly = None
    try:
        assembly = str(template.get('assembly').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if assembly:
            assembly = re.split('<br>|<br/>|<br />', assembly)
            newassembly = []
            for item in assembly:
                item = item.split('<') [0]
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = item.split('|')[1:]
                    for subitem in item:
                        char_list = ['\*', '\[', '\]', '\|', '\<br\>', '\<br\/\>', '\n', '\<br \/\>', '\{', '\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']

                        subitem = re.sub("|".join(char_list), "", subitem)
                        newassembly.append(subitem)
                else:
                    char_list = ['\*', '\[', '\]', '\|', '\<br\>', '\<br\/\>', '\n', '\<br \/\>', '\{', '\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']
                    item = re.sub("|".join(char_list), "", item)
                    assembly = item
            # print(item)

            # print(assembly)
            assembly = newassembly
            return assembly
        else:
            return None
            # print(assembly)
    except Exception as e:
        # print(assembly)
        pass
        # print('assembly error', e)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

def manufacturerParse(template):
    try:
        manufacturer = str(template.get('manufacturer').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if manufacturer:
            # print(make)
            # print(manufacturer)
            # manufacturer = re.search(r'\[\[(.*)\]\]', manufacturer)
            # manufacturer = manufacturer.split(']]')
            char_list = ['\[', '\]', '\|', '\<br\>', '\<br\/\>', '\<br \/\>', '\{\{', '\}\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']

            manufacturer = re.sub("|".join(char_list), " ", manufacturer)
            manufacturer = re.sub(r'\s+', ' ', manufacturer).rstrip().lstrip()
            manufacturer = manufacturer.split('.')[0]
            manufacturer = manufacturer.split('#')[0]
            manufacturer = manufacturer.split('<')[0]
            # print(len(manufacturer))
            # if len(manufacturer) < 2:
            #     print(manufacturer)
            # if manufacturer is None:
            #     print(template)
            # manufacturer = manufacturer.split('<br')
            # for item in manufacturer:
            #     item = str(item).replace(r'\[\[', '')
            #     print(item)
            # cars[make][model][generation] = {'manufacturer': manufacturer}
            return manufacturer
        else:
            return filename.split('.')[0]
            # print(manufacturer)
    except Exception as e:
        # print(filename.split('.')[0])
        return filename.split('.')[0]

        # print('manu error', e, template)
        pass


def bodystyleParse(template):
    try:
        bodystlye = None
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
                    paravalue = item[1].replace(']', '').replace('\n*', '').split('|')[0]
                    char_list = ['\*', '\#', '\[', '\]', '\|', '\<br\>', '\<br\/\>', '\n', '\<br \/\>', '\{', '\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']
                    paravalue = re.sub("|".join(char_list), "", paravalue)
                    paravalue = paravalue.split('<')[0]
                    # print(paravalue)
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
        # cars[make][model][generation] = {'bodystyle': newbodystyle}
        return newbodystyle
    except Exception as e:
        pass
        # print(e, 'bodystyle', bodystyle)
        # # print(item)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

def classParse(template):
    try:
        classy = str(template.get('class').value.lstrip().rstrip().encode('ascii', 'ignore'))
        classybackup = str(template.get('class').value.lstrip().rstrip().encode('ascii', 'ignore'))
        classy = classy.replace('#', ' ')
        classy = re.findall(r'\[\[(.*?)\]\]', classy)
        newclass= []
            # print(classy.group(1))
        for classes in classy:
            try:
                classes = classes.split('|')
                # cars[make][model][generation] = {'class': classes}
                for subclass in classes:
                    newclass.append(subclass)
            except:
                newclass.append(classes)
                # cars[make][model][generation] = {'class': classes}
        return newclass
    except Exception as e:
        pass
        # print(e, 'class', classy)
        # # print(item)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

def modelyearsParse(template):
    try:
        try:
            modelyears = str(template.get('production').value.lstrip().rstrip().encode('ascii', 'ignore'))
            modelyearsbackup = str(template.get('production').value.lstrip().rstrip().encode('ascii', 'ignore'))
        except:
            modelyears = str(template.get('model_years').value.lstrip().rstrip().encode('ascii', 'ignore'))
            modelyearsbsackup = str(template.get('model_years').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if modelyears:
            if car['model'] == 'Ford EXP':
                modelyears = modelyears.replace('.5', '')
                # print(modelyears)
            if car['model'] == 'GMC Typhoon':
                modelyears = modelyears.split('<')[0]
            modelyears = re.split('<br>|<br/>|<br />|<BR>', modelyears)
            newmodelyears = []
            for item in modelyears:
                paraname = None
                easyvalue = None
                easyname = None
                value = None
                fullDate = None
                partialDate = None
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    item = item.split('|')[1:]
                    for subitem in item:
                        paraname = None
                        easyvalue = None
                        easyname = None
                        value = None
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

                        if len(subitem) is 8 or len(subitem) is 6 or len(subitem) is 4:
                            newmodelyears.append(int(subitem))
                        else:
                            # newItem = []

                            paraname = re.search(r'\((.*?)\)', subitem)
                            subitem = subitem.split('<')[0]
                            # print(subitem)
                            if paraname:
                                # print(subitem)
                                paraname = str(paraname.group(0))[1:-1]
                                value = re.search(r'([0-9]+)', subitem)
                                value = value.group(0)
                                # print(value)
                                try:
                                    newItem  =  {paraname : int(value)}
                                    newmodelyears.append(newItem)
                                except Exception as e:
                                    print(e)
                                    pass
                                # print(newItem)
                            else:
                                try:
                                    if 'http' in subitem:
                                        pass
                                    # if '//' in subitem:
                                    #     print(subitem)
                                    elif ':' in subitem:
                                        easyname = subitem.split(':')[0]
                                        easyvalue = subitem.split(':')[1]
                                        newItem  =  {easyname : int(easyvalue)}
                                        newmodelyears.append(newItem)

                                    elif len(subitem.strip()) is 8 or  len(subitem.strip()) is 6 or len(subitem.strip()) is 4:
                                        newmodelyears.append(int(subitem.strip()))
                                        # print(subitem)
                                    else:
                                        pass

                                        # newmodelyears.append(subitem.strip(')'))
                                except Exception as e:
                                    print(e)
                else:
                    # print(item)
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

                    if type(item) is int:
                        if len(item) is 8 or len(item) is 6 or len(item) is 4:
                            # print(item)
                            newmodelyears.append(int(item))
                        else:
                            item = item.split(' ')[1]
                            newmodelyears.append(int(item))
                            # print(item)
                        # print(item)
                    else:
                        # newItem = []
                        paraname = re.findall(r'\((.*?)\)', item)
                        item = item.split('<')[0]
                        # print(item)

                        if paraname:
                            # paraname = str(paraname.group(0))[1:-1]
                            paraname = str(paraname[0])
                            value = re.findall(r'([0-9]+)', item)
                            if len(value) == 1:
                                # print(value)
                                newItem  =  {paraname : int(value)}
                                newmodelyears.append(newItem)
                            else:
                                starter = False;
                                for subitem in value:
                                    if len(subitem) == 8:
                                        newItem  =  {paraname : int(value)}
                                        newmodelyears.append(newItem)
                                    elif len(subitem) == 4:
                                        if not starter:
                                            firstvalue = subitem
                                            starter = True
                                        else:
                                            secondvalue = subitem
                                            value = int(str(firstvalue)+str(secondvalue))
                                            newItem  =  {paraname : int(value)}
                                            # print(newItem)
                                            newmodelyears.append(newItem)
                                            starter = False;
                                    # else:
                                    #     print(subitem)


                        else:
                            if ':' in item:
                                easyname = item.split(':')[0]
                                easyvalue = item.split(':')[1]
                                try:
                                    newItem  =  {easyname : int(easyvalue)}
                                except Exception as e:
                                    if '{' in item:
                                        easyvalue = easyvalue.split('{{')[0]
                                        newItem  =  {easyname : int(easyvalue)}
                                        newmodelyears.append(newItem)

                                    elif 'May' in item or 'China' in easyname:
                                        easyvalue = re.sub("\D", "", easyvalue)
                                        newItem  =  {easyname : int(easyvalue)}
                                        newmodelyears.append(newItem)

                                    else:
                                        # print(easyname)
                                        newmodelyears.append(int(easyname))
                                # print(newItem)
                            else:
                                item = item.lstrip().rstrip()
                                if len(item) is 8 or  len(item) is 6 or len(item) is 4:
                                    try:
                                        newmodelyears.append(int(item))
                                    except:
                                        print(item)
                                else:
                                    # print(item)
                                    if 'and' in item:
                                        item = item.split('and')
                                        for subitem in item:
                                            newmodelyears.append(int(subitem.strip()))
                                        # continue
                                    elif ',' in item:
                                        if 'produced' in item:
                                            # print(item)
                                            continue
                                        if 'El Camino' in item:
                                            item = item.split(' ')[0]
                                            newmodelyears.append(int(item))
                                            continue
                                        # print(item)
                                        fullDate = re.findall(r'[0-9]{8}', item)
                                        if len(fullDate) > 0:
                                            for subitem in fullDate:
                                                # print(subitem)
                                                if ',' in subitem:
                                                    continue
                                                newmodelyears.append(int(subitem))
                                                # print(subitem)
                                        else:
                                            fullDate = re.findall(r'[0-9]{4}', item)
                                            if len(fullDate) == 1:
                                                newmodelyears.append(int(fullDate[0]))
                                                continue
                                            elif len(fullDate) == 2:
                                                # print(int(str(fullDate[0]) + str(fullDate[1])))
                                                newmodelyears.append(int(str(fullDate[0]) + str(fullDate[1])))
                                                continue
                                            else:
                                                # print(item)
                                                pass

                                    else:
                                        try:
                                            # if 'built' in item or ',' in item:
                                            #     continue
                                            if '{{' in item:
                                                item = item.split('{{')[0]
                                            if len(item) < 4:
                                                # print(item)
                                                continue
                                            if len(re.findall(r'[0-9]',item)) < 1:
                                                # print(item)
                                                continue
                                            # print(item)
                                            fullDate = re.findall(r'[0-9]{8}', item)
                                            if len(fullDate) == 1:
                                                newmodelyears.append(int(fullDate[0]))
                                                continue
                                            # if len(fullDate) > 1:
                                            #     # item = item.split(' ')
                                            #     print(item)

                                            partialDate = re.findall(r'[0-9]{4}', item)
                                            if len(partialDate) == 2:
                                                newmodelyears.append(int(str(partialDate[0])+str(partialDate[1])))
                                            elif len(partialDate) == 1:
                                                newmodelyears.append(int(partialDate[0]))
                                                # print(partialDate)
                                                # if len(item[-1]) == 8:
                                                #     newmodelyears.append(int(item[-1]))
                                                #     continue
                                                # else:
                                                #     print(item)
                                        except Exception as e:
                                            print(e)
                                            print(item)
                                        #     for subitem in fullDate:
                                        #         newmodelyears.append(subitem)
                                        #     continue
                                        # print(item)



            modelyears = newmodelyears
            # print(car['model'])
            # print(modelyears)
            return modelyears
            # cars[make][model][generation] = {'model_years': modelyears}

    except Exception as e:
        pass
        # print(e, 'model_years')
        #
        # # print(item)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

def designerParse(template):
    designer = None
    try:
        designer = str(template.get('designer').value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
        # print(designer)
        if designer:

            # cars[make][model][generation] = {'designer': designer}
            # print(designer)
            char_list = ['\*', '\[', '\]', '\|', '\<br\>', '\<br\/\>', '\n', '\<br \/\>', '\{', '\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']

            designer = re.sub("|".join(char_list), "", designer)
            return designer
    except Exception as e:
        # print('designer error', e)
        pass

def engineParse(template):
    try:
        engine = str(template.get('engine').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if engine:
            char_list = ['\*', '\#', '\[', '\]', '\&nbsp;', '\n', 'unbulleted list','bulleted list','Unbulleted list', 'ubl']
            engine = re.sub("|".join(char_list), '', engine).rstrip('\r\n')
            engine = re.split('<br>|<br/>|<br />', engine)
            newengine = []
            # engine = list(engine.filter(None))
            # engine = list(engine.filter(' '))
            for item in engine:
                # print(item)
                # if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                #     item = item.split(' | ')
                #     for subitem in item:
                #         if 'diesel' in subitem:
                #             print(subitem)
                item = item.split('<')[0]
                item = re.findall(r'\{\{(.*?)\}\}', item)
                # print(item)
                for subitem in item:
                    if 'cid' in subitem or 'Cid' in subitem or 'CID' in subitem or 'cuin' in subitem:
                        if 'convert' in subitem.lower() or 'cvt' in subitem.lower():
                            subitem = subitem.split('|')
                            blanksub = [x for x in subitem if x != '']
                            newsub = [x for x in blanksub if x != None]
                            subitem = [x for x in newsub if x != ' ']

                            # subitem = list(subitem.filter(' '))
                            # print(subitem)
                            # subitem = list(subitem.filter(None))
                            metric = subitem[2]
                            if 'cid' in metric or 'Cid' in metric or 'CID' in metric or 'cuin' in metric:
                                easyvalue = round(float(subitem[1])*0.016387064, 1)
                                # print(easyvalue)
                            elif 'cc' in metric:
                                easyvalue = round(float(subitem[1])*0.001, 1)
                                # print(easyvalue)
                            elif 'L' in metric or 'l' in metric:
                                easyvalue = round(float(subitem[1]), 1)
                                # print(easyvalue)
                            elif '-' in subitem[2]:
                                easyvalue = (subitem[1] + subitem[2])/2
                                # print(easyvalue)
                            else:
                                easyvalue = subitem[2]
                            newengine.append(easyvalue)
                        else:
                            subitem = re.findall(r'([0-9]\.[0-9])', subitem)
                            # subitem = re.findall(r'\d{1}(\.\d{1})', subitem)
                            for subsub in subitem:
                                newengine.append(subsub)
                    else:
                        subitem = re.findall(r'([0-9]\.[0-9])', subitem)
                        # subitem = re.findall(r'\d{1}(\.\d{1})', subitem)
                        for subsub in subitem:
                            newengine.append(subsub)

                        # print(subitem)

                            # if 'metric[3]
                        # else:
                        #     print(subitem)
            # print(engine)

            # cars[make][model][generation] = {'engine': engine}
            return newengine
            # print(engine)
    except Exception as e:
        # print('engine', e)
        pass

def transmissionParse(template):
    try:
        transmission = None
        transmission = str(template.get('transmission').value.lstrip().rstrip().encode('ascii', 'ignore'))

        if transmission:
            newtransmission = []
            char_list = ['\*', '\#', '\[', '\]', '\&nbsp;', '\<br\>', '\<br\/\>', '\n', '\<br \/\>', '\{', '\}', 'unbulleted list','bulleted list','Unbulleted list', 'ubl', 'convert', 'cvt', 'Convert', 'abbr=on']
            transmission = re.sub("|".join(char_list), "", transmission).rstrip('\r\n')
            transmission = transmission.split('|')
            for item in transmission:
                newtransmission.append(item)
            return newtransmission
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
                                        # item = newwheelbase
                                        # print(item)

                                    else:
                                        # print(modelname)
                                        # item = item[0].replace(r'\((.*?\s?.*?\))', '')
                                        item = re.sub(r'\((.*?\s?.*?\))', '', item[0])
                                        modelvalue = item.split(' ')[0]
                                        newItem = {modelname : modelvalue}
                                        newwheelbase.append(newItem)

                # if type(item) is str:
                #     item = re.sub(r'\((.*?\s?.*?\))', '', item)
                #     item = item.split('<')[0]
                #     # print(item)
                #     # item = re.sub(r'\<(.*?\s?.*?)\>', '', item)
                #     item = item.lstrip().split(' ')
                #     if len(item) is 4:
                #         modelname = item[3]
                #         modelvalue = item[0]
                #         if float(modelvalue) > 1000:
                #             modelvalue = round(float(modelvalue)*0.039370, 1)
                #         newItem = {modelname : modelvalue}
                #         newwheelbase.append(newItem)
                #
                #     else:
                #         newItem = item[0]
                #         newwheelbase.append(newItem)


                # print(item)
            # print(newwheelbase)
            return newwheelbase
            # cars[make][model][generation] = {'wheelbase': newwheelbase}

    except Exception as e:
        # print('wheelbase', wheelbase, e)
        pass

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

                # length = newlength
                # print(length)

                return newlength
            # cars[make][model][generation] = {'length': newlength}

    except Exception as e:
        pass
        # print(e, 'length', length)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

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

                # width = newwidth
            return newwidth
            # cars[make][model][generation] = {'width': newwidth}

    except Exception as e:
        pass
        # print(e, 'width', width)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

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

            return newheight

            # print(newheight)

            # cars[make][model][generation] = {'height': newheight}

    except Exception as e:
        pass
        # print(e, 'height', height)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

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
                                    item[1] = item[1].lstrip()
                                    item = list(filter(None, item))
                                    easyvalue = item[1].lstrip().split(' ')
                                    easyvalue = easyvalue[0]
                                    newItem = {easyname:easyvalue}
                                    newweight.append(newItem)
                            else:
                                if '|' in item:
                                    try:
                                        easyname = re.search(r'\((.*?)\)', item)
                                        easyname = easyname.group(1)
                                        easyvalue = item.lstrip().split('|')[1]
                                        if 'kg' in item.split('|')[2]:
                                            easyvalue = int(round(float(easyvalue)/0.45359237))
                                        elif 'lb' in item.split('|')[2]:
                                            pass
                                        else:
                                            easyvalue1 = easyvalue
                                            easyvalue2 = item.split('|')[3]
                                            easyvalue = str(easyvalue1.strip()) + str(easyvalue2.strip())
                                        newItem = {easyname : easyvalue}
                                        newweight.append(newItem)
                                        # print(newItem)

                                    except:
                                        item = item.replace(',', '')
                                        item = item.split('|')
                                        easyvalue = item[1]
                                        if 'kg' in item[2]:
                                            if len(easyvalue) is 8:
                                                easyvalue1 = easyvalue[:4]

                                                easyvalue2 = easyvalue[4:]
                                                # print(easyvalue1,easyvalue2)
                                                easyvalue1 = int(round(float(easyvalue1)/0.45359237))
                                                easyvalue2 = int(round(float(easyvalue2)/0.45359237))
                                                easyvalue = str(easyvalue1) + str(easyvalue2)
                                            else:
                                                easyvalue = int(round(float(easyvalue)/0.45359237))
                                        elif 'lb' in item[2]:
                                            pass
                                        else:
                                            easyvalue1 = item[1]
                                            easyvalue2 = item[3]
                                            easyvalue = str(easyvalue1.strip()) + str(easyvalue2.strip())
                                        newweight.append(easyvalue)
                                        # print(easyvalue)
                                else:
                                    if 'lb' in item:
                                        item = item.split(' ')[0]

                                    # print(weightbackup)
                                    # print(item)
                                    newweight.append(item)

                                # try:
                                #     easyname = re.search(r'\'\'\'(.*?)\'\'\'', item)
                                #     easyname = easyname.group(1)
                                #     easyvalue = item.lstrip().split(' ')[1]
                                #     newItem = {easyname : easyvalue}
                                #     newweight.append(newItem)
                                #     print(newItem)
                                #
                                # except:
                                #     pass


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

                # weight = newweight

            # print(weightbackup)
            # print(newweight)
            # if len(newweight) is 0:
            #     newweight = None
            return newweight
            # cars[make][model][generation] = {'weight': newweight}

    except Exception as e:
        pass
        # print(e, 'weight', weight)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
def imageParse(template):
    try:
        image = str(template.get('image').value.lstrip().rstrip().encode('ascii', 'ignore'))
        imagebackup = str(template.get('image').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if image:
            if ':' in image:
                image = image.split(':')[1]
                image = image.split('|')[0]


            return image
    except Exception as e:
        pass
        # print(e, 'image')
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)

cars = []
for filename in os.listdir(root_path):
    make = str(filename.split('.')[0].encode('ascii', 'ignore'))
    # print(make)
    # cars = []
    if filename.endswith(".xml"):
    # if filename.endswith("esla.xml"):

        with open (root_path + filename, 'r') as vehicles_file:

            make = filename.split('.')[0]
            mainsoup = BeautifulSoup(vehicles_file,features="lxml")
            pages = mainsoup.find_all('page')
            for page in pages:
                try:
                    model = str(page.find('title').get_text().encode('ascii', 'ignore'))
                except e as Exception:
                    print(e)
                # print(title)
                # print(title)
                # cars = []
                texts = page.find_all('text')

                for text in texts:
                    try:
                        wikicode = mwparserfromhell.parse(text.get_text().encode('ascii', 'ignore'))
                        templates = wikicode.filter_templates(recursive = True)


                        for template in templates:

                            # if 'Infobox automobile' or 'Infobox electric' or 'Infobox racing' in template.name:
                            namecheck = ['Infobox automobile', 'Infobox electric', 'Infobox racing']
                            if any(x in template.name for x in namecheck):
                                car = {}
                                manufacturer = None
                                generation = None
                                electric = None
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




                                car['manufacturer'] = manufacturerParse(template)
                                car['make'] = make
                                car['model'] = model
                                car['generation'] = generationParse(template)
                                car['modelyears'] = modelyearsParse(template)
                                # if car['modelyears']:
                                #     if len(car['modelyears']) == 1:
                                #         if type(car['modelyears'][0]) == int:
                                #             car['modelyears'] = car['modelyears'][0]
                                car['image'] = imageParse(template)
                                car['production'] = productionParse(template)
                                car['assembly'] = assemblyParse(template)
                                car['designer'] = designerParse(template)
                                car['class'] = classParse(template)
                                car['bodystlye'] = bodystyleParse(template)
                                car['engine'] = engineParse(template)
                                car['transmission'] = transmissionParse(template)
                                car['wheelbase'] = wheelbaseParse(template)
                                car['length'] = lengthParse(template)
                                car['width'] = widthParse(template)
                                car['height'] = heightParse(template)
                                car['weight'] = weightParse(template)

                                if 'electric' in template.name:
                                    car['electric'] = True
                                else:
                                    car['electric'] = False

                                # print(car['name'])
                                cars.append(car)

                    except Exception as e:
                        print(e)
                        continue

newcars = []

for car in cars:
    newcar = car
    if car['modelyears']:

        newcar['variant'] = None
        for item in car['modelyears']:
            if type(item) == dict:
                # print(item.keys())
                newcar['variant'] = item.keys()
                if type(item.values()) == list:
                    item = int(item.values()[0])
                else:
                    item = int(item.values())
            if type(item) == int:
                if len(str(item)) == 6:
                    if int(str(item)[0:2]) == 19:
                        item = int(str(item)[0:4] + '19' + str(item)[4:])
                    elif int(str(item)[0:2]) == 20:
                        item = int(str(item)[0:4] + '20' + str(item)[4:])

                if len(str(item)) == 8:
                    prod_start = int(str(item)[0:4])
                    prod_end = int(str(item)[4:])
                    while prod_start < prod_end +1:
                        item = prod_start
                        newcar['modelyears'] = item
                        newcars.append(newcar)
                        prod_start += 1
                elif len(str(item)) == 4:
                    newcar['modelyears'] = item
                    newcars.append(newcar)

            else:
                print(item)



#EXPORT_________________________________________
#
dir = ('C:/Users/eufou/Desktop/CARS/parsed')
if not os.path.exists(dir):
    os.mkdir(dir)
#
# for key in myDict:
#     subdir = (dir +"/" + key)
#     if not os.path.exists(subdir):
#         os.mkdir(subdir)
#
def jsonOutput(filename,data):
    if data:
        with open(os.path.join(dir, filename + '.txt'), mode='w') as outfile:
            json.dump(data, outfile)
    else:
        pass


#EXPORT ACTIVITY____________________
#
def exporter():
    jsonOutput('cars', newcars)
    print('ran')

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
#
print(len(newcars))
try:
    exporter()
except Exception as e:
    print(e)
