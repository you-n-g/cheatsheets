#!/usr/bin/env bash


# 向指定的tmux窗口发送命令, 然后切换到相应 pane或者session

session=whatever  # the session can be blank to be  current window
window=${session}:0
pane=${window}.4  # This can be ":0.1"
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
tmux join-pane -s ":0.0"
