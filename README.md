# Python example code for the PhysioNet/Computing in Cardiology Challenge 2021

## What's in this repository?

We implemented a random forest classifier that uses age, sex, and the root mean square of the ECG lead signals as features. This simple example illustrates how to format your Python entry for the Challenge, and it should finish running on a sample Challenge training dataset in a minute or two on a modern personal computer. However, it is **not** designed to score well (or, more accurately, designed not to do well), so you should not use it as a baseline for your model's performance.

This code uses four main scripts, as described below, to train and test your model for the 2021 Challenge. 

## How do I run these scripts?

You can run this classifier code by installing the requirements and running

    python train_model.py training_data model
    python test_model.py model test_data test_outputs

where `training_data` is a directory of training data files, `model` is a directory for saving your model, `test_data` is the directory of test data files (you can use the training data locally for debugging and cross-validation), and `test_outputs` is a directory for saving your model's outputs. The [PhysioNet/CinC Challenge 2021 webpage](https://physionetchallenges.org/2021/) provides a training database with data files and a description of the contents and structure of these files.

After training your model and obtaining test outputs using the above two command lines, you can evaluate the scores of your model using the [PhysioNet/CinC Challenge 2021 evaluation code](https://github.com/physionetchallenges/evaluation-2021) by running

    python evaluate_model.py labels outputs scores.csv class_scores.csv

where `labels` is a directory containing files with one or more labels for each ECG recording, such as the training database on the PhysioNet webpage; `outputs` is a directory containing files with outputs produced by your algorithm for those recordings; `scores.csv` (optional) is a collection of scores for your algorithm; and `class_scores.csv` (optional) is a collection of per-class scores for your algorithm.

## Which scripts I can edit?

We will run the `train_model.py` and `test_model.py` scripts to run your training code and testing code, so check these scripts and the functions that they call.
Our example code uses four main scripts to train and test your model for the 2021 Challenge: 

Please edit the following script to add your training and testing code:
* `team_code.py` is a script with functions for training your model and running your trained model.

Please do **not** edit the following scripts. We will use the unedited versions of these scripts.
* `train_model.py` is a script for calling your training code on the training data.
* `test_model.py` is a script for calling your trained model on the test data.
* `helper_code.py` is a script with helper variables and functions that we used for our code. You are welcome to use them in your code.

These four scripts must remain in the root path of your repository, but you can put other scripts and other files in subfolders.

## How do I train, save, load, and run my model?

To train and save your model, please edit the `training_code` function in the `team_code.py` script. Please do not edit the input arguments or output arguments of the `training_code` function.

To load and run your trained model, please edit the `load_twelve_ecg_model`, `load_six_ecg_model`, and `load_two_ecg_model` as well as the `run_twelve_ecg_model`, `run_six_ecg_model`, and `run_two_ecg_model` functions in the `team_code.py` script, which takes an ECG recording as an input and returns the class labels and probabilities for the ECG recording as outputs. Please do not edit the input or output arguments of the functions for loading or running your models.

## What else is in this repository?

This README has instructions for running the example code and writing and testing your own code.

We also included a script, `extract_leads_wfdb.py`, for extracting reduced-lead sets from the training data. You can use this script to produce reduce leads data and use them to test your code. You can run this script with the following commands:

    python extract_leads_wfdb.py -i twelve_lead_directory -l II V5 -o two_lead_directory
    python extract_leads_wfdb.py -i twelve_lead_directory -l I II III aVL aVR aVF -o six_lead_directory 

## How do I run these scripts in Docker?

Using docker allows to containerize and package codes with different dependencies run identically in any environment and operating system.
To install docker, go to [Get Docker](https://docs.docker.com/install/) and install the Docker Community Edition. For troubleshooting, see [Configure and troubleshoot the Docker](https://docs.docker.com/config/daemon/).

After installing Docker, clone your repository, build an image using your code and run it on a single recording.

If you have trouble testing your code, then make sure that you can test the example code, which is known to work. 
You can test the Python example code in Linux and can test the non-Python example code on a Mac or other operating systems in a similar way.

First, create a folder, docker_test, in your home directory. 
Then, put the example code from GitHub in docker_test/python-classifier-2021, some of the training data in docker_test/input_directory and docker_test/input_training_directory,
an empty folder for the output of the training code in docker_test/output_training_directory, and an empty folder for the classifications in docker_test/output_directory.
Finally, build a Docker image and run the example code using the following steps:

    Docker
    user@computer:~/docker_test$ ls
    input_directory  output_directory  python-classifier-2021

    user@computer:~/docker_test$ ls input_directory/
    A0001.hea  A0001.mat  A0002.hea  A0002.mat  A0003.hea ...

    user@computer:~/docker_test$ cd python-classifier-2021/

    user@computer:~/docker_test/python-classifier-2021$ docker build -t image .

    Sending build context to Docker daemon  30.21kB
    [...]
    Successfully tagged image:latest

    user@computer:~/docker_test/python-classifier-2021$ docker run -it -v 
    ~/docker_test/input_training_directory:/physionet/input_training_directory -v 
    ~/docker_test/output_training_directory:/physionet/output_training_directory -v 
    ~/docker_test/input_directory:/physionet/input_directory -v ~/docker_test/output_directory:/physionet/output_directory image bash

    root@[...]:/physionet# ls
    AUTHORS.txt  Dockerfile LICENSE.txt  README.md extract_leads_wfdb.py  helper_code.py  input_directory  output_directory  requirements.txt team_code.py test_model.py    train_model.py

    root@[...]:/physionet# python train_model.py input_training_directory/ output_training_directory/

    root@[...]:/physionet# python test_model.py output_training_directory/ input_directory/ output_directory/

    root@[...]:/physionet# exit
    Exit

    user@computer:~/docker_test$ cd ..

    user@computer:~/docker_test$ ls output_directory/
    A0001.csv  A0002.csv  A0003.csv  A0004.csv  A0005.csv
    

Here are two links with good, data science-centric introductions to Docker: [How Docker Can Help You Become A More Effective Data Scientist](https://towardsdatascience.com/how-docker-can-help-you-become-a-more-effective-data-scientist-7fc048ef91d5), and [Learn Enough Docker to be Useful](https://link.medium.com/G87RxYuQIV).
For more information on using the Docker for the Challenge, please visit the [Frequently Asked Questions (FAQ)](https://physionetchallenges.org/2020/submissions).

## How do I learn more?

Please see the [PhysioNet/CinC Challenge 2021 webpage](https://physionetchallenges.org/2021/) for more details. Please post questions and concerns on the [Challenge discussion forum](https://groups.google.com/forum/#!forum/physionet-challenges).

## Useful links

- [The PhysioNet/CinC Challenge 2021 webpage](https://physionetchallenges.org/2021/)

- [MATLAB example code for the PhysioNet/CinC Challenge 2021](https://github.com/physionetchallenges/matlab-classifier-2021)

- [Evaluation code for the PhysioNet/CinC Challenge 2021](https://github.com/physionetchallenges/evaluation-2021)

- [Frequently Asked Questions (FAQ)](https://physionetchallenges.org/faq/)
