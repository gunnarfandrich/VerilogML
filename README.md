# VerilogML

## VerilogML is an in-progress set of tools created to perform feature extraction and more on RTL files.

### Currently supported languages:

  ```sh
  .v
  .vhd
  ```


<!-- GETTING STARTED -->
## Getting Started

To use this library of tools, most interactions are performed from and through metrics.py. Individual scripts can be called manually, though it is not recommended. See Usage for more information.

### Dependencies

This tool expects users to have access to Synopsis Design Compiler. All other requirements are simple python packages. To install them, run the following code in a terminal.

  ```sh
  pip install pandas numpy
  ```
On the University of Florida ECE server, these packages are already present. Simply source your environment properly to access them:

  ```sh
  source /apps/anaconda/settings
  ```

A reference library is required for the .tcl script to run in Synopsis. This file is zipped and included in the repo. Extract the file before proceeding:

  ```sh
  unzip ref.zip
  ```


<!-- USAGE EXAMPLES -->
## Usage

This tool expects a directory of RTL IP cores and a list of RTL models to run. An example list of RTL models is provided: rtl_models.xlsx
This list was made exclusively for this project, though you can supply your own. This list was made from a generous dump of the [OpenCores library](https://github.com/fabriziotappero/ip-cores)

Once you have ensured rtl_models.xlsx exists in the same directory as the main scripts, use gitScraper.py to download the list of models to analyze:
  ```sh
  python gitScraper.py
  ```

After downloading all your models, perform feature extraction and power analysis:
  ```sh
  python metrics.py -d ip-cores
  ```

Currently, the script returns a pandas DataFrame. The dataframe will be exported as "out.csv" to the working directory upon the script finishing execution.


This DataFrame is intended to be used in the future to estimate power analysis on RTL designs after a machine learning model is created and trained on collected RTL IPs.

## Known Issues and Bugs
* Testbenches return all zero values (to be expected) in the dataframe

<!-- Planned Features -->
## Planned Features
* Use Machine Learning to Estimate Power Consumption of RTL designs, WITHOUT, the need for Synopsis Design Compiler or any other proprietary, expensive, software.
* ~~Export collected dataframe to xlsx, txt file, or similar so the script doesn't need to be ran multiple times for designs with no changes~~ Commit: e6c838a
* C and C++ Support
* Automatically identify and ignore testbench files
* TBD!!!

## License and Use
Feel free to use this library for your own research and work. For pull requests, message me (I do not expect anyone to PR but I've seen crazier things happen).
(Follow GPL 3.0 License terms)

<!-- Authors -->
## Authors
* [Gunnar Fandrich](https://github.com/gunnarfandrich)
* [Cale Woodward](mailto:calewoodward@ufl.edu)
* [Monica Sheethal Gurakala](mailto:m.gurakala@ufl.edu)
* [Venkata Shanmukha Sri Sudha Renduchintala](mailto:renduchintalav@ufl.edu)




<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
Thank you to the following people for their guidance and mentoring throughout this project!
* [Dr. Swarup Bhunia](https://www.ece.ufl.edu/people/faculty/swarup-bhunia/)
* [Aritra Bhattacharyay](https://scholar.google.com/citations?user=T6ofeOEAAAAJ&hl=en)
