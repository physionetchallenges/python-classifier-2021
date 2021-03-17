#!/usr/bin/env python

# Load libraries.
from helper_code import find_challenge_files, get_leads
import os, sys, argparse
import numpy as np, scipy as sp
from scipy.io import loadmat

# Parse arguments.
def get_parser():
    description = 'Extract reduced-lead sets from the WFDB signal and header data.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_directory', type=str, required=True)
    parser.add_argument('-k', '--key', type=str, required=False, default='val')
    parser.add_argument('-l', '--reduced_leads', type=str, nargs='*', required=True)
    parser.add_argument('-o', '--output_directory', type=str, required=True)
    return parser

# Run script.
def run(args):
    # Identify the reduced leads.
    reduced_leads = args.reduced_leads
    num_reduced_leads = len(reduced_leads)

    # Create a directory for the reduced-lead header and recording files if it does not already exist.
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # Identify the full-lead header and recording files.
    full_header_files, full_recording_files = find_challenge_files(args.input_directory)

    # Extract a reduced-lead set from each pair of full-lead header and recording files.
    for full_header_file, full_recording_file in zip(full_header_files, full_recording_files):
        # Load a pair of full-lead header and recording files.
        with open(full_header_file, 'r') as f:
            full_header = f.read()
        x = loadmat(full_recording_file)[args.key]
        full_recording = np.asarray(x)

        full_lines = full_header.split('\n')
        full_leads = get_leads(full_header)
        num_full_leads = len(full_leads)

        # Check that the header and recording files match.
        if np.shape(full_recording)[0] != num_full_leads:
            print('The signal file {} is malformed: the dimensions of the signal file are inconsistent with the header file {}.'.format(full_recording_file, full_header_file))
            sys.exit()

        # Check that all of the reduced leads are available.
        unavailable_leads = [lead for lead in reduced_leads if lead not in full_leads]
        if unavailable_leads:
            print('The lead(s) {} are not available in the header file {}.'.format(', '.join(unavailable_leads), full_header_file))
            sys.exit()

        # Create a pair of reduced-lead header and recording files.
        head, tail = os.path.split(full_header_file)
        reduced_header_file = os.path.join(args.output_directory, tail)

        head, tail = os.path.split(full_recording_file)
        reduced_recording_file = os.path.join(args.output_directory, tail)

        # For the first line of the header file that describes the recording, update the number of leads.
        reduced_lines = list()

        entries = full_lines[0].split()
        entries[1] = str(num_reduced_leads)
        reduced_lines.append(' '.join(entries))

        # For the next lines of the header file that describe the leads, extract the reduced leads.
        reduced_indices = list()
        for i in range(num_reduced_leads):
            j = full_leads.index(reduced_leads[i])
            reduced_indices.append(j)
            entries = full_lines[j+1].split()
            reduced_lines.append(' '.join(entries))

        # For the remaining lines that describe the other data, copy the lines as-is.
        for j in range(num_full_leads+1, len(full_lines)):
            entries = full_lines[j].split()
            reduced_lines.append(' '.join(entries))

        # Save the reduced lead header and recording files.
        with open(reduced_header_file, 'w') as f:
            f.write('\n'.join(reduced_lines))

        reduced_recording = full_recording[reduced_indices, :]
        d = {args.key: reduced_recording}
        sp.io.savemat(reduced_recording_file, d, format='4')

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
