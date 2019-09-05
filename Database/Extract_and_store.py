from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import os
import json
from pymongo import MongoClient
from flask import Flask, render_template
import requests
from bson import ObjectId

app = Flask(__name__)
client = MongoClient()
db = client.Database_new
Company_Name_by_user = 'Niyo Solutions'
# objectId = ObjectId()


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    with open('HTML-file/niyo/jobs.html', 'r') as file:
        data = file.read()
    soup = BeautifulSoup(data, features="html.parser")
    jobs = soup.findAll(class_='component_e6bd3 expanded_80d76')
    software_jos = [job.text for job in jobs if 'Software' in job.text]
    job_info = {}
    for index in range(len(software_jos)):
        Jobs = {}
        job = software_jos[index]
        job = job.replace('Software Engineering', '').replace('₹', '***').replace('•', '***').replace('%Apply now', '')
        job = job.split('***')
        ch = list(job[0])
        for i in range(1, len(ch)):
            if (('a' <= ch[i] <= 'z') or (ch[i] == ')')) and ('A' <= ch[i + 1] <= 'Z'):
                Jobs['Title'] = job[0][:i + 1]
                Jobs['Location'] = job[0][i + 1:]
                break

        Jobs['Salary'] = job[1] + job[2]
        job_info['Job_' + str(index)] = Jobs

    return job_info


@app.route('/company_details', methods=['GET', 'POST'])
def company_details():
    with open('HTML-file/niyo/main.html', 'r') as file:
        data = file.read()
    soup = BeautifulSoup(data, features="html.parser")
    dict_1 = {}
    dict_1['Detail'] = soup.find_all(class_='description_f92d0')[0].text

    area_of_interest = []
    for i in soup.find_all(class_='styles_component__3BR-y'):
        area_of_interest.append(i.text)

    dict_1['Area_of_interest'] = area_of_interest
    detail_info = json.dumps(dict_1)
    return detail_info


@app.route('/funding', methods=['GET', 'POST'])
def funding():
    with open('HTML-file/niyo/funding.html', 'r') as file:
        data = file.read()
    soup = BeautifulSoup(data, features="html.parser")
    funding = {'Total_funding': soup.find(class_='component_43375').text.split(' ')[0].replace('Funding', '')[:-1],
               'funding_rounds': soup.find(class_='component_43375').text.split(' ')[0].replace('Funding', '')[
               -1:]}

    round_info = soup.findAll(class_='amountRaised_3c2b1')
    round_info.reverse()
    round_list = ['Seed', 'A', 'B', 'C', 'D']
    j = 0
    for i in round_info:
        if round_list[j] == 'Seed':
            funding[round_list[j]] = i.text
            j += 1
        else:
            funding['Round ' + round_list[j]] = i.text
            j += 1

    return funding


# def founders(soup):
#     data = [i.text for i in soup.findAll(class_='__halo_textContrast_dark_AAAA')]
#     founders = data[data.index('Founders') + 1: data.index('Team')]
#     return founders


@app.route('/crunch_base', methods=['GET', 'POST'])
def crunch_base():
    with open('HTML-file/NiYO Solutions _ Crunchbase.html', 'r') as file:
        data = file.read()
    soup = BeautifulSoup(data, features="html.parser")
    parameters = ['Total Funding Amount', 'Number of Funding Rounds', 'Number of Lead Investors',
                  'Monthly Visits', 'Owler Estimated Revenue', 'Number of Current Team Members']
    keywords = ['Chief', 'Executive', 'Officer', 'Associate', 'President',
                'Technology Evangelist', 'Co-Founder', 'CoFounder', 'Founder']

    info = [i.text for i in soup.findAll(class_='even')]
    Company_Information = {}
    founder = {}
    index = 0
    for i in info:
        data = i.strip().split('\xa0')
        value = data[-1]
        key = i.replace(value, '').replace('\xa0', '')
        if key in parameters:
            Company_Information[key] = value

        for keyword in keywords:
            f = {}
            if keyword.lower() in i.lower():
                value = i.strip().split(' ')
                name = value[0] + " " + value[1]
                f['Name'] = name
                f['Position'] = i.replace(name, '')
                founder['Founder_' + str(index)] = f
                index += 1
                break

    crunch_base_data = {}
    crunch_base_data['Founder'] = founder
    crunch_base_data['Company_Information'] = Company_Information
    crunch_base_data = json.dumps(crunch_base_data)
    return crunch_base_data


@app.route('/get_domain_search', methods=['GET', 'POST'])
def get_domain_search():
    contact_info = {'domain': 'https://www.goniyo.com/',
                    'webmail': False,
                    'result': 1,
                    'limit': 1,
                    'offset': 0,
                    'companyName': 'Niyo Solutions Inc.',
                    'emails': [{'email': 'vinay@goniyo.com',
                                'type': 'prospect',
                                'status': 'verified',
                                'firstName': 'Vinay',
                                'lastName': 'Bagri',
                                'position': 'CEO and Co-founder',
                                'sourcePage': 'https://www.linkedin.com/in/vinayniyo/'}],
                    'email': 'vinay@goniyo.com',
                    'type': 'prospect',
                    'status': 'verified',
                    'firstName': 'Vinay',
                    'lastName': 'Bagri',
                    'position': 'CEO and Co-founder',
                    'sourcePage': 'https://www.linkedin.com/in/vinayniyo/'}
    return contact_info

