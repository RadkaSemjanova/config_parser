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

    # hladame portchannel a ethernet
    portchannel_data = data["frinx-uniconfig-topology:configuration"][
        "Cisco-IOS-XE-native:native"
    ]["interface"]["Port-channel"]
    ten_gb_ethernet = data["frinx-uniconfig-topology:configuration"][
        "Cisco-IOS-XE-native:native"
    ]["interface"]["TenGigabitEthernet"]
    gigabitethernet = data["frinx-uniconfig-topology:configuration"][
        "Cisco-IOS-XE-native:native"
    ]["interface"]["GigabitEthernet"]

    return portchannel_data, ten_gb_ethernet, gigabitethernet


class RadkasDatabase:

    def __init__(self) -> None:
        self.dbname = "config"
        self.user = "radkaes"
        self.password = "postgres"
        self.host = "127.0.0.1"
        self.port = "5432"

        self.conn = psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        print("Connection to DB part ")
        self.cur = self.conn.cursor()

    def insert_into_table(self, data_list, portchannel=False):

        create_table_sql = """
            CREATE TABLE IF NOT EXISTS port_config (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description VARCHAR(255),
                max_frame_size INTEGER,
                config JSON,
                port_channel_id INTEGER
            )
        """

        # Execute the CREATE TABLE statement
        self.cur.execute(create_table_sql)

        for data in data_list:
            if portchannel:
                # get ID for current portchannel
                port_ids = data["Cisco-IOS-XE-ethernet:service"]["instance"]
                for id in port_ids:
                    port_id = id["id"]
                    print("ID value:", port_id)
            else:
                port_id = None

            if "description" in data:
                description = data["description"]
            else:
                description = None

            if "mtu" in data:
                mtu = data["mtu"]
            else:
                mtu = None

            config_json = json.dumps(data)

            self.cur.execute(
                "INSERT INTO port_config (name, description, max_frame_size, config, port_channel_id) VALUES (%s, %s, %s, %s, %s)",
                (f"{data['name']}", description, mtu, config_json, port_id),
            )

            self.conn.commit()
        print("Data inserted successfully!")

        # Close the cursor and connection

    def close_connection_db(self):
        self.cur.close()
        self.conn.close()


portchannel_data, ten_gb_ethernet, gigabitethernet = parse_json()
r_db = RadkasDatabase()
r_db.insert_into_table(portchannel_data, portchannel=True)
r_db.insert_into_table(ten_gb_ethernet)
r_db.insert_into_table(gigabitethernet)
r_db.close_connection_db()
