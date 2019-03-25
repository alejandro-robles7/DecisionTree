from pandas import read_csv, get_dummies
from math import log


def entropy(p):
    if p == 0 or p == 1:
        return 0
    else:
        p2 = 1 - p
        return -p * log(p, 2) - p2 * log(p2, 2)

def get(data, col_name):
    return data.loc[:, [col_name, target_col]]


def get_pivot(data):
    return get_dummies(data).groupby(target_col).sum()

def get_probs(data):
    return data.iloc[0] / data.sum()

def get_ent(data):
    return data.apply(entropy)

def get_gain(plus, n , counts, ents):
    return entropy(plus/n) - (counts.sum()/n).dot(ents)


def get_gains(data, col_name):
    n = data.shape[0]
    plus = sum(data[target_col] == 1)
    attribute = get(data, col_name)
    counts = get_pivot(attribute)
    probs = get_probs(counts)
    ents = get_ent(probs)
    gain = get_gain(plus, n, counts, ents)
    return counts.T[[1,0]], ents, gain


def get_best_attribute(data, exclude=None):
    global features_cols
    gain_dict = {}
    best_gain = -1
    best_attribute = None
    features_cols_copy = features_cols

    if exclude:
        features_cols_copy = features_cols_copy.drop(exclude)

    for col in features_cols_copy:
        counts, ents, gain = get_gains(data, col)
        gain_dict[col] = {'counts': counts, 'ent': ents, 'gain': gain}
        print(col, '| Gain:', gain)
        if gain > best_gain:
            best_gain = gain
            best_attribute = col
        print('Best Attribute:', best_attribute)
    return best_attribute, gain_dict



if __name__ == '__main__':
    target_col = 'Play'
    exclude_col = 'Day'
    df = read_csv('../data/playtennis.csv').drop(exclude_col, axis=1)
    features_cols = df.columns[df.columns != target_col]

    first_layer_best_attribute, first_layer_gain_dict = get_best_attribute(df)
    second_layer = df[first_layer_best_attribute].unique()
    second_layer_dict = {}

    for attribute in second_layer:
        data = df[df[first_layer_best_attribute] == attribute]
        try:
            best_attribute, gain_dict = get_best_attribute(data, first_layer_best_attribute)
            second_layer_dict[attribute] = {'best': best_attribute, 'dict': gain_dict}
        except:
            print(attribute, 'did not work')

    # data = df[df[first_layer_best_attribute] == 'Sunny']

    # Mild
    col = 'Temperature'
    data = df[df[col] == 'Mild']
    data2 = data[data['Humidity'] == 'Normal']
    # data3 = data2[data2['Outlook'] == 'Rain']
    # data3 = data2[data2['Outlook'] == 'Overcast']
    data3 = data2[data2['Outlook'] == 'Sunny']

    # Hot
    col = 'Temperature'
    data = df[df[col] == 'Hot']
    data2 = data[data['Humidity'] == 'High']
    # data3 = data2[data2['Outlook'] == 'Rain']
    # data3 = data2[data2['Outlook'] == 'Overcast']
    data3 = data2[data2['Outlook'] == 'Sunny']

    # Cool
    col = 'Temperature'
    data = df[df[col] == 'Cool']
    data2 = data[data['Outlook'] == 'Rain']
    # data3 = data2[data2['Outlook'] == 'Rain']
    # data3 = data2[data2['Outlook'] == 'Overcast']
    # data3 = data2[data2['Outlook'] == 'Sunny']
