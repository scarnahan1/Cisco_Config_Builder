#!/usr/bin/env python3

# Author - Shane Carnahan
# Email - Shane.Carnahan1@gmail.com
# Date - 8/27/2018
# Project - Cisco_Config_Builder
# Version - 1.0

'''
This program will take two files for input and create an output file or files based upon the number of lines in
the CSV input file.

It was crated to create cisco configuration files from a template and then use CSV input to modify specific values
to a specific device.

One input file is a template file. This file will contain variable names in key sections. These variables must match
Column names in a CSV file.
The CSV file must contain column headers with names that match the variables in the template file.
The program will create a new .txt file for each '$hostname' in the csv file. The .txt file will contain the contents
of the template file with all the variables replaced with the values specified in the csv file.

New Values can be added to the template and input file as needed. The requirements are:
    The new values must start with a $ Example:
        $newvalue
    The names must be unique
    Value names must match exactly from the template file to the header row in the CSV.
'''


import sys, os, argparse, csv, re, time
from MyLogger import my_logger


def folder_check(log_location):
    main_logging_folder = log_location + "/"
    Output = './Output'

    if not os.path.exists(main_logging_folder):
        os.makedirs(main_logging_folder)

    # check for the Output folder
    if not os.path.exists(Output):
        os.makedirs(Output)

def regex_create(dict, logger3):
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    logger3.debug(regex)
    return regex

def multiple_replace(dict, text, regex, logger4):
    # if key is in line check to see if the value is blank is so line with a !
    if re.search(regex, text) is not None:
        # Get the value for the key found in the match
        m = re.search(regex, text)
        match = m.string[m.start():m.end()]
        logger4.debug(match)
        # match = m.groupdict()
        if match in list(dict.keys()):
            var_match = dict[match]
            logger4.debug(var_match)
            if var_match == '':
                logger4.debug('The {} value was empty so returned ! to the file...'.format(match))
                text = '!\n'
                return text
            else:
                logger4.debug(regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text))
                return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)
    else:
        return text

def build_config(device_template, devices_dict, logger2, logger3, logger4):
    logger2.debug('Made it to build_config function...')
    output_file_base = './Output/'
    for item in range(0, len(devices_dict)):
        device_dict = dict(devices_dict[item])
        host = str(device_dict['$hostname'])

        # Create and Open the output file
        output_file_name = output_file_base + host + '.txt'
        output_file = open(output_file_name, 'w+')
        logger2.info('Created {}...'.format(output_file))

        # Create a regular expression from the dictionary keys
        regex = regex_create(device_dict, logger3)

        # Process for matching a line at a time...
        with open(device_template, 'r') as text:
            for line in text:
                new_text = multiple_replace(device_dict, line, regex, logger4)
                output_file.write(new_text)


def main(log_location, start_time):
    # Set up our logging here
    log_file_name = log_location + "CiscoBuild.log"
    # Set loggers for specific areas of the module
    logger1 = my_logger('CiscoBuild.main', log_file_name)
    logger2 = my_logger('CiscoBuild.build_config', log_file_name)
    logger3 = my_logger('CiscoBuild.regex_create', log_file_name)
    logger4 = my_logger('CiscoBuild.multiple_replace', log_file_name)

    # Production stuff
    input_file = arguments.input_file
    device_template = arguments.device_template

    # testing stuff
    # input_file = '3650_input.csv'
    # device_template = './input_Templates/3650-config-template.txt'

    # Check to see if input files exist
    try:
        open(input_file)
        logger1.debug('input_file was found... {}'.format(input_file))
    except Exception as err:
        logger1.info('Check the input file and path. It does not appear to exist... {}'.format(input_file))
        logger1.exception(err)
        sys.exit(1)

    try:
        open(device_template)
        logger1.debug('device template was found... {}'.format(device_template))
    except Exception as err:
        logger1.info('Check the device template file and path. It does not appear to exist... {}'.format(device_template))
        logger1.exception(err)
        sys.exit(1)

    # Read in inpput data file
    with open(input_file, encoding='utf-8-sig') as csv_inputf:
        # build a dict for current device
        reader = csv.reader(csv_inputf, skipinitialspace=True)
        header = next(reader)
        device_dict = [dict(zip(header, map(str, row))) for row in reader]
        logger1.debug(device_dict)
        build_config(device_template, device_dict, logger2, logger3, logger4)
    logger1.info('--- {} seconds ---'.format(time.time() - start_time))
    sys.exit(0)


# Standard call to the main() function.
if __name__ == '__main__':
    # Start the timer
    start_time = time.time()
    # Check for missing folders before starting up fully
    log_location = './LOGS/'
    folder_check(log_location)
    parser = argparse.ArgumentParser(description="Ciaco Config Builder", epilog='Usage: python CiscoBuild.py -input_file "input_file" -device_template "device_template"')
    parser.add_argument('-input_file', help='CSV file with inputs for switch build')
    parser.add_argument('-device_template', help='Template name for the device type being built')

    arguments = parser.parse_args()

    main(log_location, start_time)
