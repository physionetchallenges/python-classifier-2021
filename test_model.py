#!/usr/bin/env python

# Do *not* edit this script.

import numpy as np, os, sys
from team_code import load_model, run_model
from helper_code import *

# Test model.
def test_model(model_directory, data_directory, output_directory):
    # Find header and recording files.
    print('Finding header and recording files...')

    header_files, recording_files = find_challenge_files(data_directory)
    num_recordings = len(recording_files)

    if not num_recordings:
        raise Exception('No data was provided.')

    # Create a folder for the outputs if it does not already exist.
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Identify the required lead sets.
    required_lead_sets = set()
    for i in range(num_recordings):
        header = load_header(header_files[i])
        leads = get_leads(header)
        sorted_leads = sort_leads(leads)
        required_lead_sets.add(sorted_leads)

    # Load models.
    leads_to_model = dict()
    print('Loading models...')
    for leads in required_lead_sets:
        model = load_model(model_directory, leads) ### Implement this function!
        leads_to_model[leads] = model

    # Run model for each recording.
    print('Running model...')

    for i in range(num_recordings):
        print('    {}/{}...'.format(i+1, num_recordings))

        # Load header and recording.
        header = load_header(header_files[i])
        recording = load_recording(recording_files[i])
        leads = get_leads(header)
        sorted_leads = sort_leads(leads)

        # Apply model to recording.
        model = leads_to_model[sorted_leads]
        classes, labels, probabilities = run_model(model, header, recording) ### Implement this function!

        # Save model outputs.
        recording_id = get_recording_id(header)
        head, tail = os.path.split(header_files[i])
        root, extension = os.path.splitext(tail)
        output_file = os.path.join(output_directory, root + '.csv')
        save_outputs(output_file, recording_id, classes, labels, probabilities)

    print('Done.')

if __name__ == '__main__':
    # Parse arguments.
    if len(sys.argv) != 4:
        raise Exception('Include the model, data, and output folders as arguments, e.g., python test_model.py model data outputs.')

    model_directory = sys.argv[1]
    data_directory = sys.argv[2]
    output_directory = sys.argv[3]

    test_model(model_directory, data_directory, output_directory)
