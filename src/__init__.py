"""Flask app config and initialization"""
import logging.config
import psycopg2
import datetime 
from flask import Flask, jsonify
from sqlalchemy import orm
from flask_json import FlaskJSON, JsonError, json_response, as_json
import json

app = Flask(__name__, static_folder=None)
def create_app(config_obj=None):
    """Sets config from passed in config object,
    initializes Flask modules, registers blueprints (routes)

    Args:
        config_obj (class): config class to apply to app

    Returns:
        app: configured and initialized Flask app object

    """
    

    if not config_obj:
        logging.warning(
            "No config specified; defaulting to development"
        )
        import config
        config_obj = config.DevelopmentConfig

    app.config.from_object(config_obj)

    from src.models.base import db, migrate
    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)

    from src.routes import register_routes
    register_routes(app)

    return app
# @app.route("/")
# def home():
#     return "Hello World!"

@app.route("/api/subscriptions/<id>/att_plan_version/")
def test(id):
    data = []
    # data['data'] = {}
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wingattbilling")
        cursor = connection.cursor()
        


                # get data of one subscription's plan data(get only one data)

        billing_cycle_id = format(id)
        postgreSQL_billing_cycle = "select start_date, end_date from billing_cycles where id ='" + str(billing_cycle_id) + "'"
        
        cursor.execute(postgreSQL_billing_cycle)
        data_billing_cycle = cursor.fetchone()
        start_date = data_billing_cycle[0]     
        end_date = data_billing_cycle[1] 
            
        postgreSQL_att_plan = "select id, start_effective_date, end_effective_date, subscription_id from att_plan_versions"
       
        
        cursor.execute(postgreSQL_att_plan)

        data_att_plan = cursor.fetchall()
        
        for row in data_att_plan:
            
            if row[1] > start_date and row[1] < end_date:
                
                # print("effective start date is ____________")

                # print(row[1])
                # print("effective end date is ____________")
                # print(row[2])
                # print("mb_available is ______________")
                postgreSQL_select_Query = "select plan_id , status, id from subscriptions where id = '" + str(row[3]) + "'"
                cursor.execute(postgreSQL_select_Query)
                plan_id_records = cursor.fetchone()
                        
                plan_id = plan_id_records[0]
                status = plan_id_records[1]
                subscription = plan_id_records[2]
                     
                
                if status == "suspended" or status == "expired":
                    data_available = 0
                    # print("mb_available_______ ", 0 )
                else:
                    plan_id_of_subscription = plan_id_records[0]
                    postgreSQL_select_att_plan = "select * from plans where id = '" + str(plan_id) + "'"
                    cursor.execute(postgreSQL_select_att_plan)
                    data_att_plan = cursor.fetchone()
                    # for row_of_data_att_plan in data_att_plan:                    
                    current_time = datetime.datetime.now()
                    now_day = current_time.day
                    data_available = int(int(now_day)/30 * int(data_att_plan[2]))   #publish data
                                      
                       
                data.append({"start_effective_date" : row[1], "end_effective_date" : row[2] , 
                                "mb_available" : data_available})              
                
                
                # connection_2 = psycopg2.connect(user="postgres",
                #                   password="123456",
                #                   host="127.0.0.1",
                #                   port="5432",
                #                   database="wingattbilling")
                # cursor_2 = connection_2.cursor()
                try:
                    query_save = "UPDATE att_plan_versions SET mb_available = '" + str(data_available) + "' WHERE id = '" + str(row[0]) + "'"
                    cursor.execute(query_save)
                    connection.commit()
                    print(query_save)
                except:
                    pass
                    
                
                # plan_id_records = cursor.fetchall()
                # for row in plan_id_records:         
                #     plan_id = row[0]
                #     status = row[1]
                #     subscription = row[2]
                #     current_time = datetime.datetime.now()           
                    
                #     if status == "suspended" or status == "expired":
                #         print("mb_available_______ ", 0 )
                #     else:
                #         plan_id_of_subscription = row[0]
                #         postgreSQL_select_att_plan = "select * from plans where id = '" + str(plan_id) + "'"
                #         cursor.execute(postgreSQL_select_att_plan)
                #         data_att_plan = cursor.fetchall()
                #         for row_of_data_att_plan in data_att_plan:                    
                #             current_time = datetime.datetime.now()
                #             now_day = current_time.day
                #             data_available = int(now_day)/30 * int(row_of_data_att_plan[2])
                #             print(subscription,"th 's subscription's mb_available is_______ ", data_available)
                
                
            elif row[2] < start_date and row[2] > end_date:
                print()
            else:        
                print()
        # connection.commit()       
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
        # data = {'data': 'none'}
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            # data = {'data': 'none'}
            print("PostgreSQL connection is closed")

  

    # return "The name is {}".format(id)
    return jsonify(data)




@app.route("/")
def main():
    return "Main page"

@app.route("/some/path")
def some_path():
    return "A fixed path"