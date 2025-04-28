# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv('HotelBookingsData.csv')
        
    df_filtered = df[['email', 'room.name', 'hotel.name', 'nights', 'totalPrice', 'created']].copy()
    df_filtered.columns = ['email', 'room_type', 'hotel_name', 'nights_stayed', 'totalPrice', 'created']
    df_filtered['date'] = pd.to_datetime(df_filtered['created']).dt.date
    df_filtered['time'] = pd.to_datetime(df_filtered['created']).dt.strftime('%H:%M')
    return df_filtered

# --- Sidebar Upload ---
st.sidebar.header('Upload your Dataset 📂')
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Load Data
df_filtered = load_data(uploaded_file)


# --- Sidebar Navigation ---
st.sidebar.title('📊 Hotel Booking Insights')
page = st.sidebar.radio('Navigate', [
    'Overview',
    'Hotels with Most Bookings',
    'Room Types with Highest Bookings',
    'Most Frequent Customers',
    'Revenue by Hotel',
    'Revenue by Room Type',
    'Booking Frequency by Date',
    'Booking Frequency by Hour',
    'Stay Duration Frequency',
    'Average Length of Stay by Room Type'
])

# --- Pages Content ---
st.title('Hotel Booking Data Dashboard')

if page == 'Overview':
    st.subheader('📋 Dataset Overview')
    st.write('**Total Bookings:**', df_filtered.shape[0])
    st.dataframe(df_filtered.head())

elif page == 'Hotels with Most Bookings':
    st.subheader('Hotels with the Most Bookings')
    hotel_booking_counts = df_filtered['hotel_name'].value_counts().reset_index()
    hotel_booking_counts.columns = ['hotel_name', 'booking_count']
    plt.figure(figsize=(12,6))
    sns.barplot(data=hotel_booking_counts, x='booking_count', y='hotel_name', palette='viridis')
    st.pyplot(plt)

elif page == 'Room Types with Highest Bookings':
    st.subheader('Room Types with the Highest Bookings')
    room_booking_counts = df_filtered['room_type'].value_counts().reset_index()
    room_booking_counts.columns = ['room_type', 'booking_count']
    plt.figure(figsize=(12,6))
    sns.barplot(data=room_booking_counts, x='booking_count', y='room_type', palette='magma')
    st.pyplot(plt)

elif page == 'Most Frequent Customers':
    st.subheader('Top 10 Most Frequent Customers')
    top_customers = df_filtered['email'].value_counts().reset_index()
    top_customers.columns = ['email', 'booking_count']
    top_customers = top_customers.head(10)
    plt.figure(figsize=(12,6))
    sns.barplot(data=top_customers, x='booking_count', y='email', palette='coolwarm')
    st.pyplot(plt)

elif page == 'Revenue by Hotel':
    st.subheader('Total Revenue by Hotel')
    hotel_revenue = df_filtered.groupby('hotel_name')['totalPrice'].sum().reset_index().sort_values(by='totalPrice', ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(data=hotel_revenue, x='totalPrice', y='hotel_name', palette='Blues_d')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₦{int(x):,}"))
    st.pyplot(plt)

elif page == 'Revenue by Room Type':
    st.subheader('Total Revenue by Room Type')
    room_revenue = df_filtered.groupby('room_type')['totalPrice'].sum().reset_index().sort_values(by='totalPrice', ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(data=room_revenue, x='totalPrice', y='room_type', palette='Greens_d')
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₦{int(x):,}"))
    st.pyplot(plt)

elif page == 'Booking Frequency by Date':
    st.subheader('Booking Frequency by Date')
    booking_by_date = df_filtered['date'].value_counts().reset_index()
    booking_by_date.columns = ['date', 'booking_count']
    booking_by_date = booking_by_date.sort_values(by='date')
    plt.figure(figsize=(14,6))
    sns.lineplot(data=booking_by_date, x='date', y='booking_count', marker='o', color='dodgerblue')
    plt.xticks(rotation=45)
    st.pyplot(plt)

elif page == 'Booking Frequency by Hour':
    st.subheader('Booking Frequency by Hour')
    booking_by_hour = df_filtered['time'].str[:2].value_counts().reset_index()
    booking_by_hour.columns = ['hour', 'booking_count']
    booking_by_hour = booking_by_hour.sort_values(by='hour')
    plt.figure(figsize=(12,6))
    sns.barplot(data=booking_by_hour, x='hour', y='booking_count', palette='coolwarm')
    st.pyplot(plt)

elif page == 'Stay Duration Frequency':
    st.subheader('Stay Duration Frequency')
    stay_duration_freq = df_filtered['nights_stayed'].value_counts().reset_index()
    stay_duration_freq.columns = ['nights_stayed', 'frequency']
    stay_duration_freq = stay_duration_freq.sort_values(by='nights_stayed')
    plt.figure(figsize=(12,6))
    sns.barplot(data=stay_duration_freq, x='nights_stayed', y='frequency', palette='Set2')
    st.pyplot(plt)

elif page == 'Average Length of Stay by Room Type':
    st.subheader('Average Length of Stay by Room Type')
    avg_stay_by_room = df_filtered.groupby('room_type')['nights_stayed'].mean().reset_index().sort_values(by='nights_stayed', ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(data=avg_stay_by_room, x='nights_stayed', y='room_type', palette='Spectral')
    st.pyplot(plt)

