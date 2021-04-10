import os
import yaml
import requests
import mercadopago
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup


Loader_Requests = lambda path: yaml.load(requests.get(path).content, Loader=yaml.FullLoader)
Loader_YAML = lambda path: yaml.load(open(path), Loader=yaml.FullLoader)
os.environ["FILES_STORAGE"] = "/saponis_server/storage/"
os.environ['PATH_DB'] = "./saponis_server/database/"
local_config = "./saponis_server/_config.yml"


class Settings:

    def __init__(self):
        config = Loader_YAML(local_config)
        self.database_path = os.environ.get("FILES_STORAGE") + os.environ.get("PATH_DB")
        self.root_path = "../root_server/"
        self.host, self.port, self.debug = config["HOST"], config["PORT"], config["DEBUG"]
        self.routes, self.libs, self.templates, self.index_builder = self.config()
        self.path_index = "/list.html"
        self.index_title = 'Saponis.Jabon'
        path_img = "static/images/saponis_img/"
        self.saponis_img = {img: "./" + path_img + img for img in os.listdir("./" + path_img)}
        self.img_list = os.listdir("./" + path_img)

    @staticmethod
    def config():
        routes = {"base": "/"}
        libs = {"fractal-vendors": "./static/vendors", "fractal-css": "./static/css/index.css",
                "fractal-js": "./static/js", "fractal-img": "./static/images", "fractal-data": "./static/data"}
        templates = {
            f.replace('.html', ''): '/' + f.replace('.html', '') for f in os.listdir('./templates/subtemplates')}
        index_builder = {
            "head": "head.html",
            "header": "header.html",
            "navigation": "navigation.html",
            "footer": "footer.html",
            "navbar": "navbar.html",
            "javascripts": "javascripts.html"}
        return routes, libs, templates, index_builder

class MercadoPago:

    def __init__(self):
        sdk = mercadopago.sdk.SDK("")

        payment_data = {
            "transaction_amount": 100,
            "token": "CARD_TOKEN",
            "description": "Payment description",
            "payment_method_id": 'visa',
            "installments": 1,
            "payer": {
                "email": 'test_user_123456@testuser.com'
            }
        }
        result = sdk.payment().create(payment_data)
        payment = result["response"]


class Driver:
    options = webdriver.FirefoxOptions()
    options.headless = True
    executable_path = "./v0.29.0/geckodriver"

    def __init__(self):
        self.run_driver = lambda: webdriver.Firefox(options=Driver.options, executable_path=Driver.executable_path)
        self.user = "alan.matzumiya@outlook.es"

    def fb_login(self, page=None):
        self.driver = self.run_driver()
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        self.driver.get("https://www.facebook.com/login.php")
        self.driver.set_window_size(S('Width'), S('Height'))
        email = self.driver.find_element_by_id("email")
        email.send_keys(self.user)
        pwd = self.driver.find_element_by_id("pass")
        password = ""
        pwd.send_keys(password)
        button = self.driver.find_element_by_name("login")
        button.click()
        sleep(1)
        if page is not None:
            self.driver.get(f"https://www.facebook.com/{page}")
        sleep(2)
        self.driver.set_window_size(S('Width'), S('Height'))
        sleep(5)
        source = BeautifulSoup(self.driver.page_source, "lxml")
        self.driver.close()
        data_text = {}
        divs = source.find_all("div")
        html = source.prettify()
        data_text["html"] = html
        '''
        imgs = source.findAll("img")        
        data_img = {"saponis_fb": []}        
        for img in imgs:
            src = img.get("src")
            if "https://scontent.fhmo2-1.fna.fbcdn.net" in src:
                data_img["saponis_fb"].append(src)
        with open("data_img.yml", "w") as outfile:
            yaml.dump(data_img, outfile, default_flow_style=False)
        '''
        data_text["div"] = []
        for div in divs:
            data_text["div"].append(div.text.__str__())

        with open("data_text.yml", "w") as outfile:
            yaml.dump(data_text, outfile, default_flow_style=False)
        return html

    def instagram_login(self):
        self.driver = self.run_driver()
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.set_window_size(S('Width'), S('Height'))
        sleep(5)
        inputs = self.driver.find_elements_by_tag_name("input")
        inputs[0].send_keys(self.user)
        password = ""
        inputs[1].send_keys(password)
        button = self.driver.find_element_by_tag_name("button")
        button.click()
        sleep(2)
        self.driver.set_window_size(S('Width'), S('Height'))
        sleep(5)
        html = self.driver.page_source
        return html

    def driver_to_site(self, site, page):
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        if site == "facebook":
            self.driver.get("https://www.facebook.com/")
            email = self.driver.find_element_by_id("email")
            email.send_keys(self.user)
            pwd = self.driver.find_element_by_id("pass")
            password = input("password: ")
            pwd.send_keys(password)
            button = self.driver.find_element_by_name("login")
            button.click()
            sleep(1)
            self.driver.set_window_size(S('Width'), S('Height'))
            html = self.driver.page_source
            if page is not None:
                self.driver.get("https://www.facebook.com/" + page)
                sleep(1)
                self.driver.set_window_size(S('Width'), S('Height'))
                sleep(1)
                source = self.driver.page_source
                soup = BeautifulSoup(source, "html.parser")
                class_target = ["oajrlxb2", "s1i5eluu", "gcieejh5", "bn081pho", "humdl8nn",
                                "izx4hr6d", "rq0escxv", "nhd2j8a9", "j83agx80", "p7hjln8o",
                                "kvgmc6g5", "cxmmr5t8", "oygrvhab", "hcukyx3x", "jb3vyjys",
                                "d1544ag0", "qt6c0cv9", "tw6a2znq", "i1ao9s8h", "esuyzwwr",
                                "f1sip0of", "lzcic4wl", "l9j0dhe7", "abiwlrkh", "p8dawk7l",
                                "beltcj47", "p86d2i9g", "aot14ch1", "kzx2olss", "cbu4d94t",
                                "taijpn5t", "ni8dbmo4", "stjgntxs", "k4urcfbm", "tv7at329"]
                cl = ""
                for s in range(0, len(class_target) - 1):
                    cl += class_target[s] + " "
                cl += class_target[-1]
                script = "document.getElementsByClassName('" + cl + "');"
                print(script)
                print(self.driver.execute_script(script + "[0].click()"))
                divs = soup.findAll("div")
                for d in divs:
                    c = d.get("class")
                    if c is not None:
                        test = True
                        for s in class_target:
                            if s not in c:
                                test = False
                                break
                        if test:
                            self.driver.execute_script(script)
                            print("eureka!!")
                self.driver.close()
                return source
            else:
                soup = BeautifulSoup(html, "html.parser").find_all("link")
                print(soup)
                self.driver.close()
                return html
        else:
            self.driver.get("https://www." + site + ".com")
            sleep(1)
            self.driver.set_window_size(S('Width'), S('Height'))
            html = self.driver.page_source
            self.driver.close()
            return html
