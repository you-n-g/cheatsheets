
:: 设置wifi共享
netsh wlan set hostednetwork mode=allow ssid=shared_by_XXX key=XXX
netsh wlan stop hostednetwork
netsh wlan start hostednetwork


:: putty自动连接
D:
cd "D:\XXX\putty\"
putty.exe -D 127.0.0.1:8964 -l XXX_USER -pw XXX_PASSWORD XXX_HOST
::
:: putty GUI设置
:: 下载 putty.zip 
:: 这里导入相应配色 https://github.com/altercation/solarized/tree/master/putty-colors-solarized
:: 设置兼容颜色
::      Window - Colours : Enable "Allow terminal to use xterm 256-colour mode"
::      Connection - Data - Terminal details : Terminal-type string : "xterm-256color"
:: 如果还使用了tmux: 需要在 ~/.tmux.conf 中设置 set -g default-terminal "screen-256color"
:: 生成keypair
:: Connection -> Data  -> Auto-login username
::            -> SSH -> Auth -> Private key file for authentication
:: 某些不错的功能 full screen, ctrl + right click
::
:: 在图形界面设置端口转发
:: Connection -> SSH -> Tunnels -> 选择 Dynamic && Source Port 然后add ????
::
:: 使用kitty代替
:: NOTICE: 用portable的话就无法使用系统配置了
:: TODO: 优势
:: 见 http://www.9bis.net/kitty/
:: 我觉得对我比较有用的：Send to tray, Always visible, Automatic password, Roll-up, Quick start of a duplicate session
:: 最好在 kitty.ini 改下那个恶心的F7快捷键
:: [Shortcuts]
:: printall={SHIFT}{CONTROL}{F7} 
::
:: MTPutty 
:: http://ttyplus.com/downloads.html
:: 支持多个tab
:: 但是和 kitty 还是有点不兼容
::
:: 上传文件使用 winscp
::
:: # 坑篇
:: 如果报错 Unable to use key file，则需要用Putty Key Generator 重新转化一遍格式




:: sleep
ping -n XXX 127.0.0.1 >nul



:: 并行 XXXX
start XXXX


:: 查看端口占用情况
netstat -ano
