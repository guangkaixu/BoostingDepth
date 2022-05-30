import numpy as np
import cv2
import os
import os.path as osp
import matplotlib.pyplot as plt

from lwlr import sparse_depth_lwlr, recover_metric_depth

root = './test_imgs/'
mono_root = osp.join(root, 'pred_depth_mono')
mono_paths = os.listdir(mono_root)

for i, mono_path in enumerate(mono_paths):
    print('processing :', i , '/', len(mono_paths), mono_path)
    mono_path = osp.join(mono_root, mono_path)
    sparse_path = mono_path.replace('/pred_depth_mono/', '/sparse_depth/')
    if not osp.exists(sparse_path):
        print('passing :', sparse_path)
        continue
    
    mono_depth = np.load(mono_path)
    sparse_depth = np.load(sparse_path)

    global_depth = recover_metric_depth(mono_depth, sparse_depth)
    lwlr_depth = sparse_depth_lwlr(global_depth, sparse_depth, sample_mode='grid', sample_num=100)

    lwlr_path_npy = mono_path.replace('/pred_depth_mono/', '/output_lwlr_depth/npy/')
    lwlr_path_png = lwlr_path_npy.replace('/npy/', '/viz/').replace('.npy', '.png')
    os.makedirs(osp.dirname(lwlr_path_npy), exist_ok=True)
    os.makedirs(osp.dirname(lwlr_path_png), exist_ok=True)
    np.save(lwlr_path_npy, lwlr_depth)
    plt.imsave(lwlr_path_png, lwlr_depth, cmap='rainbow')
