#!/usr/bin/env python

# Load libraries.
import os, sys, argparse
from scipy.io import savemat
from helper_code import find_challenge_files, load_header, load_recording, get_leads

# Parse arguments.
def get_parser():
    description = 'Extract reduced-lead ECGs from WFDB signal and header data.'
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
        # Load the full-lead header file.
        full_header = load_header(full_header_file)
        full_leads = get_leads(full_header)
        num_full_leads = len(full_leads)

        # Update the header file.
        full_lines = full_header.split('\n')
        reduced_lines = list()

        # For the first line, update the number of leads.
        entries = full_lines[0].split()
        entries[1] = str(num_reduced_leads)
        reduced_lines.append(' '.join(entries))

        # For the next lines, extract the lead metadata but reorder as needed.
        reduced_indices = list()
        for i in range(num_reduced_leads):
            j = full_leads.index(reduced_leads[i])
            reduced_lines.append(full_lines[j+1])

        # For the remaining lines, extract the rest of the data as-is.
        for j in range(num_full_leads+1, len(full_lines)):
            reduced_lines.append(full_lines[j])

        # Save the reduced-lead header file.
        head, tail = os.path.split(full_header_file)
        reduced_header_file = os.path.join(args.output_directory, tail)
        with open(reduced_header_file, 'w') as f:
            f.write('\n'.join(reduced_lines))

        # Load the full-lead recording file, extract the lead data, and save the reduced-lead recording file.
        recording = load_recording(full_recording_file, full_header, reduced_leads, args.key)
        d = {args.key: recording}

        head, tail = os.path.split(full_recording_file)
        reduced_recording_file = os.path.join(args.output_directory, tail)
        savemat(reduced_recording_file, d, format='4')

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
