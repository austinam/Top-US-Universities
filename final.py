###FINAL PROJECT

import requests
import json
from bs4 import BeautifulSoup
import csv
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3


#start cache
CACHE_FNAME = 'cache_final_proj.json'
try:
    with open(CACHE_FNAME, 'r') as f:
        cache = f.read()
        CACHE_DICTION = json.loads(cache)
        f.close()
except:
    CACHE_DICTION = {}

def unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = unique_key(url)
    if unique_ident in CACHE_DICTION:
        #print('retrieving cache')
        return CACHE_DICTION[unique_ident]
    else:
        #print('writing cache')
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

class College():
    def __init__(self, rank, name, location, accept_rate, enroll, ratio, burl_tuition=None, burl_earnings=None):
        #print(burl_tuition)
        #print(burl_earnings)
        self.rank = rank
        self.name = name
        self.location = location
        self.accept_rate = accept_rate
        self.enroll = enroll
        self.ratio = ratio
        self.burl_tuition = burl_tuition
        self.burl_earnings = burl_earnings

        site_req1 = make_request_using_cache(self.burl_tuition)
        cost_soup = BeautifulSoup(site_req1, 'html.parser')
        sticker_block = cost_soup.find(class_="block--two-two", id="sticker-price")
        prices = sticker_block.find_all('div', class_="scalar__value")
        pr_comma = prices[0].text
        lst_pr = pr_comma.split('/')
        just_price = lst_pr[0]
        split_symbol = just_price.split(',')
        in_w_symb = split_symbol[0] + split_symbol[1]
        self.price_in = in_w_symb[1:]
        pr_comma2 = prices[1].text
        lst_pr2 = pr_comma2.split('/')
        just_price2 = lst_pr2[0]
        split_symbol2 = just_price2.split(',')
        out_w_symb = split_symbol2[0] + split_symbol2[1]
        self.price_out = out_w_symb[1:]

        site_req2 = make_request_using_cache(self.burl_earnings)
        earnings_soup = BeautifulSoup(site_req2, 'html.parser')
        earnings_block = earnings_soup.find(class_='block--two-two', id="earnings")
        earnings = earnings_block.find('div', class_='scalar__value').text
        lst_earn = earnings.split('/')
        earn_first = lst_earn[0]
        earn_split = earn_first.split(',')
        with_symb = earn_split[0] + earn_split[1]
        self.median_2_yr_earn = with_symb[1:]

    def str_for_csv(self):
        return "{},{},{},{},{},{},{},{},{}\n".format(str(self.rank), self.name, self.location, self.accept_rate, self.price_in, self.price_out, self.enroll, self.median_2_yr_earn, self.ratio)

    def __str__(self):
        #try:
        return "({}) {}, {}\nAcceptance Rate: {}\nIn-state Tuition: {}\nOut-of-state Tuition: {}\nUndergraduate Enrollment:{}\nMedian Earnings 2 Years Post Graduation: {}\nStudent to Faculty Ratio: {}".format(self.rank, self.name, self.location, self.accept_rate, self.price_in, self.price_out, self.enroll, self.median_2_yr_earn, self.ratio)
            #return "({}) {}, {}\nAcceptance Rate: {}".format(self.rank, self.name, self.location, self.price_in)
        #except:
            #return "failure"

