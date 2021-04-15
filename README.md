
NICNetwork is a python application, that generates reports/charts for NIC


### Install

First open a terminal and download this repository

```bash

$ git clone https://github.com/billbsing/NICNetwork.git
$ cd NICNetwork

```


You now need to setup the local virtual environment.

```bash

$ virtualenv venv
$ source venv/bin/activate

```

Now you need to instal the supported python libraries.

```bash

$ make install

```

### Generating Reports

You need to copy the spreadsheet to the `NICNetwork` folder and convert it to a CSV file.

The default filename for the input data is `nic_data.csv`.

Once the csv data is available you can run the chart generator.

```bash

$ ./draw_charts.py all


```

This will produce an output pdf file `nic_charts.pdf`.

### Command line options

Use the `--help` option

```bash

$ ./draw_charts.py -h

    usage: draw_charts.py [-h] [-f FILENAME] [-p PATH] [-o OUTPUT] chart names [chart names ...]

    NIC Network

    positional arguments:
    chart names           list of chart names can be one of the following: [all, country, sector].

    optional arguments:
    -h, --help            show this help message and exit
    -f FILENAME, --filename FILENAME
                            Data csv filename. Default: nic_data.csv
    -p PATH, --path PATH  Path to build the charts in. Default: charts
    -o OUTPUT, --output OUTPUT
                            Output chart name. Default: nic_charts.pdf
```

