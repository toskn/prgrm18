import gensim
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import style
from networkx.algorithms import community
import pandas as pd
import numpy as np
import sys
import math

m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
if m.endswith('.vec.gz'):
    model = \
        gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = \
        gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)


# в этом модуле предобученная модель выявляет слова,
# по которым будут в дальнейшем строиться графы
def model_start():
    # задаются переменные
    #       класс межличностных отношений с положительной оценкой
    input_words = ['любить_V', 'уважать_V', 'ценить_V']
    # проверка на отсутствие обособленных вершин в будущем графе
    for element in input_words:
        for item in input_words:
            if element == item:
                continue
            else:
                sim = model.similarity(element, item)
                if sim < 0.5:
                    sys.exit('У введенных вами'
                             ' слов слишком маленькая косинусная близость')
    words_to_append_first_wave = []
    words_to_append_second_wave = []
    final_words = []
    # ищем нужные слова по модели
    # TODO можно переписать (эту + следующую) части под отдельный модуль.
    for word in input_words:
        if word in model:
            # проверяем 10 ближайших соседей слова:
            for i in model.most_similar(positive=[word], topn=10):
                if i[1] >= 0.5:
                    words_to_append_first_wave.append(i[0])
        else:
            print('Увы, слова "%s" нет в модели!' % input_words)
    # создается список состоящий из введенных пользователем слов и первой волны
    # слов из модели:
    words_to_append_first_wave = list(set(words_to_append_first_wave))
    for element in words_to_append_first_wave:
        if not element.endswith('_V'):
            words_to_append_first_wave.remove(element)
            final_words = list(set(input_words + words_to_append_first_wave))

    # еще раз ищем нужные слова по модели, но уже по словам первой волны
    for word in set(words_to_append_first_wave):
        # есть ли слово в модели?
        if word in model:
            # проверяем 10 ближайших соседей слова:
            for i in model.most_similar(positive=[word], topn=10):
                if i[1] >= 0.5:
                    words_to_append_second_wave.append(i[0])
    # создается список состоящий из введенных пользователем слов, первой волны
    # слов из модели и второй волны:
    words_to_append_second_wave = list(set(words_to_append_second_wave))
    for item in words_to_append_second_wave:
        if not item.endswith('_V'):
            words_to_append_second_wave.remove(item)
    final_words = list(set(final_words + words_to_append_second_wave))
    return final_words


def preparing_graph(final_words):
    # задание переменных
    g = nx.Graph()  # пустой граф
    graph_edges = []
    g.add_nodes_from(final_words)
    # выделяем какие вершины графа нужно связать ребром
    for element in final_words:
        i = 0
        while i < len(final_words):
            # форматирую флоат нампая в флоат питона на всякий случай
            weight = model.similarity(element, final_words[i])
            val = weight
            weight = val.item()
            if 0.5 <= weight < 0.98:
                # здесь создан кортеж из вершин и веса для каждой связи
                graph_edges.append((element, final_words[i], weight))
            i += 1
        graph_edges = list(set(graph_edges))
    # импортирую полученный список в граф = создаю ребра
    g.add_weighted_edges_from(set(graph_edges))
    return g


def preparing_graph_for_show(final_words):
    # задание переменных
    g = nx.Graph()  # пустой граф
    graph_edges = []
    g.add_nodes_from(final_words)
    # выделяем какие вершины графа нужно связать ребром
    for element in final_words:
        i = 0
        while i < len(final_words):
            # форматирую флоат нампая в флоат питона на всякий случай
            weight = model.similarity(element, final_words[i])
            val = weight
            weight = val.item()
            if 0.5 <= weight < 0.98:
                # здесь создан кортеж из вершин и веса для каждой связи
                graph_edges.append((element, final_words[i], weight))
            i += 1
        graph_edges = list(set(graph_edges))
    # импортирую полученный список в граф = создаю ребра
    g.add_weighted_edges_from(set(graph_edges))
    return graph_edges


