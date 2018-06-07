# coding:utf8

# 这里可以找到各种图例 https://plot.ly/python/

import plotly.offline as py
py.init_notebook_mode()  # Otherwise, the figure will not be depicted.
import plotly.graph_objs as go

py.iplot(go.Data([go.Scatter(x=X, y=Y,)]))  # 直接在interactive地在jupyter里显示

py.plot(fig, filename='the_graph.html')  # 或者直接保存成文件
# 之后可以用加载html的方式显示出来
with open(html_path) as f:
    display(HTML(f.read()))


# convert matplot to plotly
# https://plot.ly/matplotlib/modifying-a-matplotlib-figure/
# https://plot.ly/matplotlib/
#
# plot...
py.iplot_mpl(plt.gcf())






# plot stacked
traces = []
cum = None
for sr in info_data['position']:
    data = info_data['position'][sr]
    if cum is None:
        cum = np.zeros(data.shape)
    text = data.apply(str)
    cum += data.values
    traces.append(go.Scatter(x=info_data['position'].index, y=cum.copy(),
                             text=text, hoverinfo='x+text',  name=sr, fill='tonexty'))
fig = go.Figure(data=traces)
fig.layout.title = 'Position change'
fig.layout.yaxis.title = 'Position'
py.iplot(fig)




# share x and multiple subplots
from plotly import tools
traces = []
for sr in info_data['earned_coin']:
    traces.append(go.Scatter(x=info_data['earned_coin'].index, y=info_data['earned_coin'][sr], name=sr))
fig = tools.make_subplots(rows=len(traces), cols=1, shared_xaxes=True)
fig['layout'].update(height=800, title='Earned coin')
for i, tr in enumerate(traces, 1):
    # 如果需要在一个subplot里画多条线，多调用几次append_trace就行
    fig.append_trace(tr, i, 1)
py.iplot(fig)


# 各种各样的线的样式： https://plot.ly/python/line-charts/


# multiple y axies
# https://plot.ly/python/multiple-axes/
