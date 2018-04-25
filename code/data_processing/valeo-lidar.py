#!/usr/bin/env python3

import os
import os.path as osp
import rays
import numpy as np
import datapool as dp
import multiprocessing as mp
import sys

DIR = osp.abspath('/datagrid/personal/jasekota/dip-dataset/valeo/zipfiles')
OUT_NPY = osp.abspath('/datagrid/personal/jasekota/dip-dataset/valeo/npys')
FILES = [osp.join(DIR, f) for f in os.listdir(DIR) if 'conv' in f]
THREADS = 20

def process_file(indir, outfile):
    fname = osp.basename(indir)
    all_files = [osp.join(indir, f) for f in os.listdir(indir) if f.endswith('.zip')]
    dapool = dp.DataPool(all_files, -1)
    data = []
    for i, ts in enumerate(dapool.tss):
        data.append(rays.get_lidar_data(dapool, ts, np.array([0, 0, 2.]), 0.005).astype('<f4'))
        print('Got array %d for file %s' % (i, fname))
        sys.stdout.flush()
    data = np.array(data)
    np.save(outfile, data)

outfiles = [osp.join(OUT_NPY, osp.basename(f)) + '.npy' for f in FILES]
os.makedirs(OUT_NPY, mode=0o755, exist_ok=True)


with mp.Pool(THREADS) as pool:
    pool.starmap(process_file, zip(FILES, outfiles))
