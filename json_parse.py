import json
import os 

import psycopg
import logging 

def parse_json():
 

    current_path = os.path.realpath(__file__)
    current_dir = os.path.dirname(current_path)
    file_path = os.path.join(current_dir, "data.json")

    f = open(file_path)
    data = json.load(f)

    #hladame portchannel a ethernet 
    portchannel_data = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["Port-channel"]
    ten_gb_ethernet = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["TenGigabitEthernet"]
    gigabitethernet = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]

    
    return portchannel_data, ten_gb_ethernet, gigabitethernet


class RadkasDatabase():

    def __init__(self) -> None:
        # parameters to connect to database
        # self.dbname = "your_database_name"
        # self.user = "your_username"
        # self.password = "your_password"
        # self.host = "localhost"  
        # self.port = "5432"  

        # # creating connection to DB
        # self.conn = psycopg.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        print("Connection to DB part ")


    def insert_into_table(data_list, portchannel = False ):
        
        #sql = """INSERT INTO config_data (name, description, max_frame_size, config, port_channel_id, ) VALUES (%s, %s, %s, %s, %s, %s)"""

        sql_data = []


        for data in data_list:
         
            if portchannel:
                #get ID for current portchannel 
                port_ids = data['Cisco-IOS-XE-ethernet:service']['instance']
            
                for id in port_ids :
                    port_id  = id['id']
                    print("ID value:", port_id )
            else: 
                port_id = None 

            if 'description' in data:
                description = data['description']
            else:
                description = None 
            
            if 'mtu' in data:
                mtu = data['mtu']
            else:
                mtu = None 

            sql_data.append((data['name'], description, mtu, data, port_id))




        # try:
        #     cur = self.conn.cursor()
        #     cur.execute(sql, data)
        #     self.conn.commit()
        #     print("Data inserted successfully!")

        # except Exception as e:
        #     # Rollback the transaction in case of an error
        #     print("Problem")
            
        # # Close the cursor and connection
        # cur.close()
        # self.conn.close()


portchannel_data, ten_gb_ethernet, gigabitethernet = parse_json()
r_db=RadkasDatabase
r_db.insert_into_table(portchannel_data, portchannel=True)
r_db.insert_into_table(ten_gb_ethernet)
r_db.insert_into_table(gigabitethernet)