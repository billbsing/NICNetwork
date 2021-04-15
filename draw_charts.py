#!/usr/bin/env python3

import argparse
import cairosvg
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
DEFAULT_OUTPUT_PATH = 'charts'
DEFAULT_OUTPUT_FILENAME = 'nic_charts.pdf'

def main():


    parser = argparse.ArgumentParser(description='NIC Charting.')

    parser.add_argument('-f', '--filename',
        default=DEFAULT_FILENAME,
        help=f'Data csv filename. Default: {DEFAULT_FILENAME}'
    )

    parser.add_argument('-p', '--path',
        default=DEFAULT_OUTPUT_PATH,
        help=f'Path to build the charts in. Default: {DEFAULT_OUTPUT_PATH}'
    )

    parser.add_argument('-o', '--output',
        default=DEFAULT_OUTPUT_FILENAME,
        help=f'Output chart name. Default: {DEFAULT_OUTPUT_FILENAME}'
    )
    parser.add_argument('chart_names',
        metavar='chart names',
        nargs='+',
        help='list of chart names can be one of the following: [all, country, sector].'
    )

    args = parser.parse_args()
    data_source = DataSource(args.filename)

    output_path = args.path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    export_list = []
    for chart_name in args.chart_names:
        if chart_name == 'country' or chart_name == 'all':

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
        with open(args.output, 'wb') as fp:
            merger.write(fp)

        for fp in file_handles:
            fp.close()
        # os.system(f'pdftk {" ".join(pdf_inputs)} cat output {args.output}')



if __name__ == '__main__':
    main()
