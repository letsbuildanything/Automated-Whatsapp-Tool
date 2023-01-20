from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

import pyperclip

options = webdriver.ChromeOptions()

options.add_argument("--user-data-dir=C:\\Users\\LENOVO\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://web.whatsapp.com/')

wait = WebDriverWait(driver, 100)
# user = wait.until(EC.presence_of_element_located(('xpath', f'//span[@title="{recipient_name}"]')))
# user.click()

#
print('choose your action from below:')
print("""
1 :: send msg
2 :: send image(s)
3 :: send sticker(s)
4 :: send document(s)
5 :: send contact(s)
6 :: create poll
7 :: change profile pic
""")


def send_msg(users_name):

    print("""
        1 :: manual message
        2 :: clipboard message
    """)

    response = int(input("Enter your response: "))
    msg = ''
    if response == 1:
        msg += input("What would you like to say him/her: ")

    elif response == 2:
        msg += pyperclip.paste()

    else:
        print('invalid argument! Please try again!')
        exit(0)

    # below code is for make fun by sending bulk/iterative message to users.
    wanna_try_fun = input('want to send bulk/iterative msg for fun!: reply(y|n) :: ')
    if wanna_try_fun.capitalize() == 'Y':
        limit = int(input("Tell me the iteration limit :: "))

        msg = (msg + '\n')*limit
        # print(msg)

    print(f'Message sent to ({", ".join(users_name)}):\n{msg}')
    send_msg_util(msg, users_name)
    print('msg sent')
    sleep(10)


def send_msg_util(message: str, users_name: list):
    msg = message
    for user in users_name:
        wait.until(EC.presence_of_element_located(('xpath', f'//span[@title="{user}"]'))).click()

        msg_box = driver.find_element(by='xpath',
                                      value='//div[@title="Type a message"]')
        msg_box.send_keys(msg, Keys.ENTER)


def send_image(users_name):
    file_path = input('Enter xpath of image file: ')
    wait.until(EC.presence_of_element_located(('xpath', f'//span[@title="{users_name[0]}"]'))).click()
    # sleep(10)
    # file_path = r'C:\Users\LENOVO\Desktop\bird-wings-flying-feature.gif'
    attach = driver.find_element(by='xpath',
                                 value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
    attach.click()

    img_file_ele = driver.find_element(by='xpath',
                                       value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input')
    img_file_ele.send_keys(file_path)

    is_msg_on_pic: bool = bool(True if input("do you want to add msg to image(y|n): ").capitalize()=='Y' else False)
    msg_on_pic = input("Add your message: ") if is_msg_on_pic else ''

    msg_with_pic_ele = wait.until(EC.presence_of_element_located(('xpath', '//div[@title="Type a message"]')))
    msg_with_pic_ele.send_keys(msg_on_pic, Keys.ENTER)
    sleep(10)
    # send_btn = driver.find_element(by='xpath', value='//div[@aria-label="Send"]')
    # send_btn.click()

    print("image sent successfully")
    sleep(10)


def send_sticker():
    print("My work is to send sticker")


def send_docs():
    print("My work is to send docs")


def send_contact():
    print("My work is to send contact")


def create_poll():
    print("My work is to create poll")

def change_pp():

    print("""
        choose from below:
        1 :: Upload new profile photo
        2 :: remove Profile photo
    """)

    option_choosen = int(input('Enter you Action: '))

    if option_choosen == 1 or option_choosen == 2:

        # below two line is common to both remove/upload
        small_pp_ele = wait.until(EC.presence_of_element_located(('xpath',
                                                                  '//div[@role="button"][@class="_3GlyB dwbWf"][@style="height: 40px; width: 40px; cursor: pointer;"]')))
        small_pp_ele.click()

        if option_choosen == 1:
            large_pp_ele = wait.until(EC.presence_of_element_located(('xpath', '//input[@type="file"][@accept="image/gif,image/jpeg,image/jpg,image/png"]')))
            large_pp_ele.send_keys(r"C:\Users\LENOVO\Desktop\color_pic\yellow.jpg")

            wait.until(EC.presence_of_element_located(('xpath', '//div[@aria-label="Submit image"]'))).click()

        else:
            # tried to hover over image
            large_pp_ele = wait.until(EC.presence_of_element_located(('xpath', '//div[@title="Photo Picker"]')))
            ActionChains(driver).move_to_element(large_pp_ele).perform()
            large_pp_ele.click()

            wait.until(EC.presence_of_element_located(('xpath', '//div[@aria-label="Remove Photo"]'))).click()
            wait.until(EC.presence_of_element_located(('xpath', '//div[@data-testid="popup-controls-ok"]'))).send_keys(Keys.ENTER)
    else:
        print('You have pressed invalid key...')

    sleep(10)

action_dict = {
    1: send_msg,
    2: send_image,
    3: send_sticker,
    4: send_docs,
    5: send_contact,
    6: create_poll,
    7: change_pp
}

action = int(input("Type your action here:: "))
if action != 7:
    recipient_name = input("enter recipient name(s): ")
    users = recipient_name.split(', ') #use regular expression to extract name properly
    action_dict[action](users)

else:
    change_pp()