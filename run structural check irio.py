# Running the structural_check_IRIO.py


from structural_check_IRIO import *

# load data IRIO Indonesia and Japan
df = pd.read_excel('data/IRIO Table Indonesia 2016 52 sectors 34 provinces.xlsx', sheet_name='IRIO-PDD (52x52)')
df_jepang = pd.read_excel('data/IRIO Japan 53 sectors.xlsx', sheet_name='S53_TBL') # IRIO Jepang 53 Sektor
df_A_jepang = pd.read_excel('data/IRIO Japan 53 sectors.xlsx', sheet_name='S53_Input_Coefficients_Matrix')
df_L_inv_jepang = pd.read_excel('data/IRIO Japan 53 sectors.xlsx', sheet_name='S53_Inverse_Matrix')

# Matrix operation Indonesia
df_Z = df.iloc[5:1772,4:1771]
mat_z = df_Z.to_numpy(dtype=int)
df_to = df.iloc[5:1772, 1953]
vec_to = df_to.to_numpy(dtype=int)
df_fd = df.iloc[5:1772, 1951]
vec_fd = df_fd.to_numpy(dtype=int)
vec_e = df.iloc[5:1772, 1950].to_numpy(dtype=int)
vec_m = df.iloc[1775, 4:1771].to_numpy(dtype=int)

# Running function Japan
check_error_japan(df_jepang, df_A_jepang, df_L_inv_jepang)

# Running Function Indonesia
cek_error = error_check(vec_to, vec_fd, mat_z, vec_e, vec_m)
irio_adj = adj_x(vec_fd, mat_z)

# Export dataframe from cek_error and irio_adj
df_export_adj = pd.DataFrame.from_dict(irio_adj, orient='index').T
df_export_adj.to_excel('example outputs/hasil cek error IRIO adj.xlsx')
df_cek_error = pd.DataFrame(cek_error)
df_cek_error.to_excel('example outputs/hasil cek error IRIO Indonesia.xlsx')

source_file = 'data/Input Ouput Table Indonesia 2016.xlsx'
sheet = 'BCD 185'

# PCT = Transaksi Total atas dasar harga pembeli
# BCT = Transkasi Total atas dasar harga dasar
# BCD = Transaksi Domestik atas dasar harga dasar

hasil_check = error_check_IO(source_file,
                             nama_sheet=sheet)
# Export Hasil Check ke folder dalam bentuk excel
pd.DataFrame(hasil_check).to_excel('example outputs/hasil cek error IO type C.xlsx', index=False)

