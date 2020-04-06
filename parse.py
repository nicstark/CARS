import os
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import os.path
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
                cars[manufacturer][model][generation] = {'production': production}
            elif all(len(flag) == 8 for flag in production):
                cars[manufacturer][model][generation] = {'production': production}
            elif len(production) == 1 and all(len(flag) == 4 for flag in production):
                cars[manufacturer][model][generation] = {'production': production}

            else:
                print(productionbackup)
                print(production)

    except Exception as e:
        print('function', e , '\n', production)
        return


for filename in os.listdir(root_path):
    manufacturer = str(filename.split('.')[0].encode('ascii', 'ignore'))
    # print(manufacturer)
    cars[manufacturer] = {}
    if filename.endswith(".xml"):

        with open (root_path + filename, 'r') as vehicles_file:


            mainsoup = BeautifulSoup(vehicles_file,features="lxml")
            #page = soup.find_all('page')
            pages = mainsoup.find_all('page')
            for page in pages:
                model = str(page.find('title').get_text().encode('ascii', 'ignore'))
                # print(title)
                # print(title)
                cars[manufacturer][model] = {}
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
                                try:
                                    generation = str(template.get("name").value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
                                except Exception as e:
                                    continue

                                productionParse(template)

                                try:
                                    assembly = str(template.get('assembly').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    if assembly:
                                        cars[manufacturer][model][generation] = {'assembly': assembly}
                                        # print(assembly)
                                except Exception as e:
                                    continue

                                try:
                                    designer = str(template.get('designer').value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
                                    if designer:
                                        cars[manufacturer][model][generation] = {'designer': designer}
                                except Exception as e:
                                    continue

                                try:
                                    engine = str(template.get('engine').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    if engine:
                                        engine = re.sub("|".join(char_list), "", engine).rstrip('\r\n')
                                        cars[manufacturer][model][generation] = {'engine': engine}
                                        # print(engine)
                                except Exception as e:
                                    continue

                                try:
                                    transmission = str(template.get('transmission').value.lstrip().rstrip().encode('ascii', 'ignore'))

                                    if transmission:
                                        transmission = re.sub("|".join(char_list), "", transmission).rstrip('\r\n')
                                        cars[manufacturer][model][generation] = {'transmission': transmission}
                                        # print(transmission)
                                except Exception as e:
                                    continue

                                try:
                                    wheelbase = str(template.get('wheelbase').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    # print(wheelbase)
                                    if wheelbase:
                                        # print(wheelbase)
                                        check = ['convert','Convert']
                                        if any(x in wheelbase for x in check):
                                            # print(wheelbase + '\n')
                                            wheelbase = wheelbase.split('|')
                                            if 'mm' in wheelbase[2]:
                                                wheelbase[1] = round(float(wheelbase[1])*0.039370, 1)
                                            wheelbase = wheelbase[1]
                                            # wheelbase = re.sub("|".join(char_list), "", wheelbase).rstrip('\r\n')
                                        else:
                                            wheelbase = wheelbase.split('&')[0]
                                        if bool(re.match('[a-zA-Z]', wheelbase)):
                                            wheelbase = wheelbase.split(' ')[1]
                                        if wheelbase < 40:
                                            wheelbase = None
                                            continue
                                        cars[manufacturer][model][generation] = {'wheelbase': wheelbase}
                                        # print(wheelbase)

                                except Exception as e:
                                    continue

                                try:
                                    length = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    lengthbackup = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                    if length:
                                        length = re.search('(\d)(\d)(\d)?(\.\d*)?', length)
                                        length = length.group(0)
                                        if float(length) > 300:
                                            length = re.search(r'\((.*?)\)', lengthbackup)
                                            length = length.group(0).split(' ')[0][1]
                                        cars[manufacturer][model][generation] = {'length': length}

                                except Exception as e:
                                    # print(e, manufacturer, model, length)
                                    # print(lengthbackup)
                                    continue

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

                                                cars[manufacturer][model][generation] = {'width': width}
                                                continue
                                            width = re.search('(\d)(\d)(\d)?(\d)?(\.\d*)?', str(width))
                                            width = width.group(0)
                                            if float(width) > 1000:
                                                width = round(float(width)*0.039370, 1)

                                        cars[manufacturer][model][generation] = {'width': width}

                                except Exception as e:
                                    # print(e, manufacturer, model, width)
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
