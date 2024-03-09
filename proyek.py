import os
from matplotlib import figure
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg') 

order_items = pd.read_csv('order_items_dataset.csv')
products = pd.read_csv('products_dataset.csv')
product_category_name_translation = pd.read_csv('product_category_name_translation.csv')
sellers = pd.read_csv('sellers_dataset.csv')
customers = pd.read_csv('customers_dataset.csv')

# EDA Functions
def explore_product_interest(order_items, products, product_category_name_translation):
    # Gabungkan data dari ORDER ITEMS dan PRODUCTS
    order_product = pd.merge(order_items[['order_id','order_item_id', 'product_id', 'seller_id']], 
                             products[['product_id', 'product_category_name']], 
                             on='product_id')

    # Gabungkan berdasarkan product_id dan product_category_name, kemudian hitung total
    order_product_combined = order_product.groupby(['product_id', 'product_category_name', 'seller_id']).size().reset_index(name='jumlah')

    # Urutkan DataFrame berdasarkan kolom 'jumlah' dari terbesar ke terkecil
    order_product_combined_sorted = order_product_combined.sort_values(by='jumlah', ascending=False)

    # Kelompokkan data berdasarkan product_category_name dan hitung total untuk setiap kategori produk
    category_product_count = order_product_combined_sorted.groupby('product_category_name')['jumlah'].sum().reset_index(name='jumlah_total')

    # Urutkan DataFrame berdasarkan jumlah total untuk setiap kategori produk dari terbesar ke terkecil
    category_product_count_sorted = category_product_count.sort_values(by='jumlah_total', ascending=False)

    # Gabungkan dengan terjemahan nama kategori produk
    merged_data_final = pd.merge(category_product_count_sorted, product_category_name_translation, 
                                 on='product_category_name', how='left')
    merged_data_final['product_category_name_english'] = merged_data_final['product_category_name_english'].fillna(merged_data_final['product_category_name'])

    # Buat diagram batang
    st.header('Pertanyaan 1: Produk yang Paling Banyak Diminati oleh Pelanggan')
    fig, ax = plt.subplots(figsize=(8, 14))
    ax.barh(merged_data_final['product_category_name_english'], merged_data_final['jumlah_total'], color='skyblue')
    ax.set_xlabel('Total Jumlah')
    ax.set_ylabel('Kategori Produk (Bahasa Inggris)')
    ax.set_title('Total Jumlah berdasarkan Kategori Produk (Bahasa Inggris)')
    ax.invert_yaxis()
    st.pyplot(fig)

    st.write("Kesimpulan :")
    st.write("Dalam proses jual beli yang terjadi pada e-commerce ini terdapat berbagai varian produk. Total terdapat 73 produk. Kemudian total order item yang dilakukan oleh pelanggan sebanyak 112.650. Untuk persebaran produk, produk dengan kategori 'cama_mesa_banho / bed_bath_table' mendominasi dengan total sekitar 12.718, diikuti oleh 'beleza_saude / health_beauty' sekitar 9.670, dan terakhir 'esporte_lazer / sports_leisure' sekitar 8.641, dan seterusnya.")

def seller_customer_distribution(sellers_df, customers_df):
    # Hitung jumlah seller di setiap state
    seller_state_count = sellers_df['seller_state'].value_counts().reset_index()
    seller_state_count.columns = ['state', 'seller_count']

    # Hitung jumlah customer di setiap state
    customer_state_count = customers_df['customer_state'].value_counts().reset_index()
    customer_state_count.columns = ['state', 'customer_count']

    # Gabungkan hasil kelompok dari kedua DataFrame
    merged_state_counts = pd.merge(seller_state_count, customer_state_count, on='state', how='outer')

    # Isi nilai NaN dengan 0
    merged_state_counts.fillna(0, inplace=True)

    # Hitung total seller dan customer
    merged_state_counts['total'] = merged_state_counts['seller_count'] + merged_state_counts['customer_count']

    # Urutkan hasil berdasarkan total
    merged_state_counts_sorted = merged_state_counts.sort_values(by='total', ascending=False)

    return merged_state_counts_sorted

def plot_seller_customer_distribution(state_counts_df):
    # Data
    states = state_counts_df['state']
    seller_counts = state_counts_df['seller_count']
    customer_counts = state_counts_df['customer_count']

    # Plot untuk seller
    st.header('Pertanyaan 2: Distribusi Penjual dan Pembeli berdasarkan Negara Bagian')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(states, seller_counts, color='skyblue')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Sellers')
    ax.set_title('Number of Sellers by State')
    ax.tick_params(axis='x', rotation=45)  # Rotasi label sumbu x agar tidak bertabrakan
    plt.tight_layout()

    # Tampilkan plot untuk seller di Streamlit
    st.pyplot(fig)

    # Plot untuk customer
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(states, customer_counts, color='lightgreen')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Customers')
    ax.set_title('Number of Customers by State')
    ax.tick_params(axis='x', rotation=45)  # Rotasi label sumbu x agar tidak bertabrakan
    plt.tight_layout()

    # Tampilkan plot untuk customer di Streamlit
    st.pyplot(fig)
    
    # kesimpulan
    st.write('Kesimpulan : ')
    st.write('Persebaran seller dan customer di berbagai negara. Untuk yang seller, negara paling banyak adalah negara SP, kemudia ada PR, ketiga ada MG, dan seterusnya. Lalu untuk persebaran customer juga yang tertinggi ada di negara SP, lalu di RJ, ketiga di MG dan seterusnya')

def main():
    st.title('Exploratory Data Analysis (EDA) E-Commerce Public Dataset')
    
    st.write("<b>Nama : Diah Afia Safitri</b>", unsafe_allow_html=True)
    st.write("<b>Email : diahafia.safitri@gmail.com</b>", unsafe_allow_html=True)
    st.write("<b>Username ID : diafias</b>", unsafe_allow_html=True)
    
    # Display the merged data
    st.header("Tentang Data :")
    st.write("Data ini terdiri dari 9 file data yang berbeda, yaitu :")
    st.write("1. order_items_dataset.csv")
    st.write("2. products_dataset.csv")
    st.write("3. product_category_name_translation.csv")
    st.write("4. customers_dataset.csv")
    st.write("5. geolocation_dataset.csv")
    st.write("6. order_payments_dataset.csv")
    st.write("7. order_reviews_dataset.csv")
    st.write("8. orders_dataset.csv")
    st.write("9. sellers_dataset.csv")
    

    # Display EDA results for Pertanyaan 1
    explore_product_interest(order_items, products, product_category_name_translation)
    
    # Hitung distribusi penjual dan pembeli
    state_counts = seller_customer_distribution(sellers, customers)
    plot_seller_customer_distribution(state_counts)
    

if __name__ == "__main__":
    main()
    
    


