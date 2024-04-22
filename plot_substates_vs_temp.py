import matplotlib.pyplot as plt
import sys
import numpy as np

def read_temp_vs_std(input_file):
    with open(input_file, 'r') as i:
        data = i.readlines()
    temp_vs_std = np.array([x.split() for x in data])
    return temp_vs_std.astype(float)

def get_substates_vs_temp(temp_vs_std, N):
    R = 0.008314 #kJ/mol K
    sqrt_N = np.sqrt(N)
    num_of_pts = temp_vs_std.shape[0]
    dof = np.zeros(num_of_pts)
    substates = np.zeros(num_of_pts)
    for i in range(num_of_pts):
        dof[i] = temp_vs_std[i, 1] / sqrt_N / R / temp_vs_std[i, 0]
        substates[i] = dof[i] ** 2 / 6

    return substates, dof

if __name__ == "__main__":
    input_file = sys.argv[1]
    N = int(sys.argv[2])
    temp_vs_std = read_temp_vs_std(input_file)
    temp = temp_vs_std[:, 0]
    substates, dof = get_substates_vs_temp(temp_vs_std, N)
    plt.plot(temp, substates, '-o')
    plt.xlabel("Temperature [K]")
    plt.ylabel("number of substates")
    plt.figure()
    plt.plot(temp, dof ** 2, '-o')
    for i in range(len(temp)):
        print("Degrees of freedom at %iK: %.2f"%(temp[i], dof[i]**2))
    plt.xlabel("Temperature [K]")
    plt.ylabel("Degrees of freedom")
    plt.show()

    pass