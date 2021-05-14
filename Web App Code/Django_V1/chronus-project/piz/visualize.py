from piz import db_operation_ORM
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from piz import PTBXL_preprocess


def load_data(path):
    # print(self.path)
    preprocesser = PTBXL_preprocess.PTBXL_preprocess(path)
    if path.endswith(".json"):
        data = preprocesser.json_convertor()
        # print('hello')
    # elif self.path.name.endswith(".csv"):
    #     data = self.csv_convertor()
    # else:
    #     data = self.dat_convertor(self.path)
    #print("load data successful!")
    # self.plot_graph(data.T[0])
    return data.T


def get_pie_chart_by_access_code(request):
    context = {}
    if request.method == "POST":
        context['access_code'] = request.POST['access_code']
        try:
            context['result'] = db_operation_ORM.get_result_with_code(context['access_code'])
            print(context['result'])
            data = context['result'].prob
            flat_list = data.split(',')
            print(flat_list)
            context['result_prob'] = flat_list
            context['labels'] = ['Myocarditi', 'Healthy control', 'Dysrhythmia', 'Myocardial infarction', 'Valvular heart disease', 'Hypertrophy',
                                 'Bundle branch block', 'Cardiomyopathy', 'n/a', 'Stable angina', 'Palpitation', 'Heart failure (NYHA)', 'Unstable angina']
            context['signal_graph'] = get_signal_graph1
            print(type(context['signal_graph']))
        except:
            context['error_info'] = 'This access code does not exist!'
            return context
    return context


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_signal_graph1(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
    plt.switch_backend("AGG")
    a = symbol_names[0]

    fig_data = x[0]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:5000], color="red")
    graph = get_graph()
    return graph


def get_signal_graph2(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[1]
    fig_data = x[1]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph3(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[2]
    fig_data = x[2]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph4(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[3]
    fig_data = x[3]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph5(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[4]
    fig_data = x[4]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph6(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[5]
    fig_data = x[5]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph7(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[6]
    fig_data = x[6]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph8(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[7]
    fig_data = x[7]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph9(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[8]
    fig_data = x[8]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph10(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[9]
    fig_data = x[9]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph11(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[10]
    fig_data = x[10]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph


def get_signal_graph12(x):
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    plt.switch_backend("AGG")
    a = symbol_names[11]
    fig_data = x[11]
    plt.figure(figsize=(30, 4))
    plt.title(a)
    plt.plot(fig_data[100:16100], color="red")
    graph = get_graph()
    return graph
#
#
# def get_signal_graph13(x):
#     symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
#                     'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
#     plt.switch_backend("AGG")
#     a = symbol_names[12]
#     fig_data = x[a][0]
#     plt.figure(figsize=(30, 4))
#     plt.title(a)
#     plt.plot(fig_data[100:16100], color="red")
#     graph = get_graph()
#     return graph
#
#
# def get_signal_graph14(x):
#     symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
#                     'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
#     plt.switch_backend("AGG")
#     a = symbol_names[13]
#     fig_data = x[a][0]
#     plt.figure(figsize=(30, 4))
#     plt.title(a)
#     plt.plot(fig_data[100:16100], color="red")
#     graph = get_graph()
#     return graph
#
#
# def get_signal_graph15(x):
#     symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
#                     'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
#     plt.switch_backend("AGG")
#     a = symbol_names[14]
#     fig_data = x[a][0]
#     plt.figure(figsize=(30, 4))
#     plt.title(a)
#     plt.plot(fig_data[100:16100], color="red")
#     graph = get_graph()
#     return graph
