import collections
import matplotlib.pyplot as plot
import pygal


class CountryCharts:

    def __init__(self, data_source):
        self._data_source = data_source


    @staticmethod
    def draw_label_size(percent):
        #absolute = int(round(percentt/100.*np.sum(all_values)))
        if percent < 2:
            return ''
        return f'{percent:.1f}%'

    def draw_pie_chart(self):

        country_size = self._data_source.countries
        country_size = dict(sorted(country_size.items(), key=lambda x: x[1], reverse=True))

        labels = []
        sizes = country_size.values()
        for label, size in country_size.items():
            percent =  (size / sum(sizes)) * 100
            labels.append(f'{label} ({size}) {percent:.1f}%')

        explode = []
        last_explode = 0.1
        for value in sizes:
            explode_value = 0
            if value < 2:
                explode_value = last_explode
                last_explode += 0.02
            explode.append(explode_value)


        fig1, ax1 = plot.subplots()
        wedges, texts, autotexts = ax1.pie(sizes,
            #explode=explode,
            labels=country_size.keys(),
            autopct=CountryCharts.draw_label_size,
            shadow=True,
            startangle=90,
            rotatelabels=True,
            labeldistance=None,
            textprops={'fontsize': 14}
        )

        ax1.legend(wedges,
            labels,
            title='Countries',
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    def draw_bar_chart(self):
        country_size = dict(sorted(self._data_source.countries.items(),  reverse=True))
        labels = country_size.keys()
        sizes = country_size.values()
        label_index = []
        for label in labels:
            label_index.append(len(label_index) + 1)

        fix, ax = plot.subplots(figsize=(12, 8))
        """
        ax.set_ylabel('Number of people')
        ax.set_title('Number of people grouped by country')
        ax.set_xticklabels(labels, rotation=45)
        plot.subplots_adjust(bottom=0.40)
        # plot.margins(0.4)
        points = ax.bar(labels, sizes,  1, label='Country')
        ax.bar_label(points)
        """
        barh = ax.barh(label_index, sizes)
        plot.subplots_adjust(left=0.40)
        ax.set_yticks(label_index)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Number of NIC members')
        ax.set_ylabel('Country')
        ax.set_title('Number of NIC members per country')
        ax.bar_label(barh)


    def draw_world_map(self, filename):
        country_size = dict(sorted(self._data_source.country_size.items()))

        style = pygal.style.Style(
            background='white',
            plot_background='white',
            foreground_subtle='black'
        )
        worldmap = pygal.maps.world.World(style=style)
        worldmap.title = 'NIC Members by country'

        for country_code_2, value in country_size.items():
            country_code = self._data_source.country_codes[country_code_2]
            country_name = country_code.name
            #if len(country_name) > 10:
                #country_name = f'{country_name[:10]}..'
            worldmap.add(f'{value}: {country_name}', [(country_code_2, value)])

        # worldmap.add('Visitors', country_size)
        worldmap.render_to_file(filename)
        # worldmap.render()
