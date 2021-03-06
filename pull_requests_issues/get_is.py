import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from dateutil.parser import parse
import csv

global flag

def get_pull_requests(kind ,url, page):
    global flag
    rest = "/"+kind+"?page="+ page +"&q=is%3Aissue+is%3Aclosed+closed%3A2019-10-30..2020-04-30"
    URL = url + rest

    print(URL)

    page = requests.get(URL.strip())
    page = page.content
    soup = BeautifulSoup(page, 'html.parser')
    issues = soup.find_all('div', class_="flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2")

    print(len(issues))

    if len(issues) < 25:
        flag = 0
    for issue in issues:

        meta_data = issue.find('relative-time')
        issue_link = issue.find_all('a', class_='link-gray-dark v-align-middle no-underline h4 js-navigation-open')

        for link in issue_link:
            time.sleep(2)
            try:
                if 'issue' in link['id']:
                    print("\n===========================\nIn a link")
                    href = link['href']
                    href = 'https://github.com'+href
                    print(href)
                    get_deeper(kind, href, meta_data['datetime'][:10]);
            except:
                pass

def get_deeper(kind, href, close_date):



    global flag
    global f1w
    global f2w
    global objects1
    global objects2


    if pre_process_date(close_date) < r1:
        print("Out of range")
        flag = 0

    if pre_process_date(close_date) > r4:
        print("Out of range")


    page = requests.get(href)
    page = page.content
    soup = BeautifulSoup(page, 'html.parser')
    participants = soup.find('div', class_="participation")
    title = soup.find('span', class_="js-issue-title")
    labels = soup.find('div', class_="labels")
    status = soup.find('span', class_="State")

    if status == None:
        status = "Status: Not-Set"

    # print(status)


    try:
        new_status = str(status['title']).strip().split(' ')[-1]
    except:
        new_status = "Not-Set"

    print("Status:",new_status)

    # comment_tab = ''


    comment_tab = soup.find('div',"TableObject-item TableObject-item--primary")
    comment_tab = soup.find('relative-time')
    comment_tab = comment_tab['datetime']
        
        
    print("ri: ----> ",comment_tab)

    open_date = pre_process_date(comment_tab)




    print("Range:",open_date, pre_process_date(close_date))

    file_changed = ''
    lines_added = ''
    lines_removed = ''

    try:
        file_changed = soup.find(id="files_tab_counter")
    except:
        files_changed = 'N/A'

    try:
        lines_added = soup.find('span', class_="text-green")
    except:
        lines_added = 'N/A'

    try:
        lines_removed = soup.find('span', class_="text-red")
    except:
        lines_removed = 'N/A'

    object_tuple = []

    if kind == "pulls":
        open_date = pre_process_date(close_date)
        time.sleep(2)
        print('In Pulls\n')
        try:
            file_changed = file_changed.text.strip()
            lines_added = lines_added.text.strip()
            lines_removed = lines_removed.text.strip()
        except:
            file_changed = '0'
            lines_added = '0'
            lines_removed = '0'
            # print('date')

        object_tuple = [title.text.strip(), labels.text.strip(), \
                        get_num(participants.text),\
                        pre_process_date(close_date).strftime('%d-%b-%Y'), \
                        file_changed, lines_added, lines_removed,\
                        new_status]



        object_tuple = [str(i) for i in object_tuple]

        try:
            print(open_date >= r4)
        except:
            print("Cant Compare Dates")

        if (open_date <= r4):
            print('Range: 1 \n -----------')
            objects1.append(object_tuple)
            print(len(objects1))
            print('Title:',title.text.strip())
            print('Labels:',labels.text.strip())
            print('Participants:',get_num(participants.text))
            print("Closed:",pre_process_date(close_date).strftime('%d-%b-%Y'))
            print('file_changed:',file_changed)
            print('lines_added:',lines_added)
            print('lines_deleted:',lines_removed)
            print(str(status['title']).strip().split(' ')[-1])
            print('\n')



    if kind == "issues":

        time.sleep(2)
        comment_tab = soup.find('div',"TableObject-item TableObject-item--primary")
        print('In Issues\n=============')
        print(title.text.strip())

        labels = soup.find('div', class_="labels css-truncate js-issue-labels")
        labels = labels.text.strip().replace('\n', ' ')
        print("labels:", labels)
        print(get_num(participants.text))
        print(open_date.strftime('%d-%b-%Y'))
        print(pre_process_date(close_date).strftime('%d-%b-%Y'))
        print(comment_tab.text.strip().split('\n')[-1].split(' ')[1].strip())
        print(new_status)

        object_tuple = [title.text.strip(), labels, \
                        get_num(participants.text), open_date.strftime('%d-%b-%Y'),\
                        pre_process_date(close_date).strftime('%d-%b-%Y'), \
                        comment_tab.text.strip().split('\n')[-1].split(' ')[1].strip(),\
                        new_status]


        object_tuple = [str(i) for i in object_tuple]

        open_date = pre_process_date(open_date.strftime('%d-%b-%Y'))
        # print("here --> ")
        # print(open_date, r4)
        # print(type(open_date), type(r4))

        try:
            print(open_date >= r4)
        except:
            print("Cant Compare Dates")

        if (open_date >= r1 and open_date <= r2) or (open_date >= r3 and open_date <= r4):
            print('Range: 1 \n -----------')
            objects1.append(object_tuple)
            print(len(objects1))
            print('Title:',title.text.strip())
            print('Labels:',labels)
            print('Participants:',get_num(participants.text))
            print('Opened:',open_date.strftime('%d-%b-%Y'))
            print("Closed:",pre_process_date(close_date).strftime('%d-%b-%Y'))
            print('Comments:',comment_tab.text.strip().split('\n')[-1].split(' ')[1].strip())
            print(str(status['title']).strip().split(' ')[-1])
            print('\n')


        print("End")

    print("End of one request \n+++++++++++++++++++++++++")




