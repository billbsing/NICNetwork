#!/usr/bin/env python3

import argparse
import cairosvg
import logging
import os
import re

import matplotlib.pyplot as plot
from NICNetwork.DataSource import DataSource
from NICNetwork.CountryCharts import CountryCharts
from NICNetwork.SectorCharts import SectorCharts
from PyPDF2 import PdfFileMerger

charts = {
    'country': 'CountryCharts',
    'sector': 'SectorCharts',
}


DEFAULT_FILENAME = 'nic_data.csv'
DEFAULT_PATH = ''
DEFAULT_CHART_FOLDER = 'charts'
DEFAULT_OUTPUT_FILENAME = 'nic_charts.pdf'
DEFAULT_CHART_NAME = 'all'


logger = logging.getLogger(__name__)

def main():


    parser = argparse.ArgumentParser(description='NIC Network')

    parser.add_argument('-f', '--filename',
        default=DEFAULT_FILENAME,
        help=f'Data csv filename. Default: {DEFAULT_FILENAME}'
    )

    parser.add_argument('-p', '--path',
        default=DEFAULT_PATH,
        help=f'Path to input data, build charts and output chart. Default: {DEFAULT_PATH}'
    )

    parser.add_argument('-c', '--charts',
        default=DEFAULT_CHART_FOLDER,
        help=f'Path to build the charts in. Default: {DEFAULT_CHART_FOLDER}'
    )

    parser.add_argument('-o', '--output',
        default=DEFAULT_OUTPUT_FILENAME,
        help=f'Output chart name. Default: {DEFAULT_OUTPUT_FILENAME}'
    )
    parser.add_argument('chart_name',
        metavar='name',
        nargs='?',
        default=DEFAULT_CHART_NAME,
        help=f'list of chart names can be one of the following: [all, country, sector]. Default {DEFAULT_CHART_NAME}'
    )

    args = parser.parse_args()

    output_path = os.path.join(args.path, args.charts)
    if output_path and not os.path.exists(output_path):
        os.mkdir(output_path)

    data_filename = os.path.join(args.path, args.filename)
    logger.info(f'reading input file {data_filename}')
    data_source = DataSource(data_filename)

    output_filename = os.path.join(args.path, args.output)

    export_list = []
    chart_name =args.chart_name.lower()
    if chart_name == 'country' or chart_name == 'all':
        print('drawing country charts')
        country_charts = CountryCharts(data_source)
        country_charts.draw_pie_chart()
        plot.savefig(f'{output_path}/country_chart_pie.svg', bbox_inches='tight')
        export_list.append('country_chart_pie')
        plot.close()

        country_charts.draw_bar_chart()
        plot.savefig(f'{output_path}/country_chart_bar.svg', bbox_inches='tight')
        export_list.append('country_chart_bar')
        plot.close()

        country_charts.draw_world_map(f'{output_path}/country_chart_map.svg')
        export_list.append('country_chart_map')
        plot.close()

    if chart_name == 'sector' or chart_name == 'all':
        print('drawring sector charts')
        sector_charts = SectorCharts(data_source)
        sector_charts.draw_pie_chart()
        plot.savefig(f'{output_path}/sector_chart_pie.svg', bbox_inches='tight')
        export_list.append('sector_chart_pie')
        plot.close()

        sector_charts.draw_bar_chart()
        plot.savefig(f'{output_path}/sector_chart_bar.svg', bbox_inches='tight')
        export_list.append('sector_chart_bar')
        plot.close()

        for sector in data_source.sectors:
            figure = sector_charts.draw_network_chart(sector)
            sector_name = re.sub('[^a-zA-Z0-9]+', '_', sector)
            network_name = f'sector_chart_network_{sector_name}'.lower()
            figure.savefig(f'{output_path}/{network_name}.svg',
                orientation='landscape',
                bbox_inches='tight',
                pad_inches=0.1
            )
            export_list.append(network_name)
            plot.close()

        figure = sector_charts.draw_network_chart()
        network_name = 'sector_chart_network'
        figure.savefig(f'{output_path}/{network_name}.svg',
            orientation='landscape',
            bbox_inches='tight',
            pad_inches=0.1
        )
        export_list.append(network_name)
        plot.close()

    if export_list:
        pdf_inputs = []
        merger = PdfFileMerger()
        for item in export_list:
            cairosvg.svg2pdf(url=f'{output_path}/{item}.svg', write_to=f'{output_path}/{item}.pdf')
            #os.system(f'cairosvg -o {output_path}/{item}.pdf {output_path}/{item}.svg')
            pdf_input = f'{output_path}/{item}.pdf'
            pdf_inputs.append(pdf_input)

        file_handles = []
        for pdf_input in pdf_inputs:
            fp = open(pdf_input, 'rb')
            file_handles.append(fp)
            merger.append(fp)


        logger.info(f'writing output to {output_filename}')
        with open(output_filename, 'wb') as fp:
            print(f'output chart to {output_filename}')
            merger.write(fp)

        for fp in file_handles:
            fp.close()
        # os.system(f'pdftk {" ".join(pdf_inputs)} cat output {args.output}')



if __name__ == '__main__':
    main()
