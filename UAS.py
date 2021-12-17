#import data
import json
import csv

#module
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
from PIL import Image


#Judul#
st.set_page_config(layout="wide") 
image = Image.open('petroleum.jpg')
st.image(image)
st.title("Informasi Data produksi Minyak Mentah di Dunia")

list_kode_negara = []
kode_negara = []
nama_negara = []
list_tahun = []

data_minyak = open("produksi_minyak_mentah.csv")
csv = csv.reader(data_minyak)
header = next(csv)
data = []
for row in csv:
    data.append(row)

for set in data:
    list_kode_negara.append(set[0])
for c in list_kode_negara:
    if c not in kode_negara:
        kode_negara.append(c)
for set in data:
    if set[1] not in list_tahun:
        list_tahun.append(set[1])    
        
with open("kode_negara_lengkap.json") as c:
    code = json.load(c)
        
for c in kode_negara:
    for group in code:
        if group["alpha-3"]==c:
            nama_negara.append(group["name"])
            
            
                  
#Kolom konfigurasi#
st.sidebar.subheader("Creator : Anggara Thomas Gunawan/12220019")
image2 = Image.open('Logo ITB.jpeg')
st.sidebar.image(image2)
st.sidebar.title("Menu Pilihan")
left_col, mid_col, right_col = st.columns(3)

# Pilihan input user
negara = st.sidebar.selectbox("Pilih negara", nama_negara)
tahun = st.sidebar.selectbox("Pilih tahun", list_tahun)

n_peringkat = st.sidebar.number_input("Jumlah peringkat produksi terbesar", min_value=1, max_value=None, value=3)


#Soal 1a#
for set in data:
    for group in code:
        if set[0]==group["alpha-3"]:
            set.insert(0,group["name"])

A_graphy = []
A_graphx = []
for set in data:
    if set[0]==negara:
        A_graphy.append(float(set[3]))
        A_graphx.append(set[2])

st.header("Produksi Minyak Mentah "+negara)
st.caption("Line plot produksi minyak mentah dari tahun 1971-2015")

fig, ax = plt.subplots()
ax.plot(A_graphx, A_graphy, color='red')
ax.grid()
fig.set_figwidth(36)
fig.set_figheight(9)
ax.set_xticklabels(A_graphx, rotation=0, fontsize=15)
ax.set_xlabel("Tahun", fontsize=31)
ax.set_ylabel("Produksi minyak mentah", fontsize=24)
st.pyplot(fig)

#Soal 1b#
B_raw = []
B_graphx = []
B_graphy = []
for set in data:
    if float(set[2])==float(tahun):
        B_raw.append((float(set[3]),set[0]))
B_raw.sort(reverse=True)
for num in range(int(n_peringkat)):
    B_graphy.append(B_raw[num][0])
    B_graphx.append(B_raw[num][1])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:int(n_peringkat)]
