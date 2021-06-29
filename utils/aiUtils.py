import pandas as pd
import numpy as np
import keras.backend as k
from sklearn.preprocessing import MinMaxScaler
from pickle import dump, load
import sys
import utils.evaluation as evaluation

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

def sensitiveResample(df,dataSplitField,resampleTime):
    """Changes the time resolution of a timeseries but respects the string 
       and other static values. In addition it can resample multiple timeseries in one dataframe
    
    Arguments:
        df {dataframe} -- The timeseries to resample
        dataSplitField {str} -- The identifier for individual timeseries (eg. moduleid)
        resampleTime {str} -- Resample rule (eg. 5T for 5 minutes)
    
    Returns:
        [dataframe] -- The resampled timeseries
    """
    allData = pd.DataFrame(columns=df.columns)
    uniqueIds = df[dataSplitField].unique()

    for currentId in uniqueIds:
        tmpDf = df[df[dataSplitField] == currentId]
        restOfResample = tmpDf.select_dtypes(exclude=['int','float64']) #'number',
        tmpColToReadd = restOfResample.columns
        tmpDataToReadd = restOfResample.iloc[0]
        tmpDf = tmpDf.resample(resampleTime).mean()
        tmpDf = tmpDf.interpolate(limit=2)
        for tmpCol in tmpColToReadd:
            tmpDf[tmpCol] = tmpDataToReadd.at[tmpCol]
        allData = allData.append(tmpDf)

    return allData

def reshapeDataForPredictionLSTM (df,timestepLength,yColumns,yLength = 1,minutefieldNumber = 0):
    """Reshapes a 2D timeseries Dataframe into a 3D numpy array. In the right way to use it for an LSTM network
    It produces the X and Y values for the LSTM, a field with the accumulative minutes of the day is required for it to work, 
    so it only uses samples within one day

    Arguments:
        df {dataframe} -- The dataframe to reshape
        timestepLength {int} -- The timestep length for X
        yColumns {list} -- The column names for Y

    Keyword Arguments:
        yLength {int} -- Currently not used, the length of Y to predit more then one value, will be splitted into another function (default: {1})
        minutefieldNumber {int} -- The minute field as described (default: {0})

    Returns:
        [dict] -- X and Y for the LSTM
    """
    dataframeAsArray = df.to_numpy(copy=True)
    dataframeAsArrayForY = df[yColumns].to_numpy(copy=True)
    dataFrameLength = dataframeAsArray.shape[0]
    samplesX = list()
    samplesY = list()
    timesteps = timestepLength
    for i in range(dataFrameLength-(timesteps+1)):
        if dataframeAsArray[i+timesteps+1][minutefieldNumber] > dataframeAsArray[i+timesteps][minutefieldNumber]:
            sample = dataframeAsArray[i:i+timesteps]	
            samplesX.append(sample)
            samplesY.append(dataframeAsArrayForY[i+timesteps+1])

    samplesX =np.array(samplesX)
    samplesY =np.array(samplesY)

    return {'x':samplesX,'y':samplesY}

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


def percenterror(y_true, y_pred): 
    """calculate the percentage error of two arrays
    
    Arguments:
        y_true {list} -- The real values
        y_pred {list} -- The predicted values
    
    Returns:
        float -- The percentage error 
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    
    y_true = y_true+0.00001
    y_pred = y_pred+0.00001
    
    y_true = y_true/100
    
    y_pred = y_pred/y_true
    
    y_pred = y_pred -100
    
    np.abs(y_pred)

    for i in range(len(y_pred)):
        if y_pred[i] > 100:
           y_pred[i] = 10 

    return np.sum(y_pred)/len(y_pred)

def fullMetrics(y_true, y_pred):
    """Evaluates the model with multiple evaluation methods
    
    Arguments:
        y_true {np.array} -- The real values
        y_pred {np.array} -- The predicted values
    
    Returns:
        [dict] -- metrics
    """
    return evaluation.evaluate_all(y_true,y_pred)


def root_mean_squared_error(y_true, y_pred):
    """Calculates the root mean squared error with the keras backend, so its compatible to the GPU. 
       Because Keras dosn't support it out of the box
    
    Arguments:
        y_true {list} -- Real value(s)
        y_pred {list} -- Predicted value(s)
    
    Returns:
        [float64] -- RSME
    """
    return k.sqrt(k.mean(k.square(y_pred - y_true))) 

def scaleDataframeAndSaveScalers(df,outputColumns,savePath,filename):
    """Scales the output and the input columns of a dataframe indiviually and saves the scalers for later use.

    
    Arguments:
        df {dataframe} -- The unscaled dataframe
        outputColumns {list} -- List of the output columns (Y)
        savePath {str} -- Folder for saving the scaler
        filename {str} -- Filename for the scalers
    
    Returns:
        [dataframe] -- The scaled dataframe
    """
    scalerOutput = MinMaxScaler()
    scalerRest = MinMaxScaler()
    df[outputColumns] = scalerOutput.fit_transform(df[outputColumns])

    df[df.columns.difference(outputColumns)] = scalerRest.fit_transform(df[df.columns.difference(outputColumns)])

    #Save scaler
    dump(scalerOutput, open(savePath + 'output_scaler' + filename + '.pkl', 'wb'))
    dump(scalerRest, open(savePath + 'rest_scaler' + filename + '.pkl', 'wb'))
    
    #Drop empty columns or rows after scaling! this is the case when we have the same value in an entire column
    df = df.dropna(axis=1,how='all')
    df.drop([col for col, val in df.sum().iteritems() if val == 0], axis=1, inplace=True)
    return df

def loadScalers(loadPath,filename):
    """Loads the previeous saved scalers from a file.
    
    Arguments:
        loadPath {str} -- folder where the scalers are located
        filename {str} -- Filename of the scalers
    
    Returns:
        [dict] -- output and input scaler.
    """
    scalerOutput = load(open(loadPath + 'output_scaler' + filename + '.pkl', 'rb'))
    scalerRest = load(open(loadPath + 'rest_scaler' + filename + '.pkl', 'rb'))
    return {'output':scalerOutput, 'input':scalerRest}

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
