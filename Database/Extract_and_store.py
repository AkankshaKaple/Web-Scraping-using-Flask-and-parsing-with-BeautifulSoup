from bs4 import BeautifulSoup
from googlesearch import search
import json
from pymongo import MongoClient
from flask import Flask, request, jsonify
from bson import ObjectId

app = Flask(__name__)
client = MongoClient()
db = client.My_Database


# Angel.co
def jobs(html_page, reference_id):
    soup = BeautifulSoup(html_page, features="html.parser")
    current_jobs = soup.findAll(class_='component_e6bd3 expanded_80d76')
    software_jos = [job.text for job in current_jobs if 'Software' in job.text]
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

    for key, val in job_info.items():
        job_info[key]['Reference_id'] = reference_id
        db.Job.insert(job_info[key])
    return job_info


# Angel.co
def details(html_page):
    soup = BeautifulSoup(html_page, features="html.parser")
    detail_info = {'Detail': soup.find_all(class_='description_f92d0')[0].text}

    area_of_interest = []
    for i in soup.find_all(class_='styles_component__3BR-y'):
        area_of_interest.append(i.text)

    detail_info['Area_of_interest'] = area_of_interest
    return detail_info


# Crunch base
def funding(html_page, reference_id):
    soup = BeautifulSoup(html_page, features="html.parser")
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
    print(fund)
    fund['Reference_id'] = reference_id
    db.Funding.insert(fund)
    return fund


# Crunch base
def Founder(html_page, reference_id):
    print(type(html_page))
    soup = BeautifulSoup(html_page, 'html.parser')
    parameters = ['Total Funding Amount', 'Number of Funding Rounds', 'Number of Lead Investors',
                  'Monthly Visits', 'Owler Estimated Revenue', 'Number of Current Team Members']
    keywords = ['Chief', 'Executive', 'Officer', 'Associate', 'President',
                'Technology Evangelist', 'Co-Founder', 'CoFounder', 'Founder']

    info = [i.text for i in soup.findAll(class_='even')]
    print(info)
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
    crunch_base_data['Company_Information']['Reference_id'] = reference_id
    for key, val in crunch_base_data['Founder'].items():
        crunch_base_data['Founder'][key]['Reference_id'] = reference_id
        db.Founder.insert(crunch_base_data['Founder'][key])
    db.Company_Information.insert(crunch_base_data['Company_Information'])
    return "Founders Saved"


# Snov io
def contact_person(domain_name):
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

    # Contact_Person_document
    db.Contact_Person.insert({'First_Name': contact_info['firstName'],
                              'Last_Name': contact_info['lastName'],
                              'Position': contact_info['position'],
                              'LinkedIn_Profile': contact_info['sourcePage'],
                              'Email': contact_info['email'],
                              'Company_Name': contact_info['companyName'],
                              'Website': 'https://www.goniyo.com/',
                              'Reference_id': ''
                              })
    return contact_info


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
    return data_dict


def available_data(data_dict, urls):
    angel = ["Round A", "Round B", "Round c", "Round D", "Seed", "Total_funding", "funding_rounds"]
    crunch_base = ["Area_of_interest", "Founder", "Company_Information"]
    linked_in = ['Employee', 'Location']
    angel_data = {'url': urls['Tech_crunch'], 'data': {}}
    crunch_base_data = {'url': urls['LinkedIn'], 'data': {}}
    linked_in_data = {'url': urls['Angel_co'], 'data': {}}
    dict_2 = {}
    key_list = []

    # combine keys of entire data
    for key in data_dict.keys():
        key_list = key_list + list(data_dict[key])
        dict_2 = {**dict_2, **data_dict[key]}

    for val in key_list:
        if val in angel:
            angel_data['data'][val] = dict_2[val]
        if val in crunch_base:
            crunch_base_data['data'][val] = dict_2[val]
        if val in linked_in:
            linked_in_data['data'][val] = dict_2[val]
    return jsonify(
        {'crunch_base_data': crunch_base_data, 'angel_co_data': angel_data, 'linked_in_data': linked_in_data})


