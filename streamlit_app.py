# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
session = get_active_session()

# Write directly to the app
st.title("Victim Resources in Montana")
st.write(
    """To have your Victim Resources added to the collection
    and displayed on the Victim Resources Map, 
    please enter the following information.
    """
)

name_of_organization = st.text_input("Name of the organization: ")

counties_served_df = session.table("VICTIM_SERVICES_DB.INFO.COUNTIES").select(col('COUNTY_NAME'))
#st.dataframe(data=counties_served_df, use_container_width=True)

counties_served_list = st.multiselect(
    "Please choose the counties your organization provides services in: ",
    counties_served_df)

mailing_address = st.text_input("Mailing Address: ")

cities_df = session.table("VICTIM_SERVICES_DB.INFO.CITIES_TOWNS").select(col('CITY_TOWN_NAME'))
#st.dataframe(data=cities_df, use_container_width=True)

cities_list = st.selectbox(
    "City: ",
    cities_df,
    index=None,
    placeholder="Please select a city")

state = st.selectbox(
    "State: ", ["MT"],
    index=None,
    placeholder="Please select state")

zip_code = st.text_input("Zip Code: ")

crisis_phone = st.text_input("24 Hour Hotline: ")

org_phone = st.text_input("Phone Number: ")

email_address = st.text_input("Email Address: ")

website = st.text_input("Website Address: ")

tribal = st.selectbox(
    "Is this organization affiliated with a tribal agency?",
    ["Yes", "No"],
    index=None,
    placeholder="Please choose Yes or No.")

agency_description_df = session.table("VICTIM_SERVICES_DB.INFO.DESCRIPTION_OF_AGENCY").select(col('DOA'))
#st.dataframe(data=agency_description_df, use_container_width=True)

agency_description_list = st.multiselect(
    "Please choose each description that represents your organization: ",
    agency_description_df)

services_provided_df = session.table("VICTIM_SERVICES_DB.INFO.SERVICES_PROVIDED").select(col('SERVICES'))
#st.dataframe(data=services_provided_df, use_container_width=True)

services_provided_list = st.multiselect(
    "Please choose each services that represents your organization: ",
    services_provided_df)
    
submitted_by = st.text_input("First and Last Name of person submitting this request: ")

submitted_by_phone = st.text_input("Phone Number you can be reached at: ")

submitted_by_email = st.text_input("Email Address you can be reached at: ")


#-------------------------------------------------------------------------------------
# Please review the following information:
#_____________________________________________________________________________________

st.title("Please review the following information: ")

if name_of_organization:
    st.write("The name of the resource is: ", name_of_organization)

if counties_served_list:

    counties_served_string = ''

    for counties_chosen in counties_served_list:
        counties_served_string += counties_chosen + ', '

    st.write("Counties Served: ", counties_served_string)    
    
if mailing_address:
    st.write("Mailing Address: ", mailing_address) 

if cities_list:
    st.write("City: ", cities_list)

if state:
    st.write("State: ", state)

if zip_code:
    st.write("Zip Code: ", zip_code)

if crisis_phone:
    st.write("24 Hour Hotline: ", crisis_phone)

if org_phone:
    st.write("Phone Number: ", org_phone)

if email_address:
    st.write("Email Address: ", email_address)

if website:
    st.write("Website: ", website)

if tribal:
    st.write("Tribal Services Provided: ", tribal)

if agency_description_list:
   # st.write("Description of Agency: ", agency_description_list)
    
    agency_description_string = ''

    for agency_description_chosen in agency_description_list:
        agency_description_string += agency_description_chosen + ', '

    st.write("Agency Descriptions Chosen: ", agency_description_string)  

if services_provided_list:
    #st.write("Services Provided: ", services_provided_list)
    
    services_provided_string = ''

    for services_provided_chosen in services_provided_list:
        services_provided_string += services_provided_chosen + ', '

    st.write("Agency Descriptions Chosen: ", services_provided_string)

if submitted_by:
    st.write("Request Submitted By: ", submitted_by)

if submitted_by_phone:
    st.write("Requestor's Phone Number: ", submitted_by_phone)

if submitted_by_email:
    st.write("Requestor's Email Address: ", submitted_by_email)

    my_insert_stmt = """ insert into victim_services_db.info.new_entries
        (
        name_of_organization,
        counties_served, 
        mailing_address,
        city,
        state,
        zip_code,
        crisis_hotline,
        phone_number,
        email_address,
        website,
        tribal_agency,
        description,
        services,
        submitted_by_name,
        submitted_by_phone,
        submitted_by_email
        )
        values (
        '"""+ name_of_organization + """',
        '"""+ counties_served_string +"""',
        '"""+ mailing_address +"""',
        '"""+ cities_list +"""',
        '"""+ state +"""',
        '"""+ zip_code +"""',
        '"""+ crisis_phone +"""',
        '"""+ org_phone +"""',
        '"""+ email_address +"""',
        '"""+ website +"""',
        '"""+ tribal +"""',
        '"""+ agency_description_string +"""',
        '"""+ services_provided_string +"""',
        '"""+ submitted_by +"""',
        '"""+ submitted_by_phone +"""',
        '"""+ submitted_by_email +"""'
        )"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Request')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.write("Your request has been submitted", submitted_by)

