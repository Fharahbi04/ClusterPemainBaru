import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv('data.csv')
bola =pd.read_csv('bolauad.csv')
# Title and description
st.title("Dashboard Analisis Data Clustering Menggunakan Metode K-means")
st.write("""Analisi ini bertujuan untuk mengelompokkan cidera apa yang pernah dialami berdasarkan posisi bermain mahasiswa baru yang mendaftar di UKM Sepak Bola UAD""")

# Display dataset
kolom_tertentu = bola[['Cidera yang pernah dialami','Nama','Posisi bermain']]  # Memilih kolom Nama dan Kota
st.write(kolom_tertentu)

# Sidebar for filters
st.sidebar.header("Filter")

# Filter 1: Cluster selection
cluster_filter = st.sidebar.multiselect(
    "Pilih Cluster",
    options=data["Cluster"].unique(),
    default=data["Cluster"].unique()
)

# Filter data by cluster
filtered_data = data[data["Cluster"].isin(cluster_filter)]

# Display filtered dataset
st.header("Data Hasil Filter Cluster")
st.dataframe(filtered_data[['Cidera', 'Nama', 'Posisi','Cluster']])  # Tampilkan hanya kolom yang relevan

# Filter 2: Visualization selection
st.sidebar.header("Visualisasi")
visualization_type = st.sidebar.selectbox(
    "Pilih Tipe Visualisasi",
    ["Scatter Plot", "Bar Chart"]
)

# Scatter plot
if visualization_type == "Scatter Plot":
    st.header("Visualisasi Cluster")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_data,
        x="Posisi",
        y="Cidera",
        hue="Cluster",
        palette="viridis",
        ax=ax
    )
    plt.title("Scatter Plot Posisi vs. Cidera")
    st.pyplot(fig)

# Bar chart
elif visualization_type == "Bar Chart":
    st.header("Bar Chart Jumlah Posisi dan Cidera")
    
    # Pastikan hanya kolom numerik yang digunakan
    bar_data = filtered_data.groupby("Cluster")[["Posisi", "Cidera"]].sum(numeric_only=True).reset_index()
    
    fig, ax = plt.subplots()
    bar_data.plot(kind="bar", x="Cluster", stacked=True, ax=ax)
    plt.title("Jumlah Posisi dan Cidera per Cluster")
    plt.ylabel("Jumlah")
    plt.xlabel("Cluster")
    st.pyplot(fig)

# Display silhouette score
silhouette_avg = 0.6134  # Precomputed in the notebook
st.header("Silhouette Score")
st.metric(label="Silhouette Score", value=f"{silhouette_avg:.4f}")
