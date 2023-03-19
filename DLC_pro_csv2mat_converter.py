# data format converter: csv (exported from DLC pro) -> mat
import os
import pandas as pd
import numpy as np
import scipy.io as scio

cwd = os.path.split(os.path.realpath(__file__))[0]
print("The current working directory:" + cwd)
print("Now to convert all csv in the current working directory and its subdirectory into mat format.")
input("Press ENTER to start...")

success_num = 0
err_num = 0
for (dir_name, sub_dirs, file_names) in os.walk(cwd):
    print("Working in: " + dir_name)
    for file_name in file_names:
        file_path = os.path.join(dir_name, file_name)
        if ((os.path.splitext(file_path)[1].lower() == ".csv")):
            print("    Converting " + file_path + "...", end="")
            try:
                data = pd.read_table(file_path, sep=";").iloc[:,:-1]
                data_dict = {"lda": np.array(data.iloc[:, 0]).reshape(len(data), 1)}
                for col in range(1, data.shape[1]):
                    data_dict["I" + str(col)] = np.array(data.iloc[:, col]).reshape(len(data), 1)
                scio.savemat(os.path.splitext(file_path)[0] + ".mat", data_dict, do_compression=True)
                success_num += 1
                print("Succeeded.")
            except Exception:
                err_num += 1
                print("Failed.")

print("Conversion process finished. Succuss: {}. Error: {}".format(success_num, err_num))
input("Press ENTER to quit...")