from pmf_functions import *

if __name__ == "__main__":
    # working directory that contains all xvgs
    pos_path = sys.argv[1]
    pos_files = sorted(glob(pos_path + "/*_water.xvg"), key=os.path.getmtime)
    plot_average_displacement_vs_site(pos_files[:-1])