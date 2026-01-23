import sqlite3
import polars as pl
import json
from dataclasses import dataclass,asdict
from typing import Optional

from matplotlib.style.core import available


@dataclass
class Member:
    Name: Optional[str] = None
    Rank: Optional[str] = None

@dataclass
class Ranks:
    ID: Optional[int] = None
    Name: Optional[str] = None


def create_Database_connect():
    conn=sqlite3.connect('BattleBots.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn



def get_category_from_database():
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT category_name FROM Category
        """)
        items = cursor.fetchall()
        item_list=[item[0] for item in items]
        conn.close()
        return item_list
    except sqlite3.Error as e:
        return f"Error retrieving categories from database: {e}"



def get_category_tags(category_name):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT Item_filter_tags FROM Category
        WHERE category_name=?
        """,(category_name,))
        items = cursor.fetchall()[0][0]
        #print(list(items))
        if items is not None:
            lst=json.loads(items)
            return lst
        return ""
    except sqlite3.Error as e:
        return f"Error retrieving tags from database: {e}"

def remove_category_from_database(category_name):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        DELETE FROM Category
        WHERE category_name=?
        
        """,(category_name,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return f"Error removing tags from database: {e}"


def insert_new_filter_tag(new_List:str,category):
    try:
        #print(type(new_List))
        conn=create_Database_connect()
        cursor=conn.cursor()

        cursor.execute("""
            UPDATE Category 
            SET Item_filter_tags=?
            WHERE category_name=?
        """,(new_List,category))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
            return f"Error updating filter tags in database: {e}"


def insert_new_category(category_name):
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()
        cursor.execute("""
              INSERT INTO Category(category_name) 
              VALUES (?)
          """, (category_name,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return f"Issue adding new category to database: {e} "


def delete_everything_from_database(database=""):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        DELETE FROM ?
        """,(database,))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return f"error delete rows from database: {e}"



def delete_room_from_database(room_name):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        DELETE FROM Room
        WHERE RoomName=?
        
        """,(room_name,))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return f"Error deleting room {e}"



def delete_item_from_Database(item_name):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        DELETE FROM  Items
        WHERE ItemName=?
        """,(item_name,))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return f"Error deleting item {e}"




def add_new_room_to_database(room_name,room_desc,Room_Image=None):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        INSERT INTO Room (RoomName,RoomDescription,Room_Image)
        VALUES (?, ?,?)
    """, (room_name,room_desc,Room_Image))
        conn.commit()
        conn.close()



    except sqlite3.Error as e:
        return f"Issue adding new room to database: {e} "


def get_items_by_subCategory(subCategory,tags:list):
    filter_item=[]
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()

        cursor.execute("""
                SELECT ItemName,ItemDescription,ItemPrice,ItemQuanity,RoomName AS Item_Stroage_Location,part_image,SubCategory FROM
                Items I JOIN Room R on I.RoomLOCATIONStorageID=R.RoomId WHERE I.SubCategory= ? 

                """, (subCategory,))
        items = cursor.fetchall()
        conn.close()

        if len(tags) > 0:
            for item in items:
                item_name = item[0]
                item_desc = item[1]
                for tag in tags:
                    if tag.lower() in item_name.lower() or tag.lower() in item_desc.lower():
                        filter_item.append(item)

            return filter_item

        if len(tags) == 0:
            return items

        return items




    except sqlite3.Error as e:
        return f"Error retrieving items from database: {e}"




def get_items_by_category(category, tags:list):
    if tags is None:
        tags = []
    #print(tags)
    filter_item=[]
    conn=create_Database_connect()
    cursor=conn.cursor()


    cursor.execute("""
        SELECT ItemName,ItemDescription,ItemPrice,ItemQuanity,RoomName AS Item_Stroage_Location,part_image,SubCategory FROM
        Items I JOIN Room R on I.RoomLOCATIONStorageID=R.RoomId WHERE I.ItemCategory= ? 
    
        """,(category,))
    items=cursor.fetchall()
    conn.close()



    if len(tags)>0:
        for item in items:
            item_name = item[0]
            item_desc=item[1]
            for tag in tags:
                if tag.lower() in item_name.lower() or tag.lower() in item_desc.lower():
                    filter_item.append(item)

        return filter_item

    if len(tags)==0:
        return items

    return items



def get_rooms():
    room_list=[]
    conn=create_Database_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT RoomName FROM Room")
    rooms = cursor.fetchall()
    room_list = [room[0] for room in rooms]
    conn.close()
    return room_list



def get_table_in_database():
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' and name NOT LIKE 'sqlite_%'
        """)
        tables=cursor.fetchall()
        table_list=[table[0] for table in tables]
        conn.close()
        return table_list
    except sqlite3.Error as e:
        return f"Error getting tables in database {e}"






def item_Or_room_exists(mode,room=None,item=None):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        if mode=='Item':
            cursor.execute("""
            SELECT ItemName FROM Items
            WHERE ItemName=?
            """,(item,))

        if mode=="Room":
            cursor.execute("""
            SELECT RoomName FROM Room
            WHERE RoomName=?
            """,(room,))

        result=cursor.fetchone()
        conn.close()
        return result is not None

    except sqlite3.Error as e:
        return f"Error deleting {mode} : {e}"

