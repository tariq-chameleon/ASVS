#Written by Tariq A.
#Repository ---> github.com/tariq-chameleon/ASVS.git

import numpy as NP
import  os as OS
def cli_visualize (ARG):    
    #ARG = [6,1,5,7,3,4,20,5,10,15]
    DISP_VECTOR=[" "," "," "," "," "," "," "," "," "," ",]
    n = 0
    elements = 10                 #+1 for \0
    max_vertical_strength = 20      # FREQ_DOMAIN_CEILING  #+1 for \0

    #[1  0  0 1].....
    #[1  0  0 1].....
    #[1  0  0 1].....
    #[1  0  0 1].....
    #[1  0  0 1].....
    #f0 f1 f2 f3.....
    #...........
    #...........









    #----------------------------------------------------------
    out_matrix = NP.zeros(elements* max_vertical_strength)
    out_matrix = out_matrix.reshape(max_vertical_strength, elements)   #reshapping Column, Row
    #----------------------------------------------------------




    #----------------------------------------------------------
   #print (ARG)
    for i in range (0,elements):    
        for j in range (0,ARG[i]):
            out_matrix[j,i] = 1

    #print (out_matrix)
    #----------------------------------------------------------







    #----------------------------------------------------------
    r = max_vertical_strength-1
    for i in range (0,max_vertical_strength):
        for c in range (0,elements):
            if out_matrix[r,c] == 1:
                DISP_VECTOR[c] = "----"
            elif out_matrix[r,c] == 0:
                DISP_VECTOR[c] = "    "
        print("%s      %s      %s      %s      %s      %s      %s      %s      %s      %s" % (DISP_VECTOR[0],DISP_VECTOR[1],DISP_VECTOR[2],DISP_VECTOR[3],DISP_VECTOR[4],DISP_VECTOR[5],DISP_VECTOR[6],DISP_VECTOR[7],DISP_VECTOR[8],DISP_VECTOR[9]))
        r-=1
    
    print    ("f0         f1        f2        f3        f4        f5        f6        f7        f8        f9")
    print    ("30 Hz    65 Hz     200 Hz    400 Hz     800 Hz   1.5 kHz   4 kHz     6.0 kHz    8.5 kHz   13 kHz") 
    #----------------------------------------------------------
    return
