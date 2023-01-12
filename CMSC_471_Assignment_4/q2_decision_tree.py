import pandas as pd
import numpy as np

#code is best run on terminal with 'python3'
#make sure pandas and numpy are installed on computer

def countLabel(label, attribute):
    count = 0
    for i in label:  # count all the examples with that attribute
        if i == attribute:
            count += 1
    return count


## To Do: Write the entropy(label) function
## Should find the information entropy of dataset (T) with class "label" i.e. Info(T)
def entropy(label):
    values = set(label)  # make list of all possible values of label
    entropy = 0
    for i in values:  # for each possible vaule, calcaute the information entropy of that value/attribute
        labelCount = countLabel(label,i)  # number of apperance of that value then divide it by total data points in label to get probabilty
        entropy += -(labelCount / len(label)) * np.log2(labelCount / len(label))  # add I(value) to entropy
    return entropy


## To Do: Write the information_gain(feature, label) function
## Should find the information gain of "feature"(X) on dataset (T) with class "label" i.e. Gain(X,T)
def information_gain(dataset, feature, label):
    firstentropy = entropy(dataset[label])  # get entropy of label which is "INFLATED" or calcaute Info(T)
    print("First Entropy is", firstentropy)
    values = set(dataset[feature])  # make list of all possible values of feature
    splitdata = split(dataset, feature)  # split data by value of feature
    secondentropy = 0
    for index in splitdata:  # calcaute Info(X,T)
        print(index)
        secondentropy += (len(index) / len(dataset)) * entropy(index[label])  # calcuate (num of value of feature / total) * Info(value of that feature)
    print("Second Entropy is", secondentropy)
    information_gain = firstentropy - secondentropy  # get info gain, Gain(X,T) = Info(T) - Info(X,T)
    return information_gain


## To Do: Fill split(dataset, feature) function
## Should split the dataset on a feature
def split(dataset, feature):
    values = set(dataset[feature])  # get all possible vaules of feature
    list = []
    for value in values:  # create list of subsets of the data each with matching value of feature, thus splitting the data on that feature
        list.append(pd.DataFrame(dataset[dataset[feature] == value].copy()))
    return list


## To Do: Fill find_best_split(dataset, label) function
## Should find the best feature to split the dataset on
## Should return best_feature, best_gain
def find_best_split(dataset, label):
    ## TO DO: Find the best feature to split the dataset
    best_gain = 0 #highest gain that exists so far
    best_feature = [] #list of features that are tied for highest gain
    best_feature_name = None
    for columnName in dataset:  # for each feature
        print(columnName)
        if columnName != 'INFLATED':  # get info gain for each feature expect of the one with label T, F of course
            gain = information_gain(dataset, columnName, label)
            print(gain)
            if gain > best_gain:  # keep feature with the highest gain
                best_gain = gain
                best_feature_name = columnName
                best_feature.clear()
                best_feature.append(best_feature_name)
            elif gain == best_gain: # any feature that ties for highest gain in added to the list
                best_feature.append(columnName)
    return best_feature, best_gain


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = pd.read_csv('balloons.csv')

    best_feature, best_gain = find_best_split(data, "INFLATED")
    f = open("output_balloons.txt", "w")
    f.write("The Best Feature is {} with a Gain of : {}".format(best_feature, best_gain))
    f.close()
