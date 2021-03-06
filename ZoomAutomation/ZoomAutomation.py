from helium import *
import time
import pickle
from selenium.webdriver import ChromeOptions
import random


class ZoomAutomation:
    def __init__(self, proxy_id=None, proxy_port=None):
        self.id = input('Enter Meeting ID : ')
        self.password = input('Enter the Passcode : ')
        self.cookies = 'cookies.pkl'
        self.name = input('Enter your name : ')
        self.proxy_id = proxy_id
        self.proxy_port = proxy_port
        self.excuses = ['Sorry i have no camera for video play',
                        'I had technical difficulties',
                        'Battery died',
                        'Laggy and slow Internet connection ',
                        'Poor internet connection']  # we can extends it as much we want

    def login(self):
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--proxy-server=' + str(self.proxy_id) + ':' + str(self.proxy_port))
        if self.proxy_id is not None:  # if user use proxy
            driver = start_chrome('https://zoom.us', options=options)
        else:  # if user don't use proxy
            driver = start_chrome('https://zoom.us')  # opening the Chrome window
        cookies = pickle.load(open(self.cookies, 'rb'))  # loading cookies so that we can bypass authentication
        try:
            print('loading cookies')
            for cookie in cookies:
                print(cookie)
                driver.add_cookie(cookie)  # Adding cookies in our Chrome driver
        finally:
            print('Cookies loaded Sucessfully')
            go_to('https://zoom.us/wc/join/' + str(self.id))  # joining the meeting
        wait_until(lambda: Text('Your Name').exists())  # Waiting until 'Your Name' get appear
        time.sleep(0.5)
        name = driver.find_element_by_id('inputname')  # selecting input field
        if name.get_attribute('value') == 0:  # checking if our input field is not empty
            click(name)
            write(self.name)  # if empty writing name
            joinbtn = driver.find_element_by_id('joinBtn')  # selecting join button
            click(joinbtn)  # clicking in join button
        else:
            joinbtn = driver.find_element_by_id('joinBtn')
            click(joinbtn)
        wait_until(lambda: Text('Meeting Passcode').exists(), 160)  # now again waiting for password field to appear
        time.sleep(0.5)
        passcode = driver.find_element_by_id('inputpasscode')  # selecting passcode field
        click(passcode)  # clicking on passcode field
        write(self.password)  # writing our passcode
        if TextField('Meeting Passcode').value == self.password:  # checking if our passcode is filled
            joinbtn = driver.find_element_by_id('joinBtn')  # selecting join button
            click(joinbtn)  # clicking on join button
        updatecookies = driver.get_cookies()  # updating cookies so that is not get expire soon
        pickle.dump(updatecookies, open('cookies.pkl', 'wb'))
        return driver

    def main(self, driver):
        if Text('Later').exists():  # waitng for Start my video to appear
            click('Later')  # if appear click on later
            print('Later is clicked ')
            self.chat(driver)  # calling chat function to drop the message
        elif Text('Stay muted').exists():  # waitng for unmute  to appear
            click('Stay muted')  # if appear click on later
            print('Muted is clicked')  # calling chat function to drop the message
            self.chat(driver)
        else:
            print('we got nothing')
            pass

    def chat(self, driver):
        if driver.get_window_size()['width'] < 778:
            self.SChat(driver)
        else:
            self.LCHat(driver)

    def LCHat(self, driver):  # If our Window Screen is large
        if not Text('open the chat pane').exists():
            footer = driver.find_element_by_class_name('footer__btns-container')
            hover(footer)
        if not Text('Zoom Group Chat').exists():
            click('open the chat pane')
        textARE = driver.find_element_by_class_name('chat-box__chat-textarea')
        click(textARE)
        text = random.choice(self.excuses)
        write(text)
        press(ENTER)

        try:
            section_menu = driver.find_element_by_id('chatSectionMenu')
            click(section_menu)
            section_menu_list = driver.find_elements_by_class_name('chat-header__menu')[0]
            Close = section_menu_list.find_element_by_tag_name('a')
            click(Close)
        except:
            time.sleep(0.5)
            cross = driver.find_element_by_xpath(
                '//*[(@id = "chat-window")]//*[contains(concat( " ", @class, " " ), concat( " ", "ax-outline-blue", " " ))]')
            click(cross)

    def SChat(self, driver):  # If our Window Screen is small
        print('small screen working')
        More = driver.find_element_by_id('moreButton')
        click(More)
        click('Chat')
        textARE = driver.find_element_by_class_name('chat-box__chat-textarea')
        click(textARE)
        text = random.choice(self.excuses)
        write(text)
        press(ENTER)
        cross = driver.find_element_by_xpath(
            '//*[(@id = "chat-window")]//*[contains(concat( " ", @class, " " ), concat( " ", "ax-outline-blue", " " ))]')
        click(cross)


if __name__ == '__main__':
    zoom = ZoomAutomation()  # creating object of our class
    driver = zoom.login()  # Calling login function to perform login
    End_Time = time.time() + 50 * 60  # because normal meeting is of 50 min we set it 50 min. but you can change according to your requirement
    while time.time() < End_Time:
        try:
            zoom.main(driver)
        except Exception as e:
            print(e)
            pass
    kill_browser()