def linkedIn(html_page, reference_id):
    soup = BeautifulSoup(html_page, 'html.parser')

    # overview / description element extracted
    overview_element = soup.find('p')

    # extracting all fields headings
    content_headings = [i.text.strip() for i in
                        soup.find_all('dt', class_='org-page-details__definition-term t-14 t-black t-bold')]

    # extracting all fields descriptions
    content_elements = [i.text.strip() for i in
                        soup.find_all('dd', class_='org-page-details__definition-text t-14 t-black--light t-normal')]

    heading_and_elements = [i.text.strip().replace('\n', '') for i in soup.find_all(class_='overflow-hidden')]

    contents = {'Company_Overview': overview_element.text.strip(), 'reference_id': reference_id}

    data = [i.strip() for i in heading_and_elements[0].split('  ') if i != '']
    for i in range(len(data) - 1):
        if data[i] in content_headings:
            contents[data[i]] = data[i + 1]
    return contents


@app.route('/get_urls', methods=['POST'])
def send_urls():
    company_name = request.form['company_name']
    sites = ['LinkedIn', 'Angel_co', 'Tech_crunch', 'Website']
    urls = {}
    # for site in sites:
    #     query = company_name + site
    #     url_generator = search(query, tld="com", num=1, stop=1, pause=2)
    #     for url in url_generator:
    #         urls[site] = url
    # db.URLs.insert(urls)
    urls = {"LinkedIn": "https://in.linkedin.com/company/niyo-solutions-inc",
            "Angel_co": "https://angel.co/company/niyo-sol/jobs",
            "Tech_crunch": "https://www.crunchbase.com/organization/niyo-solutions",
            "Website": "https://www.goniyo.com/"}

    info = contact_person(urls['Website'])

    print('Check if company data already exists in database')
    # check if table exists in database

    collection = db.collection_names(include_system_collections=False)
    flag = False
    for collect in collection:
        print(collect)
        if 'Company_Data' != collect:
            flag = False
        else:
            flag = True
            break

    if flag:
        print(flag)
        cursor = db.Company_Data.find()
        for cursor_data in cursor:
            # check if company website already exists in database
            if urls['Website'] == cursor_data['Website']:
                data_id = str(cursor_data['_id'])
                print('Company already exists in database')
                # Check if everything is present in the database
                return available_data(print_data(data_id), urls)
            else:
                print('Company does not exist in database')
                return available_data({}, urls)
    else:
        print(flag)
        return available_data({}, urls)


@app.route('/upload-file', methods=['POST'])
def read_file():
    # global contact_info, reference_id
    global doc
    reference_id = ''
    contact_info = {}
    key = request.form['key']
    html_page = request.files['html_data'].read().decode("utf-8")
    website = request.form['website']
    key = key.split('$')[1]

    cursor = db.Company_Data.find({'Website': website})
    for document in cursor:
        reference_id = str(document['_id'])

    if key == 'angel_co_funding':
        funding(html_page, reference_id)
        return "Funding Saved"

    elif key == 'angel_co_jobs':
        jobs(html_page, reference_id)
        return "Jobs Saved"

    elif key == 'angel_co_main':
        cursor = db.Contact_Person.find({'Website': website})
        for data in cursor:
            print("data : ", data)
            contact_info = data
        company_info_ac = details(html_page)
        db.Company_Data.insert({'Website': website,
                                "Company_Name": contact_info['Company_Name'],
                                'Area_of_interest': company_info_ac['Area_of_interest'],
                                'Company size': '',
                                'Headquarters': '',
                                'Founded': ''
                                })
        cursor = db.Company_Data.find({'Website': website})
        for c in cursor:
            document = c
            document['_id'] = str(document['_id'])

        db.Contact_Person.update({"Website": website},
                                 {"$set": {
                                     "Reference id": document['_id']
                                 }})
        return jsonify(document)

    # elif key == 'angel_co_people':
    #     print('aa')
    #     return "people"

    elif key == 'crunch_base':
        Founder(html_page, reference_id)
        return "Founders Saved"

    elif key == 'linkedin_about':
        linkedIn_content = linkedIn(html_page, reference_id)
        db.Company_Data.update({"_id": ObjectId(reference_id)},
                               {"$set": {
                                   "Company size": linkedIn_content["Company size"],
                                   "Headquarters": linkedIn_content['Headquarters'],
                                   "Founded": linkedIn_content['Founded']
                               }})

        cursor = db.Company_Data.find({"_id": ObjectId(reference_id)})
        for doc in cursor:
            doc['Reference_id'] = reference_id
            doc['_id'] = str(doc['_id'])
        return jsonify(doc)

    else:
        return "Oops, Input Valid Page"


if __name__ == '__main__':
    app.run(debug=True)
