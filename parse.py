import os
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import os.path
from lxml import etree
import re
import pandas as pd
from io import StringIO, BytesIO
import mwparserfromhell

myDict = {}

root_path = "C:/Users/eufou/Desktop/CARS/"


# def checkDupes(check,against,key):
#     for x in against:
#         if check == x[key]:
#             return True
cars = {};

def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

# def findall(p, s):
#     i = s.find(p)
#     while i != -1:
#         yield i
#         i = s.find(p, i+1)

def fileParse():
    for filename in os.listdir(root_path):
        manufacturer = str(filename.split('.')[0].encode('ascii', 'ignore'))
        # print(manufacturer)
        cars[manufacturer] = {}
        if filename.endswith("Buick.xml"):

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

                                if 'Infobox' in template.name:
                                    generation = None
                                    production = None
                                    designer= None
                                    engine= None
                                    engines= None
                                    transmission= None
                                    transmissions= None
                                    assembly = None
                                    char_list = ['\[', '\]', '\&nbsp\;L', '\/\>', '\}', '\{', 'unbulleted list', '\&nbsp\;'];
                                    try:
                                        generation = str(template.get("name").value.lstrip().split('<')[0].rstrip().encode('ascii', 'ignore'))
                                    except Exception as e:
                                        continue
                                    try:
                                        production = str(template.get('production').value.lstrip().rstrip().encode('ascii', 'ignore'))
                                        if production:
                                            cars[manufacturer][model][generation] = {'production': production}
                                    except Exception as e:
                                        continue
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

                                        if wheelbase:
                                            wheelbase = re.sub("|".join(char_list), "", wheelbase).rstrip('\r\n')
                                            cars[manufacturer][model][generation] = {'wheelbase': wheelbase}
                                            print(wheelbase)
                                    except Exception as e:
                                        continue
                                    try:
                                        length = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))

                                        if length:
                                            length = re.sub("|".join(char_list), "", length).rstrip('\r\n')
                                            cars[manufacturer][model][generation] = {'length': length}
                                            # print(transmission)
                                    except Exception as e:
                                        continue
                                    try:
                                        length = str(template.get('length').value.lstrip().rstrip().encode('ascii', 'ignore'))

                                        if length:
                                            length = re.sub("|".join(char_list), "", length).rstrip('\r\n')
                                            cars[manufacturer][model][generation] = {'length': length}
                                            # print(transmission)
                                    except Exception as e:
                                        continue


                        except Exception as e:
                            print(e)
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

dir = ('C:/Users/eufou/Desktop/CARS/parsed')
if not os.path.exists(dir):
    os.mkdir(dir)

for key in myDict:
    subdir = (dir +"/" + key)
    if not os.path.exists(subdir):
        os.mkdir(subdir)

def jsonOutput(subdir,filename,data):
    if data:
        with open(os.path.join(dir + subdir, filename + '.txt'), mode='w') as outfile:
            json.dump(data, outfile)
    else:
        pass


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


fileParse()
# print(cars)
# print(vehicles)

# exporter()
