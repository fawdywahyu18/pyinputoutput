"""
Structural Check on Input-Output Table
There are 1 function in this script: structural check IO
The aim of the function is to check whether the IO table has a valid structure or not
We do the structural check by reversing the process of estimating the demand side and supply side multiplier
If the reverse process is succeed (both the demand and supply side), the the result will be the same as the output vector

@author: Fawdy
"""

import numpy as np

def structural_check_IO(Z_mat, fd_vec, output_vec,
                        import_vec, margin_vec, tax_vec,
                        va_vec, tax_input_vec, import_input_vec):
    
    mat_Z = Z_mat
    vec_output = output_vec
    
    mat_output = vec_output * np.identity(len(vec_output))
    inv_x = np.linalg.inv(mat_output)
    mat_A = np.matmul(mat_Z, inv_x)

    mat_fd = fd_vec
    mat_impor = import_vec
    mat_marjin = margin_vec
    mat_pajak = tax_vec
    mat_fd_new = mat_fd - mat_impor - mat_marjin - mat_pajak

    mat_res = np.identity(len(mat_A)) - mat_A
    mat_L = np.linalg.inv(mat_res) # Inverse Leontief Matrix
    
    # Test Demand Side
    mat_test = np.matmul(mat_L, mat_fd_new)
    test = vec_output - mat_test # Tested!!!
    result_test_demand = np.round(np.mean(test), 3) #TESTED!!!

    # Supply-Side Multiplier besi dan baja dasar (Exogenous Model)
    mat_B = np.matmul(inv_x, mat_Z) # allocation coeffcient
    mat_res2 = np.identity(len(mat_B)) - mat_B
    mat_G = np.linalg.inv(mat_res2) # the output inverse
    mat_va = va_vec
    mat_pajak_input = tax_input_vec
    mat_impor_input = import_input_vec
    mat_va_new = mat_va + mat_pajak_input + mat_impor_input
    
    # Test Supply Side
    mat_test_supply = np.matmul(np.transpose(mat_va_new), mat_G)
    test_supply = vec_output - np.transpose(mat_test_supply) # Testted!!!
    result_test_supply = np.round(np.mean(test_supply), 3) #TESTED!!!
    
    struct_check_res = {
        'result from demand side': result_test_demand,
        'result from supply side': result_test_supply}

    return struct_check_res
