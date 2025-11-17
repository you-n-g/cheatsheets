#!/usr/bin/env bash


# 向指定的tmux窗口发送命令, 然后切换到相应 pane或者session

session=whatever  # the session can be blank to be  current window
window=${session}:0
pane=${window}.4  # This can be ":0.1".   "session:window_name" is also ok
tmux send-keys -t "$pane" C-c 
tmux send-keys -t "$pane" C-p 'some -new command' C-m
tmux send-keys -t "$pane" C-p C-m
tmux select-pane -t "$pane"   # this will no switch the window
sleep 1 # 中间可以留一秒切过去， 看完之后再切回来！！！
tmux select-window -t "$window" #  select 只管选择相应session里的window, 不管是在前台还是后台
tmux attach-session -t "$session"  # attach-session 才是把 session 切换到前台的关键命令



# 用tmux新开一个窗口来执行命令
tmux new-window "sleep 5 && autossh root@123.56.94.165 -R0.0.0.0:2348:0.0.0.0:22" # -t session:window_INDEX -n name
tmux splitw -h -t sgx:1  # 把目标窗口的当前pane 分左右两边


# 如何按你的设定一键启动环境
# 参考 https://github.com/you-n-g/deployment4personaluse/blob/master/helper_scripts/start_tmux.sh



# 把另外一个pane弄到当前window新建的一个pane
tmux join-pane -s ":0.0"  # 带session name 可以是 "[session name]:0.0"
join-pane -t {last}  # 这个非常好用， 一般手动输入pane的 session name, window name 很麻烦，但是通过选择器来决定这个
                     # join关系一切就变得更简单了


# trouble shooting

ctrl + q  # 有时候整个pane会卡住，我无法稳定复现，但是这个可以解决



# 找到特定PID对应的session.  https://stackoverflow.com/a/29444427
tmux list-panes -a -F "#{pane_pid} #{session_name}:#{window_index}:#{pane_index}" | grep ^<PID>


# Environment 变量
## Tmux控制一套session最小粒度的变量机制，这套变量机制由session environment(每个session独有的变量)和global environment(感觉像是server创建时设置的环境变量)组成
## **这套变量不会影响已有的window, 只会影响新建的窗口**
# Environment 相关控制指令
## update-environment: 从tmux外的 shell环境中拿到变量(所以在tmux内部的任何修改都无法继承)， 在每次create session和 attach session时改变 tmux本身的变量
### 这个对应的option是一组空格隔开的变量，千万要注意留有空格 set-option -ga update-environment " CONDA_DEFAULT_ENV"
## setenv 和 showenv:  可以直接修改 environment, 如果想在tmux内部修改environment可以用这个

# ref
# https://superuser.com/questions/1423554/how-does-tmux-spawn-multiple-sessions
# https://stackoverflow.com/questions/20701757/tmux-setting-environment-variables-for-sessions




# libtmux
# apis: https://github.com/tmux-python/libtmux
# 坑
# 1. 发送特殊控制键有一点问题, 可以通过下面的方式解决
# https://github.com/tmux-python/libtmux/issues/88
# https://github.com/tmux-python/libtmux/issues/13
#  server.find_where({ "session_name": "server-tmux" }).find_where({'window_name': 'jiji'}).select_pane(0).send_keys('C-c', enter=False, suppress_history=False)
#  Newer version:
#  - server.sessions.get(session_name=SESSION_NAME).windows.get(window_name=WINDOW_NAME).panes[0].send_keys('C-c', enter=False, suppress_history=False)


# 管理服务器
# 相比ansible
## libtmux 更容易debug, 更容易配置,  而且和python一起使用更灵活;  使用做开发
# Ansible的优势
## ansible更容易一下看出哪个出错了
## Ansible有机制保证相应的步骤一定是执行成功了, 适合做生产
## 可以并行地做，tmux只能单个window执行一个task




# 一些概念
# key-table: 
# - 设计目的是为了定义连续的命令
# - 实现方式是让你输入一个key后， 触发进入另外一个 key-table， 几个key-table串起来就可以达到等价于连续前缀的效果
# - https://stackoverflow.com/a/53418329

