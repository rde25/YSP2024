import zscore as Z
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy


# Individual values for expected (moving average) - observed (actual)
def chi_squared_value(expected_val, observed_val):
    try:
        return math.pow((observed_val-expected_val), 2)/expected_val
    except:
        return


def get_average(arr):
    sum = 0
    for x in arr:
        sum += x
    return sum/len(arr)


# Computes average of a range of values, compares individual values to it
def chi_over_range(focus, window_size, values):
    try:
        average = get_average(values[focus - window_size + 1:focus + 1])
        sum = 0
        for i in range(focus - window_size + 1, focus + 1):
            sum += chi_squared_value(average, values[i])
        return sum
    except:
        return


# Chi Value maintained the same over an interval, compared to next: weird graph
def generate_chi_values(expected_values, actual_values, window_size):
    cv = []
    for i in range(0, len(actual_values)):
        # this_chi_value = chi_over_range(i, window_size, values)
        if i == 0:
            cv.append(None)
        elif i % window_size == 0:
            this_chi_value = chi_squared_value(expected_values[i], actual_values[i])
            cv.append(this_chi_value)
        else:
            this_chi_value = cv[i - 1]
            cv.append(this_chi_value)
    return cv

def chi_analysis(file_name, window_size, change_point):
    values = Z.extract_values_from_file(file_name)
    val_length = len(values)

    moving_averages = Z.get_moving_averages(values, 0, window_size)
    # (moving_averages)

    deviations = Z.get_deviations(values, moving_averages, 0, window_size)

    # chi_values = generate_chi_values(moving_averages, values, window_size)
    chi_values = []
    for i in range(0, val_length):
        # this_chi_value = chi_squared_value(moving_averages[i], values[i])
        # this_chi_value = chi_over_range(i, window_size, values)
        this_chi_value = chi_over_range(i, window_size, moving_averages)
        chi_values.append(this_chi_value)

    # print(chi_values)

    chi_ma = Z.get_moving_averages(chi_values, 0, window_size)

    chi_dev = Z.get_deviations(chi_values, chi_ma, 0, window_size)

    x_values = [x for x in range(0, val_length)]


    # fig, ax = plt.subplots(5)
    fig, ax = plt.subplots(2)
    title = "Chi-Squared Analysis for " + file_name
    fig.suptitle(title)
    print()
    print()
    print(title)

    cp_index = change_point-1

    ax[0].plot(x_values, moving_averages)
    ax[0].set_title("Moving Average, Window=" + str(window_size))

    # ax[1].plot(x_values, deviations)
    # ax[1].set_title("Moving Standard Deviation, Window=" + str(window_size))

    ax[1].plot(x_values, chi_values)
    ax[1].set_title("Chi-Squared Values, Window=" + str(window_size))

    # ax[3].plot(x_values, chi_ma)
    # ax[3].set_title("Chi-Squared Moving Average, CSW=15, Window=" + str(window_size))

    # ax[4].plot(x_values, chi_dev)
    # ax[4].set_title("Chi-Squared Moving Deviation, CSW=15, Window=" + str(window_size))

    adj_chi = [c for c in chi_values if c is not None]

    count = 0
    first_detect = -1
    max_chi = max(adj_chi)
    mc_index = chi_values.index(max_chi)

    for c in adj_chi:
        if c > max_chi - max_chi * 0.25:
            local_index = chi_values.index(c)
            print(local_index)
            try:
                ax[0].plot(local_index, moving_averages[local_index], 'g.')
                # ax[1].plot(local_index, deviations[local_index], 'g.')
                ax[1].plot(local_index, chi_values[local_index], 'g.')
                # ax[3].plot(local_index, chi_ma[local_index], 'g.')
                # ax[4].plot(local_index, chi_dev[local_index], 'g.')
            except:
                pass
            if count == 0:
                first_detect = local_index
            count += 1
    count -= 1 # max is automatically one
    print("Outliers Detected: " + str(count))


    try:
        ax[0].plot(mc_index, moving_averages[mc_index], 'y*')
        # ax[1].plot(mc_index, deviations[mc_index], 'y*')
        ax[1].plot(mc_index, chi_values[mc_index], 'y*')
        # ax[3].plot(mc_index, chi_ma[mc_index], 'y*')
        # ax[4].plot(mc_index, chi_dev[mc_index], 'y*')
    except:
        pass

    if change_point > 0:
        ax[0].plot(cp_index, moving_averages[cp_index], 'r*')
        # ax[1].plot(cp_index, deviations[cp_index], 'r*')
        ax[1].plot(cp_index, chi_values[cp_index], 'r*')
        # ax[3].plot(cp_index, chi_ma[cp_index], 'r*')
        # ax[4].plot(cp_index, chi_dev[cp_index], 'r*')

        print("Detection Time: " + str(first_detect-cp_index))


    cp_legend = mpatches.Patch(color='r', label='Change Point')
    abs_max_c_legend = mpatches.Patch(color='y', label='Absolute Maximum Chi-Squared Value')
    close_to_max_c_legend = mpatches.Patch(color='g', label='Chi-Squared Values Close to Max')
    # abs_min_z_legend = mpatches.Patch(color='y', label='Absolute Minimum Z-Score')
    # zdll = 'Z-Score Deviation Under Threshold: ' + str(zdev_threshold)
    # z_dev_legend = mpatches.Patch(color='b', label=zdll)
    fig.legend(handles=[cp_legend, abs_max_c_legend, close_to_max_c_legend])


    fig.tight_layout()
    plt.show()

def chi_run():
    ws = 25
    # {function call} status for ws=25 | outliers ws = 25, detection time | status for ws=50, outliers ws=50, detection
    chi_analysis("log_normal_ade_846.txt", ws, -1) # true negative - spikes | 0 | false positive, 18
    chi_analysis("log_attack_ade_846.txt", ws, -1) # true negative - spikes | 0 | true negative, 0
    chi_analysis("cp_500_ade_846.txt", ws, 500) # true positive - parabola | 15, 18 | true positive, 2, 31
    chi_analysis("raw_cp_500_ade_846.txt", ws, 500) # false negative - spikes | 0, NA | false positive & false negative

    chi_analysis("log_attack_ade_2254.txt", ws, -1) # true negative - spikes | 0 | true negative - spikes/far, 1
    chi_analysis("log_normal_ade_2254.txt", ws, -1) # true negative - spikes | 0 | true negative
    chi_analysis("cp_800_ade_2254.txt", ws, 800) # true positive - parabola | 12, 18 | true positive, 23, 44
    chi_analysis("raw_cp_800_ade_2254.txt", ws, 800) # false negative - spikes | 0, NA | false negative - spikes

    chi_analysis("log_attack_ade_1605.txt", ws, -1) # true negative - spikes/far | 1 | true negative, 0
    chi_analysis("log_normal_ade_1605.txt", ws, -1) # true negative - spikes | 0 | true negative, 0
    chi_analysis("cp_800_ade_1605.txt", ws, 800) # true positive - parabola | 11, 22 | true positive, 25, 45
    chi_analysis("raw_cp_800_ade_1605.txt", ws, 800) # false negative - spikes/far | 1, NA | false negative

    # values = Z.extract_values_from_file("cp_500_ade_846.txt")
    # exp_500 = Z.get_moving_averages(values, 0, 50)
    # print(chi_over_range(500, 50, values))
    # print(generate_chi_values(exp_500, values, 50))
