#!/usr/bin/env python

# Load libraries.
from helper_code import *
import os, sys, argparse
import numpy as np, scipy as sp, scipy.io

# Parse arguments.
def get_parser():
    description = 'Extract a reduced lead set from WFDB signal and header data.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_directory', type=str, required=True)
    parser.add_argument('-k', '--signal_key', type=str, required=False, default='val')
    parser.add_argument('-l', '--reduced_leads', type=str, nargs='*', required=True)
    parser.add_argument('-o', '--output_directory', type=str, required=True)
    return parser

# Run script.
def run(args):
    reduced_leads = args.reduced_leads
    num_reduced_leads = len(reduced_leads)

    # Find the full lead header and recording files.
    full_header_files, full_recording_files = find_challenge_files(args.input_directory)

    # Create a directory for the reduced lead header and recording files if it does not already exist.
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # Extract a reduced lead set from each pair of header and recording files.
    for full_header_file, full_recording_file in zip(full_header_files, full_recording_files):
        # Load full header and recording.
        full_header = load_header(full_header_file)
        full_recording = load_recording(full_recording_file, args.signal_key)

        # Get full lead names from header and check that are reduced leads are available.
        full_leads = get_leads(full_header)
        num_full_leads = len(full_leads)

        if np.shape(full_recording)[0] != num_full_leads:
            print('The signal file {} is malformed: the dimensions of the signal file are inconsistent with the header file {}.'.format(full_recording_file, full_header_file))
            sys.exit()

        unavailable_leads = [lead for lead in reduced_leads if lead not in full_leads]
        if unavailable_leads:
            print('The lead(s) {} are not available in the header file {}.'.format(', '.join(unavailable_leads), full_header_file))
            sys.exit()

        # Create the reduced lead header and recording files.
        head, tail = os.path.split(full_header_file)
        reduced_header_file = os.path.join(args.output_directory, tail)

        head, tail = os.path.split(full_recording_file)
        reduced_recording_file = os.path.join(args.output_directory, tail)

        root, extension = os.path.splitext(tail)
        recording_id = root

        # Initialize outputs.
        full_lines = full_header.split('\n')
        reduced_lines = list()

        # For the first line, we need to update the recording number and the number of leads.
        entries = full_lines[0].split()
        entries[0] = recording_id
        entries[1] = str(num_reduced_leads)
        reduced_lines.append(' '.join(entries))

        # For the next lines that describe the leads, we need to update the signal filename.
        reduced_indices = list()
        for lead in args.reduced_leads:
            i = full_leads.index(lead)
            reduced_indices.append(i)
            entries = full_lines[i+1].split()
            entries[0] = recording_id
            reduced_lines.append(' '.join(entries))

        # For the remaining lines that describe the other data, we do not need to update anything.
        for i in range(num_full_leads+1, len(full_lines)):
            entries = full_lines[i].split()
            reduced_lines.append(' '.join(entries))

        # Save the reduced lead header and recording files.
        with open(reduced_header_file, 'w') as f:
            f.write('\n'.join(reduced_lines))

        reduced_recording = full_recording[reduced_indices, :]
        d = {args.signal_key: reduced_recording}
        sp.io.savemat(reduced_recording_file, d)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
