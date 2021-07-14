
from dataclasses import dataclass

import logging

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values

from config import config


@dataclass
class Category:
    topic: str
    subtopic: str
    name: str
    url: str

@dataclass
class Product:
    topic1: str
    topic2: str
    topic3: str

    name: str
    id: str

    qty:    str
    measure: str

    price: float
    price_discount: float
    price_old: float



def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
            CREATE TABLE IF NOT EXISTS products (

                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,       
                store   varchar(100),
                topic1  varchar(200),
                topic2  varchar(200),
                topic3  varchar(200),        
                name  varchar(200),     
                id    integer,
                qty   varchar(20),
                measure  varchar(20),        
                price    NUMERIC(10,2),
                price_discount    NUMERIC(10,2),
                price_old    NUMERIC(10,2)
            )
        """,)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        logging.debug(f"Init table PRODUCTS")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Error creating table PRODUCTS: {error}")
    finally:
        if conn is not None:
            conn.close()

def write_products(products , store):
#"INSERT INTO products ( store , topic1 , topic2 , topic3 , name , id , qty , measure , price , price_discount , price_old  ) VALUES %s"
    products_tuple_list = []
    for product in products:
        products_tuple_list.append( ( store , product.topic1 , product.topic2 , product.topic3 ,  \
                                      product.name , product.id , product.qty , product.measure , \
                                      product.price , product.price_discount , product.price_old

                                     ) ) 

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        execute_values( cur , \
            "INSERT INTO products ( store , topic1 , topic2 , topic3 , name , id , qty , measure , price , price_discount , price_old  ) VALUES %s" , \
            products_tuple_list )
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Error saving products into database: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()


