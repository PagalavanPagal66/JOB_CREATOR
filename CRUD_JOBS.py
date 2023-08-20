import streamlit as st
import flask
import sqlite3

conn = sqlite3.connect(r'C:\Users\pagal\PycharmProjects\TEXT\PSG_iTech\DataBases\Jobs.db')
c = conn.cursor()

page_by_img ="""
<style>
[data-testid="stHeader"]{
background-color : rgba(0,0,0,0);
}
[data-testid="stAppViewContainer"]{
background-image: linear-gradient(-225deg, #5D9FFF 0%, #B8DCFF 48%,#6BBBFF 100%);
</style>
"""
st.markdown(page_by_img,unsafe_allow_html=True)

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


add_selectbox = st.sidebar.selectbox(
    "Type of CRUD operation to be performed : ",
    ("ADD","EDIT","DELETE")
)


if(add_selectbox == 'DELETE'):
    count = 0
    companyname = st.text_input("ENTER COMPANY NAME : ")
    for iter in Domains:
        create_hash_table(iter)
        value = find_company_in_domain(iter,companyname)
        count += len(value)
        if(len(value)!=0):
            st.success(iter) #Domain
        for i in range(0,len(value)):
            col1,col2,col3 = st.columns(3)
            with col1:
                st.write("NAME : " + value[i][0])
                st.write("LOC  : " + value[i][1])
                st.write("MAIL  : " + value[i][2])
            with col2:
                st.write("ROLE :  " + value[i][3])
                st.write("SALARY : " +value[i][4])
                st.write("EXP : " + value[i][5])
            with col3:
                if(st.button("DELETE",key=str(i)+iter)):
                    delete_user(c,conn,iter,value[i][0],value[i][4],value[i][3],value[i][5],value[i][2],value[i][1],value[i][6])
                    st.error("DELETED SUCCESSFULLY")
            st.write("SKILL : " + value[i][6])

            st.write("--------------------------------------")

if(add_selectbox == 'ADD'):
    col1, col2 = st.columns(2)
    with col1:
        companyname = st.text_input("ENTER COMPANY NAME : ")
        domain = st.selectbox("DOMAIN : ",Domains)
        companyloc = st.text_input("LOCATION : ")
    with col2:
        companymail = st.text_input("MAIL : ")
        companyrole = st.text_input("ROLE : ")
        companysalary = st.text_input("SALARY : ")
    companyexp = st.slider("EXP : ", min_value=0, max_value=15)
    companyskills = (st.multiselect("SKILLS : ", Domains))
    companyskill=""
    for iterator in companyskills:
        companyskill+=iterator+'/'
    st.write(companyskill)
    if(st.button("SUBMIT")):
        add_jobsdata(c,conn,domain,companyname,companyloc,companymail,companyrole,companysalary,companyexp,companyskill)
        st.success("ADDED SUCCESSFULLY...!")

if(add_selectbox=="EDIT"):
    count = 0
    companyname = st.text_input("ENTER COMPANY NAME : ")
    if(st.button("SUBMIT",key = "BUTTON-KEY-SUBMIT")):
        for iter in Domains:
            create_hash_table(iter)
            value = find_company_in_domain(iter, companyname)
            count += len(value)
            if (len(value) != 0):
                st.success(iter)  # Domain
            for i in range(0, len(value)):
                col1, col2, col3 = st.columns(3)
                ucompanyskill = st.text_input("SKILL : ", value=value[i][6], key=str(i) + iter + "SKILL")
                with col1:
                    ucompanyname = st.text_input("NAME  : " ,value=value[i][0],key = str(i)+iter+"NAME")
                    ucompanyloc = st.text_input("LOCATION : ",value=value[i][1],key = str(i)+iter+"LOCATION")
                    ucompanymail = st.text_input("MAIL  : " ,value=value[i][2],key = str(i)+iter+"MAIL")
                with col2:
                    ucompanyrole = st.text_input("ROLE :  " ,value= value[i][3],key = str(i)+iter+"ROLE")
                    usalary = st.text_input("SALARY : " ,value=value[i][4],key = str(i)+iter+"SALARY")
                    uexp = st.text_input("EXP : " ,value =value[i][5],key = str(i)+iter+"EXP")
                with col3:
                    st.write("          ")
                    st.write("          ")
                    if st.button("SUBMIT",key=str(i)+iter):
                        update_user(c,conn,iter,value[i][0],value[i][1],value[i][2],value[i][3],value[i][4],value[i][5],value[i][6],ucompanyname,ucompanyloc,ucompanymail,ucompanyrole,usalary,uexp,ucompanyskill)
                        st.info("UPDATED SUCCESSFULLY")
                st.write("----------------------------------------------------------")
        if count==0:
            st.write("NO JOBS ADDED")
