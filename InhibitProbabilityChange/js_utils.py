import json
import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# change to informative names between different runs
# files names
JSONS_DIR_NAME = "jsons_bbin_0.25_r1_r2_pab_ac_1"
RES_DIR_NAME = "results_bbin_0.25_r1_r2_pab_ac_1"
ALL_RESULTS_FN = "results_pab_pac_bbin_0.25_r1_r2_pab_ac_1.json"

# 4 saved values names
NO_FIRE = "no_fire"
BOTH_FIRE = "both_fire"
B_WIN = "b_win"
C_WIN = "c_win"


"""
creates json file with the given parameters.
"""
def create_json(file_path, params):
    with open(file_path, 'w') as json_file:
        json.dump(params, json_file, indent=4)


"""
loads json file.
"""
def load_json(fn):
    fn = f"{JSONS_DIR_NAME}//{fn}"
    if not fn.endswith('json'):
        fn = fn + '.json'
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            dct = json.load(f)
        return dct
    else:
        return None


"""
creates matrix of specific value (col).
"""
def create_mat(file_path, col):
    with open(file_path, 'r') as f:
        data = json.load(f)
    mat = np.zeros((51, 51))
    for i, r1 in enumerate(np.round(np.linspace(0.6, 12.8, 51), 2)):
        for j, r2 in enumerate(np.round(np.linspace(0.6, 12.8, 51), 2)):
            val = [item["vals"][f"{col}"] for item in data if item.get("r_bin") == r1 and item.get("r_cin") == r2]
            if val:
                mat[i, j] = val[0]
    return mat


"""
creates heatmap of the given data.
"""
def create_heatmap(data, x_axis, y_axis, title, path):
    plt.figure(figsize=(10, 8))
    h = sns.heatmap(data, cmap=sns.cubehelix_palette(as_cmap=True), vmin=0, vmax=1)
    h.set(xlabel=x_axis, ylabel=y_axis)
    plt.title(title)
    # plt.savefig("pie_fig.svg", format='svg', bbox_inches='tight')
    plt.yticks(np.arange(0, len(data), 2), np.round(np.linspace(0.6, 12.8, 26), 2))
    plt.xticks(np.arange(0, len(data), 2), np.round(np.linspace(0.6, 12.8, 26), 2))
    h.set_yticklabels(h.get_yticklabels(), rotation=0, ha='right', fontsize=8)
    h.set_xticklabels(h.get_yticklabels(), rotation=0, ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{path}\\{title}.png", bbox_inches='tight')


"""
creates rgb plot of the 3 given matrices.
"""
def create_rgb_plot(r_mat, g_mat, b_mat, title, x_axis, y_axis, path):
    p = plt.figure(figsize=(10, 8))
    rgb_image = np.stack((np.sqrt(r_mat), np.sqrt(g_mat), np.sqrt(b_mat)), axis=-1)
    plt.imshow(rgb_image)
    plt.title(title)
    plt.yticks(np.arange(0, len(r_mat), 2), np.round(np.linspace(0.6, 12.8, 26), 2))
    plt.xticks(np.arange(0, len(r_mat), 2), np.round(np.linspace(0.6, 12.8, 26), 2))
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.xticks(rotation=0, ha='center', fontsize=8)
    plt.yticks(rotation=0, ha='right', fontsize=8)
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='C win'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='B win'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='No fire')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()
    plt.savefig(f"{path}\\{title}.png", bbox_inches='tight')
