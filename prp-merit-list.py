'''

THIS IS JUST THE DATA FETCHED FROM PRP API ENDPOINT
AS LONG AS IT ALLOWS

I WILL KEEP ON MAKING MERIT LISTS | GAZAT DOCS REAL QUICK

AND UPLOADING THEM TO GOOGLE DRIVE or HERE ON GITHUB



---------------------------

I GOT HOLD OF API ENDPOINT BY CHANCE

--------------------------


Please use original links | give proper credits if u use them 



'''


import requests
from json import dump,load
from docx import Document
import re
from time import sleep
from os.path import exists
from os import getcwd, mkdir

TYPE_PROGRAM =  {
        'fcps': 1,
        'ms': 2,
        'md': 3,
        'mds' : 4, 
        'fcpsd': 5
    }



def get_merit_by_type(program_name: str, page: int):

    '''
    
    Gets a merit page of program [program_name]
    

    args
    -------

    program_name: fcps, ms, md, mds, fcpsd
    page: 1---
    
    '''
   

    url = 'http://prp.phf.gop.pk/MeritGazat/MeritGetAllByTypeView'    
    r = requests.post(url, params={
        'pageNum': int(page),
        'top': 20,
        'typeId': TYPE_PROGRAM[program_name],
        'search': ''
    },
    headers= {
        'Referer': 'https://prp.phf.gop.pk/phftt/merit/list-'+program_name,
        'origin': 'https://prp.phf.gop.pk',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'content-type' : 'application/json; charset=utf-8'
    })
    print(r.headers)
    return r.json()


def save_file(data: list, filename: str):
    '''
    saves data [list] to filename

    args
    -----

    data: data got from gazat or merit
    filename: filename

    '''
    doc = Document()

    columns_ = []
    for i in data[0].keys():
        key_ = re.split('(?=[A-Z])', i)
        key_title = ' '.join([_.title() for _ in key_])
        columns_.append(key_title)

   
    number_of_columns = len(list(data[0].keys()))
    number_of_rows = len(data)
    # add a table to the end and create a reference variable
    # extra row is so we can add the header row
    table = doc.add_table(rows=number_of_rows+1,cols=number_of_columns)
    heading = table.rows[0]
    for i in list(range(len(columns_))):
        heading.cells[i].text = columns_[i]

    
    table_cells = table._cells
    for i in range(1, number_of_rows+1,1):
        
        row_cells = table_cells[i*number_of_columns:(i+1)*number_of_columns]
        print(row_cells)
        text_ = [str(c) for c in list(data[i-1].values())]
        for c, t in enumerate(row_cells):
            t.text =  text_[c]
        print(row_cells)
    doc.save(filename+'.docx')


def get_whole_merit(program_name: str):
    '''
    
    Gets a whole merit of program [program_name]
    

    args
    -------

    program_name: fcps, ms, md, mds, fcpsd   
    
    '''

    data = []
    page = 1
    curr_data = get_merit_by_type(program_name, page)
    while len(curr_data) != 0:
        data += curr_data
        page += 1
        sleep(2)
        curr_data = get_merit_by_type(program_name, page)

    return data



def get_gazat_by_type(program_name: str, page: int):

    '''
    
    Gets a gazat page of program [program_name]
    of page [page]

    args
    -------

    program_name: fcps, ms, md, mds, fcpsd
    page: 1----

    '''



    url = f'http://prp.phf.gop.pk/MeritGazat/GazatGetAllByTypeView'

    r = requests.post(url, params={
        'pageNum': int(page),
        'top': 20,
        'typeId': int(TYPE_PROGRAM[program_name]),
        'search': ''
    },
    headers= {
        'Referer': 'http://prp.phf.gop.pk/MeritGazat/Gazat'+program_name.upper(),
        'origin': 'https://prp.phf.gop.pk',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    },
    verify=False)
    return r.json()


def get_whole_gazat(program_name: str):
    '''
    
    Gets a whole gazat page of program [program_name]
    

    args
    -------

    program_name: fcps, ms, md, mds, fcpsd
   
    
    '''
    data = []
    page = 1
    curr_data = get_gazat_by_type(program_name, page)
    while len(curr_data) != 0:
        data += curr_data
        page += 1
        curr_data = get_gazat_by_type(program_name, page)
    return data

def save_stats(year: str, month:str, merit_list: str):
    '''
    save stats.md in the folder merit/year/month/
    '''
    Text = f'### {month} {year}\n'
    Text += '| Program  |  Speciality  | Highest | Lowest |  \n| ------ | ------ | ------ | ------ |\n'
    if exists('merit_stats.json'):
        with open('merit_stats.json', 'r') as f:
            data = load(f)
        for prog in data:
            percs = data[prog]
            for sub in percs:
                print(percs[sub])
                Text += f'| {prog.upper()} | {sub} | {max(percs[sub])} | {min(percs[sub])}| \n'
    check_path(f'merit/{year}/{month}/{merit_list}/')
    with open(f'merit/{year}/{month}/{merit_list}/stats.md', 'w') as f:
        f.write(Text)

def check_path(path: str):
    '''
    creates the path if not exists
    '''
    
    path_splitted = path.split('/')
    path_base = getcwd()

    for i in range(len(path_splitted)):

        path_ = path_base +'/'+'/'.join(path_splitted[:i+1])
        print('checking path if exists', path_)
        if not exists(path_):
            print('creating directory', path_.split('/')[-1], 'root directory: ', '[', path_base, ']')
            mkdir(path_)

''''

These small lines save whole gazat of all programs


'''


def get_all_merits():
    '''
    saves all merit list to documents and stats in merit_stats.json
    '''
    data_perc = {}

    programs = ['fcps', 'ms', 'md', 'mds', 'fcpsd']
    for program in programs:
        data = get_whole_merit(program)
        for item in data:
            if program not in data_perc:
                data_perc[program] = {}
            if item['specialityName'] not in data_perc[program]:
                data_perc[program][item['specialityName']] = []
            data_perc[program][item['specialityName']].append(item['marks'])
        save_file(data, program)

    with open('merit_stats.json', 'w') as f:
        dump(data_perc, f, indent=1)


save_stats('2022', 'july', 'first')