import json
import sqlite3
import streamlit as st
import streamlit_authenticator  as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_searchbox import st_searchbox
import database_backend as db
import time
import polars as pl
import pandas as pd
from pathlib import Path
from encrypt_file import encryptAndDecrypt
import streamlit_shadcn_ui as ui



def display_tag_add_deletion(tags_list:list=None,type='add'):

    if type=='remove':
        with st.form(f" Remove filter tag", clear_on_submit=True):
            tag_to_remove = st.multiselect("Please select which tag you want to remove", options=[""] + item_tags)
            remove_tag_button = st.form_submit_button(f"Remove Tag", type="primary")
            print(tag_to_remove)
            if remove_tag_button:
                valid_flag_for_removal = True
                if len(tag_to_remove) == 0:
                    valid_flag_for_removal = False
                    st.error("Please select at least one tag to remove")

                if valid_flag_for_removal:
                    for tag in tag_to_remove:
                        tags_list.remove(tag)
                        
                    st.success(f"{tag_to_remove} has been successfully removed from {category_to_add_new_fiter}")
                    
                    
                    db.insert_new_filter_tag(json.dumps(tags_list), category_to_add_new_fiter)
                time.sleep(1.5)
                st.rerun()


    if type=='add':

        with st.form(f"Add new filter tag", clear_on_submit=True):
            new_tag = st.text_input(f"Add new filter tag for {category_to_add_new_fiter}")
            submit_new_filter_tag = st.form_submit_button("Add new filter tag", type='primary')


            if tags_list is None:
                tags_list = []

            if submit_new_filter_tag:
                valid_Flag = True
                if len(new_tag) == 0:
                    valid_Flag = False

                if new_tag in tags_list:
                    valid_Flag = False
                    st.error(f"{new_tag} tag for {category_to_add_new_fiter} already exists in database")

                if valid_Flag:
                    tags_list.append(new_tag)
                    st.success(
                        f'{new_tag} tag for {category_to_add_new_fiter} has been added to database')
                    #print(tags_list)
                    print(db.insert_new_filter_tag(json.dumps(tags_list), category_to_add_new_fiter))
                time.sleep(1.5)
                st.rerun()




def reterive_categories_as_datafrfame(retrive_column="cat"):
    conn=sqlite3.connect('BattleBots.db')


    df=pd.read_sql_query("SELECT category_name as Category FROM Category",conn)
    return df



def display_items(category_items,chosen_category,selected_tags):
    for idx,item in enumerate(category_items):
        item_name,item_desc,price,stock,item_loc,ImageOfPart=item
        with st.expander(f"{chosen_category}_{idx+1}",expanded=True):
            if ImageOfPart is not None:
                st.image(ImageOfPart,width=200)
            st.write(f"**Item Name:** {str(item_name).capitalize()}")
            st.write(f"**Item Description:** {item_desc}")
            st.write(f"**Item Price:** CAD $ {price:.2f}")
            st.write(f"**Currently in stock**: {stock}")
            st.write(f"**Storage Location:** {item_loc}")




d=encryptAndDecrypt()
login_file=d.decrypt()
#with open(login_file, "r") as file:
config = yaml.load(login_file, Loader=SafeLoader)
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

st.logo(
    image="logo_images/BattleBotsLogo.png",size="large")
st.title("Welcome to the BattleBots Management System")
st.image(image="logo_images/Logo_40.png")
st.write("To access the database, please log in.")


@st.dialog("Confirm your table you want to delete")
def confirm(table):
    st.write(f"Do you want to clear {table}")
    if st.button("YES"):
        st.session_state.confirm={'confirm':'YES'}
        st.rerun()

    if st.button("NO"):
        st.session_state.confirm = {'confirm': 'NO'}
        st.rerun()



def returnItemNames(query:str):
    conn=sqlite3.connect('BattleBots.db')
    #print(query)
    if not query:
        return []
    result= conn.execute(f"""
    SELECT ItemName 
    FROM Items
    WHERE lower(ItemName) LIKE '%{query.lower()}%'
    LIMIT 10
    """).fetchall()

    return [row[0] for row in result]


