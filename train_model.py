#!/usr/bin/env python

# Do *not* edit this script.

import sys
from team_code import training_code

if __name__ == '__main__':
    # Parse arguments.
    if len(sys.argv) != 3:
        raise Exception('Include the data and model folders as arguments, e.g., python train_model.py data model.')

    data_directory = sys.argv[1]
    model_directory = sys.argv[2]
    training_code(data_directory, model_directory) ### Implement this function!

    print('Done.')
