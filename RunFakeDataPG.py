from CreateFakeDataPG import CreateFakeDataPG
import sys
from faker import Faker
import uuid
import random


def getDictFakePartners(num_rows, fake_data, man_list):
    
    partners = {"guid": [],
                "description": [],
                "isactive": [],
                "manager_uid": []
                }
    
 
    for _ in range(num_rows):

        partners["guid"].append(str(uuid.uuid4()))
        partners["description"].append(fake_data.company()) 
        partners["isactive"].append(random.choice(['0', '1'])) 
        partners["manager_uid"].append(random.choice(man_list)) 
    
    return partners


def getDictFakeDepartments(num_rows, fake_data):

    dep = {"parent": str(uuid.uuid4()),
           "uuid": [],
           "description": []}

    for _ in range(num_rows):

        dep["uuid"].append(str(uuid.uuid4()))
        dep["description"].append(fake_data.company()) 
    
    return dep

def getDictFakeManagers(num_rows, dep_uuids, fake_data):  

    man = {"uuid": [],
           "name" : [],
           "second_name" : [],
           "full_name" : [],
           "phone" : [],
           "department" : []
          }
    
    for _ in range(num_rows):

        name = fake_data.first_name()
        second_name = fake_data.last_name()

        man["uuid"].append(str(uuid.uuid4()))
        man["name"].append(name)
        man["second_name"].append(second_name)
        man["full_name"].append(name + " " + second_name)
        man["phone"].append(fake_data.msisdn()[0:12])
        man["department"].append(random.choice(dep_uuids))

    return man  

def getDictFakeClassifiers(num_rows):

    Classifiers = {"uuid": [],
                   "description": [],
                   "type_of_measurement": [],
                   "value_of_measurement_numeric": [],
                   "value_of_measurement_string": []
                }


    Product_type  = {
        "unit_type": "type",
        "value": ["wine", "vodka", "champagne", "whisky"]

    }
 
    wine_color = {
        "unit_type": "color",
        "value": ["white", "red", "pink"]
    }

    alcohol_percent = {
        "unit_type": "percent",
        "min_val": 12,
        "max_val": 45

    }

    volume_liters = {
        "unit_type": "l",
        "min_val": 0.5,
        "max_val": 1.5
    }

   
    for i in range(num_rows):
        product_type_row = random.choice(Product_type["value"])
        volume_liters_row = random.uniform(volume_liters["min_val"], volume_liters["max_val"])
        wine_color_row = None

        if product_type_row == "wine" or product_type_row == "champagne":
            alcohol_percent_row = random.uniform(12, 24)
            wine_color_row = random.choice(wine_color["value"])
        elif product_type_row == "vodka" or product_type_row == "whisky":
            alcohol_percent_row = random.uniform(40, 45)

        inserted_row_dict = [
            {"description": "volume liters", "type of measurement": volume_liters["unit_type"], "value of measurement numeric": volume_liters_row, "value of measurement string": None},
            {"description": "product type", "type of measurement": Product_type["unit_type"], "value of measurement numeric": None, "value of measurement string": product_type_row},
            {"description": "alcohol percent", "type of measurement": alcohol_percent["unit_type"], "value of measurement numeric": alcohol_percent_row, "value of measurement string": None},
            {"description": "wine color", "type of measurement": wine_color["unit_type"], "value of measurement numeric": None, "value of measurement string": wine_color_row}
        ]  

        for el in inserted_row_dict:
            
            Classifiers["uuid"].append(str(uuid.uuid4()))
            Classifiers["description"].append(el["description"])
            Classifiers["type_of_measurement"].append(el["type of measurement"])
            Classifiers["value_of_measurement_numeric"].append(el["value of measurement numeric"])
            Classifiers["value_of_measurement_string"].append(el["value of measurement string"])

    return Classifiers   

def getDictFakeGoods(num_rows, fake_data, classif_uuids):

    len_classif_uuids = len(classif_uuids)

    goods = {"UUID": [],
            "description": []
            }


    good_classificators = {"UUID": [],
                            "good_uuid": [],
                            "classifier_uuid": []}
    


    for _ in range(num_rows):
        good_uuid = str(uuid.uuid4())
        
        for _ in range(random.randint(2, 4)):
            ran_classif = random.choice(classif_uuids)
            good_classificators["UUID"].append(str(uuid.uuid4()))
            good_classificators["good_uuid"].append(good_uuid)
            good_classificators["classifier_uuid"].append(ran_classif)
            
        goods["UUID"].append(good_uuid)
        goods["description"].append(fake_data.company())

    
    return {"goods": goods, "good_classificators": good_classificators}




