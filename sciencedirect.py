from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import os
import csv
from datetime import date , time
from ScienceDirect.notify import show_notification
import logging

if not os.path.exists("Scraper_Logs"):
    
    os.mkdir("Scraper_Logs")
#script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the file name and path relative to the script directory
file_name = 'Scraper_Logs\scraper_log_file.log'
#file_path = os.path.join(script_dir, file_name)
#print(file_path)    
with open(file_name, 'w') as file:
    print("file created for logs")
    pass    
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
    filename=file_name)

logger = logging.getLogger(__name__)
show_notification("SciDir_crawler Notification", "ScienceDirect crawler has created a folder Scraper_Logs")




class ScienceDirect(webdriver.Chrome):
    
    def __init__(self,
                driver_path=r"C:\\chromedriver_win32\\chromedriver.exe",
                teardown=False):
        self.drive_path = driver_path
        self.teardown = teardown
        chrome_options = Options()
        # Add any desired options here
        # For example, to run Chrome in headless mode:
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=chrome_options)
        
        os.environ['PATH'] += self.drive_path
        super(ScienceDirect, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()
        
               
        
        
    def __exit__(self,exc_type , exc_val, exc_to):
        if self.teardown:
            self.quit()   
        
    def land_first_page(self,url=None):
        self.get(f"{url}")
        
        
    def sign_in(self, username=None, pswrd = None):
        try:
            
            email_input = self.find_element(By.NAME, value = "pf.username")
            email_input.send_keys(f"{username}")
            button_login = self.find_element(By.ID, value = "bdd-elsPrimaryBtn")
            button_login.click()
            pwd_input = self.find_element(By.ID, value = "bdd-password")
            pwd_input.send_keys(f"{pswrd}")
            Sign_IN = self.find_element(By.ID, value = "bdd-elsPrimaryBtn")
            Sign_IN.click()
            
        except Exception as e:
            logger.exception("Sign In Exceptions: %s", str(e))
            show_notification("ScienceDirect Scraper Error",
                              "Login Error occured in ScienceDirect, Please check Scraper_Logs Folder!"
                              )
        
    """def count_spaces(self,string):
        spaces = 0
        for i in string:
            if i == " ":
                spaces += 1
        return spaces"""
            
    def GetArticleLinks(self, keyword_input=None, year = None):
        try :
                    
            print("Enter the keywords you want to search")
            keyword_input = input()
            
            query = keyword_input.replace(" ","%20",-1)
            print(query)
            print("Which year or range you want to search, e.g. 2002 or 2002-2005")
            date_range = input()
            
            year = str(date_range)
            
            print("Enter the Offset number (multiple of 100 e.g. 0, 1000 or 1200) as starting point for the search")
            offset = input()
            offset = int(offset)
            print("The Scraper is searching for results....")
            
            article_links = []
            pagination = 10
            self.get(f"https://www.sciencedirect.com/search?qs={query}&show=100&date={year}&offset={offset}")
            self.set_script_timeout(10)
            pages_range = self.find_element(By.XPATH, "*//ol[@id = 'srp-pagination']//li[contains(text(),'Page ')]").text
            index_of = pages_range.index('of')

            pages = pages_range[index_of + 3:]
            total_pages = int(pages)
            show_pages = 100
            print(f"Your {keyword_input} results contain {total_pages} pages")
            if total_pages < pagination:
                print(f"Extracting article links for {total_pages} pages...")
                for p in range(pagination):
                    self.get(f"https://www.sciencedirect.com/search?qs={query}&show={show_pages}&date={year}&offset={offset}")
                    results = self.find_elements(By.CLASS_NAME, value = "result-list-title-link")
                    print(f"Page {p+1} contains {len(results)} articles")
                    for result in results:
                        
                        article_links.append({"url":result.get_attribute("href"),"Title":result.text})
                    offset += show_pages
            else:
                print("Extracting article links for first 10 pages...")
                for p in range(pagination):
                    self.get(f"https://www.sciencedirect.com/search?qs={query}&show={show_pages}&date={year}&offset={offset}")
                    results = self.find_elements(By.CLASS_NAME, value = "result-list-title-link")
                    print(f"Page {p+1} contains {len(results)} articles")
                    for result in results:
                        
                        article_links.append({"url":result.get_attribute("href"),"Title":result.text})
                    offset += show_pages
            
            f = open(f'{query}'+"_"+f'{year}.csv', 'w')
            f.close()
        except Exception as e:
            logger.error("An Error occured: %s",str(e))
            """show_notification("Science Scraper Error",
                              "An Error occured while scraping links for articles from ScienceDirect, Please check Scraper_Logs Folder!",
                              file_name)"""
            
        print(f'{query}'+"_"+f'{year}.csv file created.')
        return [article_links,query,year,keyword_input]
    
    
    def ClickEnvelops(self,keywords,year_range,Urls,Titles):
            list_of_dict = []
            envelope_icons = self.find_elements(By.CLASS_NAME,"icon-envelope")
            if envelope_icons:
                    for icon in envelope_icons:
                        try:
                            icon.click()
                            self.implicitly_wait(2)
                            workspace_div = self.find_element(By.CLASS_NAME, "Workspace")
                            author_info = workspace_div.find_element(By.ID, 'workspace-author')

                            email = author_info.find_element(By.XPATH, "//div[@class = 'e-address']//a")
                            print(email.text)
                            authors = author_info.find_element(By.CLASS_NAME, "given-name")

                            print(authors.text)

                            surnames = author_info.find_element(By.CLASS_NAME, "surname")
                            authors_name = authors.text + " " + surnames.text
                            list_of_dict.append({"Run_Date":date.today(), "Keyword_input":keywords,
                                                 "Year_Range":year_range,"URLs":Urls,"Title":Titles,"emails":email.text, "names":authors_name})
                            
                        except Exception as e:
                            logger.error("An error occured: %s",str(e))
                            """show_notification("Science Scraper Error",
                              "An Error occured while scraping emails of authors from ScienceDirect, Please check Scraper_Logs Folder!",
                              file_name)"""
                            
                            pass
            else:
                    pass
            for row in list_of_dict:
                for key in row:
                    if row[key] =='':
                        row[key] = "None"
            
            return list_of_dict
        
        
    def ClickCapture(self):
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://challenges.cloudflare.com/cdn-cgi/challenge-platform']")))
        time.sleep(10)
        WebDriverWait(self, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ctp-label']"))).click()
        checkbox = self.find_element(By.CSS_SELECTOR, value = 'label[class = "ctp-checkbox-label"]')
        print("Captcha CheckBox Element is visible? " + str(checkbox.is_displayed()))
        #driver.implicitly_wait(50)
        checkbox.click()
        
           
    def ExtractEmails(self):
        
        links = self.GetArticleLinks()
        headers = ["Run_Date","Keyword_input","Year_Range","URLs","Title","emails", "names"]
        with open(f'{links[1]}'+"_"+f'{links[2]}.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
                                
            for count, link in enumerate(links[0]):
                print("#^^#"*10)
                print(count)
                print("#^^#"*10)
                print(f"Opening link --> {link['url']}")
                print(link['Title'])
                self.get(link['url'])
                try:
                    results = self.ClickEnvelops(links[3],links[2],link['url'],link['Title'])
                    writer.writerows(results)
                    #print(dictionary_list)

                except Exception as e:
                    time.sleep(2)
                    logger.info("Check if website is asking for any varification through captcha box Or %s ", str(e))
                    show_notification("Science Scraper Error",
                              "Please check if any Captcha Box appeared in Chrome and check Scraper_Logs Folder!"
                              )
                    
                    self.ClickCapture()
                    results = self.ClickEnvelops(links[3],links[2],link['url'],link['Title'])
                    writer.writerows(results)
                    #print(dictionary_list)
            