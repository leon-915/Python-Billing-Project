"""Plan related tasks"""
from celery.utils.log import get_task_logger

# from src.celery_app import celery
import psycopg2
import datetime 

log = get_task_logger(__name__)


@app.route("/")
# @celery.task()
def calculate_mb_available():
    """ADD CODE HERE"""
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wingattbilling")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select plan_id , status, id from subscriptions"
        
        cursor.execute(postgreSQL_select_Query)

        plan_id_records = cursor.fetchall()
        for row in plan_id_records:
            # print("Id = ", row[0], )
            # print("Model = ", row[1])
            # print("Price  = ", row[2])
            # connection = psycopg2.connect(user="postgres",
            #                       password="123456",
            #                       host="127.0.0.1",
            #                       port="5432",
            #                       database="wingattbilling")
            # cursor = connection.cursor()
            # postgreSQL_select_available_data = "select mb_available from plans where id = '" + str(row[0]) + "'"
            # # postgreSQL_select_status = 
            # cursor.execute(postgreSQL_select_available_data)

            # mb_available = cursor.fetchone()
            
            plan_id = row[0]
            status = row[1]
            subscription = row[2]
            current_time = datetime.datetime.now()
            
            
                
            if status == "suspended" or status == "expired":
                print("mb_available_______ ", 0 )
            else:
                plan_id_of_subscription = row[0]
                postgreSQL_select_att_plan = "select * from plans where id = '" + str(plan_id) + "'"
                cursor.execute(postgreSQL_select_att_plan)
                data_att_plan = cursor.fetchall()
                for row_of_data_att_plan in data_att_plan:                    
                    current_time = datetime.datetime.now()
                    now_day = current_time.day
                    data_available = int(now_day)/30 * int(row_of_data_att_plan[2])
                    print(subscription,"th 's subscription's mb_available is_______ ", data_available)


                # get data of one subscription's plan data(get only one data)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        
calculate_mb_available()        
