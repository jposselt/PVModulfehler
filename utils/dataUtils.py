import pandas as pd
import sys

def createTimeIndexForDataframe(df,indexField):
    """Converts a given dataframe into a timeseries.
    
    Arguments:
        df {dataframe} -- The to be converted dataframe
        indexField {string} -- The time fieldname 
    
    Returns:
        [dataframe] -- the timeseries dataframe
    """
    df[indexField] = pd.DatetimeIndex(df[indexField])
    df.set_index(indexField, inplace=True)
    return df


def normalize(df):
    """A simple min max normalizer for a dataframe
    
    Arguments:
        df {dataframe} -- The dataframe to normalize
    
    Returns:
        dataframe -- The normalized dataframe
    """
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


def memtest():
    """Test how much memory ist available on the local machine.
    """
    sl = []
    i = 0
    fill_size = 1024
    if sys.version.startswith('2.7'):
        fill_size = 1003
    if sys.version.startswith('3'):
        fill_size = 497
    print(fill_size)
    MiB = 0
    while True:
        s = str(i).zfill(fill_size)
        sl.append(s)
        if i == 0:
            try:
                sys.stderr.write('size of one string %d\n' % (sys.getsizeof(s)))
            except AttributeError:
                pass
        i += 1
        if i % 1024 == 0:
            MiB += 1
            if MiB % 25 == 0:
                sys.stderr.write('%d [MiB]\n' % (MiB))
