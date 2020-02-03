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
