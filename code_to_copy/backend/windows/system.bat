
:: 设置wifi共享
netsh wlan set hostednetwork mode=allow ssid=shared_by_XXX key=XXX
netsh wlan stop hostednetwork
netsh wlan start hostednetwork


:: putty自动连接
D:
cd "D:\XXX\putty\"
putty.exe -D 127.0.0.1:8964 -l XXX_USER -pw XXX_PASSWORD XXX_HOST




:: sleep
ping -n XXX 127.0.0.1 >nul



:: 并行 XXXX
start XXXX


:: 查看端口占用情况
netstat -ano
