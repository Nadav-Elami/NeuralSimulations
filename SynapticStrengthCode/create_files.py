from js_utils import *

"""
creates 1326 json files that differ by their w_ab and w_ac values.
"""
def create_jsons_files():
    if not os.path.exists(JSONS_DIR_NAME):
        os.makedirs(JSONS_DIR_NAME)
    for i, w1 in enumerate(np.round(np.linspace(0, 10.5, 51), 2)): # Strong synaptic weight = 10.5
        for w2 in np.round(np.linspace(0, 10.5, 51)[i:], 2):
            params = {"w": 1.6,
                    "w_ab": w1,  
                    "w_ac": w2,
                    "w_ex":  6.5,
                    "w_inhibit": 5,
                    "p_ab": 0.5,
                    "p_ac": 0.5,
                    "p_bbin": 0.25,
                    "p_ccin": 0.25,
                    "r_bin": 3.2,
                    "r_cin": 3.2}
            create_json(os.path.join(JSONS_DIR_NAME, f"w_ab_{w1}_w_ac_{w2}.json"), params)


"""
creates the results directory that will contain the results for each json file.
"""
def create_results_dir():
    if not os.path.exists(RES_DIR_NAME):
        os.makedirs(RES_DIR_NAME)


if __name__ == "__main__":
    create_jsons_files()
    create_results_dir()




