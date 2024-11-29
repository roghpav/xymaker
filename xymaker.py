'''
Author:     Pável Adolfo Figueroa Rodríguez
email:      figueroa.pav@gmail.com

make x.csv and y.csv files from unordered dataset file and unordered target file

$python xymaker.py -d [unordered dataset] -t [unordered target]

the first column of each file have to be ID, example:

dataset file:
ID,  feature0,    feature1, ...
01,  0.230,       1.23,     ...
02,  0.360,       2.25,     ...
.
.
.

target or label file:
#ID,    #class1 #class2 ...
04,     0,      1,      ...
01,     1,      1,      ...
.
.
.

'''

import csv
import argparse
import os
from colorama import Fore, Back, Style

class xy_maker():
    def __init__(self, features_file, label_file, column=1, xfilename=f"x.csv", yfilename=f"y.csv"):

        self.features_file = features_file
        self.label_file = label_file
        self.column = column
        self.outputXFileName = xfilename
        self.outputYFileName = yfilename

        self.y_list = list()
        self.x_list = list()

        self.__x__ = list()
        self.__y__ = list()

    def fromcvs(self):

        # open label file
        self.y_list = self.__readcvs__(self.label_file)

        # Open features file
        self.x_list = self.__readcvs__(self.features_file)

        if not ( (len(self.y_list)==0) or (len(self.x_list)==0) ):
            if self.column > len(self.y_list[0]):
                print(f"{Fore.RED}Error:{Style.RESET_ALL} column index is grater than columns number")
            else:
                # Remove the header of y list
                print(f"y file for column: {self.y_list[0][self.column]}")
                self.y_list.pop(0)

                # Append the header names row and then delete it
                self.__x__.append(self.x_list[0])
                self.x_list.pop(0)

                # -----------------------------------------------------------------------------------
                dict_list_y = dict()
                for idy in self.y_list:
                    dict_list_y.update({idy[0]:idy[self.column]})

                for idx in self.x_list:
                    try:
                        self.__y__.append([dict_list_y[idx[0]]])
                        self.__x__.append(idx)
                    except:
                        print(f"{Fore.BLUE}Info:{Style.RESET_ALL} no matches founds for ID {idx[0]} in target file")

                # -----------------------------------------------------------------------------------
                
                print(f"saving...")
                self.__savelist2csv__(self.outputXFileName, self.__x__)
                self.__savelist2csv__(self.outputYFileName, self.__y__)

    def __readcvs__(self, filename):

        templist = list()

        try:
            with open(filename) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    templist.append(row)
        except:
            print(f'{Fore.RED}Error:{Style.RESET_ALL} While trying to read {filename} please make sure it is a csv file ')

        return templist

    def __savelist2csv__(self, filename, listobj):

        try:
            with open(filename, 'w') as f:
                write = csv.writer(f)
                write.writerows(listobj)
        except:
            print(f'{Fore.RED}Error:{Style.RESET_ALL} While trying to save {filename} ')
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--udataset", help="Unordered dataset file cvs format")
    parser.add_argument("-t", "--utarget", help="Unordered target file cvs format")
    parser.add_argument("-c", "--column", help="Column from target (when the target file contains more than one label)")
    args = parser.parse_args()

    print(80*'-')
    print(f"x y csv files maker")
    print(f"make x.csv and y.csv files from unordered dataset file and unordered target file")

    if not ( (args.udataset==None) or (args.utarget==None)  ):
        if os.path.isfile(args.udataset) and os.path.isfile(args.utarget):
            column = 1
            contt = False
            if not(args.column == None):
                try:
                    column = int(args.column)
                    if column < 1:
                        print(f"{Fore.RED}Error:{Style.RESET_ALL} Column argument should be grater or equal than 1")
                    else:
                        contt = True
                except:
                    print(f"{Fore.RED}Error:{Style.RESET_ALL} Column argumnet should be a integer")
            else:
                print(f"Column no selected defaul column: 1")
                contt = True

            if contt:
                print(f"Creating a x file from: {args.udataset}")
                print(f"Creating a y file from: {args.utarget} Column selected: {column}")
                xym = xy_maker(args.udataset, args.utarget, column=column)
                xym.fromcvs()
        else:
            if not os.path.isfile(args.udataset):
                print(f'{Fore.RED}Error:{Style.RESET_ALL} {args.udataset} file does not exist')
            if not os.path.isfile(args.utarget):
                print(f'{Fore.RED}Error:{Style.RESET_ALL} {args.utarget} file does not exist')

    else:
        print(80*'-')
        print(f'How to use:')
        print(f'$python csv_xymaker.py -d [unordered dataset] -t [unordered target] -c [column from target, default 1]')
        print(80*'-')
    
    print(f"Done.")


if __name__ == '__main__':
    main()

