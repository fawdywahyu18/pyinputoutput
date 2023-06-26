# -*- coding: utf-8 -*-
"""
Script Structural Check IRIO Indonesia

@author: Fawdy
"""

import pandas as pd
import numpy as np

def check_error_japan(df_all=None, df_a=None, df_L_inv=None):
   
    # Matrix Operation IRIO Jepang
    mat_A_jepang = df_a.iloc[5:482, 4:481].to_numpy(dtype=float)
    mat_L_inv_jepang = df_L_inv.iloc[5:482, 4:481].to_numpy(dtype=float)

    # Cleaning vector output and final demand jepang
    df_output_jepang = df_all.iloc[5:581, 734]
    df_fd_jepang = df_all.iloc[5:581, 733]

    # Creating Sequnce to delete the rows in vector output and final demand
    seq_list = []
    index_del = 58
    while index_del < 581:
        end_index = index_del + 11
        sequence = range(index_del, end_index, 1)
        range_list = list(sequence)
        range_array = np.array(range_list)
        seq_list.append(range_array)
        index_del += 64
    seq_array = np.concatenate(seq_list)

    clean_output = df_output_jepang.drop(seq_array).to_numpy(dtype=float)
    clean_fd = df_fd_jepang.drop(seq_array).to_numpy(dtype=float)

    mat_L_jepang = np.identity(len(mat_A_jepang)) - mat_A_jepang
    cek_inv = (np.linalg.inv(mat_L_jepang)) - mat_L_inv_jepang
    cek_error_f2_jepang = clean_fd - (mat_L_jepang @ clean_output)
    cek_error_x2_jepang = clean_output - ((np.linalg.inv(mat_L_jepang)) @ clean_fd)

    # Creating Matrix Z Jepang
    # Creating Sequnce to delete the columns in matrix Z
    seq_list_col = []
    index_del_col = 53
    while index_del_col < 657:
        end_index_col = index_del_col + 20
        sequence_col = range(index_del_col, end_index_col, 1)
        range_list_col = list(sequence_col)
        range_array_col = np.array(range_list_col)
        seq_list_col.append(range_array_col)
        index_del_col += 73
    seq_array_col = np.concatenate(seq_list_col)

    # The original Matrix Z Japan
    df_Z_jepang = df_all.iloc[5:581, 4:661]

    # Delete columns based on the column indexes
    df_Z_cc = df_Z_jepang.iloc[:, [i for i in range(df_Z_jepang.shape[1]) if i not in seq_array_col]]
    mat_Z_jepang_ori = df_Z_cc.drop(seq_array).to_numpy(dtype=float)

    # Matrix Z yang berasal dari matrix A
    mat_output_jepang = clean_output * np.identity(len(clean_output))
    mat_Z_jepang = mat_A_jepang @ mat_output_jepang

    # Cek apakah matrix Z dan Matrix A jepang ori sama dengan hasil pengolahan dari matrix A jepang
    cek_Z = mat_Z_jepang_ori - mat_Z_jepang # PROOF!!
    mat_A_jepang_ori = np.nan_to_num(mat_Z_jepang_ori / clean_output[:, np.newaxis])
    cek_A = mat_A_jepang - mat_A_jepang_ori

    cek_error_x1_jepang = clean_output - (np.sum(mat_Z_jepang, axis=1, dtype=np.float64) + clean_fd)
    cek_error_f1_jepang = clean_fd - (clean_output - (mat_Z_jepang @ np.ones(len(clean_output))))
    
    # result for making sure that mumpy produces the same matrix Z, matrix A, and Matrix Leontief Inverse Japan
    result_making_sure = {
        'cek inverse': cek_inv,
        'cek matrix Z': cek_Z,
        'cek matrix A': cek_A
        }

    result_cek_error_jepang = {
        'cek error output 1': cek_error_x1_jepang,
        'cek error output 2': cek_error_x2_jepang,
        'cek error final demand 1': cek_error_f1_jepang,
        'cek error final demand 2': cek_error_f2_jepang
        }
    df_error_jepang = pd.DataFrame(result_cek_error_jepang)
    return df_error_jepang.to_excel('example outputs/results of check error IRIO Japan.xlsx')

