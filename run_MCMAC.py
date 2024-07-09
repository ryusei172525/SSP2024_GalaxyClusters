#<--23/12/2022
#<--Run Dawson's code
#<--author: Rogerio Monteiro-Oliveira (rmonteiro@asiaa.sinica.edu.tw)

#<--Required modules
from MCMAC_pre_merger import MCengine_pre_merger
from MCMAC_post_merger import MCengine_post_merger 
import numpy as np
import pandas as pd


def empty(dataf, i):
    dataf['M1p'][i] = None
    dataf['M1p.lower'][i] = None
    dataf['M1p.upper'][i] = None

    dataf['M2p'][i] = None
    dataf['M2p.lower'][i] = None
    dataf['M2p.upper'][i] = None

    dataf['z1p'][i] = None
    dataf['z1p.lower'][i] = None
    dataf['z1p.upper'][i] = None

    dataf['z2p'][i] = None
    dataf['z2p.lower'][i] = None
    dataf['z2p.upper'][i] = None

    dataf['d.proj.out'][i] = None
    dataf['d.proj.out.lower'][i] = None
    dataf['d.proj.out.upper'][i] = None

    dataf['v.rad.obs.out'][i] = None
    dataf['v.rad.obs.out.lower'][i] = None
    dataf['v.rad.obs.out.upper'][i] = None

    dataf['alpha.out'][i] = None
    dataf['alpha.out.lower'][i] = None
    dataf['alpha.out.upper'][i] = None

    dataf['v.3d.obs.out'][i] = None
    dataf['v.3d.obs.out.lower'][i] = None
    dataf['v.3d.obs.out.upper'][i] = None

    dataf['d.3d.out'][i] = None
    dataf['d.3d.out.lower'][i] = None
    dataf['d.3d.out.upper'][i] = None

    dataf['v.3d.col.out'][i] = None
    dataf['v.3d.col.out.lower'][i] = None
    dataf['v.3d.col.out.upper'][i] = None

    dataf['d.max.out'][i] = None
    dataf['d.max.out.lower'][i] = None
    dataf['d.max.out.upper'][i] = None

    dataf['TSC0'][i] = None
    dataf['TSC0.lower'][i] = None
    dataf['TSC0.upper'][i] = None

    dataf['TSC1'][i] = None
    dataf['TSC1.lower'][i] = None
    dataf['TSC1.upper'][i] = None

    dataf['T.out'][i] = None
    dataf['T.out.lower'][i] = None
    dataf['T.out.upper'][i] = None

    dataf['prob.out'][i] = None
    dataf['prob.out.lower'][i] = None
    dataf['prob.out.upper'][i] = None

#<--Definitions
N_mc = 1000

#<--Work directory (edit accordingly)
dir_cat = '../catalogues/'
dir_output = '../output/'

#<--Input catalogues (as prepared in ../R/make_catalogue.R)
#<--This is a post-merger code: it must be run only for snapshots after the pericentric passage!
files = []

files.append('zh_1to1_b0_z')
files.append('zh_1to1_b0.5_z')
files.append('zh_1to1_b1_z')

files.append('zh_1to3_b0_z')
files.append('zh_1to3_b0.5_z')
files.append('zh_1to3_b1_z')

files.append('zh_1to10_b0_z')
files.append('zh_1to10_b0.5_z')
files.append('zh_1to10_b1_z')


#<--Run over each file (i.e. a given merger configuration)
for i in range(0, len(files)): 

 print(files[i])

 #<--Open the current catalogue (ZuHone)
 filename = dir_cat + files[i] + '.txt'
 
 #<--Create a file to save the updated catalogue
#  out_file = dir_cat + files[i] + '_updated.txt'
 out_file = dir_output + files[i] + '_MCMAC.txt'

  
 #<--Read the catalogue into df	
 df = pd.read_csv(filename, sep="\t")

 #<--Create new columns
 df['M1p'] = 0.
 df['M1p.lower'] = 0.
 df['M1p.upper'] = 0.

 df['M2p'] = 0.
 df['M2p.lower'] = 0.
 df['M2p.upper'] = 0.
  
 df['z1p'] = 0.
 df['z1p.lower'] = 0.
 df['z1p.upper'] = 0.  

 df['z2p'] = 0.
 df['z2p.lower'] = 0.
 df['z2p.upper'] = 0.
  
 df['d.proj.out'] = 0.
 df['d.proj.out.lower'] = 0.
 df['d.proj.out.upper'] = 0.
  
 df['v.rad.obs.out'] = 0.
 df['v.rad.obs.out.lower'] = 0.
 df['v.rad.obs.out.upper'] = 0.  
  
 df['alpha.out'] = 0.
 df['alpha.out.lower'] = 0.
 df['alpha.out.upper'] = 0.
 
 df['v.3d.obs.out'] = 0.
 df['v.3d.obs.out.lower'] = 0.
 df['v.3d.obs.out.upper'] = 0.
 
 df['d.3d.out'] = 0.
 df['d.3d.out.lower'] = 0.
 df['d.3d.out.upper'] = 0.
 
 df['v.3d.col.out'] = 0.
 df['v.3d.col.out.lower'] = 0.
 df['v.3d.col.out.upper'] = 0. 
  
 df['d.max.out'] = 0.
 df['d.max.out.lower'] = 0.
 df['d.max.out.upper'] = 0.  
  
 df['TSC0'] = 0.
 df['TSC0.lower'] = 0.
 df['TSC0.upper'] = 0.

 df['TSC1'] = 0.
 df['TSC1.lower'] = 0.
 df['TSC1.upper'] = 0.

 df['T.out'] = 0.
 df['T.out.lower'] = 0.
 df['T.out.upper'] = 0.
  
 df['prob.out'] = 0.
 df['prob.out.lower'] = 0.
 df['prob.out.upper'] = 0. 
 

 #<--Run MCMAC for each snapshot in the current merger configuration
 for cont in range(0, len(df)): 
  print(filename, df['age'][cont])
