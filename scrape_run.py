from ScienceDirect.sciencedirect import ScienceDirect
import ScienceDirect.constants as const
from ScienceDirect.user_registration import Register_User
from ScienceDirect.notify import show_notification
import os




if __name__ == "__main__":
    
    registration =  Register_User("users_scidir.db")
    registration.createTable()
    registration.login_user()


    with ScienceDirect() as bot:
        bot.land_first_page(url=const.BASE_URL)
        bot.sign_in(username=const.USER_NAME, pswrd=const.PASSWRD)
        #bot.implicitly_wait(5)
        bot.ExtractEmails()
    show_notification(" Science Scraper Finished ",
                    "Sciedir_crawler has finished the search for you keyword, Please check the CSV file for results !"
                )    
    
    """notification.notify(title = " Task Complete ",
                            message = "Your science_scraper application has finished its job!",
                            timeout = 10
                            )  
    
    time.sleep(300)
   """