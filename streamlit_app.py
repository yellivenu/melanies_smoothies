# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session  ##sis version
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":apple: Customize Your Smoothie! :pineapple:")
st.write(
    """   Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your smoothie will be:", name_on_order)
    

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favourite fruit is :", option)

cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session() ##sis version
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose upto 5 ingredients:',my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/+ fruit_chosen+")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""', '"""+name_on_order+"""')"""
    time_to_insert=st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