def pre_process_date(date):
        return parse(date, fuzzy=True)

def get_num(string):
    return string.strip().split(' ')[0].replace(' ','')

def get_name(string):
    return string.split('/')[-1].strip()

def driver(type_of):
    print("Starting for "+type_of+"\n=====================")

    global flag

    repos = open('list').readlines()
    for repo in repos:

        print("Starting for Repo "+repo+"\n=====================")

        name = get_name(repo)

        global f1
        global f2

        global f1w
        global f2w

        global objects1
        global objects2

        objects1 = []
        objects2 = []

        if type_of == 'pulls':
            dat = ['Title', 'Labels', 'Participants', 'Close_date', 'files_changed', 'lines_added','lines_deleted','Status']
        elif type_of == 'issues':
            dat = ['Title', 'Labels', 'Participants', 'Open_date', 'Close_date', 'Comments', 'Status']

        flag = 1
        print(flag)
        for page in range(1,100):
            if flag == 1:
                print("page_changed_to",page)
                get_pull_requests(type_of,repo,str(page))
                time.sleep(2)
            else:
                break

        with open('data/'+name+'_'+type_of+'_'+str(r1.strftime('%b-%d-%Y')) + '_' + str(r2.strftime('%b-%d-%Y')) + '.csv', 'w', newline='') as csvfile:
            f1w = csv.writer(csvfile)
            f1w.writerow(dat)
            for k in objects1:
                f1w.writerow(k)

        with open('data/'+name+'_'+type_of+'_'+str(r3.strftime('%b-%d-%Y')) + '_' + str(r4.strftime('%b-%d-%Y')) + '.csv', 'w', newline='') as csvfile:
            f2w = csv.writer(csvfile)
            f2w.writerow(dat)
            for k in objects2:
                f2w.writerow(k)

    print('Terminating ... ')

r1 = pre_process_date("2019,Nov,1")
r2 = pre_process_date("2020,Jan,31")

r3 = pre_process_date("2020,Feb,1")
r4 = pre_process_date("2020,May,18")

driver("pulls")
# driver("issues")
