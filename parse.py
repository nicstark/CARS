import os
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

def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

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
        # print(wheelbase)
        if wheelbase:
            wheelbase = re.split('<br>|<br/>|<br />', wheelbase)
            for item in wheelbase:
                if 'ubl ' in item or 'list' in item or '{ubl' in item or 'unbulleted' in item:
                    newwheelbase = []
                    item = re.split(r'(\s\|\s)', item)

                    if len(item) is 1:
                        item = re.split(r'(\|\{)', item[0])
                        # print(item)
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

                    item = newwheelbase
                elif '|' in str(item):
                    item = re.split('\|', item)
                    if ':' in item[0]:
                        item[0] = re.split(':', item[0])[0]
                        newItem = {}
                        if float(item[1]) > 1000:
                            item[1] = round(float(item[1])*0.039370, 1)
                        newItem[item[0]] = item[1]
                        item = newItem
                    elif '}}' in item[-1]:
                        modelindicator = re.search(r'\((.*?)\)', item[-1])
                        if modelindicator:
                            modelindicator = str(modelindicator.group(0))[1:-1]
                            newItem = {}
                            item[1] = item[1].split('-')[0]
                            if float(item[1]) > 1000:
                                item[1] = round(float(item[1])*0.039370, 1)
                            newItem[modelindicator] = item[1]
                            item = newItem
                        else:
                            if float(item[1]) > 1000:
                                item[1] = round(float(item[1])*0.039370, 1)
                            item = item[1]
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
                        item = {modelname : modelvalue}
                    else:
                        if '(' in item:
                            parans = re.search(r'\((.*?)\)', item)
                            # print(parans.groups())
                            for paran in parans.groups():
                                if 'mm' in paran:
                                    pass
                                else:
                                    modelname = str(paran)
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
                                            # print(newItem)
                                        item = newwheelbase
                                    else:
                                        modelvalue = item[0].split(' ')[1]
                                        item = {modelname : modelvalue}
                        # else:
            print(item)
                        # print(item)
                            # if float(item[1]) > 1000:
                            #     item[1] = round(float(item)*0.039370, 1)
                        # print(item)

                    # elif 'vert' in item[0] or 'cvt' in item[0]:
                    #     item = item[1].split('-')[0]
                    #     if float(item) > 1000:
                    #         item = round(float(item)*0.039370, 1)
                    #
                    # else:
                    #     pass
                # else:
                #     if ':' in item:
                #         print(item)



            # print(wheelbase)
            #     item = item.split(':')
            #     # if item
            #     # item = {item[0]:item[1]}
            #     if len(item) == 3 or len(item) == 5:
            #         print(item)
            # char_list = ['<br>| <br/> | <br />']
            # manufacturer = re.sub("|".join(char_list), " ", manufacturer)
            # check = ['convert','Convert', 'cvt']
            # if any(x in wheelbase for x in check):
            #     # print(wheelbase + '\n')
            #     wheelbase = wheelbase.split('|')
            #     if 'mm' in wheelbase[2]:
            #         wheelbase[1] = round(float(wheelbase[1])*0.039370, 1)
            #     wheelbase = wheelbase[1]
            #     # wheelbase = re.sub("|".join(char_list), "", wheelbase).rstrip('\r\n')
            # else:
            #     wheelbase = wheelbase.split('&')[0]
            # if bool(re.match('[a-zA-Z]', wheelbase)):
            #     wheelbase = wheelbase.split(' ')[1]
            # if wheelbase < 40:
            #     wheelbase = None
                # continue
            cars[make][model][generation] = {'wheelbase': wheelbase}
            # print(wheelbase)

    except Exception as e:
        print('wheelbase', wheelbase, e)


def lengthParse(template):
    try:
        length = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
        lengthbackup = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
        if length:
            length = re.search('(\d)(\d)(\d)?(\.\d*)?', length)
            length = length.group(0)
            if float(length) > 300:
                length = re.search(r'\((.*?)\)', lengthbackup)
                length = length.group(0).split(' ')[0][1]
            cars[make][model][generation] = {'length': length}

    except Exception as e:
        print(e, make, model, length)
        # print(lengthbackup)


