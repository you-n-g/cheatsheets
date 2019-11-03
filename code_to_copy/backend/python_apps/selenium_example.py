# conda install selenium
# sudo apt-get install chromium-chromedriver
# sudo apt-get install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy

from selenium import webdriver

from tqdm.autonotebook import tqdm
from pathlib import Path


from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--proxy-server=127.0.0.1:6489')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
browser = webdriver.Chrome(options=chrome_options)


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