def main():   
    fake_data = Faker()
    num_rows_dep = 3
    num_rows_man = 5
    num_rows_classifiers = 10
    num_rows_goods = 10
    num_rows_partners = 10

    dep = getDictFakeDepartments(num_rows_dep, fake_data)

    man = getDictFakeManagers(num_rows_man, dep["uuid"], fake_data)

    classifiers = getDictFakeClassifiers(num_rows_classifiers)

    goods = getDictFakeGoods(num_rows_goods, fake_data, classifiers["uuid"])

    partners = getDictFakePartners(num_rows_partners, fake_data, man["uuid"])
      
    try:
        with CreateFakeDataPG() as pg:
            for i in range(len(dep["uuid"])):
                uuid_dep = dep["uuid"][i]
                description_dep = dep["description"][i]
                parent_dep = dep["parent"]

                pg.cursor.execute("""
                INSERT INTO department ("UUID", description, parent)
                VALUES (%s, %s, %s)""", (uuid_dep, description_dep, parent_dep))

            for i in range(len(man["uuid"])):
                uuid_man = man["uuid"][i]
                name_man = man["name"][i]
                second_name_man = man["second_name"][i]
                full_name_man = man["full_name"][i]
                phone_man = man["phone"][i]
                department_man = man["department"][i]

                pg.cursor.execute("""
                INSERT INTO manager ("UUID", name, second_name, full_name, phone, department)
                VALUES (%s, %s, %s, %s, %s, %s)""", (uuid_man, name_man, second_name_man, full_name_man, phone_man, department_man))

            

            for i in range(len(classifiers["uuid"])):
                uuid_classifiers = classifiers["uuid"][i]
                description_classifiers = classifiers["description"][i]
                type_of_measurement_classifiers = classifiers["type_of_measurement"][i]
                value_of_measurement_numeric_classifiers = classifiers["value_of_measurement_numeric"][i]
                value_of_measurement_string_classifiers = classifiers["value_of_measurement_string"][i]

                pg.cursor.execute("""
                INSERT INTO classifiers ("uuid", description, type_of_measurement, value_of_measurement_numeric, value_of_measurement_string)
                VALUES (%s, %s, %s, %s, %s)""", (uuid_classifiers, 
                                                 description_classifiers, 
                                                 type_of_measurement_classifiers, 
                                                 value_of_measurement_numeric_classifiers, 
                                                 value_of_measurement_string_classifiers))

           

            for i in range(len(goods["goods"]["UUID"])):
                uuid_goods = goods["goods"]["UUID"][i]
                description_goods = goods["goods"]["description"][i]
                

                pg.cursor.execute("""
                INSERT INTO good ("UUID", description)
                VALUES (%s, %s)""", (uuid_goods, description_goods))

  

            for i in range(len(goods["good_classificators"]["good_uuid"])):
                uuid_good_classificators = goods["good_classificators"]["UUID"][i]
                good_uuid_good_classificators = goods["good_classificators"]["good_uuid"][i]
                classifier_uuid_good_classificators = goods["good_classificators"]["classifier_uuid"][i]

                pg.cursor.execute("""
                INSERT INTO goods_classificator ("UUID", good_uuid, classifier_uuid)
                VALUES (%s, %s, %s)""", (uuid_good_classificators, 
                                        good_uuid_good_classificators, 
                                        classifier_uuid_good_classificators, 
                                        ))    



            for i in range(len(partners["guid"])):
                guid_partner = partners["guid"][i]
                description_partner = partners["description"][i]
                isactive_partner = partners["isactive"][i]
                manager_uid_partner = partners["manager_uid"][i]          

                pg.cursor.execute("""
                INSERT INTO partners (guid, description, isactive, manager_uid)
                VALUES (%s, %s, %s, %s)""", (guid_partner, 
                                        description_partner, 
                                        isactive_partner,
                                        manager_uid_partner 
                                        ))    

            pg._conn.commit()
        return 0
    except RuntimeError as e:
        print(f"[!] Ошибка при работе с базой: {e}")
        return 2

            

    # try:
    #     pg = CreateFakeDataPG()
    #     pg.openConnectonDB()
        
    #     pg.openCursorDB()

    #     num_rows_dep = 3
    #     dep = getDictFakeDepartments(num_rows_dep)
    #     for _ in range(dep):
    #        # parse dict....
         
    #           pg.execute("""
    #     INSERT INTO department ("UUID", description, parent)
    #     VALUES (%s, %s, %s)""", (uuid, description, parent))

    #     pg.closeCursorDB()

    #     pg.openCursorDB()

    #     num_rows_man = 5
    #     man = getDictFakeManagers(dep, num_rows_man)
    #     for _ in range(num_rows_man):
    #  #       todo execute cursor

    #     pg.closeCursorDB()
 



    #     return 1
    # except ValueError as ve:
    #     print("missing connection parameters ", ve)

    #     return 2
    # finally:
    #     if pg:
    #         try:
    #             pg.closeConnectionDB()
    #             pg.closeCursorDB()
    #         except RuntimeError as re:
    #             print("Runtime logic error", re)
    #         except ConnectionError as se:
    #             print("Cursor closing error", se)     

if __name__ == "__main__":
    sys.exit(main())




        
   
            
     


    