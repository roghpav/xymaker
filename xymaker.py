#!/usr/bin/env python3
"""
XY Maker - Create aligned X and Y files for machine learning datasets.

This script processes unordered dataset and target files in CSV format, matching records by ID
to create aligned X (features) and Y (labels) files ready for machine learning applications.

Author:     Pável Adolfo Figueroa Rodríguez
Email:      figueroa.pav@gmail.com

Usage:
    python xymaker.py -d [unordered dataset] -t [unordered target] [-c column_index] [-x x_filename] [-y y_filename]
    
Input file format examples:
    Dataset file:
    ID,  feature0,    feature1, ...
    01,  0.230,       1.23,     ...
    02,  0.360,       2.25,     ...
    
    Target/label file:
    ID,    class1, class2, ...
    04,     0,      1,      ...
    01,     1,      1,      ...
"""

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)


class XYMaker:
    """Creates aligned X and Y data files from unordered dataset and target files."""
    
    def __init__(
        self, 
        features_file: str, 
        label_file: str, 
        column: int = 1, 
        x_filename: str = "x.csv", 
        y_filename: str = "y.csv",
        delimiter: str = ','
    ):
        """
        Initialize the XYMaker with file paths and processing options.
        
        Args:
            features_file: Path to the features/dataset CSV file
            label_file: Path to the labels/target CSV file
            column: Column index in the target file to extract labels (1-based indexing)
            x_filename: Output filename for features
            y_filename: Output filename for labels
            delimiter: CSV delimiter character
        """
        self.features_file = features_file
        self.label_file = label_file
        self.column = column
        self.output_x_filename = x_filename
        self.output_y_filename = y_filename
        self.delimiter = delimiter
        
        # Data containers
        self.features_data: List[List[str]] = []
        self.labels_data: List[List[str]] = []
        self.aligned_x_data: List[List[str]] = []
        self.aligned_y_data: List[List[str]] = []
    
    def process(self) -> Tuple[int, int]:
        """
        Process the input files and create aligned X and Y files.
        
        Returns:
            Tuple containing (number of matched records, number of unmatched records)
        """
        # Read input files
        self.features_data = self._read_csv(self.features_file)
        self.labels_data = self._read_csv(self.label_file)
        
        if not self.features_data or not self.labels_data:
            logging.error("One or both input files are empty or couldn't be read")
            return (0, 0)
        
        # Validate column index
        if self.column >= len(self.labels_data[0]):
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} Column index {self.column} is greater than "
                         f"the number of columns in target file ({len(self.labels_data[0])})")
            return (0, 0)
        
        # Get label column name
        label_column_name = self.labels_data[0][self.column]
        print(f"Using label column: {label_column_name}")
        
        # Store the header for the X file
        x_header = self.features_data[0]
        self.aligned_x_data.append(x_header)
        
        # Create a header for Y file with the label name
        self.aligned_y_data.append([label_column_name])
        
        # Create a dictionary for fast lookup of labels by ID
        labels_dict = self._create_labels_dict()
        
        # Align the data
        matched, unmatched = self._align_data(labels_dict)
        
        # Save the aligned data
        self._save_csv(self.output_x_filename, self.aligned_x_data)
        self._save_csv(self.output_y_filename, self.aligned_y_data)
        
        return matched, unmatched
    
    def _create_labels_dict(self) -> Dict[str, str]:
        """
        Create a dictionary mapping IDs to their corresponding label values.
        
        Returns:
            Dictionary with ID as key and label value as value
        """
        labels_dict = {}
        # Skip the header row (index 0)
        for row in self.labels_data[1:]:
            if row and len(row) > self.column:
                labels_dict[row[0]] = row[self.column]
        return labels_dict
    
    def _align_data(self, labels_dict: Dict[str, str]) -> Tuple[int, int]:
        """
        Align features with corresponding labels based on IDs.
        
        Args:
            labels_dict: Dictionary mapping IDs to labels
            
        Returns:
            Tuple of (matched_count, unmatched_count)
        """
        matched_count = 0
        unmatched_count = 0
        
        # Skip the header row (index 0)
        for row in self.features_data[1:]:
            if not row:
                continue
                
            record_id = row[0]
            if record_id in labels_dict:
                self.aligned_x_data.append(row)
                self.aligned_y_data.append([labels_dict[record_id]])
                matched_count += 1
            else:
                print(f"{Fore.BLUE}Info:{Style.RESET_ALL} No match found for ID {record_id} in target file")
                unmatched_count += 1
                
        return matched_count, unmatched_count
    
    def _read_csv(self, filename: str) -> List[List[str]]:
        """
        Read data from a CSV file into a list of lists.
        
        Args:
            filename: Path to the CSV file
            
        Returns:
            List of rows, where each row is a list of field values
        """
        data = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=self.delimiter)
                for row in reader:
                    data.append(row)
            return data
        except FileNotFoundError:
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} File {filename} not found")
        except PermissionError:
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} No permission to read {filename}")
        except Exception as e:
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} Failed to read {filename}: {str(e)}")
        return []
    
    def _save_csv(self, filename: str, data: List[List[str]]) -> bool:
        """
        Save data to a CSV file.
        
        Args:
            filename: Output file path
            data: List of rows to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimiter)
                writer.writerows(data)
            print(f"Successfully saved {filename}")
            return True
        except PermissionError:
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} No permission to write to {filename}")
        except Exception as e:
            logging.error(f"{Fore.RED}Error:{Style.RESET_ALL} Failed to save {filename}: {str(e)}")
        return False


def main():
    """Parse command line arguments and run the XY Maker."""
    parser = argparse.ArgumentParser(
        description="Create aligned X and Y files from unordered dataset and target files"
    )
    parser.add_argument("-d", "--dataset", dest="udataset", help="Unordered dataset file (CSV format)")
    parser.add_argument("-t", "--target", dest="utarget", help="Unordered target file (CSV format)")
    parser.add_argument("-c", "--column", type=int, default=1, 
                        help="Column index from target file (1-based indexing, default: 1)")
    parser.add_argument("-x", "--x-file", dest="x_filename", default="x.csv",
                        help="Output filename for features (default: x.csv)")
    parser.add_argument("-y", "--y-file", dest="y_filename", default="y.csv",
                        help="Output filename for labels (default: y.csv)")
    parser.add_argument("--delimiter", default=",", 
                        help="CSV delimiter character (default: comma)")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print(f"XY Maker - Create aligned X and Y files for machine learning datasets")
    print("=" * 80)
    
    # Check for required arguments
    if not args.udataset or not args.utarget:
        print("Missing required arguments.")
        print("\nUsage:")
        print("  python xymaker.py -d [dataset_file.csv] -t [target_file.csv] [-c column_index]")
        print("\nFor more information:")
        print("  python xymaker.py --help")
        print("=" * 80)
        return
    
    # Check if files exist
    dataset_path = Path(args.udataset)
    target_path = Path(args.utarget)
    
    if not dataset_path.is_file():
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Dataset file {args.udataset} does not exist")
        return
        
    if not target_path.is_file():
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Target file {args.utarget} does not exist")
        return
    
    # Validate column index
    if args.column < 1:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Column index must be greater than or equal to 1")
        return
    
    # Process files
    print(f"Creating features file: {args.x_filename} from: {args.udataset}")
    print(f"Creating labels file: {args.y_filename} from: {args.utarget} (column: {args.column})")
    
    maker = XYMaker(
        args.udataset, 
        args.utarget, 
        column=args.column,
        x_filename=args.x_filename,
        y_filename=args.y_filename,
        delimiter=args.delimiter
    )
    
    matched, unmatched = maker.process()
    
    print("\nProcessing complete:")
    print(f"  - Records matched: {matched}")
    print(f"  - Records not matched: {unmatched}")
    print(f"  - Total input records: {matched + unmatched}")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Process interrupted by user.{Style.RESET_ALL}")
        sys.exit(1)