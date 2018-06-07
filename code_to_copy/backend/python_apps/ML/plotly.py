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


# 各种各样的线的样式 style： https://plot.ly/python/line-charts/



# pandas的结合，可以直接从Dataframe中画图
# https://plot.ly/ipython-notebooks/cufflinks/
# 如果不想在online上画图，那么请先调用offline模式
import cufflinks as cf
cf.go_offline()

# cufflinks  是我见过画stack图最好用的工具
# stack的bar画出来非常方便， stack的Area可能就不太方便了

# layout_update可能会挺方便
df.iplot(layout_update={'height': 400, 'width': 900, 'title': 'XXX'})

# 直接获得traces
df.iplot(asFigure=True)['data']  # 返回的是一堆trace，即go.scatter的list
# 需要注意的是它带了颜色.




# 其他问题
# 如果出现 xticks 被建材掉， 那么调整layout
# https://stackoverflow.com/questions/38105723/prevent-long-x-axis-ticklabels-from-being-cut-off-in-bar-charts-with-plotly-in-r
fig.layout.margin.b = 250
fig.layout.margin.r = 250


# multiple y axies
# https://plot.ly/python/multiple-axes/
