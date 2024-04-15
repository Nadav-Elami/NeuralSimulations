from js_utils import *


"""
creates 1326 json files that differ by their p_ab and p_ac values.
"""
def create_jsons_files():
    if not os.path.exists(JSONS_DIR_NAME):
        os.makedirs(JSONS_DIR_NAME)
    for i, r1 in enumerate(np.round(np.linspace(0.6, 12.8, 51), 2)):
        for r2 in np.round(np.linspace(0.6, 12.8, 51)[i:], 2):
            params = {"w": 1.6,
                    "w_inter": 6.5,
                    "w_ex":  6.5,
                    "w_inhibit": 5,
                    "p_ab": 1,
                    "p_ac": 1,
                    "p_bbin": 0.25,
                    "p_ccin": 0.25,
                    "r_bin": r1,
                    "r_cin": r2}
            create_json(os.path.join(JSONS_DIR_NAME, f"rbin_{r1}_rcin_{r2}.json"), params)


"""
creates the results directory that will contain the results for each json file.
"""
def create_results_dir():
    if not os.path.exists(RES_DIR_NAME):
        os.makedirs(RES_DIR_NAME)


if __name__ == "__main__":
    create_jsons_files()
    create_results_dir()


