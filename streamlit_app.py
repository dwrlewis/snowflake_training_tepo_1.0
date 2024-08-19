# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of the Smoothie will be", name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) #.select(col('FRUIT_NAME') isolated to single column
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

# option = st.selectbox(
#     'What is your favourite fruit?', 
#     ('Banana', 'Strawberries', 'Peaches'))
# st.write('Your favourite fruit is:', option)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# multiset data in ingredients_list is python list, it can be queried:
#st.write(ingredients_list) # list with ids, similar to dictionary format
#st.text(ingredients_list) # traditional python list

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            st.subheader(fruit_chosen + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')""" 

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