try:
    authenticator.login()
    if st.session_state.get('authentication_status'):
        st.write(f'Welcome *{st.session_state.get("name")}*')
        tab1,tab2,tab3,tab4=st.tabs(["**View Items** 🔍 ", "**Add new Items or Delete Item** (➕/➖)", "**Update Items**","**Admin Page** 🖥️🔑"])
        with tab1:
            view_all_items_by_category=st.toggle("View all items by category")
            current_category=db.get_category_from_database()

            if view_all_items_by_category:
                chosen_category=st.selectbox("Please select which category you want to view",options=[""]+current_category)


                if chosen_category:
                    filter_tags=db.get_category_tags(chosen_category)



                    select_tags=st.multiselect("filter options",options=filter_tags)


                    category_items = db.get_items_by_category(chosen_category,select_tags)

                    if len(filter_tags)>0:
                        print("TEST")

                        if len(category_items)==0 and len(select_tags)>0:
                            st.warning(f"⚠️ No items found in the {chosen_category} category with the selected tags")

                        elif len(category_items)==0 and len(select_tags)==0:
                            st.warning(f"⚠️ No items found in the {chosen_category} category")
                    else:
                        st.warning(f"⚠️ There are no **filter tags** found for {chosen_category} category please add them in the admin page ")


                    display_items(category_items,chosen_category,select_tags)



                   
            else:
                st.subheader("View Items")
                selected_item=st_searchbox(returnItemNames,placeholder="Search for an item",key="LookupItem")
                if selected_item:
                    item_name, item_desc, price, category, roomLocationID,ImageOfPart,ItemAmount=db.get_item_details(selected_item)
                    if ImageOfPart is not None:
                        st.image(ImageOfPart,width=200)

                    with st.expander(expanded=True,label='Item'):
                        st.write(f"**Item Name:** {item_name}")
                        st.write(f"**Item Description:** {item_desc}")
                        st.write(f"**Item Price:** CAD $ {price:.2f}")
                        st.write(f"**Amount**: {ItemAmount}")
                        st.write(f"**Item Category:** {category}")
                        room_name = db.get_rooms()[roomLocationID-1] if roomLocationID else "Unknown"
                        st.write(f"**Storage Location:** {room_name}")




        with tab2:
            on=st.toggle("Delete Item")

            if on:
                is_valid = True
                Delete_type=st.selectbox(label="Please select what you want to delete",options=["","Room","Item"])
                if Delete_type=="Item":
                    items = db.get_items()
                    item_to_delete_from_database=st.multiselect("Select the item",options=items)

                    if item_to_delete_from_database:
                        confirm_button = st.button(f"Delete {item_to_delete_from_database} ", type='primary')
                    else:
                        st.write("Please select an item to delete")

                    confirm_button=st.button(f"Delete {item_to_delete_from_database} ", type='primary')
                    if confirm_button:
                        is_valid=True
                        if len(item_to_delete_from_database)==0:
                            is_valid=False
                            st.error(f"⚠️ Please select a Item to remove")

                        if is_valid:
                            db.delete_item_from_Database(item_to_delete_from_database)
                            st.success(f"✅ {item_to_delete_from_database} has been successfully deleted")
                            time.sleep(2.0)
                            st.rerun()

                if Delete_type=="Room":
                    rooms=db.get_rooms()
                    room_to_remove=st.selectbox(label="Please select which room you would like to remove",options=[""]+rooms)
                    confirm_remove_room_button=st.button(f"Remove {room_to_remove} ",type="primary")
                    if confirm_remove_room_button:
                        if len(room_to_remove)==0:
                            is_valid=False
                            st.error("⚠️ Please select a room to remove")

                        if is_valid:
                            db.delete_room_from_database(room_to_remove)
                            st.success(f"✅ {room_to_remove} has been successfully deleted")
                            time.sleep(2.0)
                            st.rerun()

            else:
                st.subheader("Please add a new item you want to the database")
                with st.expander("✏️ Add New Items to database"):

                    with st.form("Add new Item",clear_on_submit=True):
                        rooms = db.get_rooms()
                        item_Name=st.text_input("Item Name",key="item_name")
                        item_desc=st.text_area("Item Description",key="item_description")
                        item_price=st.number_input("Item Price",key="item_price",min_value=0.0,step=0.01)
                        item_category=st.selectbox("Item Category",options=[""]+db.get_category_from_database(),key="item_category")
                        storageLocation=st.selectbox("Storage Location",key="storage_location",options=[""]+db.get_rooms())
                        itemQuality=st.number_input("Please enter how many of the item you have",min_value=0,step=1)
                        image= st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"], key="item_image")
                        submitted = st.form_submit_button("Add Item",type="primary")


                    if submitted:
                        Valid = True
                        room_id=db.getRoomID(storageLocation)
                        if image is not None:
                            image_data=image.read()
                        if image is None:
                            image_data=None


                        itemInDatabaseCheck=db.item_Or_room_exists(mode="Item",item=item_Name)


                        if len(item_Name)==0:
                            Valid=False
                            st.error("⚠️ **Error**: Please enter the items name")

                        if itemQuality==0:
                            Valid=False
                            st.error("⚠️ **Error**: Please enter a Quantity greater than 0")

                        if len(item_category)==0:
                            Valid=False
                            st.error("⚠️ **Error**: Please enter a Category")

                        if len(storageLocation)==0:
                            Valid=False
                            st.error("⚠️ **Error**: Please select a Room")

                        elif itemInDatabaseCheck:
                            Valid = False
                            st.error(f"{item_Name} already exist")

                        if not itemInDatabaseCheck and Valid:
                            db.insertNewItem(item_Name, item_desc, item_price, item_category, room_id, image_data, itemQuality)
                            st.success(f"{item_Name} has been added to database")
                            time.sleep(2.0)
                            st.rerun()

                        time.sleep(3.0)
                        st.rerun()

                with st.expander("🏢 Add a new room location"):
                    with st.form("Add new room to database"):
                        room_name=st.text_input("Room name",key="RoomName")
                        room_desc=st.text_area("Room Description",key="RoomDesc")
                        room_image = st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"],
                                                 key="Room_image")
                        room_submitted = st.form_submit_button("Add Item", type="primary")

                        if room_submitted:
                            Valid = True
                            if room_image:
                                room_image_data=room_image.read()
                            if room_image is None:
                                room_image_data=None

                            itemInDatabaseCheck = db.item_Or_room_exists(mode="Room", room=room_name)


                            if len(room_name)==0:
                                Valid=False
                                st.error("⚠️ **Error**: Please enter the room Name")



                            if len(room_desc)==0:
                                Valid=False
                                st.error("⚠️ **Error**: Please enter the room's Description")


                            elif itemInDatabaseCheck:
                                Valid=False
                                st.error(f"{room_name} already exist")


                            if not itemInDatabaseCheck and Valid==True:
                                db.add_new_room_to_database(room_name, room_desc,room_image_data)

                            time.sleep(2.0)
                            st.rerun()

        with tab3:
            st.subheader("Update items in the database")

            with st.form("Update Item"):
                item_to_update=st.selectbox("Item Name to Update",key="update_item_name",options=[""]+db.get_items())
                new_desc=st.text_area("New Item Description",key="update_item_description")
                new_price=st.number_input("New Item Price",key="update_item_price",min_value=0.0,step=0.01)
                #new_category=st.selectbox("New Item Category",["","Screws","Battery","Wheels","ESC"],key="update_item_category")
                submitted_update = st.form_submit_button("Update Item",type="primary")
                if submitted_update:
                    db.update_item(new_price,new_desc)
                    time.sleep(2.0)
                    st.success()
                    st.rerun()

        with tab4:

            tables = db.get_table_in_database()
            st.subheader("Admin Page")
            with st.expander("Download tables to csv file"):
                download_specific_category = st.toggle("Download csv file of specific item by category")

                if download_specific_category:
                    st.subheader("Download Category Mode")
                    item_category=db.get_item_categories()
                    item_category_to_download=st.selectbox(label="Chose which category you want to download",options=[""]+item_category)

                    if len(item_category_to_download)>0 :
                       #get_items_button = st.button(f"Get all items from {item_category_to_download}")
                        #if get_items_button:
                        items_for_cat=db.get_all_items_by_category(item_category_to_download)
                        st.dataframe(items_for_cat)
                        st.download_button(label=f"📥 Download all items from  {item_category_to_download} Category",file_name=f"{item_category_to_download}_items.csv",data=items_for_cat.write_csv(),
                                               mime="text/xlsx",type="primary")


                else:
                    st.subheader("Download Table Mode")
                    table_to_view = st.selectbox(label="Chose which table to view",options=[""]+tables)
                    if table_to_view:
                        table_as_dataframe = db.export_database_to_dataframe(table_to_view)
                        st.dataframe(table_as_dataframe, use_container_width=True, hide_index=True)
                        psd=table_as_dataframe.write_csv()
                        st.download_button(label=f"📥 Download {table_to_view} to csv ", data=psd,
                                    file_name=f'{str(table_to_view).lower().capitalize()}.csv', mime='text/xlsx',
                                    type="primary")
            with st.expander("Upload csv file or download template"):
                template_to_download=st.selectbox("Please select which template you would like to download",options=[""]+tables)
                if template_to_download:
                    template_path=Path(f'Template/{template_to_download}_template.csv')
                    csv_bytes=template_path.read_bytes()
                    st.download_button(label=f"📥 Download template for {template_to_download} table",file_name="Items_template.csv", mime='text/xlsx',data=csv_bytes,type="primary")
                csv_file=st.file_uploader(label="Please upload the csv file",type=['csv'],accept_multiple_files=False)
                upload_button=st.button("Upload")

                if upload_button and csv_file is not None:
                    table_name=str(csv_file.name).split('.')[0]
                    upload_file_to_dataframe=pl.read_csv(source=csv_file).to_pandas()

                    try:
                        conn=db.create_Database_connect()
                        upload_file_to_dataframe.to_sql(table_name,conn,if_exists='replace',index=False)
                        conn.commit()




                    except Exception as e:
                        print(f"Upload issue {e}")


                    finally:
                        conn.close()
                        st.success(f"{csv_file.name} has been successfully uploaded")
                        time.sleep(0.5)
                        st.rerun()
            with st.expander("Add new Category or item filter tags"):
                item_filter_toggle=st.toggle("Add item filter tags")

                if item_filter_toggle:
                    categories=[cat[0] for cat in reterive_categories_as_datafrfame().values]
                    category_to_add_new_fiter=st.selectbox("Please select a category that you want to add new filter ",[""]+categories)
                    if category_to_add_new_fiter:

                        item_tags=db.get_category_tags(category_to_add_new_fiter)
                        


                        if len(item_tags)>0:
                            with st.expander(f"Filter tags for {category_to_add_new_fiter} category",expanded=True):
                                #st.write("TEST")
                                for tag in range(0,len(item_tags)):
                                    st.write(f"{tag+1} - **{item_tags[tag]}**")

                            display_tag_add_deletion(item_tags,type='add')

                            add_or_remove_tags=st.toggle("Remove Filter tags")

                            if add_or_remove_tags:
                                display_tag_add_deletion(item_tags,type='remove')

                        



                        else:
                            st.warning(f"No filter tags found for {category_to_add_new_fiter} please add one")
                            display_tag_add_deletion(type='add')




                        #print(category_to_add_new_fiter)
                        #get_category_tags(category_name)



                        #st.write(item_tags[0])


                else:
                    cat=db.get_category_from_database()
                    #category_df = reterive_categories_as_datafrfame()
                    #st.dataframe(category_df,width='stretch',hide_index=True)
                    category_submit_valid=True
                    
                    if len(cat) > 0:
                        with st.expander("Current Categories",expanded=True):
                            for category in range(0,len(cat)):
                                st.write(f"{category+1} - {cat[category]}")

                    else :
                        st.warning("No categories are in the database!")

                    toggle_button_to_remove_category=st.toggle("Remove Category")


                    if toggle_button_to_remove_category:
                        categories=db.get_category_from_database()
                        st.subheader("Please select a category that you want to remove")
                        with st.form("Remove Category",clear_on_submit=True):
                            category_to_remove=st.multiselect("Please select a category that you want to remove",[""]+categories)
                            category_to_remove_button=st.form_submit_button(label="Remove Category",type="primary")
                            if category_to_remove_button:
                                valid_remove_category_flag=True
                                if len(category_to_remove)==0:
                                    valid_remove_category_flag=False
                                    st.error("Please select a category that you want to remove")

                                if valid_remove_category_flag:
                                    for c in categories:
                                        print(c)
                                        db.remove_category_from_database(c)
                                    st.success(f"✅ {category_to_remove} has been successfully removed")
        
                                time.sleep(1.5)
                                st.rerun()

                    else:

                        with st.form("Add new Category to database",clear_on_submit=True):
                            category_name=st.text_input("Please enter the new category you want to add").capitalize()
                            submit_new_category=st.form_submit_button("Add Category", type="primary")
                            if submit_new_category:
                                if len(category_name)==0:
                                    category_submit_valid=False
                                    st.error("⚠️ Please enter a category name")
                                    time.sleep(1.5)
                                    st.rerun()

                                if category_name in db.get_category_from_database():
                                    category_submit_valid=False
                                    st.error(f"⚠️ {category_name} Category already exist in the database")
                                    time.sleep(1.5)
                                    st.rerun()

                                if category_submit_valid:
                                    print(db.insert_new_category(category_name))
                                    st.success(f"✅ {category_name} has been successfully added to the database")
                                    time.sleep(1.5)
                                    st.rerun()





                            #db.insert_new_category(category_name.capitalize())
                            #st.success(f"✅ {category_name} has been successfully added to the database")
                            #time.sleep(1.5)
                            #st.rerun()






            with st.expander("Clear Table info"):
                choice=st.selectbox("Please select which table you want to clear",options=[""]+db.get_table_in_database())
                if len(choice)>0:
                    delete=st.toggle("Delete")
                    if delete:
                        delete_button=st.button(f"Delete {choice}",type='primary')
                        if delete_button:
                            db.delete_everything_from_database(choice)




        authenticator.logout()
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')

    with open('../config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


except Exception as e:
    st.error(e)



