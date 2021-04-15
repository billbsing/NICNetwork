import matplotlib.pyplot as plot
import pygal
import networkx

class SectorCharts:

    def __init__(self, data_source):
        self._data_source = data_source

    @staticmethod
    def draw_label_size(percent):
        #absolute = int(round(percentt/100.*np.sum(all_values)))
        if percent < 2:
            return ''
        return f'{percent:.1f}%'

    def draw_pie_chart(self):

        sector_size = self._data_source.sector_size
        sector_size = dict(sorted(sector_size.items(), key=lambda x: x[1], reverse=True))

        labels = []
        sizes = sector_size.values()

        for label, size in sector_size.items():
            percent =  (size / sum(sizes)) * 100
            labels.append(f'{label} ({size}) {percent:.1f}%')

        explode = []
        last_explode = 0.1
        for value in sizes:
            explode_value = 0
            if value < 5:
                explode_value = last_explode
                last_explode += 0.02
            explode.append(explode_value)


        fig1, ax1 = plot.subplots()
        wedges, texts, autotexts = ax1.pie(sizes,
            #explode=explode,
            labels=sector_size.keys(),
            autopct=SectorCharts.draw_label_size,
            shadow=True,
            startangle=90,
            rotatelabels=True,
            labeldistance=None,
            textprops={'fontsize': 12}
        )
        ax1.legend(wedges,
            labels,
            title='Sectors',
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


    def draw_bar_chart(self):

        sector_size = dict(sorted(self._data_source.sector_size.items(), reverse=True))
        labels = sector_size.keys()
        sizes = sector_size.values()
        label_index = []
        for label in labels:
            label_index.append(len(label_index) + 1)


        fix, ax = plot.subplots(figsize=(12, 8))

        barh = ax.barh(label_index, sizes)
        plot.subplots_adjust(left=0.40)
        ax.set_yticks(label_index)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Number of people')
        ax.set_ylabel('Sector')
        ax.set_title('Number of people grouped by sector')
        ax.bar_label(barh)



    def draw_network_chart(self, sector_name=None):
        node_color = []
        node_size = []
        node_names = []
        graph = networkx.Graph()
        for sector in self._data_source.sectors:
            if sector_name is None or sector_name == sector:
                node_size = 300
                if sector_name:
                    node_size = 1000
                node_names.append(sector)
                graph.add_node(sector, color='red', size=node_size)

        #for name, sectors in self._data_source.name_sector.items():
            #graph.add_node(name,  color='green', size=20)
            #node_color.append('green')
            #node_size.append(200)

        for name, sectors in self._data_source.name_sector.items():
            is_found = False
            for sector in sectors:
                if sector_name is None or sector_name == sector:
                    is_found = True
            if is_found:
                for sector in sectors:
                    edge_color = 'grey'
                    if sector_name is None or sector_name == sector:
                        edge_color = 'red'
                        if name not in node_names:
                            graph.add_node(name, color='green', size=100)
                            node_names.append(name)
                    if sector not in node_names:
                        graph.add_node(sector, color='grey', size=100)
                        node_names.append(sector)
                    graph.add_edge(name, sector, color=edge_color)

        pos = networkx.spring_layout(graph, k=0.1 * len(graph.nodes()), iterations=20)
        node_color = networkx.get_node_attributes(graph, 'color')
        node_size = networkx.get_node_attributes(graph, 'size')
        edge_color = networkx.get_edge_attributes(graph, 'color')

        if len(graph.nodes()) > 100:
            figure = plot.figure(figsize=(46, 33))           # A0
        elif len(graph.nodes()) > 10:
            figure = plot.figure(figsize=(16, 11))           # A3
        else:
            figure = plot.figure(figsize=(11, 8))           # A4

        if sector_name:
            plot.title(f'Sector: {sector_name}')
        else:
            plot.title(f'All Sectors')

        networkx.draw_kamada_kawai(graph,
        #networkx.draw_networkx(graph,
            #pos=pos,
            with_labels=True,
            node_size=list(node_size.values()),
            node_color=node_color.values(),
            width=1,
            style='dotted',
            edge_color=edge_color.values(),
            font_size=12,
            font_family='Arial',
        )
        return figure
