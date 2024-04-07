from js_utils import *

"""
creates one results file that contains the results per each parameter file.
"""
def create_results_file():
    all_results = []
    for fn in os.listdir(RES_DIR_NAME):
        if fn.endswith(".json"):
            file_path = os.path.join(RES_DIR_NAME, fn)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                all_results.append(data)
    create_json(ALL_RESULTS_FN, all_results)
    print("created results file")
    return


create_results_file()

"""
creates the 5 heatmaps and rgb plot
"""
def create_all_plots(file_path, x_axis, y_axis):
    # creates 4 matrices
    b_win = create_mat(file_path, B_WIN)
    c_win = create_mat(file_path, C_WIN)
    no_fire = create_mat(file_path, NO_FIRE)
    both_fire = create_mat(file_path, BOTH_FIRE)

    # creates heatmaps from matrices
    create_heatmap(b_win, x_axis, y_axis, B_WIN,"/home/labs/ulanovsky/nadave/SSY/")
    create_heatmap(c_win, x_axis, y_axis, C_WIN,"/home/labs/ulanovsky/nadave/SSY/")
    create_heatmap(no_fire, x_axis, y_axis, NO_FIRE, "/home/labs/ulanovsky/nadave/SSY/")
    create_heatmap(both_fire, x_axis, y_axis, BOTH_FIRE, "/home/labs/ulanovsky/nadave/SSY/")
    create_heatmap((b_win+c_win), x_axis, y_axis, "One Fire", "/home/labs/ulanovsky/nadave/SSY/")
    # create_heatmap((b_win+c_win+no_fire+both_fire), x_axis, y_axis, "All together")

    # creates rgb plot for c_win, b_win, no_fire - success cases
    create_rgb_plot(c_win, b_win, no_fire, "R=C win, G=B win, B=No fire", x_axis, y_axis, "/home/labs/ulanovsky/nadave/SSY/")


create_all_plots(ALL_RESULTS_FN, "w_ac", "w_ab")