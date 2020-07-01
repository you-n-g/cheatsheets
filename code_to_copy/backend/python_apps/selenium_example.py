'''
最后有用的(还没有验证那些是必须的)
大概率没用的: xserver-xorg-hwe-16.04 xserver-xorg
sudo apt-get install lightdm   # 然后启动 lightdm 就自动启动xserver了
确保你本地有安装 XQuartz 之类的软件(MobaXterm就可以)
启动Xserver， 设置display
- https://unix.stackexchange.com/questions/561468/empty-screen-launching-chromium-browser-over-x11-from-ubuntu-16-to-osx-xquartz
    - 这里我理解是直接用本地的 XServer + X11Forwarding 出错时，可能用这个比较有效。
    - 更建议的方法是直接用 vncserver在服务器上启动X Server，然后本地vnc可以随时连上去看服务器的X App

如果google的账户登录不了，出现了: this browser or app may not be secure
- https://stackoverflow.com/a/59607923


TODO:
    - 把页面加载完成了才获取元素放到默认example里: https://stackoverflow.com/a/26567563
'''
# conda install selenium
# sudo apt-get install chromium-chromedriver
# sudo apt-get install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy


from tqdm.autonotebook import tqdm
from pathlib import Path


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--proxy-server=127.0.0.1:6489')  # 这里可以设置代理
# headless 
# https://www.cnblogs.com/yimiaoyikan/p/10225849.html
# - chrome的无界面状态，不用打开GUI, 少了真实的加载css,js和渲染页面的工作, 性能要高很多
# - 这里还列出了一些连接远程端口调试相关的东西
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
option.add_argument("user-data-dir=selenium")
# 这里我可以设置存储用户信息，保存用户session
# - https://stackoverflow.com/a/48665557
browser = webdriver.Chrome(options=chrome_options)
# browser.page_source #  to get the entire page txt



# 获得中国地级市

browser.get("https://zh.wikipedia.org/wiki/Template:%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9C%B0%E7%BA%A7%E4%BB%A5%E4%B8%8A%E8%A1%8C%E6%94%BF%E5%8C%BA")
links = []
for ele in tqdm(browser.find_elements_by_xpath('//*[@id="collapsibleTable0"]/tbody/tr/td/table/tbody/tr/td/div/ul/li/a')):
    links.append((ele.text, ele.get_attribute('href')))

res_p = Path("anki_data")
res_p.mkdir(parents=True, exist_ok=True)

# 获得地级市详细信息
for name, link in tqdm(links):
    browser.get(link)
    # 为了能获取到完整的页面

    def S(X):
        return browser.execute_script('return document.body.parentNode.scroll'+X)
    browser.set_window_size(S('Width'), S('Height'))
    ele = browser.find_element_by_class_name('infobox')
    ele.screenshot(str(res_p / f'{name}_answer.png'))
    for ele in browser.find_elements_by_xpath('//table[contains(@class, "infobox")]//img'):
        src = ele.get_attribute('src')
        found_pattern = False
        for pattern in ["locat", "_in_", "local", "china"]:
            if pattern in src.lower():
                ele.screenshot(str(res_p / f'{name}_question.png'))
                found_pattern = True
                break
        if found_pattern:
            break
    else:
        raise Exception("Question not found")