def get_data():
    lst_schools = []
    rank_ = 0
    for i in range(1,7):
        baseurl = 'https://www.niche.com/colleges/search/best-colleges/?page={}'.format(i)
        info = make_request_using_cache(baseurl)
        soup = BeautifulSoup(info, 'html.parser')
        lst1 = soup.find_all('div', class_='card__inner')
        new_url = soup.find_all('a', class_='search-result__link')
        #delete sponsored colleges
        del(new_url[9])
        del(new_url[17])
        for url in new_url:
            rank_ += 1
            #url_list.append(url['href'])
            school_url = url['href']
            new_req = make_request_using_cache(school_url)
            new_soup = BeautifulSoup(new_req, 'html.parser')

            #acceptance rate ------
            accept_rate = new_soup.find_all('div', class_='scalar__value')
            acp_lst = []
            for thing in accept_rate:
                if '%' in thing.find('span').text:
                    acp_lst.append(thing.text)
            acp_rate = acp_lst[0]

            #name of school -----
            name_info = new_soup.find('a', class_='entity-name__link')
            school_name = name_info.text

            #location of school ----
            loc_info = new_soup.find_all('span', class_="bare-value")
            location_school_comma = loc_info[0].text
            lst_split_loc = location_school_comma.split(',')
            location_school = lst_split_loc[0] + ' ' + lst_split_loc[1]

            #school ranking ----
            #go in numerical order on site
            school_rank = rank_

            #undergraduate enrollement -----
            enroll_info = new_soup.find(class_="block--two", id='students')
            undergrad_enroll = enroll_info.find('div', class_="scalar__value")
            enroll_num = undergrad_enroll.find('span')
            underg_e_comma = enroll_num.text
            try:
                enroll_split = underg_e_comma.split(',')
                undergraduate_enrollment = enroll_split[0] + enroll_split[1]
            except:
                undergraduate_enrollment = underg_e_comma

            #student:faculty ----
            faculty_info = new_soup.find(class_='block--two-poll', id='academics')
            fac_stud = faculty_info.find('div', class_='scalar__value')
            student_fac_ratio_symb = fac_stud.text
            split_ratio = student_fac_ratio_symb.split(':')
            student_fac_ratio = split_ratio[0]

            #tuition link ----
            url_find = new_soup.find(class_="block--two", id='cost')
            cost_link = url_find.find('a', class_='expansion-link__text')['href']

            #earnings link ----
            url_find2 = new_soup.find(class_="block--horiz-poll", id='after')
            earnings_link = url_find2.find('a', class_='expansion-link__text')['href']

            #utilize class:
            college_info = College(school_rank, school_name, location_school, acp_rate, undergraduate_enrollment, student_fac_ratio, cost_link, earnings_link)
            lst_schools.append(college_info)
    return lst_schools


def load_school_data():
    sch_data = get_data()
    with open('college_data.csv', 'w') as f:
        f.write('Rank, Name, Location, Acceptance Rate, In-state Tuition, Out-of-State Tuition, Enrollment-undergrad, Median Income-2 years, Student:Faculty\n')
        for school in sch_data:
            dta = school.str_for_csv()
            f.write(dta)
    f.close()

#CREAT SECOND CSV WITH REGION DATA
def create_region_csv():
    region_lst = ['West', 'Midwest', 'Northeast', 'South']
    northeast_st = ["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"]
    midwest_st = ["IL", "IN", "MI", "OH", "WI", "IA", "KS", "MN", "MS", "NE", "ND",  "SD", "MO"]
    west_st = ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY", "AK", "CA", "HI", "OR", "WA"]
    south_st = ["AL", "AR", "DC", "DE", "FL", "GA", "KY", "LA",  "MD", "NC",  "OK", "SC", "TN", "TX",  "VA",  "WV"]


    with open('regions.csv', 'w') as f:
        f.write('State Name, State Region\n')
        for state in northeast_st:
            north_lst = ''
            north_lst += state
            north_lst += ', northeast\n'
            f.write(north_lst)
        for state in midwest_st:
            mid_lst = ''
            mid_lst += state
            mid_lst += ', midwest\n'
            f.write(mid_lst)
        for state in west_st:
            west_lst = ''
            west_lst += state
            west_lst += ', west\n'
            f.write(west_lst)
        for state in south_st:
            south_lst = ''
            south_lst += state
            south_lst += ', south\n'
            f.write(south_lst)
    f.close()


database = 'colleges.sqlite'
schools_csv = 'college_data.csv'
regions_csv = 'regions.csv'

try:
    conn = sqlite3.connect(database)
    cur = conn.cursor()
except Exception as e:
    print(e)

def create_region_table(csv_file):
    statement_drop = "DROP TABLE IF EXISTS 'Regions';"
    cur.execute(statement_drop)
    conn.commit()

    st_create_regions = '''
    CREATE TABLE 'Regions' (
    'State' TEXT PRIMARY KEY,
    'Region' TEXT NOT NULL
    );
    '''
    cur.execute(st_create_regions)
    conn.commit()

    region_file = open(csv_file, 'r')
    csvr = csv.reader(region_file)
    csv_lst = list(csvr)
    del(csv_lst[0])
    for row in csv_lst:
        insertion = (row[0], row[1])
        statement_insert = 'INSERT INTO "Regions" '
        statement_insert += 'VALUES (?, ?)'
        cur.execute(statement_insert, insertion)

    conn.commit()

