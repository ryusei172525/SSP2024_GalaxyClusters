from multiprocessing import Pool
from MCMAC_pre_merger import MCengine_pre_merger
from MCMAC_post_merger import MCengine_post_merger 
import numpy as np
import pandas as pd

def empty(dataf, i):
    dataf.loc[i, 'M1p':'prob.out.upper'] = None

# 定義
N_mc = 1000

# 作業ディレクトリ
dir_cat = '../catalogues/'
dir_output = '../output/'

# 入力カタログ
files = [
    'zh_1to1_b0_z', 'zh_1to1_b0.5_z', 'zh_1to1_b1_z',
    'zh_1to3_b0_z', 'zh_1to3_b0.5_z', 'zh_1to3_b1_z',
    'zh_1to10_b0_z', 'zh_1to10_b0.5_z', 'zh_1to10_b1_z'
]

def process_cont(cont, df, filename):
    
    Z1 = (df['z1'][cont], df['z1.e'][cont])
    Z2 = (df['z2'][cont], df['z2.e'][cont])
    M1 = (df['M1'][cont], df['M1.e'][cont])
    M2 = (df['M2'][cont], df['M2.e'][cont])
    D_proj = (df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont], 0.05 * df['sep.Mpc'][cont])

    if cont + 1 < len(df):  # インデックスが範囲内であることを確認
        if df['sep.Mpc'][cont] > df['sep.Mpc'][cont + 1]:
            t = MCengine_pre_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)
        elif df['sep.Mpc'][cont] < df['sep.Mpc'][cont + 1]:
            t = MCengine_post_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)
        else:
            return None
    else:
        t = MCengine_post_merger(N_mc, M1, M2, Z1, Z2, D_proj, dir_output)
    
    return cont, t

def update_dataframe(result, df):
    if result is None:
        return
    cont, t = result

    quantiles = [0.5, 0.16, 0.84]
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
    
    for i, col in enumerate(columns):
        var = t[i // 3]
        if var is not None and np.issubdtype(var.dtype, np.number):
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
        df = df[df['age'] <= 2.0]
    elif "1to1_b0.5" in filename:
        df = df[df['age'] <= 2.0]
    elif "1to1_b1" in filename:
        df = df[df['age'] <= 2.0]
    elif ("1to3_b0" or "1to3_b0.5") in filename:
        df = df[df['age'] <= 2.0]
    elif "1to3_b1" in filename:
        df = df[df['age'] <= 2.5]
    elif "1to10_b0" in filename:  
        df = df[df['age'] <= 2.0]
    elif "1to10_b0.5" in filename:
        df = df[df['age'] <= 2.4]
    elif "1to10_b1" in filename:
        df = df[df['age'] <= 3.0]

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