@app.route('/print_data', methods=['POST', 'GET'])
def print_data():
    Company_Name_by_document = ''
    cursor_1 = db.Company_Data.find()
    for data_1 in cursor_1:
        if Company_Name_by_user.lower() in data_1['Company_Name'].lower():
            Company_Name_by_document = data_1['Company_Name']
    cursor = db.Company_Data.find({'Company_Name': Company_Name_by_document})
    data_list = []
    data_list_1 = []
    data_list_2 = []
    data_list_3 = []
    data_list_4 = []
    data_list_5 = []
    data_list_6 = []
    data_list_7 = []
    ref_id = ''

    # Company_Data
    for data in cursor:
        ref_id = data['_id']
        data['_id'] = str(data['_id'])
        data_list_1.append(data)
    data_list.append(data_list_1)
    print(data_list)

    print('Company_Data')

    # Company_Information
    cursor = db.Company_Information.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_2.append(data)
        print("data_list_2 : ", data_list_2)
    data_list.append(data_list_2)
    print('Company_Information')

    # Contact_Person
    cursor = db.Contact_Person.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_3.append(data)
    data_list.append(data_list_3)
    print('Contact_Person')

    # Founder
    cursor = db.Founder.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_4.append(data)
    data_list.append(data_list_4)
    print('Founder')

    # Funding
    cursor = db.Funding.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_5.append(data)
    data_list.append(data_list_5)
    print('Funding')

    # Jobs
    cursor = db.Company_Information.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_6.append(data)
    data_list.append(data_list_6)

    print('Jobs')

    # URLs
    cursor = db.URLs.find({'_id': ObjectId(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_list_7.append(data)
    data_list.append(data_list_7)
    print('URLs')
    return json.dumps(data_list)


@app.route('/check_existing', methods=['POST', 'GET'])
def check_existing():
    print('Entered')
    cursor_1 = db.Company_Data.find()
    for data_1 in cursor_1:
        if Company_Name_by_user.lower() in data_1['Company_Name'].lower():
            res = requests.get('http://127.0.0.1:5000/print_data')
            return json.loads(res.text)


@app.route('/get_urls', methods=['GET', 'POST'])
def get_urls():
    Company_Name = ''

    if 'Database_new' not in db.collection_names():
        print('No Such Collection')
    else:
        res = requests.get('http://127.0.0.1:5000/check_existing')
        Company_Name = json.loads(res.text)

    print(Company_Name)
    sites = ['LinkedIn', 'Angel_co', 'Tech_crunch', Company_Name]
    urls = {}
    for site in sites:
        query = Company_Name + site
        url_generator = search(query, tld="com", num=1, stop=1, pause=2)
        for url in url_generator:
            if site == Company_Name:
                urls['Website'] = url
                break
            urls[site] = url

    # Contact_person
    res = requests.get('http://127.0.0.1:5000/get_domain_search')
    contact_info = json.loads(res.text)

    # Company_detail
    res = requests.get('http://127.0.0.1:5000/company_details')
    company_info_ac = json.loads(res.text)

    # Company_Data
    db.Company_Data.insert({'Website': urls['Website'],
                            "Company_Name": contact_info['companyName'],
                            'Area_of_interest': company_info_ac['Area_of_interest'],
                            })

    # Get primary key for the document
    cursor = db.Company_Data.find({'_id': contact_info['companyName']})
    reference_id = ''
    for data in cursor:
        reference_id = str(data['_id'])

    # urls_document
    urls['Reference_id'] = reference_id
    db.URLs.insert(urls)

    # Contact_Person_document
    db.Contact_Person.insert({'First_Name': contact_info['firstName'],
                              'Last_Name': contact_info['lastName'],
                              'Position': contact_info['position'],
                              'LinkedIn_Profile': contact_info['sourcePage'],
                              'Email': contact_info['email'],
                              'Reference_id': reference_id
                              })

    # Jobs_document
    res = requests.get('http://127.0.0.1:5000/jobs')
    job = json.loads(res.text)
    job['Reference_id'] = reference_id
    db.Jobs.insert(job)

    # Founders_document and Comp_info_document
    res = requests.get('http://127.0.0.1:5000/crunch_base')
    crunch_base_data = json.loads(res.text)
    crunch_base_data['Founder']['Reference_id'] = reference_id
    crunch_base_data['Company_Information']['Reference_id'] = reference_id
    db.Founder.insert(crunch_base_data['Founder'])
    db.Company_Information.insert(crunch_base_data['Company_Information'])

    # funding_document
    res = requests.get('http://127.0.0.1:5000/funding')
    funding = json.loads(res.text)
    funding['Reference_id'] = reference_id
    db.Funding.insert(funding)
    print('Printing')
    res = requests.get('http://127.0.0.1:5000/print_data')
    return json.loads(res.text)

if __name__ == '__main__':
    app.run(debug=True)
