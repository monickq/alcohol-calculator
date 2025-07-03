import pandas as pd
import streamlit as st
import time
import altair as alt

# read data from excel
data = pd.read_excel("data/alcohol_info.xlsx")

st.header(":blue[Blood Alcohol Content Calculator] " + "\U0001F377", divider="rainbow", width="stretch")
st.markdown("How much alcohol is in your :red[blood]?")

# choose sex
sex = st.radio("Choose sex:", ["male", "female"])

# weight
weight = st.slider("Enter weight (kg)", min_value=40, max_value=200)

# extract alcohol types from excel to list
types = data["Type"].dropna().unique().tolist()

# user's choice
alcohol_type = st.selectbox("Choose alcohol:", types)

# data type - matches user input with data in excel sheet
chosen_type = data[data["Type"] == alcohol_type].iloc[0]

# setting 1 portion for chosen alcohol
filtered_data = data[data["Type"] == alcohol_type]
portions = filtered_data["1 portion/ml"].dropna().unique().tolist()

amount = st.selectbox("1 portion (ml)", portions) 
amount_chosen = filtered_data[filtered_data["1 portion/ml"] == amount].iloc[0]

# portion amount
amount_of_portions = st.slider("How many portions?", 1, 20)

# time window
time_ago = st.number_input("How many hours ago?", min_value=1, max_value=24, step=1)

# formula for blood alcohol calculation
alcohol_percentage = chosen_type["Percentage"]
density = 0.789
r = 0.68 if sex == "male" else 0.55

def calculate_bac():
    alcohol_in_grams = alcohol_percentage*0.01 * amount * amount_of_portions  * density
    alcohol_beginning = alcohol_in_grams / (weight * r)
    result = round(((alcohol_beginning) - (time_ago * 0.15)), 2)
    if result >= 0:
        return result
    else:
        return "0.00 ‰"

bigmac_kcal = 550
kcal = chosen_type["kcal/portion"]
kcal_consumed = kcal * amount_of_portions
consumed_to_bigmac = (kcal_consumed/bigmac_kcal).__round__(1)

egg_kcal = 70
consumed_to_egg = (kcal_consumed/egg_kcal).__round__()


if st.button("Get result"):
    st.subheader("Your blood alcohol content is...")
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)
        time.sleep(0.01)
    time.sleep(1.25)
    st.title(f"{calculate_bac()} ‰")
    st.subheader(f"You also consumed {kcal_consumed} calories.")
    st.write(f"That's like {consumed_to_bigmac} of Big Mac or {consumed_to_egg} egg(s). " + "\U0001F4A1")
    st.write("\n")
    chart = alt.Chart(data).mark_line().encode(
        x= "Type",
        y = "kcal/portion"
    )

    st.subheader("Calories based on type of alcohol (1 portion)")
    st.altair_chart(chart, use_container_width=True)
