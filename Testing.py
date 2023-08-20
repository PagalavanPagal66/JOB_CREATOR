import streamlit as st
import smtplib
import sqlite3
from streamlit_option_menu import option_menu
import hashlib
import random
import ssl


companyconn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\Company.db')
companycursor = companyconn.cursor()
conn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\Jobs.db')
c = conn.cursor()
skillsetconn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\SkillSets.db')
skillsetcursor = skillsetconn.cursor()


Domains =('DeepLearning',
		  'MachineLearning',
		  'WebDevelopment',
		  'Agriculture',
		  'Marketing',
		  'AppDevelopment',
		  'FashionTech',
		  'IOT',
		  'ARVR',
		  'CloudComputing',
		  'CyberSecurity',
		  'SoftwareTesting',
		  'DataStructures',
		  'SocialMediaBranding',
		  'FoodTechnology',
		  'Chemistry',
		  'Physics',
		  'Biology',
		  'BigData',
		  'BlockChain',
		  'Networking',
		  'Aeronautics',
		  'QuantumComputing',
		  'DroneTechnology',
		  'Economics',
		  'Cinematography',
		  'Robotics',
		  'GraphicsDesign',
		  'DatabaseConnectivity',
		  'Accounting'
)
def create_hash_table(Domain):
    jobsconn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\Jobs.db')
    jobscursor = jobsconn.cursor()
    jobscursor.execute('CREATE TABLE IF NOT EXISTS ' + Domain + '(companyname TEXT NOT NULL,companylocation TEXT NOT NULL,companymail TEXT NOT NULL,vacancyrole TEXT NOT NULL,salary TEXT NOT NULL,exp TEXT NOT NULL,skillset TEXT NOT NULL);')
    jobsconn.commit()

def add_jobsdata(c,conn,Domain,companyname,companyloc,companymail,companyrole,companysalary,companyexp,companyskill):
    jobsconn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\Jobs.db')
    jobscursor = jobsconn.cursor()
    jobscursor.execute('INSERT INTO '+Domain + ' (companyname,companylocation,companymail,vacancyrole,salary,exp,skillset) VALUES (?,?,?,?,?,?,?)',(companyname,companyloc,companymail,companyrole,companysalary,companyexp,companyskill))
    jobsconn.commit()

def view_all_users(c,Domain):
    c.execute('SELECT * FROM '+Domain)
    data = c.fetchall()
    return data

def isvalidjob(c,conn,Domain,companyname,companysalary,companyrole,companyexp,companymail,companyloc,companyskill):
    c.execute('SELECT * FROM '+Domain+' WHERE companyname =(?) AND vacancyrole = (?) AND salary = (?) AND companylocation = (?) AND companymail = (?) AND exp = (?) AND skillset = (?)',(companyname,companyrole,companysalary,companyloc,companymail,companyexp,companyskill))
    li=c.fetchall()
    return len(li)

def delete_user(c,conn,Domain,companyname,companysalary,companyrole,companyexp,companymail,companyloc,companyskill):
    c.execute("DELETE FROM "+Domain+" WHERE companyname =(?) AND vacancyrole = (?) AND salary = (?) AND companylocation = (?) AND companymail = (?) AND exp = (?) AND skillset = (?)",(companyname,companyrole,companysalary,companyloc,companymail,companyexp,companyskill))
    print("DELETED - ",companyname,"From table ",Domain)
    conn.commit()

def update_user(c,conn,Domain,companyname,companyloc,companymail,companyrole,companysalary,companyexp,companyskill,ucompanyname,ucompanyloc,ucompanymail,ucompanyrole,ucompanysalary,ucompanyexp,ucompanyskill):
    c.execute("UPDATE "+Domain+" SET companyname =(?) , vacancyrole = (?) , salary = (?) , companylocation = (?) , companymail = (?) , exp = (?) , skillset = (?) WHERE companyname =(?) AND vacancyrole = (?) AND salary = (?) AND companylocation = (?) AND companymail = (?) AND exp = (?) AND skillset = (?)",(ucompanyname,ucompanyrole,ucompanysalary,ucompanyloc,ucompanymail,ucompanyexp,ucompanyskill,companyname,companyrole,companysalary,companyloc,companymail,companyexp,companyskill))
    conn.commit()