st.header(str(n_peringkat)+" Negara dengan Produksi Terbesar Tahun "+str(tahun))
st.caption("Bar plot negara dengan produksi minyak mentah terbesar")
fig, ax = plt.subplots()
ax.barh(B_graphx, B_graphy, color='blue')
ax.set_yticklabels(B_graphx, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
st.pyplot(fig)

zero_country1 = []
zero_code1 = []
zero_reg1 = []
zero_subreg1 = []
zero_dict1 = dict()
for set in B_raw:
    if set[0]==0:
        zero_country1.append(set[1])
for name in zero_country1:
    for group in code:
        if group["name"]==name:
            zero_code1.append(group["alpha-3"])
            zero_reg1.append(group["region"])
            zero_subreg1.append(group["sub-region"])
            
zero_dict1["Negara"] = zero_country1
zero_dict1["Kode"] = zero_code1
zero_dict1["Region"] = zero_reg1
zero_dict1["Sub-region"] = zero_subreg1
zero_table1 = pd.DataFrame(zero_dict1)
D_dict1 = dict()
D_raw1 = []
for set in data:
    if float(set[2])==float(tahun):
        D_raw1.append((float(set[3]),set[0]))
D_raw1.sort()

D_dict1["Deskripsi"] = ["Produksi terbesar","Produksi terkecil"]
D_dict1["Negara"] = [B_raw[0][1],D_raw1[0][1]]
for group in code:
    if group["name"]==B_raw[0][1]:
        code1 = group["alpha-3"]
        region1 = group["region"]
        subregion1 = group["sub-region"]
for group in code:
    if group["name"]==D_raw1[0][1]:
        code2 = str(group["alpha-3"])
        region2 = group["region"]
        subregion2 = group["sub-region"]
D_dict1["Kode"]= [code1,code2]
D_dict1["Region"] = [region1,region2]
D_dict1["Sub-region"]=[subregion1,subregion2]
D_table1 = pd.DataFrame(D_dict1)


with st.expander("Summary Data Tahun "+tahun):
    st.subheader(" Tabel Summary Data Tahun "+str(tahun))
    st.table(D_table1)
    st.subheader(" Tabel Zero Production Tahun "+str(tahun))
    st.write("Kumpulan negara dengan besar produksi minyak mentah nol pada tahun "+tahun)
    st.table(zero_table1)


#Soal 1c#
C_dict = dict()
C_raw = []
C_graphx = []
C_graphy = []

for name in nama_negara:
    sum_prod=0
    for set in data:
        if set[0]==name:
            sum_prod = sum_prod+float(set[3])
            C_dict[name] = sum_prod

for name,prod in C_dict.items():
    tup = prod,name
    C_raw.append(tup)
C_raw.sort(reverse=True)

for num in range(int(n_peringkat)):
    C_graphx.append(C_raw[num][1])
    C_graphy.append(C_raw[num][0])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:int(n_peringkat)]
st.header(str(n_peringkat)+" Negara dengan Produksi Terbesar Kumulatif")
st.caption("Bar plot negara dengan produksi minyak mentah terbesar dari tahun 1971-2015")
fig, ax = plt.subplots()
ax.barh(C_graphx, C_graphy, color='blue')
ax.set_yticklabels(C_graphx, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Produksi Minyak Mentah", fontsize=12)
st.pyplot(fig)

zero_country2 = []
zero_code2 = []
zero_reg2 = []
zero_subreg2 = []
zero_dict2 = dict()
for set in C_raw:
    if set[0]==0:
        zero_country2.append(set[1])
for name in zero_country2:
    for group in code:
        if group["name"]==name:
            zero_code2.append(group["alpha-3"])
            zero_reg2.append(group["region"])
            zero_subreg2.append(group["sub-region"])

zero_dict2["Negara"] = zero_country2
zero_dict2["Kode"] = zero_code2
zero_dict2["Region"] = zero_reg2
zero_dict2["Sub-region"] = zero_subreg2
zero_table2 = pd.DataFrame(zero_dict2)

D_dict2 = dict()
D_raw2 = []
for name,prod in C_dict.items():
    c = prod,name
    D_raw2.append(c)
D_raw2.sort()

D_dict2["Deskripsi"] = ["Produksi terbesar","Produksi terkecil"]
D_dict2["Negara"] = [str(C_raw[0][1]),str(D_raw2[0][1])]
for group in code:
    if group["name"]==C_raw[0][1]:
        code1 = group["alpha-3"]
        region1 = group["region"]
        subregion1 = group["sub-region"]
for group in code:
    if group["name"]==D_raw2[0][1]:
        code2 = str(group["alpha-3"])
        region2 = group["region"]
        subregion2 = group["sub-region"]
D_dict2["Kode"]= [code1,code2]
D_dict2["Region"] = [region1,region2]
D_dict2["Sub-region"]=[subregion1,subregion2]
D_table2 = pd.DataFrame(D_dict2)


with st.expander("Summary Data Kumulatif"):
    st.subheader(" Tabel Summary Data Kumulatif")
    st.table(D_table2)
    st.subheader(" Tabel Zero Production Kumulatif")
    st.write("Kumpulan negara dengan besar produksi minyak mentah nol untuk keseluruhan tahun")
    st.table(zero_table2)