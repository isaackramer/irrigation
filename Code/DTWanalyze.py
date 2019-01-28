import pandas as pd
import matplotlib.pyplot as plt
from numpy import array, zeros, full, argmin, inf
from math import isinf

MEASUREMENTS_NUMBER = 26496
MEASUREMENTS_PER_DAY = 287


def signal_plot(signal1, signal2):
    plt.plot(signal1, 'r', label='signal1')
    plt.plot(signal2, 'g', label='signal2')
    plt.legend()
    plt.show()


def distance_cost_plot(cost_matrix, path,  x_title, y_title, title):

    plt.imshow(cost_matrix.T, interpolation='nearest', cmap='Reds')
    plt.gca().invert_yaxis()
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.grid()
    plt.colorbar()
    plt.plot(path[0], path[1], 'b')
    plt.show()


def day_mean_data_calculate(data):

    frames = []
    dates = [5, 6, 7]
    for i in dates:
        for j in range(1, 30):
            mask = (data['date_time'] >= '2018-' + str(i) +'-' + str(j)) & (data['date_time'] <= '2018-' + str(i) +'-' + str(j+1))
            temp = data.loc[mask]
            frames.append(temp.mean(axis=0, skipna=True))
    return frames



def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)


def dtw(x, y, dist, warp=1, w=inf, s=1.0):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure
    :param int warp: how many shifts are computed.
    :param int w: window size limiting the maximal distance between indices of matched entries |i,j|.
    :param float s: weight applied on off-diagonal moves of the path. As s gets larger, the warping path is increasingly biased towards the diagonal
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    assert isinf(w) or (w >= abs(len(x) - len(y)))
    assert s > 0
    r, c = len(x), len(y)
    if not isinf(w):
        D0 = full((r + 1, c + 1), inf)
        for i in range(1, r + 1):
            D0[i, max(1, i - w):min(c + 1, i + w + 1)] = 0
        D0[0, 0] = 0
    else:
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if (isinf(w) or (max(0, i - w) <= j <= min(c, i + w))):
                D1[i, j] = dist(x[i], y[j])
    C = D1.copy()
    jrange = range(c)
    for i in range(r):
        if not isinf(w):
            jrange = range(max(0, i - w), min(c, i + w + 1))
        for j in jrange:
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
            D1[i, j] += min(min_list)
    if len(x) == 1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path




def main(column1, column2):


    # Import csv file with proper datetime format
    df = pd.read_csv("TDR_data_clean.txt", parse_dates={'date_time': [0]}, dayfirst=True)

    # Edit column header names to enable splitting later on
    df.columns = (df.columns.str.replace(' ', '_').str.replace('(', '')
                  .str.replace(')', '').str.replace(',', '').str.replace('\'', '')
                  .str.replace('Interface', '').str.replace('Sensor_', ''))

    df = df.fillna(value=0)

    frames = day_mean_data_calculate(df)
    result = pd.concat(frames, axis=1).T
    x = result[column1]
    y = result[column2]

    l2_norm = lambda x, y: (x - y) ** 2

    d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=l2_norm)

    distance_cost_plot(cost_matrix, path, column1, column2, "Distance by day")


if __name__ == "__main__":
    main('A_VWC_1', 'A_VWC_2')

