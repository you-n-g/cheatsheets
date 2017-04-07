
:: 设置wifi共享
netsh wlan set hostednetwork mode=allow ssid=shared_by_XXX key=XXX
netsh wlan stop hostednetwork
netsh wlan start hostednetwork


:: putty自动连接
D:
cd "D:\XXX\putty\"
putty.exe -D 127.0.0.1:8964 -l XXX_USER -pw XXX_PASSWORD XXX_HOST
:: 具体配置 && 比较在印象笔记中 


:: Xshell 
:: 具体的配置方法在 印象笔记中, 这个repo主要是用来贴常用代码，所以配置方法就不管了



:: sleep
ping -n XXX 127.0.0.1 >nul



:: 并行 XXXX
start XXXX


:: 查看端口占用情况
netstat -ano

:: 查看分区的信息
echo list volume > listvol.scr
diskpart /s listvol.scr