def create_colleges(csv_file):
    statement_drop = "DROP TABLE IF EXISTS 'Colleges';"
    cur.execute(statement_drop)
    conn.commit()

    st_create_colleges = '''
    CREATE TABLE 'Colleges' (
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Rank' INTEGER NOT NULL,
    'Name' TEXT NOT NULL,
    'Location' TEXT NOT NULL,
    'State' TEXT,
    'Acceptance' TEXT NOT NULL,
    'In_State_Tuition' INTEGER NOT NULL,
    'Out_of_State_Tuition' INTEGER NOT NULL,
    'Enrollment' INTEGER NOT NULL,
    'Median_Income_2years' INTEGER NOT NULL,
    'Number_Students_per_FacultyMember' INTEGER NOT NULL,
    FOREIGN KEY (State) REFERENCES Regions(State)
    );
    '''
    cur.execute(st_create_colleges)
    conn.commit()

    college_file = open(csv_file, 'r')
    csvr = csv.reader(college_file)
    csv_lst = list(csvr)
    del(csv_lst[0])
    for row in csv_lst:
        insertion = (row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[6].strip(), row[7].strip(), row[8].strip())
        statement_insert = 'INSERT INTO "Colleges" '
        statement_insert += 'VALUES (NULL, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement_insert, insertion)

    conn.commit()

#add_region_table(regions_csv)

def foreign_key():
    lst = []
    select = 'SELECT Location FROM Colleges'
    cur.execute(select)
    for row in cur:
        x = row[0]
        splt = x.split()
        if len(splt) == 2:
            lst.append(splt[1])
        elif len(splt) == 3:
            lst.append(splt[2])
        elif len(splt) == 4:
            lst.append(splt[3])

    lst1 = []
    select1 = 'SELECT Id FROM Colleges'
    cur.execute(select1)
    for row in cur:
        x = row[0]
        lst1.append(x)


    new_lst = list(zip(lst, lst1))

    lst2 = []
    select2 = 'SELECT Region FROM Regions WHERE State = ?'
    for item in lst:
        cur.execute(select2, [item])
        for row in cur:
            lst2.append(row[0])

    new_l = list(zip(new_lst, lst2))

    for thing in new_l:
        update = 'UPDATE Colleges SET State = ? WHERE Id = ?'
        id_ = thing[0][1]
        st = thing[0][0].strip()
        cur.execute(update, (st,id_,))

    conn.commit()

#Logic for user commands ----

def command_by_region(input1):
    #stmt = 'SELECT Region, COUNT(Name) FROM (SELECT Region, Name FROM Colleges LIMIT ?) GROUP BY Region'
    stmt = 'SELECT t.Region, COUNT(t.Name) FROM (SELECT r.Region, c.Name FROM Colleges as c JOIN Regions as r ON c.State = r.State LIMIT ?) as t GROUP BY t.Region'
    limit = input1
    out = cur.execute(stmt, [limit])
    output = cur.fetchall()

    label_lst = []
    for thing in output:
        label_lst.append(thing[0])
    values_lst = []
    for thng in output:
        num = int(thng[1])
        values_lst.append(num)
    labels = label_lst
    values = values_lst

    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='pie_chart_regions')

    #return out.fetchall()

#print(command_by_region('5'))

def command_tuition(input1, input2):
    limit = input1
    column = ''
    if input2 == 'in':
        column = 'In_State_Tuition'
    elif input2 == 'out':
        column = 'Out_of_State_Tuition'
    stmt = 'SELECT Rank, '
    stmt += column
    stmt += ' FROM Colleges LIMIT '
    stmt += limit

    out = cur.execute(stmt)
    output = cur.fetchall()

    x_rank_lst = []
    y_tuition_lst = []
    for thing in output:
        x_rank_lst.append(thing[0])
        y_tuition_lst.append(thing[1])

    x_axis = x_rank_lst
    y_axis = y_tuition_lst

    trace = go.Scatter(
        x = x_axis,
        y = y_axis,
        mode = 'markers'
    )

    data = [trace]
    #print(data)
    py.plot(data, filename='scatter-tution')

    # return out.fetchall()

