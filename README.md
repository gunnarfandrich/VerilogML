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

Currently, the script returns a pandas DataFrame. This DataFrame is intended to be used in the future to estimate power analysis on RTL designs after a machine learning model is created and trained on collected RTL IPs.

<!-- Authors -->
## Authors
* [Gunnar Fandrich](gunnarfandrich@ufl.edu)
* [Cale Woodward]()
* Monica Sheethal Gurakala
* Venkata Shanmukha Sri Sudha Renduchintala




<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
Thank you to the following people for their guidance and mentoring throughout this project!
* [Dr. Swarup Bhunia](https://www.ece.ufl.edu/people/faculty/swarup-bhunia/)
* [Aritra Bhattacharyay](https://scholar.google.com/citations?user=T6ofeOEAAAAJ&hl=en)
