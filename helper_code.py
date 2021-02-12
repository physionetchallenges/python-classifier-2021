#!/usr/bin/env python

# Do *not* edit this script.
# These are helper variables and functions that you can use with your code.

import numpy as np, os
from scipy.io import loadmat

# Define 12, 6, and 2 lead ECG sets.
twelve_leads = ('I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6')
six_leads = ('I', 'II', 'III', 'aVR', 'aVL', 'aVF')
three_leads = ('I', 'II', 'V2')
two_leads = ('II', 'V5')

# Check if a variable is an integer or represents an integer.
def is_integer(x):
    try:
        if int(x)==float(x):
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False

# Find header and recording files.
def find_challenge_files(data_directory):
    header_files = list()
    recording_files = list()
    for f in os.listdir(data_directory):
        root, extension = os.path.splitext(f)
        if not root.startswith('.') and extension=='.hea':
            header_file = os.path.join(data_directory, root + '.hea')
            recording_file = os.path.join(data_directory, root + '.mat')
            if os.path.isfile(header_file) and os.path.isfile(recording_file):
                header_files.append(header_file)
                recording_files.append(recording_file)
    return header_files, recording_files

# Load header file as a string.
def load_header(header_file):
    with open(header_file, 'r') as f:
        header = f.read()
    return header

# Load recording file as an array.
def load_recording(recording_file, header=None, leads=None, key='val'):
    x = loadmat(recording_file)[key]
    recording = np.asarray(x, dtype=np.float32)
    return recording

# Get leads from header.
def get_leads(header):
    leads = list()
    for i, l in enumerate(header.split('\n')):
        entries = l.split(' ')
        if i==0:
            num_leads = int(entries[1])
        elif i<=num_leads:
            leads.append(entries[-1])
        else:
            break
    return leads

# Get age from header.
def get_age(header):
    age = None
    for l in header.split('\n'):
        if l.startswith('#Age'):
            try:
                age = float(l.split(': ')[1].strip())
            except:
                age = float('nan')
    return age

# Get age from header.
def get_sex(header):
    sex = None
    for l in header.split('\n'):
        if l.startswith('#Sex'):
            try:
                sex = l.split(': ')[1].strip()
            except:
                pass
    return sex

# Get frequency from header.
def get_num_leads(header):
    num_leads = None
    for i, l in enumerate(header.split('\n')):
        if i==0:
            try:
                num_samples = float(l.split(' ')[1])
            except:
                pass
        else:
            break
    return num_leads

# Get frequency from header.
def get_frequency(header):
    frequency = None
    for i, l in enumerate(header.split('\n')):
        if i==0:
            try:
                frequency = float(l.split(' ')[2])
            except:
                pass
        else:
            break
    return frequency

# Get number of samples from header.
def get_num_samples(header):
    num_samples = None
    for i, l in enumerate(header.split('\n')):
        if i==0:
            try:
                num_samples = float(l.split(' ')[3])
            except:
                pass
        else:
            break
    return num_samples

# Get ADC gains (ADC units per physical unit), floating-point number for ECG leads, from header.
def get_adcgains(header, leads):
    adc_gains = np.zeros(len(leads), dtype=np.float32)
    for i, l in enumerate(header.split('\n')):
        entries = l.split(' ')
        if i==0:
            num_leads = int(entries[1])
        elif i<=num_leads:
            current_lead = entries[-1]
            if current_lead in leads:
                j = leads.index(current_lead)
                try:
                    adc_gains[j] = float(entries[2].split('/')[0])
                except:
                    pass
        else:
            break
    return adc_gains

# Get baselines from header.
def get_baselines(header, leads):
    baselines = np.zeros(len(leads), dtype=np.float32)
    for i, l in enumerate(header.split('\n')):
        entries = l.split(' ')
        if i==0:
            num_leads = int(entries[1])
        elif i<=num_leads:
            current_lead = entries[-1]
            if current_lead in leads:
                j = leads.index(current_lead)
                try:
                    baselines[j] = float(entries[4].split('/')[0])
                except:
                    pass
        else:
            break
    return baselines

# Get labels from header.
def get_labels(header):
    labels = list()
    for l in header.split('\n'):
        if l.startswith('#Dx'):
            entries = l.split(': ')[1].split(',')
            for entry in entries:
                labels.append(entry.strip())
    return labels

# Save outputs from model.
def save_outputs(output_file, classes, labels, probabilities):
    # Extract the recording identifier from the filename.
    head, tail = os.path.split(output_file)
    root, extension = os.path.splitext(tail)
    recording_identifier = root

    # Format the model outputs.
    recording_string = '#{}'.format(recording_identifier)
    class_string = ','.join(str(c) for c in classes)
    label_string = ','.join(str(l) for l in labels)
    probabilities_string = ','.join(str(p) for p in probabilities)
    output_string = recording_string + '\n' + class_string + '\n' + label_string + '\n' + probabilities_string + '\n'

    # Save the model outputs.
    with open(output_file, 'w') as f:
        f.write(output_string)