def find_company_in_domain(Domain,companyname):
    c.execute("SELECT * FROM "+Domain+' WHERE companyname =(?)',(companyname,))
    li = c.fetchall()
    return li


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

selected = option_menu(
    menu_title= None,
    options = ['HOME','DETAILS','CONTACT'],
    icons = ['house','house','book'],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal"
)

from email.message import EmailMessage
def otpmailing(con,mail):
    email_sender = "cfpredictor123@gmail.com"
    email_password = "qtlvbndfudxrvqrb"
    email_receiver = mail

    subject = "Authentication"
    body = str(con)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def create_usertable():
    companycursor.execute('CREATE TABLE IF NOT EXISTS final (username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,mail TEXT NOT NULL UNIQUE,companydescription TEXT NOT NULL,companylink TEXT NOT NULL UNIQUE,companylogo BLOB NOT NULL UNIQUE);')
    companyconn.commit()

create_usertable()


def create_new_set(tablename):
    skillsetcursor.execute('CREATE TABLE IF NOT EXISTS '+tablename+' (skillset TEXT);')
    skillsetconn.commit()

def already_added(tablename,skill):
    skillsetcursor.execute('SELECT * from '+tablename+' WHERE skillset = (?)',(skill,))
    data = skillsetcursor.fetchall()
    return len(data)

def add_skillset(tablename,skillset):
    for skill in skillset:
        if(already_added(tablename,skill)==0):
            skillsetcursor.execute('INSERT INTO '+tablename+' (skillset) VALUES (?)',(skill,))
            skillsetconn.commit()

def view_all_skills(tablename):
    skillsetcursor.execute('SELECT * from '+tablename)
    return skillsetcursor.fetchall()

def add_userdata(username,password,mail,companydescription,companylink,companylogo):
    companycursor.execute('INSERT INTO final (username,password,mail,companydescription,companylink,companylogo) VALUES (?,?,?,?,?,?)',(username,password,mail,companydescription,companylink,companylogo))
    companyconn.commit()

def view_all_users_login():
    companycursor.execute('SELECT * FROM final')
    data = companycursor.fetchall()
    return data

def verify_company(companyname,password):
    companycursor.execute('SELECT * FROM final WHERE username = (?) AND password = (?)',(companyname,password))
    data  = companycursor.fetchall()
    return len(data)

def view_company_details(companyname):
    companycursor.execute('SELECT * FROM final WHERE username = (?) ',(companyname,))
    data = companycursor.fetchall()
    return data


if(selected == "HOME"):
    value = st.selectbox("OPERATION : " , ("LOGIN",'SIGNUP','LOGOUT'))
    if(value=="SIGNUP"):
        companyname = st.text_input("COMPANY NAME : ")
        password =st.text_input("COMPANY PASSWORD : ",type= 'password')
        hashed_pswd = make_hashes(password)
        companymail = st.text_input("COMPANY MAIL : ")
        companydescription = st.text_area("COMPANY DESCRIPTION : ")
        companylink = st.text_input("COMPANY LINK : ")
        companylogofile  = st.file_uploader("COMPANY LOGO : ", accept_multiple_files=True)
        try:
            for uploaded_file in companylogofile:
                bytes_data = uploaded_file.read()
        except:
            pass
        if(st.button("SUBMIT")):
            companylogo  = bytes_data
            #st.write(companyname+" "+hashed_pswd+" "+companyname+" "+companydescription+" "+companylink+" ")
            add_userdata(companyname,hashed_pswd,companymail,companydescription,companylink,companylogo)
            st.success("ADDED")

    if(value == "LOGIN"):
            companyname = st.text_input("COMPANY NAME : ")
            password = st.text_input("PASSWORD : ",type='password')
            if(st.button("SUBMIT")):
                hashed_pswd = make_hashes(password)
                if(verify_company(companyname,check_hashes(password,hashed_pswd))):
                    st.success("LOGGED IN")
                    with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\Flag.txt', 'w') as f:
                        d = '1'
                        f.write(d)
                    with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\CompanyName.txt','w') as f:
                        pass
                    with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\CompanyName.txt','w') as f:
                        f.write(companyname)
                else:
                    st.error("WRONG CREDENTIALS")

    if(value == 'LOGOUT'):
        with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\Flag.txt', 'w') as f:
            d = '0'
            f.write(d)
        with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\CompanyName.txt','w') as f:
            pass
        st.error("LOGGED OUT")

