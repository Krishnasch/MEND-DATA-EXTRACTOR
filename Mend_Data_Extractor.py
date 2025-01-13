import warnings
from idlelib.tooltip import Hovertip
from tkinter import *
import requests
from tkinter import messagebox as msg_box
import csv
warnings.filterwarnings('ignore')

def get_all_products(mend_url, org_id, user_key):
    data = {
        "requestType": "getAllProducts",
        "userKey": f"{user_key}",
        "orgToken": f"{org_id}"
    }
    headers = {'Content-type': 'application/json'}
    all_product_response = requests.post(mend_url, json=data, headers=headers, verify=False)
    return all_product_response


def get_tags_by_product(mend_url, product, user_key):
    data = {
        "requestType": "getProductTags",
        "userKey": f"{user_key}",
        "productToken": f"{product}"
    }
    headers = {'Content-type': 'application/json'}
    product_tags_response = requests.post(mend_url, json=data, headers=headers, verify=False)
    return product_tags_response


def get_all_projects(mend_url, project, user_key):
    data = {
        "requestType": "getAllProjects",
        "userKey": f"{user_key}",
        "productToken": f"{project}"
    }
    headers = {'Content-type': 'application/json'}
    all_project_response = requests.post(mend_url, json=data, headers=headers, verify=False)
    print(all_project_response.json())
    return all_project_response

def get_alerts_by_project(mend_url, project, user_key):
    data = {
        "requestType": "getProjectAlerts",
        "userKey": f"{user_key}",
        "projectToken": f"{project}"
    }
    headers = {'Content-type': 'application/json'}
    project_alerts_response = requests.post(mend_url, json=data, headers=headers, verify=False)
    return project_alerts_response

def get_all_projects_by_token(md_url, product, user_key):
    data = {
        "requestType": "getAllProjects",
        "userKey": f"{user_key}",
        "productToken": f"{product['productToken']}"
    }
    headers = {'Content-type': 'application/json'}
    all_project_response = requests.post(md_url, json=data, headers=headers, verify=False)
    return all_project_response


root = Tk()
root.title("MEND API")
mend_pic = PhotoImage(file = 'mend_logo_light.png')
root.iconphoto(False, mend_pic)
root.geometry("1340x1080")

label = Label(root, text="MEND API", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8,rowspan=2,padx=50,pady=40)
exit_button = Button(root, text="Exit", padx=5, pady=5,font=('Arial', 15), command=root.destroy)

url = StringVar()
prod_token = StringVar()
user_token = StringVar()
org_token = StringVar()
proj_token = StringVar()
local_path_token = StringVar()

def get_product():
    md_url = url.get()
    user = user_token.get()
    org_id = org_token.get()
    if md_url == '' or user == '' or org_id == '':
        msg_box.showerror("Error", "Please provide SERVER URL, ORGANIZATION TOKEN and USER TOKEN")
        return True
    my_label.config(text="")
    my_response.delete(1.0, END)
    response = get_all_products(md_url, org_id, user)
    product_count = 0
    for product in response.json()['products']:
        product_count = product_count + 1
        name = product['productName']
        token = product['productToken']
        my_response.insert(END, name + "(Token:"+  token +")\n")
    print(product_count)
    my_label.config(text="Total Product Count(s):"+str(product_count))
    prod_token.set('')
    org_token.set('')
    user_token.set('')

def get_project():
    pd_token = prod_token.get()
    md_url = url.get()
    user = user_token.get()
    if md_url == '' or user == '':
        msg_box.showerror("Error", "Please provide SERVER URL, USER TOKEN and PRODUCT TOKEN")
        return True
    my_label.config(text="")
    my_response.delete(1.0, END)
    response = get_all_projects(md_url, pd_token, user)
    product_count = 0
    for product in response.json()['projects']:
        product_count = product_count + 1
        name = product['projectName']
        token = product['projectToken']
        my_response.insert(END,"Project Name:"+ name + " Project Token:"+ token + "\n")
    print(product_count)
    my_label.config(text="Total Project Count(s): "+str(product_count))
    prod_token.set('')
    org_token.set('')
    user_token.set('')

