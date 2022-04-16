import mysql.connector as conn
import pymongo
from flask import Flask, render_template,request
from flask_cors import CORS,cross_origin
from navigate import Navigate
from subcategory_url import Subcat
from scrapper import Scrapper
import logger

app = Flask(__name__)
log = logger.Logger()

@app.route('/',methods=['GET','POST'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/ineuron_data',methods=['POST'])
@cross_origin()
def ineuron_course():
    if request.method == 'POST':
        try:
            if request.form['num'] == "":
                num = 292
            else:
                num = int(request.form['num'])
            # Object of Navigate Class
            nav = Navigate()
            # Calling method course_subcategory of Navigate for URLS of subcategories
            sub_urls = nav.course_subcategory()
            # Object of Subcat class
            sub = Subcat(sub_urls)
            # Calling method courses_url of Subcat for urls of each courses in subcategory
            course_url = sub.courses_url()
            # Object of Scrapper class
            scp = Scrapper(course_url[:num])
            # Calling course_page method of Scrapper to get the scrapped data of each courses
            ineuron_data = scp.course_page()
            log.INFO("Scrapping Operation Successfull!!")

            if request.form['username'] != "" and request.form['pswd'] != "":
                log.INFO("SQL operation initiated")
                host = str(request.form['host'])
                username = str(request.form['username'])
                pswd = str(request.form['pswd'])
                database = str(request.form['database'])

                sql_database(host,username,pswd,database,ineuron_data)

            if request.form['CLIENT_URL'] != "":
                log.INFO("MongoDB operation initiated")
                Mongo_Client = str(request.form['CLIENT_URL'])
                database = str(request.form['database'])
                mongo_database(Mongo_Client,database,ineuron_data)

            return render_template('results.html', ineuron_data=ineuron_data[0:(len(ineuron_data))])

        except Exception as e:
            log.ERROR(f'The Exception message is:  {e}')
            return e
    else:
        return render_template('index.html')

def sql_database(host,user,pswd,DB,ineuron_data):
    try:
        mydb = conn.connect(host = host, user = user, passwd = pswd)
        log.INFO("SQL login successfull")
    except:
        log.ERROR("Error in sql login")
        return "Wrong SQL Credentials"


    cur = mydb.cursor()
    cur.execute("show databases")
    database_list = cur.fetchall()
    try:
        if DB in database_list:        # Checking whether DB exist or not if yes then use it or Create New one
            cur.execute(f"USE {DB}")
        else:
            cur.execute(f"CREATE database {DB}")
            cur.execute(f"USE {DB}")

        table_name = "iNeuron_Course"
        cur.execute("show tables")
        table_list = cur.fetchall()

        if table_name in table_list:   # Checking whether table "iNeuron_Course" exist or not if yes then drop it
            cur.execute(f"drop table {table_name}")

        cur.execute(f"CREATE TABLE {table_name}(Title VARCHAR(255),Course Description VARCHAR(1000),"
                    f"Price VARCHAR(30),Class Timings VARCHAR(100),Doubt-class Timings VARCHAR(10n     0),"
                    f"Course Overview VARCHAR(1000),Features VARCHAR(1000),Instructors VARCHAR(50)"
                    f"Requirements VARCHAR(500),Syllabus VARCHAR(5000))")
        for data in ineuron_data:
            cur.execute(f"INSERT INTO {table_name} VALUES({data['Title']},{data['Course Description']},{data['Price']},"
                        f"{data['Class Timings']},{data['Doubt-class Timings']},{data['Course Overview']},"
                        f"{data['Features']},{data['Instructors']},{data['Requirements']},{data['Syllabus']})")
        mydb.commit()
        log.INFO("Successfully inserted data into SQL DB")
    except Exception as e:
        log.ERROR(f"Error occured while inserting data in SQL: {e}")
        return "Error occured while inserting data in SQL",e



def mongo_database(CLIENT_URL,cluster,ineuron_data):
    try:
        client = pymongo.MongoClient(CLIENT_URL)
        db = client.test
        log.INFO("MongoDB Client connection successfull")
    except:
        log.WARN("Problem in connection to MongoDB client")
        log.ERROR("Problem in connection to MongoDB client")
        return "Incorrect MongoDB Client"

    try:
        db = client[cluster]
        Coll_Name = "iNeuron_Course"
        Collection_list = db.list_collection_names()

        if Coll_Name in Collection_list:   # Checking whether DB exist or not if yes then drop that
            db.drop_collection(Coll_Name)

        COLL = db[Coll_Name]
        COLL.insert_many(ineuron_data)
        log.INFO("Successfully inserted data into Mongo DB")
    except Exception as e:
        log.WARN("Error occured while inserting data in MongoDB")
        log.ERROR(f"Error occured while inserting data in MongoDB: {e}")
        return "Error occured while inserting data in MongoDB",e

if __name__=="__main__":
    app.run(host='localhost', port=9001)