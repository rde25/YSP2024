# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy



def find_range(midpoint, length, upper_bound):
    increment = 0
    if length % 2 == 0:
        increment = int(length / 2)
    else:
        increment = int((length - 1) / 2)
    lower = midpoint - increment
    higher = midpoint + increment
    if increment > midpoint or lower < 0 or higher >= upper_bound:
        return
    else:
        return [lower, higher]


def moving_average_right(array, index, length):
    try:
        if index + 1 < length: return
        xsum = 0
        checker = 0
        for i in range(index - length + 1, index + 1):
            xsum += array[i]
            checker += 1
        return xsum / length
    except:
        return


def moving_average_mid(array, midpoint_index, length):
    try:
        range_values = find_range(midpoint_index, length, len(array))
        lower = range_values[0]
        higher = range_values[1]
        xsum = 0
        checker = 0
        # print(str(index - increment+1) + " " + str(index + increment+1))
        for i in range(lower, higher + 1):
            xsum += array[i]
            checker += 1
        # print(y / length)
        # print(checker)
        return xsum / length
    except:
        return


def moving_standard_deviation_right(expected, array, index, length):
    if index + 1 < length: return
    try:
        xsum = 0
        checker = 0
        for i in range(index - length + 1, index + 1):
            xsum += math.pow(expected - array[i], 2)
            checker += 1
        pre = xsum / length
        return math.sqrt(pre)
    except:
        return


def moving_standard_deviation_mid(expected, array, midpoint_index, length):
    try:
        range_values = find_range(midpoint_index, length, len(array))
        lower = range_values[0]
        upper = range_values[1]
        ysum = 0
        checker = 0
        for i in range(lower, upper + 1):
            ysum += math.pow(expected - array[i], 2)
            checker += 1
        pre = ysum / length
        return math.sqrt(pre)
    except:
        return


def testing_z_analysis(test_array):
    test_array_length = len(test_array)

    print(test_array)
    print(test_array_length)

    # Test Moving Average (works)
    test_averages = []
    for j in range(0, test_array_length):
        ma = moving_average_mid(test_array, j, 3)
        if ma is not None:
            test_averages.append(ma)
        else:
            test_averages.append(None)
    print(test_averages)
    print(len(test_averages))

    # Test Moving Standard Deviation (works)
    test_deviations = []
    for j in range(0, test_array_length):
        md = moving_standard_deviation_mid(test_averages[j], test_array, j, 3)
        if md is not None:
            test_deviations.append(md)
        else:
            test_deviations.append(None)
    print(test_deviations)
    print(len(test_deviations))

    test_z_scores = []
    for i in range(0, test_array_length):
        if test_averages[i] is not None:
            z = (test_array[i] - test_averages[i]) / test_deviations[i]
            test_z_scores.append(z)
        else:
            test_z_scores.append(None)
    print(test_z_scores)
    print(len(test_z_scores))


def generate_vlines(graph, list):
    for i in list:
        graph.axvline(x=i, color='r')


def extract_values_from_file(file_name):
    reader = open(file_name, "r")
    values = [float(value.strip()) for value in reader]
    reader.close()
    return values


def get_moving_averages(array, skip, window_size):
    array_length = len(array)
    new_arr = []
    for i in range(0, array_length):
        if i <= (skip-1):
            new_arr.append(None)
            continue
        ma = moving_average_right(array, i, window_size)
        if ma is not None:
             new_arr.append(ma)
        else:
            new_arr.append(None)
    return new_arr


def get_deviations(val_array, average_array, skip, window_size):
    arr_length = len(val_array)
    new_arr = []
    for j in range(0, arr_length):
        if j <= (skip-1):
            new_arr.append(None)
            continue
        md = moving_standard_deviation_right(average_array[j], val_array, j, window_size)
        if md is not None:
            new_arr.append(md)
        else:
            new_arr.append(None)
    return new_arr


