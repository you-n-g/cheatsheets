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
tmux select-window -t "$window"
tmux attach-session -t "$session"



# 用tmux新开一个窗口来执行命令
tmux new-window "sleep 5 && autossh root@123.56.94.165 -R0.0.0.0:2348:0.0.0.0:22"




# 把另外一个pane弄到当前window新建的一个pane
tmux join-pane -s ":0.0"
