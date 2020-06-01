from  flask import  Flask
from flask import abort, redirect, url_for
from selenium import webdriver
from  flask import  render_template

app  =  Flask(__name__)

@app.route('/tools/' , methods=['GET', 'POST'])
@app.route('/tools/<string:wd>' , methods=['GET', 'POST'])
def  tools(wd=None):
     if wd==None:
        return  render_template('tools.html')
     chrome_options = webdriver.ChromeOptions()
     # chrome_options.add_argument('--headless')
     chrome_options.add_argument('--no-sandbox')
     browser = webdriver.Chrome(executable_path="C:/Program Files (x86)/Google\Chrome/Application/chromedriver.exe",options=chrome_options)

     browser.get("https://www.baidu.com/s?wd=%s" % wd)
     element = browser.find_element_by_id("1").find_element_by_tag_name("a")
     get_attribute=element.get_attribute("href")
     browser.quit()
     return redirect(get_attribute)



if  __name__  ==  '__main__':

    app.run(host='0.0.0.0',debug=True)