for filename in os.listdir(root_path):
    make = str(filename.split('.')[0].encode('ascii', 'ignore'))
    # print(make)
    cars[make] = {}
    if filename.endswith(".xml"):

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


                                generationParse(template)

                                productionParse(template)

                                assemblyParse(template)

                                manufacturerParse(template)

                                designerParse(template)

                                engineParse(template)

                                transmissionParse(template)

                                wheelbaseParse(template)

                                try:
                                    width = str(template.get('width').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    widthbackup = str(template.get('width').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    if width:

                                        width = re.search('(\d)(\d)(\d)?(\.\d*)?', width)
                                        width = width.group(0)

                                        if float(width) > 100:
                                            try:
                                                width = widthbackup.split('{{')[1]
                                                if 'ubl' in width:
                                                    width = widthbackup.split('{{')[3]
                                            except:
                                                width = widthbackup.split(' ')[1]
                                            try:
                                                width = width.split('|')[1]
                                            except:

                                                cars[make][model][generation] = {'width': width}
                                                continue
                                            width = re.search('(\d)(\d)(\d)?(\d)?(\.\d*)?', str(width))
                                            width = width.group(0)
                                            if float(width) > 1000:
                                                width = round(float(width)*0.039370, 1)

                                        cars[make][model][generation] = {'width': width}

                                except Exception as e:
                                    # print(e, make, model, width)
                                    # print(widthbackup)
                                    continue


                    except Exception as e:
                        # print(e)
                        continue
                    # root = etree.fromstring(str(text))
                    # for bits in root:

                    # print(etree.tostring(root))
                    # print(type(root[0]))
                    # print(len(root))


                    # cleantext = text.get_text().encode('ascii', 'ignore')
                    # lines = cleantext.split('Infobox')
                    # for line in lines:
                    #     try:
                    #         # print(re.split('name=' or 'name =', lines)[1])
                    #         # print(lines[1].split('name')[1])
                    #         if 'ref name' in line:
                    #             fix = line.split('ref name')
                    #             for fixline in fix:
                    #                 if 'name =' in fixline:
                    #                     fixline = fixline.split('name =')[1].lstrip()[:200]
                    #                     newline= fixline.split('|')[0]
                    #                     print(newline)
                    #                 else:
                    #                     fixline = fixline.split('name=')[1].lstrip()[:200]
                    #                     newline= fixline.split('|')[0]
                    #                     print(newline)
                    #         else:
                    #             for line in fix:
                    #                 if 'name =' in line:
                    #                     line = line.split('name =')[1].lstrip()[:200]
                    #                     newline= line.split('|')[0]
                    #                     print(newline)
                    #                 else:
                    #                     line = line.split('name=')[1].lstrip()[:200]
                    #                     newline= line.split('|')[0]
                    #                     print(newline)
                    #     except Exception as e:
                    #             # print(e)
                    #             continue
                    # regex = re.compile('\|(.*?)\|')
                    # lines = re.findall(regex, cleantext)
                    # print(lines[0], lines[1])
                    # for line in lines[1:]:
                    #     print(line.split('|')[0].lstrip()[2:])
                    # if "name =" in cleantext:
                    #     find_between(cleantext "name = ", )
                    #     print(line)
                #reg = r'\[^{\{]'
                #result = [m.start() for m in re.finditer(texts[0].get_text(), 'Infobox')]

                #result = [(i, cleantext[i:i+2]) for i in findall(start, cleantext)]
                #regex = re.compile('Infobox (.*?) \}\}')
                # regex = re.compile('Infobox(.*?)\|')
                # regex = re.compile('\{\{Infobox(.*?)\}\}')
                # regex = re.compile('name(.*?)\|')
                # result = re.findall(regex, cleantext)
                # print(result)
                #print(result)

                # for text in texts:
                #     cleantext= text.get_text().encode('ascii', 'ignore')
                #     try:
                #         # result = re.search('{{Infobox automobile(.*)}}', text)
                #         # print(result.group(1))
                #         #result = re.search(r'\{\{\Infobox automobile(.*)\}\}', cleantext).group(1)
                #         #result = text.partition('[')[-1].rpartition(']')[0]
                #         #result = find_between(cleantext, start, end)
                #         result = [m.start() for m in re.finditer(cleantext, start)]
                #         print(result)
                #
                #     except Exception as e:
                #         print("Phone ", e)
                #         continue
                # wikitables = page.find_all(".wikitable")
                # print(right_table)
                # for entry in page:
                #     titles = entry.find_all('title')
                #     # for title in titles:
                #         # print(title
                #     text = entry.find('text')
                    #autobox = text.find_all('')
                    # test = text.find_all(string = "Tesla")
                    # if len(test) > 0:

                    # s = 'asdf=5;iwantthis123jasd'
                    # result = re.search('{{(.*)}}', s)
                    # print(result.group(1))



                    # test = text[text.find("{{")+1:myString.find("}}")]
                    # print(test)



                # currentvehicles = soup.find_all('title')
                # for vehicle in currentvehicles:
                #     vehicles.append(vehicle.get_text().encode('ascii', 'ignore'))
                    # print(vehicle.get_text().encode('ascii', 'ignore'))
                # date = soup.find('abbr')
                # date = date.get('title')
                # b = datetime.strptime(date[:-10], "%Y-%m-%dT%X")
                # milliDate = unix_time_millis(b)
                # phone_object['Date'] = int(milliDate)
                # if title[:14] == "Placed call to":
                #     phone_object['Type'] = "Placed"
                #     title = title.split("to")
                #
                #     try:
                #         phone_object['Person'] = title[1][1:]
                #         duration = soup.find('abbr', 'duration').get_text()
                #         b = datetime.strptime("1970,1,1," + duration[1:-1], "%Y,%m,%d,%X")
                #         milliBegin = unix_time_millis(b)
                #         phone_object['Duration'] = int(milliBegin)
                #
                #     except:
                #         print ("error: ", filename)

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
