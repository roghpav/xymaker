# XYMaker

A utility tool for preparing radiomics datasets by creating matched feature (x.csv) and label (y.csv) files from unordered datasets.

## Overview

XYMaker is designed to help researchers working with radiomics features by aligning feature datasets with their corresponding labels. It functions like a join operation that relates dataset files and target files by common values in their identifier columns.

This tool was created specifically for radiomics workflow preparation, where [PyRadiomics](https://pyradiomics.readthedocs.io/en/latest/) or similar tools generate feature files that need to be matched with clinical outcomes or other labels that may come from different sources or collaborators.

## Installation

```bash
# Clone the repository
git clone https://github.com/roghpav/xymaker.git
cd xymaker
```

## How to Use

```bash
python3 xymaker.py -d [unordered dataset] -t [unordered target] -c [target file column]
```

### Parameters:

- `-d, --dataset`: Path to your features dataset CSV file
- `-t, --target`: Path to your target/labels CSV file
- `-c, --column`: Column number in target file to extract as labels (default: 1)

## How It Works

The script uses the dataset file as a guide and creates:
1. **x.csv**: Contains the original feature data in the same order
2. **y.csv**: Contains only the target values corresponding to each row in x.csv

### Example Input Files

**Features file (dataset.csv):**

| ID | Feature1 | Feature2 | ... |
|----|----------|----------|-----|
| 01 | 0.352    | 1.245    | ... |
| 02 | 0.861    | 0.723    | ... |
| 03 | 1.442    | 0.982    | ... |
| 50 | 2.314    | 1.103    | ... |

**Labels file (labels.csv):**

| ID | Label1   | Label2   | ... |
|----|----------|----------|-----|
| 10 | 1        | 0        | ... |
| 01 | 0        | 1        | ... |
| 03 | 1        | 0        | ... |
| 30 | 0        | 1        | ... |

### Example Output Files

**x.csv:**
- Similar to the features file but potentially reordered

**y.csv:**
- Contains only the selected label column values matched to corresponding rows in x.csv

## Use in Radiomics Workflow

In radiomics analysis, this tool helps streamline the preparation of datasets for machine learning algorithms by:

1. Ensuring feature data and labels are properly aligned by case ID
2. Handling scenarios where different team members provide feature extraction and labeling
3. Preparing data in a format ready for training and testing ML models

## Requirements

- Python 3.x
- CSV input files with matching IDs in the first column

## License

[MIT License](LICENSE)