from bs4 import BeautifulSoup
from googlesearch import search
import json
from pymongo import MongoClient
from flask import Flask
import requests
from bson import ObjectId

app = Flask(__name__)
client = MongoClient()
db = client.F_Database
Company_Name = 'Niyo Solutions'
HTMLs = ['funding.html', 'jobs.html', 'linkedin.html', 'main.html',
         'people.html', 'crunch_base.html']

html_data = {}
for html in HTMLs:
    with open('HTML-file/niyo/' + html, 'r') as file:
        data = file.read()
    html_data[html.replace('.html', '')] = data

print(html_data.keys())


# @app.route('/get_html', methonds=['POST'])
# def get_html():
#


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    soup = BeautifulSoup(html_data['jobs'], features="html.parser")
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
    soup = BeautifulSoup(html_data['main'], features="html.parser")
    dict_1 = {'Detail': soup.find_all(class_='description_f92d0')[0].text}

    area_of_interest = []
    for i in soup.find_all(class_='styles_component__3BR-y'):
        area_of_interest.append(i.text)

    dict_1['Area_of_interest'] = area_of_interest
    detail_info = json.dumps(dict_1)
    return detail_info


@app.route('/funding', methods=['GET', 'POST'])
def funding():
    soup = BeautifulSoup(html_data['funding'], features="html.parser")
    fund = {'Total_funding': soup.find(class_='component_43375').text.split(' ')[0].replace('Funding', '')[:-1],
            'funding_rounds': soup.find(class_='component_43375').text.split(' ')[0].replace('Funding', '')[
                              -1:]}

    round_info = soup.findAll(class_='amountRaised_3c2b1')
    round_info.reverse()
    round_list = ['Seed', 'A', 'B', 'C', 'D']
    j = 0
    for i in round_info:
        if round_list[j] == 'Seed':
            fund[round_list[j]] = i.text
            j += 1
        else:
            fund['Round ' + round_list[j]] = i.text
            j += 1

    return fund


@app.route('/crunch_base', methods=['GET', 'POST'])
def crunch_base():
    soup = BeautifulSoup(html_data['crunch_base'], features="html.parser")
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
    crunch_base_data = {'Founder': founder, 'Company_Information': Company_Information}
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


@app.route('/print_data/<data_id>', methods=['POST', 'GET'])
def print_data(data_id):
    print('Print data')
    Company_Name_by_document = ''
    cursor_1 = db.Company_Data.find({'_id': ObjectId(data_id)})
    for data_1 in cursor_1:
        Company_Name_by_document = data_1['Company_Name']

    print(Company_Name_by_document)

    ref_id = ''
    data_dict = {}
    # Company_Data
    cursor = db.Company_Data.find({'Company_Name': Company_Name_by_document})
    for data in cursor:
        ref_id = data['_id']
        # print(type(ref_id), type(data['_id']))
        # print(ref_id, data['_id'])
        data['_id'] = str(data['_id'])
        data_dict['Company_Data'] = data
        break


    # Company_Information
    cursor = db.Company_Information.find({'Reference_id': str(ref_id)})
    for data in cursor:
        print(type(ref_id), type(data['_id']))
        data['_id'] = str(data['_id'])
        data_dict['Company_Information'] = data
        break

    # Contact_Person
    cursor = db.Contact_Person.find({'Reference_id': str(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_dict['Contact_Person'] = data
        break

    # Founder
    cursor = db.Founder.find({'Reference_id': str(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_dict['Founder'] = data
        break

    # Funding
    cursor = db.Funding.find({'Reference_id': str(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_dict['Funding'] = data
        break

    # Jobs
    cursor = db.Company_Information.find({'Reference_id': str(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_dict['Company_Information'] = data
        break

    # URLs
    cursor = db.URLs.find({'Reference_id': str(ref_id)})
    for data in cursor:
        data['_id'] = str(data['_id'])
        data_dict['URLs'] = data
        break
    print(data_dict)
    return json.dumps(data_dict)


@app.route('/get_urls', methods=['GET', 'POST'])
def get_urls():
    sites = ['LinkedIn', 'Angel_co', 'Tech_crunch', 'Website']
    urls = {}
    for site in sites:
        query = Company_Name + site
        url_generator = search(query, tld="com", num=1, stop=1, pause=2)
        for url in url_generator:
            urls[site] = url
    return json.dumps(urls)


@app.route('/database', methods=['GET', 'POST'])
def database():
    # Get URLs of related to company
    res = requests.get('http://127.0.0.1:5000/get_urls')
    urls = json.loads(res.text)

    print('Check if company data already exists in database')
    cursor = db.Company_Data.find()
    for data in cursor:
        print(Company_Name.lower())
        # check if company website already exists in database
        if urls['Website'] == data['Website']:
            data_id = str(data['_id'])
            print('Company already exists in database')
            res = requests.get('http://127.0.0.1:5000/print_data/'+data_id)
            return json.loads(res.text)
        else:
            print('Company does not exist in database')

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
    cursor = db.Company_Data.find({'Company_Name': contact_info['companyName']})
    reference_id = ''
    for data in cursor:
        reference_id = str(data['_id'])
        break

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
    res = requests.get('http://127.0.0.1:5000/print_data' + reference_id)
    return json.loads(res.text)


if __name__ == '__main__':
    app.run(debug=True)
