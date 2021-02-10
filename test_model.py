#!/usr/bin/env python

# Do *not* edit this script.

import numpy as np, os, sys
from team_code import load_twelve_lead_model, load_six_lead_model, load_three_lead_model, load_two_lead_model
from team_code import run_twelve_lead_model, run_six_lead_model, run_three_lead_model, run_two_lead_model
from helper_code import *

# Test model.
def test_model(model_directory, data_directory, output_directory):
    # Load model.
    print('Loading models...')

    twelve_lead_model = load_twelve_lead_model(model_directory)
    six_lead_model = load_six_lead_model(model_directory)
    three_lead_model = load_three_lead_model(model_directory)
    two_lead_model = load_two_lead_model(model_directory)

    # Find header and recording files.
    print('Finding header and recording files...')

    header_files, recording_files = find_challenge_files(data_directory)
    num_recordings = len(recording_files)

    if not num_recordings:
        raise Exception('No data was provided.')

    # Create a folder for the outputs if it does not already exist.
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    # Run model for each recording.
    print('Running model...')

    for i in range(num_recordings):
        print('    {}/{}...'.format(i+1, num_recordings))

        # Load header and recording.
        header = load_header(header_files[i])
        recording = load_recording(recording_files[i])
        leads = get_leads(header)

        # Apply model to recording.
        if all(lead in leads for lead in twelve_leads):
            classes, labels, probabilities = run_twelve_lead_model(twelve_lead_model, header, recording)
        elif all(lead in leads for lead in six_leads):
            classes, labels, probabilities = run_six_lead_model(six_lead_model, header, recording)
        elif all(lead in leads for lead in three_leads):
            classes, labels, probabilities = run_three_lead_model(three_lead_model, header, recording)
        elif all(lead in leads for lead in two_leads):
            classes, labels, probabilities = run_two_lead_model(two_lead_model, header, recording)
        else:
            raise NotImplementedError('No model is implemented for the lead set {}.'.format(', '.join(leads)))

        # Save model outputs.
        head, tail = os.path.split(header_files[i])
        root, extension = os.path.splitext(tail)
        output_file = os.path.join(output_directory, root + '.csv')
        save_outputs(output_file, classes, labels, probabilities)

    print('Done.')

if __name__ == '__main__':
    # Parse arguments.
    if len(sys.argv) != 4:
        raise Exception('Include the model, data, and output folders as arguments, e.g., python test_model.py model data output.')

    model_directory = sys.argv[1]
    data_directory = sys.argv[2]
    output_directory = sys.argv[3]

    test_model(model_directory, data_directory, output_directory)