def get_z_scores(observed_arr, expected_arr, dev_arr):
    length = len(observed_arr)
    arr = []
    for i in range(0, length):
        if expected_arr[i] is not None:
            z = (observed_arr[i] - expected_arr[i]) / dev_arr[i]
            arr.append(z)
        else:
            arr.append(None)
    return arr


def z_analysis(file_name, zdev_threshold, window_size, change_point):
    values = extract_values_from_file(file_name)
    value_length = len(values)

    # Calculate Moving Averages
    moving_averages = get_moving_averages(values, 100, window_size)
    # print(moving_averages)
    # print(len(moving_averages))

    # Calculate Moving Standard Deviation
    deviations = get_deviations(values, moving_averages, 100, window_size)
    # print(deviations)
    # print(len(deviations))

    # Calculate Z-scores
    z_scores = get_z_scores(values, moving_averages, deviations)
    # print(z_scores)
    # print(len(z_scores))

    # Finding Outlier Z Scores

    """
    outlier_list = []
    for i in range(0, value_length):
        if z_scores[i] is not None:
            if abs(z_scores[i]) > abs(low_threshold):
                # print(i)
                outlier_list.append(i)
    """
    # print("\n")

    z_score_ma = get_moving_averages(z_scores, 0, window_size)
    # print(moving_averages)
    # print(len(z_score_ma))

    z_dev = get_deviations(z_scores, z_score_ma, 0, 15)
    #     # 50: 47, 37, 48
    #     # 25: 38, 37, 43
    #     # 20: 36, 31, 43
    #     # 15: 36, 32, 42
    #     # 10: 30, 29, 42

    # Adjust to remove "null" values
    # adjusted_moving_averages = numpy.array([i for i in moving_averages if i is not None])
    # adjusted_deviations = numpy.array([i for i in deviations if i is not None])
    # adjusted_z_scores = numpy.array([i for i in z_scores if i is not None])
    # adjusted_z_score_ma = numpy.array([i for i in z_score_ma if i is not None])

    # Domain
    x_values = [x for x in range(0, value_length)]
    # x_values = numpy.array([x for x in range(99, value_length - int(window_size / 2))])

    # xvzma = numpy.array([i for i in range(0, value_length) if z_score_ma[i] is not None])
    # xvzma = numpy.array([x for x in range(0, value_length), value_length - window_size)])

    fig, ax = plt.subplots(3)
    # fig, ax = plt.subplots(4)
    # fig, ax = plt.subplots(5)

    title = "Z-Score Analysis for " + file_name
    fig.suptitle(title)

    print()
    print()
    print(title)

    """Set Colors"""
    default_color = 'm'
    # default_color = 'c'
    cp_color = 'r*' # Change Point
    lmaxz_color = 'g*' # Local Max Z Score
    amaxz_color = 'k.' #  Absolute Max Z Score
    aminzc_color = 'y*' # Absolute Min Z Score
    zsd_color = 'b.' # Z Score Deviation Under Threshold

    # Create Legend
    cp_legend = mpatches.Patch(color='r', label='Change Point')
    loc_max_z_legend = mpatches.Patch(color='g', label='Local Maximum Z-Score')
    abs_max_z_legend = mpatches.Patch(color='k', label='Absolute Maximum Z-Score')
    # abs_min_z_legend = mpatches.Patch(color='y', label='Absolute Minimum Z-Score')
    zdll = 'Z-Score Deviation Under Threshold: ' + str(zdev_threshold)
    z_dev_legend = mpatches.Patch(color='b', label=zdll)
    fig.legend(handles=[cp_legend, loc_max_z_legend, abs_max_z_legend, z_dev_legend])

    # Plots

    # readd default color
    ax[0].plot(x_values, moving_averages, color=default_color)
    ax[0].set_title("Moving Average, Window=" + str(window_size))

    # ax[1].plot(x_values, deviations, color=default_color)
    # ax[1].set_title("Moving Standard Deviation, Window=" + str(window_size))

    ax[1].plot(x_values, z_scores, color=default_color)
    ax[1].set_title("Z-Scores")

    # ax[3].plot(x_values, z_score_ma)
    # ax[3].set_title("Z-Score Moving Average")

    # ax[4].plot(x_values, values, color=default_color)
    # ax[4].set_title("Actual Values")

    ax[2].plot(x_values, z_dev, color=default_color)
    ax[2].set_title("Z-Score Deviation, Window=15, ZMA Window=" + str(window_size))

    # Find Z Square Deviation Points
    adj_z_dev = [zd for zd in z_dev if zd is not None]
    min_z_dev_i = z_dev.index(min(adj_z_dev))

    print("Z Deviation Points (if applicable):")
    count = 0
    first_detect = -1
    for zd in adj_z_dev:
        """Z Deviation Threshold"""
        if zd < zdev_threshold:
            local_index = z_dev.index(zd)
            print(local_index)
            ax[0].plot(local_index, moving_averages[local_index], zsd_color, label="Deviant Z")
            # ax[1].plot(local_index, deviations[local_index], zsd_color, label="Deviant Z")
            ax[1].plot(local_index, z_scores[local_index], zsd_color, label="Deviant Z")
            # ax[3].plot(local_index, z_score_ma[local_index], zsd_color, label="Deviant Z")
            ax[2].plot(local_index, z_dev[local_index], zsd_color, label="Deviant Z")
            if count == 0:
                first_detect = local_index
            count += 1
        if zd == min(adj_z_dev):
            ax[0].plot(min_z_dev_i, moving_averages[min_z_dev_i], aminzc_color, label="Deviant Z")
            # ax[1].plot(min_z_dev_i, deviations[min_z_dev_i], aminzc_color, label="Deviant Z")
            ax[1].plot(min_z_dev_i, z_scores[min_z_dev_i], aminzc_color, label="Deviant Z")
            # ax[3].plot(min_z_dev_i, z_score_ma[local_index], zsd_color, label="Deviant Z")
            ax[2].plot(min_z_dev_i, z_dev[min_z_dev_i], aminzc_color, label="Deviant Z")
    print("Total ZDP: " + str(count))
    print("Distance to First: " + str(first_detect-change_point+1))

    # ax[4].plot(min_z_dev_i, z_dev[min_z_dev_i], 'm*')
    # ax[0].plot(min_z_dev_i, moving_averages[min_z_dev_i], 'm*')
    # ax[1].plot(min_z_dev_i, deviations[min_z_dev_i], 'm*')
    # ax[2].plot(min_z_dev_i, z_scores[min_z_dev_i], 'm*')
    # ax[3].plot(min_z_dev_i, z_score_ma[min_z_dev_i], 'm*')
    print("Lowest Z Deviation:")
    print(z_dev[min_z_dev_i])

    if change_point >= 0:
        cp_index = change_point - 1
        print("Distance from Change Point to Min Z Dev:")
        print(min_z_dev_i - cp_index)

        ax[0].plot(cp_index, moving_averages[cp_index], cp_color)
        # ax[1].plot(cp_index, deviations[cp_index], cp_color)
        ax[1].plot(cp_index, z_scores[cp_index], cp_color)
        # ax[3].plot(cp_index, z_score_ma[cp_index], cp_color)
        # ax[4].plot(cp_index, values[cp_index], cp_color)
        ax[2].plot(cp_index, z_dev[cp_index], cp_color)

        adj_z_1 = [i for i in z_scores if i is not None]
        adj_z_2 = []
        for j in range(cp_index - int(window_size), cp_index + int(window_size)):
            try:
                adj_z_2.append(z_scores[j])
            except:
                continue
        # print(adj_z_2)
        max_z_score = max(adj_z_2)
        max_z_score2 = max(adj_z_1)
        mzc2_index = z_scores.index(max_z_score2)

        print("Absolute Max Z Score:")
        print(max_z_score2)
        print("Distance from Absolute MZS to CPI:")
        print(mzc2_index-cp_index)

        print("Max Z Score in range of " + str(window_size*2) + " around CP:")
        print(max_z_score)
        max_z_score_index = z_scores.index(max_z_score)
        # print(max_z_score_index-cp_index) # 2, -6, 49
        print("Distance from Local Max Z Score to CPI:")
        print(max_z_score_index - cp_index)  # 2, -194, -557
        # print(max_z_score_index)
        # print("Actually...")
        # print(z_scores[cp_index])
        # print(cp_index)
        # print()
        ax[0].plot(max_z_score_index, moving_averages[max_z_score_index], lmaxz_color)
        ax[0].plot(mzc2_index, moving_averages[mzc2_index], amaxz_color)
        #
        # ax[1].plot(max_z_score_index, deviations[max_z_score_index], lmaxz_color)
        # ax[1].plot(mzc2_index, deviations[mzc2_index], amaxz_color)
        ax[1].plot(max_z_score_index, z_scores[max_z_score_index], lmaxz_color)
        ax[1].plot(mzc2_index, z_scores[mzc2_index], amaxz_color)
        # ax[3].plot(max_z_score_index, z_score_ma[max_z_score_index], lmaxz_color)
        # ax[3].plot(mzc2_index, z_score_ma[mzc2_index], amaxz_color)
        ax[2].plot(max_z_score_index, z_dev[max_z_score_index], lmaxz_color)
        ax[2].plot(mzc2_index, z_dev[mzc2_index], amaxz_color)
    else:
        adj_z_scores = [i for i in z_scores if i is not None]
        max_z = max(adj_z_scores)
        print("Absolute Max Z Score:")
        print(max_z)

    # for i in outlier_list:
    # ax[0].plot(i, moving_averages[i], lmaxz_color)
    # ax[1].plot(i, deviations[i], lmaxz_color)
    # ax[2].plot(i, z_scores[i], lmaxz_color)
    # ax[3].plot(i, z_score_ma[i], lmaxz_color)
    # ax[4].plot(i, values[i], lmaxz_color)

    fig.tight_layout()
    plt.show()

    # plt.show()

    # print(matplotlib.get_configdir())
    # print(len(adjusted_moving_averages))
    # print(len(adjusted_deviations))
    # print(len(adjusted_z_scores))
    # print(len(x_values))