#command_tuition('15', 'in')

def command_acp_rate(input1):
    stmt = 'SELECT Rank, Acceptance FROM Colleges LIMIT ?'
    limit = input1
    out = cur.execute(stmt, [limit])
    output = cur.fetchall()

    x_rank_lst = []
    y_acpt_lst = []
    for thing in output:
        x_rank_lst.append(thing[0])
        strp = thing[1].strip('%')
        y_acpt_lst.append(strp)

    x_axis = x_rank_lst
    y_axis = y_acpt_lst

    trace = go.Scatter(
        x = x_axis,
        y = y_axis
    )

    data = [trace]

    py.plot(data, filename='line-acceptance')


#command_acp_rate('10')

def command_enrollment(input1):
    stmt = 'SELECT Name, Enrollment FROM Colleges LIMIT ?'
    limit = input1
    out = cur.execute(stmt, [limit])
    output = cur.fetchall()

    x_rank_lst = []
    y_enroll_lst = []
    for thing in output:
        x_rank_lst.append(thing[0])
        y_enroll_lst.append(thing[1])

    x_axis = x_rank_lst
    y_axis = y_enroll_lst

    trace = go.Scatter(
        x = x_axis,
        y = y_axis,
        mode = 'markers'
    )

    data = [trace]
    py.plot(data, filename='scatter-enrollment')

#command_enrollment('9')

def command_earnings(input1):
    stmt = 'SELECT Name, Median_Income_2years FROM Colleges LIMIT ?'
    limit = input1
    out = cur.execute(stmt, [limit])
    output = cur.fetchall()

    x_rank_lst = []
    y_earning_lst = []
    for thing in output:
        x_rank_lst.append(thing[0])
        y_earning_lst.append(thing[1])

    x_axis = x_rank_lst
    y_axis = y_earning_lst

    trace = go.Scatter(
        x = x_axis,
        y = y_axis,
        mode = 'markers'
    )

    data = [trace]
    py.plot(data, filename='scatter-earnings')

#print(command_earnings('4'))

def command_ratio(input1):
    stmt = 'SELECT Name, Number_Students_per_FacultyMember FROM Colleges LIMIT ?'
    limit = input1
    out = cur.execute(stmt, [limit])
    output = out.fetchall()

    x_list = []
    y_list = []
    for thing in output:
        x_list.append(thing[0])
        y_list.append(thing[1])

    data = [go.Bar(
            x = x_list,
            y = y_list
    )]

    py.plot(data, filename='basic-bar')

#print(command_ratio('50'))

def process_command(command1, command2, command3):
    if command2.lower() == 'regions':
        return command_by_region(command1)
    if command2.lower() == 'tuition':
        second_input = command3
        return command_tuition(command1, second_input)
    if command2.lower() == 'acceptance':
        return command_acp_rate(command1)
    if command2.lower() == 'enrollment':
        return command_enrollment(command1)
    if command2.lower() == 'student:faculty':
        return command_ratio(command1)
    if command2.lower() == 'income':
        return command_earnings(command1)
    conn.close()

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response3 = ''
        badcommand = False
        response1 = input('Enter the number of schools that you would like to search for: ')
        if response1.lower() == 'help':
            print(help_text)
            continue
        elif response1 == '':
            continue
        elif response1.lower() == 'exit':
            break
        elif response1.isdigit() == False:
            badcommand = True
        else:
            response1 = response1.lower()
        response2 = input('Enter what information you would like to see: ')
        if response2.lower() == 'tuition':
            response3 = input('Enter "in" for in-state tuition, "out" for out of state tuition: ')
        elif response2.lower() == 'help':
            print(help_text)
            continue
        elif response2 == '':
            continue
        elif response2.lower() == 'exit':
            break
        elif response2.lower() not in ['regions', 'tuition', 'acceptance', 'enrollement', 'student:faculty', 'income']:
            badcommand = True
        else:
            response2 = response2.lower()
        if badcommand == True:
            print('bad input, see help.txt for help')
            continue
        else:
            x = process_command(response1, response2, response3)
            continue


if __name__=="__main__":
    #get_data()
    #load_school_data()
    #create_region_csv()
    #create_region_table(regions_csv)
    #create_colleges(schools_csv)
    #foreign_key()
    interactive()