# Error Check
def error_check(vector_x=None, vector_fd=None, matrix_z=None, vektor_e=None,
                vektor_m=None,
                pembulatan=False, 
                digit_pembulatan=None,
                adjusting_A=False):
    # vector_x = vec_to_world
    # vector_fd = vec_fd_world
    # matrix_z = mat_z_world
    # adjusting_A = False
    # pembulatan=False
    
    mat_A = np.nan_to_num(matrix_z / vector_x[:, np.newaxis])
    
    if adjusting_A==True:
        vec_numerator = vector_x - vektor_e
        vec_denumerator = vector_x - vektor_e + vektor_m
        vec_p = np.nan_to_num(vec_numerator / vec_denumerator)
        mat_p = vec_p * np.identity(len(vec_p))
        mat_A_selected = mat_p @ mat_A
    else:
        mat_A_selected = mat_A

    if pembulatan==True:
        mat_A_ce = np.around(mat_A_selected, decimals=digit_pembulatan)
        vector_x_ce = np.around(vector_x, decimals=digit_pembulatan)
        vector_fd_ce = np.around(vector_fd, decimals=digit_pembulatan)
        matrix_z_ce = np.around(matrix_z, decimals=digit_pembulatan)
    else:
        mat_A_ce = mat_A_selected
        vector_x_ce = vector_x
        vector_fd_ce = vector_fd
        matrix_z_ce = matrix_z
    
    mat_L = np.identity(len(mat_A_ce)) - mat_A_ce
    mat_L_inv = np.linalg.inv(mat_L)
    
    cek_error_x1 = vector_x_ce - (np.sum(matrix_z_ce, axis=1, dtype=np.float64) + vector_fd_ce)
    cek_error_x2 = vector_x_ce - (mat_L_inv @ vector_fd_ce)
    
    cek_error_f1 = vector_fd_ce - (vector_x_ce - (matrix_z_ce @ np.ones(len(vector_x_ce))))
    cek_error_f2 = vector_fd_ce - (mat_L @ vector_x_ce)
    
    result_cek_error = {
        'cek error output 1': cek_error_x1,
        'cek error output 2': cek_error_x2,
        'cek error final demand 1': cek_error_f1,
        'cek error final demand 2': cek_error_f2
        }
    
    return result_cek_error

# Adjusment on X and new Leontief
def adj_x(vector_fd=None, matrix_z=None):
    
    # vector_fd = vec_fd
    # matrix_z = mat_z
    
    z_sum = np.sum(matrix_z, axis=1)
    vector_x_new = z_sum + vector_fd
    mat_A = np.nan_to_num(matrix_z / vector_x_new[:, None])
    
    # New Leontief
    mat_x_new = vector_x_new * np.identity(len(vector_x_new))
    mat_x_new_inv = np.linalg.pinv(mat_x_new)
    mat_fd = vector_fd * np.identity(len(vector_fd))
    new_leontief = mat_fd @ mat_x_new_inv
    leon_inv = np.linalg.pinv(new_leontief)
    
    # Validasi Inverse Leotief Baru
    test_vector_x = vector_x_new - (leon_inv @ vector_fd)
    
    # Cek error pada final demand
    mat_L = np.identity(len(mat_A)) - mat_A
    mat_L_inv = np.linalg.inv(mat_L)
    cek_error_f1 = vector_fd - (vector_x_new - (matrix_z @ np.ones(len(vector_x_new))))
    cek_error_f2 = vector_fd - (mat_L @ vector_x_new)
    
    # Cek error pada vektor output
    cek_error_x1 = vector_x_new - (np.sum(matrix_z, axis=1, dtype=np.float64) + vector_fd)
    cek_error_x2 = vector_x_new - (mat_L_inv @ vector_fd)
    
    result_adjx = {
        'Vektor Output Adjusted': vector_x_new,
        'Matrix Inverse Leontief Baru': leon_inv,
        'Validasi Vektor Output': test_vector_x,
        'Cek Error output 1': cek_error_x1,
        'Cek Error output 2': cek_error_x2,
        'Cek Error Final Demand 1': cek_error_f1,
        'Cek Error Final Demand 2': cek_error_f2,
        }

    return result_adjx