def get_product_tags():
    pd_token = prod_token.get()
    md_url = url.get()
    user = user_token.get()
    if md_url == '' or user == '':
        msg_box.showerror("Error", "Please provide SERVER URL, USER TOKEN and PRODUCT TOKEN")
        return True
    my_label.config(text="")
    my_response.delete(1.0, END)
    response = get_tags_by_product(md_url, pd_token, user)
    for product_tags in response.json()['productTags']:
        trx_id = ''
        snow_app_id = ''
        fortify_id = ''
        if 'tags' in product_tags:
            if 'Trouxid' in product_tags['tags']:
                trx_id = product_tags['tags']['Trouxid'][0]
            if 'SNOW_APP_ID' in product_tags['tags']:
                snow_app_id = product_tags['tags']['SNOW_APP_ID'][0]
            if 'fortifyappid' in product_tags['tags']:
                fortify_id = product_tags['tags']['fortifyappid'][0]
        my_response.insert(END,"Trouxid:"+ trx_id + " SNOW_APP_ID:"+  snow_app_id + " fortifyappid:"+  fortify_id + "\n")
        prod_token.set('')
        org_token.set('')
        user_token.set('')

def get_vul_count():
    cri_count = 0
    hig_count = 0
    med_count = 0
    lw_count = 0
    pj_token = proj_token.get()
    md_url = url.get()
    user = user_token.get()
    if md_url == '' or user == '':
        msg_box.showerror("Error", "Please provide SERVER URL, USER TOKEN and PROJECT TOKEN")
        return True
    my_label.config(text="")
    my_response.delete(1.0, END)
    project_alerts_response = get_alerts_by_project(md_url, pj_token, user)

    for alerts in project_alerts_response.json()['alerts']:
        if 'vulnerability' in alerts:
            if alerts['vulnerability']['severity'] == 'critical':
                cri_count = cri_count + 1
            elif alerts['vulnerability']['severity'] == 'high':
                hig_count = hig_count + 1
            elif alerts['vulnerability']['severity'] == 'medium':
                med_count = med_count + 1
            elif alerts['vulnerability']['severity'] == 'low':
                lw_count = lw_count + 1
    my_response.insert(END, "Critical:" + str(cri_count) + "\n" + "High:" + str(hig_count) + "\n" + "Medium:" + str(med_count) + "\n" + "Low:" + str(lw_count))
    prod_token.set('')
    org_token.set('')
    user_token.set('')

