import numpy as np
import pandas as pd
import string
import operator

global_dict = {}

def convertToNpArray(train,test):
    """
    Converts the data into numpy arrays
    :param train: training data csv path
    :param test: test data csv path
    :return: training data and labels, test data and labels
    """
    train_data = pd.read_csv(train,delimiter=',', quotechar='"',
                             dtype=None,encoding = "ISO-8859-1",
                             usecols=[0,5])
    train_target = train_data.iloc[:,0]
    train_target_array = np.array(train_target)
    train_target_array = np.reshape(train_target_array,(len(train_target_array),1))
    train_data = train_data.iloc[:,1]
    train_data_array = np.array(train_data)
    train_data_array = np.reshape(train_data_array,(len(train_data_array),1))

    test_data = pd.read_csv(test,delimiter=',', quotechar='"',
                             dtype=None,encoding = "ISO-8859-1",
                            usecols=[0,5], names=['label','tweet'])
    test_data = test_data[test_data.label != 2]
    test_data = test_data.values
    test_target = test_data[:,0]
    test_target_array = np.array(test_target)
    test_target_array = np.reshape(test_target_array, (len(test_target_array), 1))
    test_data = test_data[:,1]
    test_data_array = np.reshape(test_data, (len(test_data), 1))

    return train_data_array,train_target_array,test_data_array,test_target_array

def remove_punc(data_array):
    """

    :param data_array:
    :return:
    """
    translator = str.maketrans(string.punctuation, len(string.punctuation)*' ')
    for i in range(len(data_array)):
        data_array[i][0] = data_array[i][0].translate(translator)
    return data_array
#end

def remove_stopwords(data_array,stopwords_file_path):
    """

    :param data_array:
    :param stopwords_file_path:
    :return:
    """
    stopwords = open(stopwords_file_path,'r')
    stopwords_list = stopwords.read().split('\n')
    for i in range(len(data_array)):
        tweet_tokenized = data_array[i][0].split(' ')
        tweet_tokenized = [word.lower() for word in tweet_tokenized]
        for word in tweet_tokenized:
            if word in stopwords_list:
                tweet_tokenized.remove(word)
        data_array[i][0] = ' '.join(tweet_tokenized)
    return data_array


#end


def build_global_vocab(data_array):
    """

    :param data_array:
    :return:
    """
    global features
    for i in range(len(data_array)):
        tweet_tokenized = data_array[i][0].split(' ')
        for word in tweet_tokenized:
            if word in global_dict.keys():
                global_dict[word] +=1
            else:
                global_dict[word] = 1
    global_dict.pop('')
    features = dict(sorted(global_dict.items(), key=operator.itemgetter(1),reverse=True)[:2000])



def encodeDataArray(data_array):
    global features
    top_2000_word_list = list(features.keys())
    encoded_array = np.empty((len(data_array),len(top_2000_word_list)))
    for i in range(len(data_array)):
        for j in range(len(top_2000_word_list)):
            if top_2000_word_list[j] in data_array[i][0]:
                encoded_array[i][j] = 1
            else:
                encoded_array[i][j] = 0
    return encoded_array

if __name__=="__main__":
    global features

    train_data_array, train_target_array, test_data_array,test_target_array=convertToNpArray\
        ('data/training.1600000.processed.noemoticon.csv','data/testdata.manual.2009.06.14.csv')

    #Round 1 - Remove stop words
    train_data_array = remove_stopwords(train_data_array, 'stopwords.txt')
    test_data_array = remove_stopwords(test_data_array, 'stopwords.txt')

    # Remove punctuations from train and test
    train_data_array = remove_punc(train_data_array)
    test_data_array = remove_punc(test_data_array)

    # Round 2 - Remove stop words
    train_data_array = remove_stopwords(train_data_array, 'stopwords.txt')
    test_data_array = remove_stopwords(test_data_array, 'stopwords.txt')

    #Build top 2000 words from training data array
    build_global_vocab(train_data_array)

    #Encode the training and test data
    train_encoded_array = encodeDataArray(train_data_array)
    test_encoded_array = encodeDataArray(test_data_array)

    np.save('data/train_encoded_array.npy',train_encoded_array)
    np.save('data/test_encoded_array.npy', test_encoded_array)


    # print(test_encoded_array)

    # print(global_dict)
    # print(features)
    # test_data_array = remove_stopwords(test_data_array, 'stopwords.txt')
    # print(train_data_array)
    # print(np.shape(train_data_array))
    # print(np.shape(train_target_array))
    # print(np.shape(test_data_array))
    # print(np.shape(test_target_array))
    # remove_punc(train_data_array)
    # print(test_data_array)