def showing_graph(graph_edges, final_words, communities1, degree_counter1):
    style.use('ggplot')
    first_node = []
    second_node = []
    for element in graph_edges:
        first_node.append(element[0])
        second_node.append(element[1])
    # созадем датафрейм с нашими данными
    df = pd.DataFrame({'from': first_node, 'to': second_node})

    # создаем датафрейм с характеристиками наших вершин
    # цвет
    groups_graph = []
    for element in final_words:
        for i, item in enumerate(communities1):
            item = list(item)
            for x in item:
                if element == x:
                    groups_graph.append(i)

    # размер
    sizes_graph = []
    for element in final_words:
        for i, item in enumerate(degree_counter1):
            if element == item:
                sizes_graph.append(10*int(
                    math.fabs(i - len(degree_counter1)+2)))

    carac = pd.DataFrame({'ID': final_words, 'color': groups_graph,
                          'size': sizes_graph})

    # строим граф
    g = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to',
                                               create_using=nx.Graph())
    g.nodes()
    # меняем порядок в караке, чтобы вершинам соответствовали нужные
    # цвета и размеры
    carac = carac.set_index('ID')
    carac = carac.reindex(g.nodes())

    # раскрашиваем вершины:
    nx.draw(g, with_labels=True, node_color=carac['color'],
            cmap=plt.cm.Set1, node_size=carac['size'])
    plt.axis('off')
    plt.show()


def centrality_and_params_graph(g):
    degree_counter = []
    betweenness_counter = []
    closeness_counter = []
    eigen_counter = []

    deg = nx.degree_centrality(g)
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        degree_counter.append(nodeid)
    biggest_deg = {key: value for key, value in deg.items() if value in
                   sorted(set(deg.values()), reverse=True)[:2]}
    bet = nx.betweenness_centrality(g)
    for nodeid in sorted(bet, key=bet.get, reverse=True):
        betweenness_counter.append(nodeid)
    biggest_bet = {key: value for key, value in bet.items() if value in
                   sorted(set(bet.values()), reverse=True)[:2]}
    cls = nx.closeness_centrality(g)
    for nodeid in sorted(cls, key=cls.get, reverse=True):
        closeness_counter.append(nodeid)
    biggest_cls = {key: value for key, value in cls.items() if value in
                   sorted(set(cls.values()), reverse=True)[:2]}
    eig = nx.eigenvector_centrality(g)
    for nodeid in sorted(eig, key=eig.get, reverse=True):
        eigen_counter.append(nodeid)
    biggest_eig = {key: value for key, value in eig.items() if value in
                   sorted(set(eig.values()), reverse=True)[:2]}

    radius = nx.radius(g)

    diameter = nx.diameter(g)

    assort_coef = nx.degree_pearson_correlation_coefficient(g)

    clustering = nx.average_clustering(g)

    node_number = g.number_of_nodes()

    edge_number = g.number_of_edges()

    communities = community.greedy_modularity_communities(g)

    dict_return = {'biggest_deg': biggest_deg, 'biggest_bet': biggest_bet,
                   'biggest_cls': biggest_cls, 'biggest_eig': biggest_eig,
                   'radius': radius, 'diameter': diameter,
                   'assort_coef': assort_coef,
                   'clustering': clustering, 'node_number': node_number,
                   'edge_number': edge_number,
                   'communities': communities}
    print(dict_return)
    return 0


def communities1(g):
    communities1 = community.greedy_modularity_communities(g)
    return communities1


def degree_counter1(g):
    degree_counter1 = []
    deg = nx.degree_centrality(g)
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        degree_counter1.append(nodeid)
    return degree_counter1


def pic_graph(g):
    style.use('ggplot')
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='red', node_size=10)
    nx.draw_networkx_edges(g, pos, edge_color='yellow')
    nx.draw_networkx_labels(g, pos, font_size=20, font_family='Arial')
    plt.axis('off')
    plt.show()


centrality_and_params_graph(preparing_graph(model_start()))

showing_graph(preparing_graph_for_show(model_start()), model_start(),
              communities1(preparing_graph(model_start())),
              degree_counter1(preparing_graph(model_start())))