def get_all_details():
    og_token = org_token.get()
    md_url = url.get()
    user = user_token.get()
    local_path = local_path_token.get()
    if md_url == '' or user == '':
        msg_box.showerror("Error", "Please provide SERVER URL, USER TOKEN, ORGANIZATION TOKEN and LOCAL DIRECTORY PATH")
        return True
    my_label.config(text="")
    my_response.delete(1.0, END)
    response = get_all_products(md_url, og_token, user)
    fields = ["PRODUCT NAME", "PRODUCT TOKEN", "PROJECT NAME", "PROJECT TOKEN", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
    with (open(local_path + '/DOWNLOAD-MEND-DATA.csv',
               'w', newline='') as file):
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        my_response.insert(END, "File download complete in given local directory path")
        for product in response.json()['products']:
            all_project_response = get_all_projects_by_token(md_url, product, user)
            for project in all_project_response.json()['projects']:
                cri_count = 0
                hig_count = 0
                med_count = 0
                lw_count = 0
                project_alerts_response = get_alerts_by_project(md_url, project['projectToken'], user)
                for alerts in project_alerts_response.json()['alerts']:
                    if 'vulnerability' in alerts:
                        if alerts['vulnerability']['severity'] == 'critical':
                            cri_count = cri_count + 1
                        elif alerts['vulnerability']['severity'] == 'high':
                            hig_count = hig_count + 1
                        elif alerts['vulnerability']['severity'] == 'medium':
                            med_count = med_count + 1
                        elif alerts['vulnerability']['severity'] == 'low':
                            lw_count = lw_count + 1

                writer.writerow({'PRODUCT NAME': product["productName"], 'PRODUCT TOKEN': product["productToken"],
                                 'PROJECT NAME': project["projectName"], 'PROJECT TOKEN': project["projectToken"],
                                 'CRITICAL': cri_count, 'HIGH': hig_count,
                                 'MEDIUM': med_count, 'LOW': lw_count})


url_label = Label(root, text="SERVER URL", font=('Arial', 15))
org_token_label = Label(root, text="ORGANIZATION TOKEN", font=('Arial', 15))
user_token_label = Label(root, text="USER TOKEN", font=('Arial', 15))
product_token_label = Label(root, text="PRODUCT TOKEN", font=('Arial', 15))
project_token_label = Label(root, text="PROJECT TOKEN", font=('Arial', 15))
local_path_label = Label(root, text="LOCAL DIRECTORY PATH", font=('Arial', 15))

url_label.grid(row=3, column=0, columnspan=1,padx=5,pady=5)
org_token_label.grid(row=4, column=0, columnspan=1,padx=5,pady=5)
user_token_label.grid(row=5, column=0, columnspan=1,padx=5,pady=5)
product_token_label.grid(row=6, column=0, columnspan=1,padx=5,pady=5)
project_token_label.grid(row=7, column=0, columnspan=1,padx=5,pady=5)
local_path_label.grid(row=8, column=0, columnspan=1,padx=5,pady=5)

url_text = Entry(root, textvariable=url, width=55, bd=5, font=('Arial', 15))
org_token_text = Entry(root, textvariable=org_token,width=55, bd=5, font=('Arial', 15))
user_token_text = Entry(root, textvariable=user_token,width=55, bd=5, font=('Arial', 15))
product_token_text = Entry(root, textvariable=prod_token, width=55, bd=5, font=('Arial', 15))
project_token_text = Entry(root, textvariable=proj_token, width=55, bd=5, font=('Arial', 15))
local_path_text = Entry(root, textvariable=local_path_token, width=55, bd=5, font=('Arial', 15))

url_text.grid(row=3, column=1, columnspan=1,padx=50,pady=5)
org_token_text.grid(row=4, column=1, columnspan=1,padx=50,pady=5)
user_token_text.grid(row=5, column=1, columnspan=1,padx=50,pady=5)
product_token_text.grid(row=6, column=1, columnspan=1,padx=50,pady=5)
project_token_text.grid(row=7, column=1, columnspan=1,padx=50,pady=5)
local_path_text.grid(row=8, column=1, columnspan=1,padx=50,pady=5)


get_product_button = Button(root, command=get_product, text="Get All Product(s) for given Organization Token", padx=50, pady=5, bd=5, font=('Arial', 15))
Hovertip(get_product_button,'Please provide URL, Organization Token and User Token')
get_project_button = Button(root, command=get_project, text="Get All Project(s) By Product Token", padx=50, pady=5, bd=5, font=('Arial', 15))
Hovertip(get_project_button,'Please provide URL, User Token and Product Token')
#get_product_tags_button = Button(root, command=get_product_tags, text="Get All Product Tags By Product Token", padx=50, pady=5, bd=5, font=('Arial', 15))
#Hovertip(get_product_tags_button,'Please provide URL, User Token and Product Token')
get_project_vul_count_button = Button(root, command=get_vul_count, text="Get All Project Vulnerabilities count by Project Token", padx=55, pady=5, width=30, bd=5, font=('Arial', 15))
Hovertip(get_project_vul_count_button,'Please provide URL, User Token and Project Token')
get_all_details_button = Button(root, command=get_all_details, text="Download all details for given Organization Token", padx=55, pady=5, width=30, bd=5, font=('Arial', 15))
Hovertip(get_all_details_button,'Please provide URL, User Token, Organization Token and LOCAL DIRECTORY PATH')


get_product_button.grid(row=9, column=1, columnspan=1,padx=2,pady=0)
get_project_button.grid(row=10, column=1)
#get_product_tags_button.grid(row=10, column=1, columnspan=1,padx=2,pady=0)
get_project_vul_count_button.grid(row=11, column=1, columnspan=1,padx=2,pady=0)
get_all_details_button.grid(row=12, column=1, columnspan=1,padx=2,pady=0)
exit_button.grid(row=0, column=100, columnspan=1,padx=2,pady=0)

my_label = Label(root, font=('Arial Bold', 30))
my_label.grid(row=14, column=1)

my_response = Text(root, width=140)
my_response.grid(row=16, column=1)


root.mainloop()
