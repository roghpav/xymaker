# xymaker!

Hi, this script is useful to get the x.csv and y.csv files from dataset and target or label files, it is like a join function that relates dataset files and target files by common values of the first column of both files, x files usually keep the identifier column and the header rows while y file only contains target values.

In the radiomics workflow it helps to test, specially when the information or target and labels files comes from different sources or persons


## How to use

```console
$ python3 xymaker.py -d [unordered dataset] -t [unordered target] -c [target file column]

```

By default, column selected is 1.

## How it works

The script takes the features file and makes the label file inserting the label value in the correspond line, it is important to note that the guide is the feature file. 

Example of feature file (feature file need to be csv):

|ID |Feature1|Feature2 |...|
|-- |---------|---------|---|
|01 |value		|value		|...|
|02 |value		|value		|...|
|...|...			|...			|...|
|50 |value 	  |value		|...|

Example of label file (label file need to be csv):

|ID |Label1		|Label2 	|...|
|-- |---------|---------|---|
|10 |value		|value		|...|
|01 |value		|value		|...|
|...|...			|...			|...|
|30 |value 	  |value		|...|

x.csv file is similar to feature file while y.csv file just keep the label of selected column