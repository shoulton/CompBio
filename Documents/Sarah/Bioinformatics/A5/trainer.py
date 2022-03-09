import argparse
import numpy as np

def make_training_array(training_set):
    seq_len = len(training_set[0].strip())

    training_model = np.empty((4, seq_len), dtype=object)
    nt_dict = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

    for i in range(seq_len):
        line_dict = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        count = 0
        for line in training_set:
            c = line[i].upper()
            line_dict[c] = line_dict[c] + 1
            count += 1
        count = str(count)
        training_model[0, i] = str(line_dict['A']) + "/" + count
        training_model[1, i] = str(line_dict['C']) + "/" + count
        training_model[2, i] = str(line_dict['G']) + "/" + count
        training_model[3, i] = str(line_dict['T']) + "/" + count
    return training_model

def make_output_file(training_array, output_file):
    headers = "Position"
    num_positions = training_array.shape[1]
    for pos in range(num_positions):
        headers = headers + "\t" + str(pos + 1)
    a_line = "A"
    for pos in range(num_positions):
        a_line = a_line + "\t" + str(training_array[0,pos])
    c_line = "C"
    for pos in range(num_positions):
        c_line = c_line + "\t" + str(training_array[1,pos])
    g_line = "G"
    for pos in range(num_positions):
        g_line = g_line + "\t" + str(training_array[2,pos])
    t_line = "T"
    for pos in range(num_positions):
        t_line = t_line + "\t" + str(training_array[3,pos])

    out = headers + "\n" + a_line + "\n" + c_line + "\n" + g_line + "\n" + t_line + "\n"

    with open(output_file, "w") as of:
        of.write(out)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=True, type=str, help="input the training set file")
    parser.add_argument("-o",required=True, type=str, help="input the output file")
    args = parser.parse_args()

    training_set = []
    try:
        with open(args.f) as f:
            training_set = f.readlines()

    except Exception:
        print("An invalid training set was input, please check file and try again.")

    training_array = make_training_array(training_set)
    make_output_file(training_array, args.o)