def export_database_to_dataframe(table_name):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`")

        rows=cursor.fetchall()
        conn.close()
        col_names=[desc[0] for desc in cursor.description]
        df=pl.DataFrame(rows,schema=col_names)
        return df
    except sqlite3.Error as e:
        return f"Error: {e}"


def update_item(itemDescription,ItemPrice):
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("""
    UPDATE Items 
    SET ItemDescription=?,ItemPrice=? 
    
    """,(itemDescription,ItemPrice))

def getRoomID(room_name):
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("SELECT RoomID FROM Room WHERE RoomName = ?", (room_name,))
    room_id = cursor.fetchone()
    conn.close()
    return room_id[0] if room_id else None


def get_items():
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("""
    SELECT ItemName FROM Items
    """)
    items=cursor.fetchall()
    items = [row[0] for row in items ]
    return items


def get_all_items_by_category(ItemCategory):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT ItemName,ItemDescription,ItemPrice,ItemQuanity,RoomName AS Item_Stroage_Location,part_image FROM Items I JOIN Room R on I.RoomLOCATIONStorageID=R.RoomId
        WHERE I.ItemCategory=?
        
        """,(ItemCategory,))
        items_by_category=cursor.fetchall()
        #print(items_by_category)
        columns_for_item_by_category=[desc[0] for desc in cursor.description]
        df=pl.DataFrame(items_by_category,schema=columns_for_item_by_category,orient="row")
        conn.close()
        return df
    except sqlite3.Error as e:
        return f"Error retrieving items :{e}"


def get_item_categories():
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT DISTINCT ItemCategory FROM Items
        """)
        category = cursor.fetchall()
        conn.close()
        return [cat[0] for cat in category]


    except sqlite3.Error as e:
        return f"Error retrieving item categories: {e}"






def insertNewSubCategory(name,CategoryName):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT ID FROM Category WHERE category_name=?
        """,(CategoryName,))
        CategoryId=cursor.fetchone()[0]
        #print(CategoryId)

        cursor.execute("""
        INSERT INTO SubCategory(Name,CategoryID) VALUES(?,?)
        """,(name,CategoryId))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return f"Error adding new SubCategory :{e}"



def get_subCategories(CategoryName):
    try:
        conn=create_Database_connect()
        cursor=conn.cursor()

        cursor.execute("""
               SELECT ID FROM Category WHERE category_name=?
               """, (CategoryName,))
        CategoryId = cursor.fetchone()[0]

        cursor.execute("""
        SELECT Name FROM SubCategory
        WHERE CategoryID=?
        """,(CategoryId,))
        Subcategories=cursor.fetchall()
        conn.close()
        Subcategories_list=[Subcategory[0] for Subcategory in Subcategories]

        return Subcategories_list

    except sqlite3.Error as e:
        return f"Error retrieving sub categories: {e}"


def check_items_exist_in_database():
    try:

        conn=create_Database_connect()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT ItemName FROM Items""")
        items=cursor.fetchall()

        if len(items)==0:
            return False
        else:
            return True




    except sqlite3.Error as e:
        return f"Error retrieving items: {e}"


def insertNewItem(item_name,item_desc,item_price,item_category,room_Location_id:int,image,itemAmount,Subcategory):
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("""
    INSERT INTO Items (ItemName, ItemDescription, ItemPrice, ItemCategory,RoomLOCATIONStorageID,part_image,ItemQuanity,SubCategory)
    VALUES (?, ?, ?, ?,?,?,?,?)
    """, (item_name, item_desc, item_price, item_category,room_Location_id,image,itemAmount,Subcategory))
    conn.commit()
    conn.close()

def get_item_details(item_name):
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("""
    SELECT ItemName, ItemDescription, ItemPrice, ItemCategory, RoomLOCATIONStorageID,part_image,ItemQuanity,SubCategory
    FROM Items
    WHERE ItemName = ?
    """, (item_name,))
    item_details = cursor.fetchone()
    conn.close()
    return item_details



def get_Ranks():
    conn=create_Database_connect()
    cursor=conn.cursor()
    cursor.execute("""
    SELECT RANK_Name FROM Ranks
    """)
    ranks=cursor.fetchall()
    conn.close()
    return ranks

def add_members(MemberName,rank_id=1):
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Members(Name) VALUES(?)
        """, (MemberName,))

        assigned_member_id=cursor.lastrowid #Gets the last auto_generated_Id

        cursor.execute("""
        INSERT INTO MemberRanks(Member_ID,RANk_ID) VALUES(?,?)
        
        """,(assigned_member_id,rank_id))


        conn.commit()
        print(f"Added member: {MemberName}")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()




def return_club_members():
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT M.Name,R.RANK_Name FROM Members M
        JOIN MemberRanks MR  ON M.ID = MR.Member_ID
        JOIN Ranks R on MR.Rank_ID = R.ID
        
        """)
        members=pl.DataFrame([asdict(Member(Name=member[0],Rank=member[1])) for member in cursor.fetchall()])
        return True,members.to_pandas()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


def update_Members_ranks(MemberName,new_rank):
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()


        cursor.execute("""
        SELECT ID FROM Ranks
        WHERE RANK_NAME= ?
        """,(new_rank,))
        new_rank_id=cursor.fetchone()[0]


        cursor.execute("""
        SELECT ID FROM Members WHERE Name = ?
        """,(MemberName,))
        MemberID=cursor.fetchone()[0]

        cursor.execute("""
        UPDATE MemberRanks SET RANK_ID = ? WHERE Member_ID = ?""",(new_rank_id,MemberID))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


def get_ranks():
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Ranks;
        
        """)
        available_ranks=[Ranks(ID=ranks[0],Name=ranks[1]) for ranks in cursor.fetchall()]
        return available_ranks



    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()




def remove_member(Member_ID):
    try:
        conn = create_Database_connect()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM Members
        WHERE ID=?

                       """,(Member_ID,))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()



