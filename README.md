
This NHL analytics and fantasy hockey tool. Use it to:
- calculate player fantasy stats in a single season
- deep dive into single season performance
- visualize player stats across their career to identify trends

To use this tool do the following:
1. clone this repo
2. in a terminal window use the environment.yml file to set up the conda environment

  `conda env create -f environment.yml`

3. run main.ipynb in a jupyter notebook. To run this do the following:

  a) type `jupyter notebook` in a terminal window (same directory where main.ipynb is). This will open a jupyter notebook session in a web browser
  b) in the web browser jupyter notebook session click on main.ipynb
  c) in cell 3) change the default fantasy scoring system to your league system
  d) in cell 4) change the default skater and regular season to what you want to analyze
  e) click "kernel" then "restart and run all" to run the kernel.


Note: do not change the folder structure and what files are stored where. This is needed to accurately grab pngs of NHL logos to plot.

Note: this tool is not complete. The following work in is progress:
  1. I'm adding new capabilities for more in-depth player analysis.
  2. Moving this tool to a GUI window environment in progress. gui_driver.py does not have all of the functionality of the jupyter notebook (yet).

Also, ignore the sandbox. It is where I test new ideas for the project. Or don't ignore it and look at messy code.