# test_array = [3, 5, 6, 7, 8, 2, 5, 6, 7, 8, 2, 0]
# testing_z_analysis(test_array)
# window = 150


# for 50 & 15 & 0.25, works for all but 846 change
# for 50 & 25 & 0.25, works for all but 846 change
# for 50 & 25 & 0.32, isolated not on 1605 change, works for all but 846 change

def z_run():
    # window of 50, z dev threshold of 0.25, z dev window of 25 works for all but 846 change
    # 846 absolute maximum is near change point
    """T=0.25, W=50"""
    # z_analysis("846_change_point_255.txt", 0.25, 50, 255)  # z dev 0.312 with 50, 0.25, 15  | ---
    # z_analysis("2254_change_point_749.txt", 0.25, 50, 779)  # z dev 0.076 with 50, 0.25, 15 | 809
    # z_analysis("1605_change_point_450.txt", 0.25, 50, 450)  # z dev 0.078 with 50, 0.25, 15 | 465

    # z_analysis("846_no_change_point.txt", 0.20, 50, -1)  # z dev 0.418 with 50, 0.25, 15
    # z_analysis("2254_no_change_point.txt", 0.20, 50, -1)  # z dev 0.326 with 50, 0.25, 15
    # z_analysis("1605_no_change_point.txt", 0.20, 50, -1)  # z dev 0.259 with 50, 15 (0.226 with 50, 10)
    # z_analysis("1605_no_change_point_edited.txt", 0.20, 50, -1)

    # originally 5, then 4 & 2, then -3.5 & 1.8
    # # -2.5, -4, -4 for low threshold for z score

    """T=0.25, W=100"""
    # z_analysis("846_change_point_255.txt", 0.25, 100, 255) # z dev 0.151 with 100, 0.25, 15- 68 away | 298-323 = 26
    # # local max z 1.858 - +05 away | absolute 1.868 - +005 away
    # z_analysis("2254_change_point_749.txt", 0.25, 100, 799) # z dev 0.038 with 100, 0.25, 15 - 50 away | 825-870 but also 1178-1184 and 1200-1201 = 55-9=46
    # # local max z 0.969 - -19 away | absolute 2.102 - -557 away
    # z_analysis("1605_change_point_450.txt", 0.25, 100, 450) # z dev 0.049 with 100, 0.25, 15 - 53 away | 489-532 but also 942 = 45-1=44
    # # local max z 1.146 - -76 away | absolute 1.943 - -149 away

    """RUN: T=0.20, W=100"""
    # z_analysis("846_change_point_255.txt", 0.25, 100, 255) # z dev 0.151 with 100, 0.20, 15  - 68 away | 300-302 & 319-323 = 8
    # # local max z 1.858 - +05 away | absolute 1.868 - +005 away
    # z_analysis("2254_change_point_749.txt", 0.20, 100, 799) # z dev 0.038 with 100, 0.20, 15 - 50 away | 829-869 = 41
    # # local max z 0.969 - -19 away | absolute 2.102 - -557 away
    # z_analysis("1605_change_point_450.txt", 0.20, 100, 450) # z dev 0.049 with 100, 0.20, 15 - 53 away | 494-516 = 23
    # # local max z 1.146 - -76 away | absolute 1.943 - -149 away

    # z_analysis("846_no_change_point.txt", 0.20, 100, -1)  # z dev 0.416 with 100, 15
    # # absolute max z score 1.842
    # z_analysis("2254_no_change_point.txt", 0.20, 100, -1)  # z dev 0.267 with 100, 15
    # # absolute max z score 2.388
    # z_analysis("1605_no_change_point.txt", 0.20, 100, -1)  # z dev nan with 100, 15
    # # absolute max z score 1.256

    """T=0.25, W=150"""
    # z_analysis("846_change_point_255.txt", 0.25, 150, 255) # errors
    # z_analysis("2254_change_point_749.txt", 0.25, 150, 799) # z dev 0.068 with 150, 15 | 850-917
    # z_analysis("1605_change_point_450.txt", 0.25, 150, 450) # z dev 0.028 with 150, 15 | 521-564 but also 942

    # z_analysis("846_no_change_point.txt", -2.5, 150, -1)  # z dev 0.456 with 150, 15
    # z_analysis("2254_no_change_point.txt", -4, 150, -1)  # z dev 0.256 with 150, 15
    # z_analysis("1605_no_change_point.txt", -4, 150, -1)  # z dev nan with 150, 15

    """T=0.20, W=25"""
    z_analysis("846_change_point_255.txt", 0.20, 100, 255) # errors
    z_analysis("2254_change_point_749.txt", 0.20, 100, 799) # z dev 0.068 with 150, 15 | 850-917
    z_analysis("1605_change_point_450.txt", 0.20, 100, 450) # z dev 0.028 with 150, 15 | 521-564 but also 942

    z_analysis("846_no_change_point.txt", 0.20, 100, -1) # errors
    z_analysis("2254_no_change_point.txt", 0.20, 100, -1) # z dev 0.068 with 150, 15 | 850-917
    z_analysis("1605_no_change_point_edited.txt", 0.20, 100, -1) # z dev 0.028 with 150, 15 | 521-564 but also 942


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
