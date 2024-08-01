from multiprocessing import Pool

# 事前分布を変更する場合はMCMACのコードを変更する
# default prior: angle 0-90 degree
# from MCMAC_post_merger import MCengine_post_merger 

# change prior: angle 0-20 degree
from MCMAC_post_merger_changeprior import MCengine_post_merger 

# weak lensing mass bias
weak_lensing_bias_1to1 = False
weak_lensing_bias_1to3 = False
weak_lensing_bias_1to10 = False

if weak_lensing_bias_1to1 == True:
    bias = 1.64
elif weak_lensing_bias_1to3 == True:
    bias = 1.43
elif weak_lensing_bias_1to10 == True:
    bias = 1.28
else:
    bias = 1.0

print("bias", bias)

import numpy as np
import pandas as pd

def empty(dataf, i):
    dataf.loc[i, 'M1p':'prob.out.upper'] = None

# 定義
N_mc = 1000

# 作業ディレクトリ
dir_cat = '../catalogues/'
dir_output = '../output_20degree_only_post/'

# 入力カタログ
files = [
    'zh_1to1_b0_z', 'zh_1to1_b0.5_z', 'zh_1to1_b1_z',
    'zh_1to3_b0_z', 'zh_1to3_b0.5_z', 'zh_1to3_b1_z',
    'zh_1to10_b0_z', 'zh_1to10_b0.5_z', 'zh_1to10_b1_z'
]

# weak lensing biasを考慮するときのみbiasが異なるのでratioごとに実行する必要がある！
# files = [
#     'zh_1to10_b0_z', 'zh_1to10_b0.5_z', 'zh_1to10_b1_z'
# ]

def process_cont(cont, df, filename):
    Z1 = (df['z1'][cont], df['z1.e'][cont])
    Z2 = (df['z2'][cont], df['z2.e'][cont])
    M1 = (df['M1'][cont]*bias, df['M1.e'][cont]*bias)
    M2 = (df['M2'][cont]*bias, df['M2.e'][cont]*bias)
    D_proj = (df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont])

    t = MCengine_post_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)
    
    return cont, t

def update_dataframe(result, df):
    if result is None:
        return
    cont, t = result

    quantiles = [0.5, 0.16, 0.84]  # Define the quantiles to calculate: 50th (median), 16th, and 84th percentiles

    columns = ['M1p', 'M1p.lower', 'M1p.upper', 'M2p', 'M2p.lower', 'M2p.upper',
               'z1p', 'z1p.lower', 'z1p.upper', 'z2p', 'z2p.lower', 'z2p.upper',
               'd.proj.out', 'd.proj.out.lower', 'd.proj.out.upper',
               'v.rad.obs.out', 'v.rad.obs.out.lower', 'v.rad.obs.out.upper',
               'alpha.out', 'alpha.out.lower', 'alpha.out.upper',
               'v.3d.obs.out', 'v.3d.obs.out.lower', 'v.3d.obs.out.upper',
               'd.3d.out', 'd.3d.out.lower', 'd.3d.out.upper',
               'v.3d.col.out', 'v.3d.col.out.lower', 'v.3d.col.out.upper',
               'd.max.out', 'd.max.out.lower', 'd.max.out.upper',
               'TSC0', 'TSC0.lower', 'TSC0.upper', 'TSC1', 'TSC1.lower', 'TSC1.upper',
               'T.out', 'T.out.lower', 'T.out.upper', 'prob.out', 'prob.out.lower', 'prob.out.upper']

    # Iterate over the column names and their corresponding quantile indices
    for i, col in enumerate(columns):
        var = t[i // 3]  # Select the variable corresponding to the current column
        # Check if the variable is not None and is a numeric type
        if var is not None and np.issubdtype(var.dtype, np.number):
            # Calculate the quantile value and assign it to the corresponding cell in the dataframe
            df.loc[cont, col] = np.quantile(var, quantiles[i % 3])

def process_file(file):
    print(file)
    filename = dir_cat + file + '.txt'
    out_file = dir_output + file + '_MCMAC.txt'
    df = pd.read_csv(filename, sep="\t")

    df[['M1p', 'M1p.lower', 'M1p.upper', 'M2p', 'M2p.lower', 'M2p.upper',
        'z1p', 'z1p.lower', 'z1p.upper', 'z2p', 'z2p.lower', 'z2p.upper',
        'd.proj.out', 'd.proj.out.lower', 'd.proj.out.upper',
        'v.rad.obs.out', 'v.rad.obs.out.lower', 'v.rad.obs.out.upper',
        'alpha.out', 'alpha.out.lower', 'alpha.out.upper',
        'v.3d.obs.out', 'v.3d.obs.out.lower', 'v.3d.obs.out.upper',
        'd.3d.out', 'd.3d.out.lower', 'd.3d.out.upper',
        'v.3d.col.out', 'v.3d.col.out.lower', 'v.3d.col.out.upper',
        'd.max.out', 'd.max.out.lower', 'd.max.out.upper',
        'TSC0', 'TSC0.lower', 'TSC0.upper', 'TSC1', 'TSC1.lower', 'TSC1.upper',
        'T.out', 'T.out.lower', 'T.out.upper', 'prob.out', 'prob.out.lower', 'prob.out.upper']] = 0.
    
    # 条件に基づく行の削除
    if "1to1_b0" in filename:
        collision_time = 2 - 0.68
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to1_b0.5" in filename:
        collision_time = 2 - 0.66
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to1_b1" in filename:
        collision_time = 2 - 0.6
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to3_b0" in filename:
        collision_time = 2 - 0.8
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to3_b0.5" in filename:
        collision_time = 2 - 0.76
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to3_b1" in filename:
        collision_time = 2.5 - 1.18
        df = df[df['age'] <= 2.5]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to10_b0" in filename:  
        collision_time = 2 - 0.96
        df = df[df['age'] <= 2.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to10_b0.5" in filename:
        collision_time = 2.4 - 1.26
        df = df[df['age'] <= 2.4]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
    elif "1to10_b1" in filename:
        collision_time = 3 - 1.76
        df = df[df['age'] <= 3.0]
        df['merger'] = df['age'].apply(lambda x: 'pre' if x < collision_time else 'post')
        
    with Pool(processes=30) as pool:  # コア数を指定
        results = pool.starmap(process_cont, [(cont, df, filename) for cont in range(len(df))])
    
    for result in results:
        update_dataframe(result, df)

    out = df.to_csv(sep='\t', index=False, header=True)
    with open(out_file, 'w') as f:
        f.write(out)

if __name__ == "__main__":
    for file in files:
        process_file(file)