#   # Cut calculation for time saving
#   if ("1to3_b0" or "1to3_b0.5") in filename and df['age'][cont] > 2:
#     # empty(df, cont)
#     continue
#   elif "1to3_b1" in filename and df['age'][cont] > 2.5:
#     # empty(df, cont)
#     continue
#   elif "1to10_b0" in filename and df['age'][cont] > 2:
#     # empty(df, cont)
#     continue
#   elif "1to10_b0.5" in filename and df['age'][cont] > 2.4:
#     # empty(df, cont)
#     continue
#   elif "1to10_b1" in filename and df['age'][cont] > 3:
#     # empty(df, cont)
#     continue    
  
  print("calculate MCMAC!")
  Z1 = (df['z1'][cont], df['z1.e'][cont])
  Z2 = (df['z2'][cont], df['z2.e'][cont])
  M1 = (df['M1'][cont], df['M1.e'][cont])
  M2 = (df['M2'][cont], df['M2.e'][cont])
  D_proj  = ( df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont] ) #<--Uncertainty is 5% of the face value
 
  # if D_proj[i] is bigger than D_proj[i+1], we can consider D_proj[i] shows this is pre-merger
  # However, if D_proj[i] is less than D_proj[i+1], we can consider D_proj[i] shows this is post-merger
  if df['sep.Mpc'][cont] > df['sep.Mpc'][cont + 1]:
    print("MCMAC pre merger")
    t = MCengine_pre_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)
  elif df['sep.Mpc'][cont] < df['sep.Mpc'][cont + 1]:
    print("MCMAC post merger")
    t = MCengine_post_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)

  #<--MCMAC_post_merger output
  #0| m_1_out,
  #1| m_2_out,
  #2| z_1_out,
  #3| z_2_out,
  #4| d_proj_out,
  #5| v_rad_obs_out,
  #6| alpha_out,
  #7| v_3d_obs_out,
  #8| d_3d_out,
  #9| v_3d_col_out,
  #10| d_max_out,
  #11| TSM_0_out,
  #12| TSM_1_out,
  #13| T_out,
  #14| prob_out
  
  print(cont)
  
  var = t[0]
  df['M1p'][cont] = np.quantile(var, 0.5)        #<--median
  df['M1p.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['M1p.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma  

  var = t[1]
  df['M2p'][cont] = np.quantile(var, 0.5)        #<--median
  df['M2p.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['M2p.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma 
  
  var = t[2]
  df['z1p'][cont] = np.quantile(var, 0.5)        #<--median
  df['z1p.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['z1p.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma   
  
  var = t[3]
  df['z2p'][cont] = np.quantile(var, 0.5)        #<--median
  df['z2p.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['z2p.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma 
  
  var = t[4]
  df['d.proj.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['d.proj.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['d.proj.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma  
  
  var = t[5]
  df['v.rad.obs.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['v.rad.obs.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['v.rad.obs.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma   
  
  var = t[6]
  df['alpha.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['alpha.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['alpha.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma  
 
  var = t[7]
  df['v.3d.obs.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['v.3d.obs.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['v.3d.obs.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma 
 
  var = t[8]
  df['d.3d.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['d.3d.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['d.3d.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma 
 
  var = t[9]
  df['v.3d.col.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['v.3d.col.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['v.3d.col.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma 
  
  var = t[10]
  df['d.max.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['d.max.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['d.max.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma   
     
  TSC0 = t[11]
  df['TSC0'][cont] = np.quantile(TSC0, 0.5)        #<--median
  df['TSC0.lower'][cont] = np.quantile(TSC0, 0.16) #<--1 \sigma 
  df['TSC0.upper'][cont] = np.quantile(TSC0, 0.84) #<--1 \sigma

  TSC1 = t[12]
  df['TSC1'][cont] = np.quantile(TSC1, 0.5)        #<--median
  df['TSC1.lower'][cont] = np.quantile(TSC1, 0.16) #<--1 \sigma
  df['TSC1.upper'][cont] = np.quantile(TSC1, 0.84) #<--1 \sigma

  var = t[13]
  df['T.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['T.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['T.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma  
  
  var = t[14]
  df['prob.out'][cont] = np.quantile(var, 0.5)        #<--median
  df['prob.out.lower'][cont] = np.quantile(var, 0.16) #<--1 \sigma 
  df['prob.out.upper'][cont] = np.quantile(var, 0.84) #<--1 \sigma  
  
 #<--for cont in range(0, len(df)): 


 #<--Save the updated catalogue 
 out = df.to_csv(sep = '\t', index = False, header = True)
 f = open(out_file,'w')
 f.write(out)
 f.close()

