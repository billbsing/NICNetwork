
NICNetwork is a python application, that generates reports/charts for NIC


### Install

You need to do the following:

First open a terminal session on your computer.

Then download this repository.


```bash
git clone https://github.com/billbsing/NICNetwork.git
```

move into the new downloaded folder:

```bash
cd NICNetwork
```

### Generate the report using Docker ( simplest/easiest)

1. First you need to install and have Docker running on your computer.

2. Then open up a terminal/command line.

3. Create a folder, 'cd' to the folder and copy your data file called 'nic_data.csv' to this folder.

4. Run the docker command:

    docker run -v $PWD:/work billbsing/nic_network

5. The created chart will be called 'nic_charts.pdf'


## or

### Seting up to generate the report using python and the development files

You now need to setup the local virtual environment. You will only need to do this part once.

```bash
virtualenv venv
```

You need to do this before each time you come back to the folder to run the charting command.
Now make sure any new library and builds are used in the `venv` folder.

```bash
source venv/bin/activate
```

Now you need to instal/update the supported python libraries.

```bash
make install
```

### Generating the report

You need to copy the spreadsheet to the `NICNetwork` folder and convert it to a CSV file.

The default filename for the input spreadsheet CSV file is `nic_data.csv`.

Once the csv file is available you can now run the chart generator.

```bash
./draw_charts.py

```

This will produce an output pdf file called `nic_charts.pdf`.

All of the source charts generated can be found in the `NICNetwork/charts` folder.

### Command line options

Use the `--help` option

```bash
./draw_charts.py --help

usage: draw_charts.py [-h] [-f FILENAME] [-p PATH] [-o OUTPUT] [name]

NIC Network

positional arguments:
  name                  list of chart names can be one of the following: [all, country, sector]. Default all

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Data csv filename. Default: nic_data.csv
  -p PATH, --path PATH  Path to build the charts in. Default: charts
  -o OUTPUT, --output OUTPUT
                        Output chart name. Default: nic_charts.pdf

```