if(selected == 'DETAILS'):
    with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\Flag.txt', 'r') as f:
        data = f.read()
    if(data == '0'):
        st.error("PLEASE SIGN IN TO CONTINUE...")
    if(data == '1'):
        add_selectbox = st.sidebar.selectbox(
            "Type of CRUD operation to be performed : ",
            ("ADD", "EDIT", "DELETE")
        )
        with open(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\CompanyName.txt', 'r') as f:
            companyname = f.read()

        companymail = view_company_details(companyname)[0][2]

        if (add_selectbox == 'DELETE'):
            count = 0
            for iter in Domains:
                create_hash_table(iter)
                value = find_company_in_domain(iter, companyname)
                count += len(value)
                if (len(value) != 0):
                    st.success(iter)  # Domain
                for i in range(0, len(value)):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("NAME : " + value[i][0])
                        st.write("LOC  : " + value[i][1])
                    with col2:
                        st.write("ROLE :  " + value[i][3])
                        st.write("SALARY : " + value[i][4])
                        st.write("EXP : " + value[i][5])
                    with col3:
                        if (st.button("DELETE", key=str(i) + iter)):
                            delete_user(c, conn, iter, value[i][0], value[i][4], value[i][3], value[i][5], value[i][2],
                                        value[i][1], value[i][6])
                            st.error("DELETED SUCCESSFULLY")
                    st.write("SKILL : " + value[i][6])

                    st.write("--------------------------------------")

        if (add_selectbox == 'ADD'):
            col1, col2 = st.columns(2)
            with col1:
                domain = st.selectbox("DOMAIN : ", Domains)
                companyloc = st.text_input("LOCATION : ")
            with col2:
                companyrole = st.text_input("ROLE : ")
                companysalary = st.text_input("SALARY : ")
            companyexp = st.slider("EXP : ", min_value=0, max_value=15)
            companyskills = (st.multiselect("SKILLS : ", Domains))
            companyskill = ""
            for iterator in companyskills:
                companyskill += iterator + ' '
            st.write(companyskill)
            if (st.button("SUBMIT")):
                add_jobsdata(c, conn, domain, companyname, companyloc, companymail, companyrole, companysalary,
                             companyexp, companyskill)
                st.success("ADDED SUCCESSFULLY...!")
        if (add_selectbox == "EDIT"):
            count = 0
            for iter in Domains:
                create_hash_table(iter)
                value = find_company_in_domain(iter, companyname)
                count += len(value)
                if (len(value) != 0):
                    st.success(iter)  # Domain
                for i in range(0, len(value)):
                    col1, col2, col3 = st.columns(3)
                    ucompanyskillset = st.multiselect("SKILL : ",options = Domains, key=str(i) + iter + "SKILL")
                    with col1:
                        ucompanyloc = st.text_input("LOCATION : ", value=value[i][1],key=str(i) + iter + "LOCATION")
                        ucompanyrole = st.text_input("ROLE :  ", value=value[i][3], key=str(i) + iter + "ROLE")
                    with col2:
                        usalary = st.text_input("SALARY : ", value=value[i][4], key=str(i) + iter + "SALARY")
                        uexp = st.text_input("EXP : ", value=value[i][5], key=str(i) + iter + "EXP")
                    with col3:
                        st.write("          ")
                        st.write("          ")
                        if st.button("SUBMIT", key=str(i) + iter):
                            ucompanyskill = ""
                            for skill in ucompanyskillset:
                                ucompanyskill+=skill
                                ucompanyskill+=' '
                            update_user(c, conn, iter, value[i][0], value[i][1], value[i][2], value[i][3],
                                        value[i][4], value[i][5], value[i][6], companyname, ucompanyloc,
                                        companymail, ucompanyrole, usalary, uexp, ucompanyskill)
                            st.info("UPDATED SUCCESSFULLY")
                    st.write("----------------------------------------------------------")
            if count == 0:
                st.write("NO JOBS ADDED")