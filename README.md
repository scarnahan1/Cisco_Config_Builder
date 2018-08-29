# Cisco_Config_Builder
There are two modules that can be run.

## CiscoBuild.py 

Will take two files for input and create an output file or files based upon the number of lines in 
the CSV input file.

It was crated to create cisco configuration files from a template and then use CSV input to modify specific values
to a specific device.

The output files are saved to the Output folder location where the program is located. 

One input file is a template file. This file will contain variable names in key sections. These variables must match
Column names in a CSV file.
The CSV file must contain column headers with names that match the variables in the template file.
The program will create a new .txt file for each '$hostname' in the csv file. The .txt file will contain the contents
of the template file with all the variables replaced with the values specified in the csv file.

New Values can be added to the template and input file as needed. The requirements are:
    The new values must start with a $ 


```
Example:
$newvalue
    The names must be unique
    Value names must match exactly from the template file to the header row in the CSV.
```
## FileCompare.py
 
Was created to compare the pre and post output of log files from Cisco devices. It simply takes 
the two files and compares them and logs the differences to a log file for review. It has a very simple GUI front end
built with TKinter. I'm not a GUI design guy so it's just barely functional.
It Should be self explanatory what to do when you run the program. 
    
 ### Installing
 Python 3.6.6
 
 The MyLogger module is the only custom module required to run and is incluced in the repository. All other modules 
 are part of the standard python 3.6.6 build.
 
### Running
Run from command line or batch file.

```
Example for CiscoBuild.py:

python3 CiscoBuild.py -input_file 3650_input.csv -device_template ./input_Templates/3650-config-template

```
 ## Authors

* **Shane Carnahan** - *Initial work* - [Shane Carnahan](https://github.com/scarnahan1)

See also the list of [contributors](https://github.com/scarnahan1/Cisco_Config_Builder/contributors) who participated in this project.