# Structural Check on the IO table
def error_check_IO(sumber_file, nama_sheet='PCT 185'):
    
    # sumber_file = source_file
    # nama_sheet = 'PCT 185'
    # PCT = Transaksi Total atas dasar harga pembeli
    # BCT = Transkasi Total atas dasar harga dasar
    # BCD = Transaksi Domestik atas dasar harga dasar

    
    # Preparing the matrix
    df = pd.read_excel(sumber_file, sheet_name=nama_sheet)
    df_extracted = df.iloc[3:,2:].reset_index().drop(columns=['index'])
    df_Z = df_extracted.iloc[2:187, 1:186].reset_index().drop(columns=['index'])
    series_output = df_extracted.iloc[2:187,-2].reset_index().drop(columns=['index'])
    # series_hh = df_extracted.iloc[2:187,188].reset_index().drop(columns=['index'])
    mat_Z = df_Z.to_numpy(dtype=int)
    vec_output = series_output.to_numpy(dtype=int)
    # vec_hh = series_hh.to_numpy(dtype=int)
    
    # Demand-Side
    mat_output = vec_output * np.identity(len(vec_output))
    inv_x = np.linalg.inv(mat_output)
    mat_A = np.matmul(mat_Z, inv_x)

    df_fd = df_extracted.iloc[2:187, 194].reset_index().drop(columns=['index'])
    mat_fd = df_fd.to_numpy(dtype=int)
    df_impor = df_extracted.iloc[2:187, 199].reset_index().drop(columns=['index'])
    mat_impor = df_impor.to_numpy(dtype=int)
    df_marjin = df_extracted.iloc[2:187, 203].reset_index().drop(columns=['index'])
    mat_marjin = df_marjin.to_numpy(dtype=int)
    df_pajak = df_extracted.iloc[2:187, 204].reset_index().drop(columns=['index'])
    mat_pajak = df_pajak.to_numpy(dtype=int)
    mat_fd_new = mat_fd - mat_impor - mat_marjin - mat_pajak
    vec_fd_new = np.ravel(mat_fd_new)
    
    mat_res = np.identity(len(mat_A)) - mat_A
    output_1d = np.ravel(vec_output)
    cek_error_x1_demand = output_1d - (np.sum(mat_Z, axis=1, dtype=np.float64) + vec_fd_new)
    cek_error_f1_demand = vec_fd_new - (output_1d - (mat_Z @ np.ones(len(output_1d))))
    cek_error_f2_demand = mat_fd_new - (mat_res @ vec_output)
    cek_error_x2_demand = vec_output - ((np.linalg.inv(mat_res)) @ mat_fd_new)

    # Supply-Side
    mat_B = np.matmul(inv_x, mat_Z) # allocation coeffcient
    mat_res2 = np.identity(len(mat_B)) - mat_B
    mat_G = np.linalg.inv(mat_res2) # the output inverse
    df_va = df_extracted.iloc[194, 1:186].reset_index().drop(columns=['index'])
    mat_va = df_va.to_numpy(dtype=int)
    df_pajak_input = df_extracted.iloc[189, 1:186].reset_index().drop(columns=['index'])
    mat_pajak_input = df_pajak_input.to_numpy(dtype=int)
    df_impor_input = df_extracted.iloc[190, 1:186].reset_index().drop(columns=['index'])
    mat_impor_input = df_impor_input.to_numpy(dtype=int)
    mat_va_new = mat_va + mat_pajak_input + mat_impor_input
    vec_va_new = np.ravel(mat_va_new)
    
    df_input = df_extracted.iloc[195, 1:186].reset_index().drop(columns=['index'])
    vec_input = df_input.to_numpy(dtype=int)
    
    input_1d = np.ravel(vec_input)
    mat_xb = mat_output @ mat_B
    
    cek_error_x1_supply = input_1d - (np.sum(mat_Z, axis=0, dtype=np.float64) + vec_va_new)
    cek_error_va1_supply = vec_va_new - (input_1d - np.sum(mat_xb, axis=0, dtype=np.float64))
    cek_error_va2_supply = vec_va_new - (np.transpose(vec_input) @ mat_res2).flatten()
    cek_error_x2_supply = input_1d - (np.transpose(mat_va_new) @ mat_G).flatten()

    
    check_test = {
        'Check error output 1 demand': cek_error_x1_demand,
        'Check error output 2 demand': cek_error_x2_demand.flatten(),
        'Check error final demand 1 demand': cek_error_f1_demand,
        'Check error final demand 2 demand': cek_error_f2_demand.flatten(),
        'Check error output 1 supply': cek_error_x1_supply,
        'Check error output 2 supply': cek_error_x2_supply,
        'Check error value add 1 supply': cek_error_va1_supply,
        'Check error value add 2 supply': cek_error_va2_supply,
        }
    
    return check_test

