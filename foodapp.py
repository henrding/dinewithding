import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageOps

# Path to photos folder
PHOTOS_DIR = '/Users/henryding/Desktop/dinewithding/photos'

@st.cache_data
def load_data():
    return pd.read_csv('/Users/HenryDing/Desktop/dinewithding/foodie_data.csv')  # Replace with your CSV filename

data = load_data()

st.title("Dine with Ding: Restaurant Search")

all_cuisines = sorted(data['Cuisine'].dropna().unique())

all_prices = sorted(data['Price ($-$$$)'].dropna().unique())

# Get unique moods from data for filtering (assuming column is named 'Mood')
all_moods = sorted(data['Mood'].dropna().unique())

st.sidebar.header("Filter Options")

selected_cuisines = st.sidebar.multiselect("Select Cuisine(s):", all_cuisines)
selected_prices = st.sidebar.multiselect("Select Price Tier(s):", all_prices)
selected_moods = st.sidebar.multiselect("Select Mood(s):", all_moods)

search_name = st.sidebar.text_input("Search Restaurant Name (optional):").strip().lower()

filtered = data.copy()

if selected_cuisines:
    filtered = filtered[filtered['Cuisine'].isin(selected_cuisines)]

if selected_prices:
    filtered = filtered[filtered['Price ($-$$$)'].isin(selected_prices)]

if selected_moods:
    filtered = filtered[filtered['Mood'].isin(selected_moods)]

if search_name:
    filtered = filtered[filtered['Restaurant'].str.lower().str.contains(search_name)]

if filtered.empty:
    st.write("No results found with the selected filters.")
else:
    st.write(f"Found {len(filtered)} results:")

    for idx, row in filtered.iterrows():
        st.subheader(row['Restaurant'])
        st.write(f"Cuisine: {row['Cuisine']}")
        st.write(f"Price: {row['Price ($-$$$)']}")
        st.write(f"Mood: {row['Mood']}")
        st.write(f"Dish(es): {row['Dish(es)']}")

        image_filename = f"IMG_{idx + 2}.jpeg"
        img_path = os.path.join(PHOTOS_DIR, image_filename)

        if os.path.isfile(img_path):
            try:
                image = Image.open(img_path)
                image = ImageOps.exif_transpose(image)
                st.image(image, use_container_width=True)
            except Exception as e:
                st.write(f"Error loading image: {e}")
        else:
            st.write("Image file not found.")
