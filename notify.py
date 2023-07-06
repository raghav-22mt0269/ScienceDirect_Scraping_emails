import os
import time


from plyer import notification

def show_notification(title, message):
    

    # Set up the notification
    notification.notify(
        title=title,
        message=message,
        app_icon="noun-data-science-2475218.ico",
        timeout=10
        #threaded=True,
        #callback_on_click=lambda: os.startfile(folder_path)
    )





            
    
            