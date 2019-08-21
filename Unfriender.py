import getpass
import pickle
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

SCROLL_PAUSE_TIME = 5

exec_path = input("Enter executable path for geckodriver: ")

firefox_profile = webdriver.FirefoxProfile()
# Disable CSS
firefox_profile.set_preference('permissions.default.stylesheet', 2)
# Disable images
firefox_profile.set_preference('permissions.default.image', 2)
# Disable Flash
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

driver = webdriver.Firefox(
    firefox_profile=firefox_profile,
    executable_path=exec_path  #"D:\\geckodriver-v0.24.0-win64\\geckodriver.exe"
)
driver.get("https://www.facebook.com/")

username_box = driver.find_element_by_id("email")
email = input("Enter email: ")
username_box.send_keys(email)
print("Email Id entered")
sleep(1)

password_box = driver.find_element_by_id("pass")
pwd = getpass.getpass(promt="Your password: ")
password_box.send_keys(pwd)
print("Password entered")

login_box = driver.find_element_by_id("loginbutton")
login_box.click()
sleep(2)

try:
    code_box = driver.find_element_by_id("approvals_code")
    login_code = getpass.getpass(promt="Authentication Code: ")
    code_box.send_keys(login_code)
    print("login code sent")
    submit_box = driver.find_element_by_id("checkpointSubmitButton")
    submit_box.click()
    sleep(1)
    options = driver.find_elements_by_name("name_action_selected")
    options[1].click()
    sleep(1)
    submit_box = driver.find_element_by_id("checkpointSubmitButton")
    submit_box.click()
    sleep(1)
except NoSuchElementException:
    print("Successfully logged in")

real_friends = []

#add same location at which you save your pickle below
try:
    pickle_in = open("real_friends.pickle", "rb")
    real_friends = pickle.load(pickle_in)
except IOError:
    print("Pickle not present")

if len(real_friends) == 0:
    User = input("Enter your first name: ")
    Profile = driver.find_element_by_link_text(User)
    Profile = Profile.get_attribute("href")
    driver.get(Profile)
    sleep(1)
    print("Switched to profile")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    All_friends = driver.find_element_by_link_text("Friends")
    All_friends = All_friends.get_attribute("href")
    driver.get(All_friends)
    sleep(1)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        count = count + 1
        print(count)

    friends = []
    friends_divs = driver.find_elements_by_css_selector("div[class='fsl fwb fcb']")
    for friends_div in friends_divs:
        friends_as = friends_div.find_elements_by_tag_name("a")
        for friends_a in friends_as:
            friends.append(friends_a.get_attribute("href"))

    print("Total Friends found: " + str(len(friends)))

    count = 0
    for friend in friends:
        if count < 1500:
            count = count + 1
            continue
        if friend.find("friends_tab") != -1:
            real_friends.append(friend)

    #Add a certain pickle location

    pickle_out = open("real_friends.pickle", "wb")
    pickle.dump(real_friends, pickle_out)

flag = 0
count = 0
ind = 0
trial = 0
#pickle to continue from where you left off last time

last_unfriended = ''
try:
    pickle_in = open("D:\\WORK\\last_unfriended.pickle", "rb")
    last_unfriended = pickle.load(pickle_in)
except IOError:
    print("Pickle for last unfriended not present")
for friend in real_friends:
    ind = ind + 1
    if (last_unfriended == '' or friend.find(last_unfriended) != -1):
        flag = 1
    if flag == 0:
        continue
    if count > 100:
        break
    driver.get(friend)
    print("Trying Friend number: " + str(ind) + " out of " + str(len(real_friends)))
    trial = trial + 1
    try:
        elem = driver.find_element_by_partial_link_text("India")
    except NoSuchElementException:
        # Code for unfriending
        print("Being Unfriended:  " + friend)
        sleep(1)
        div = driver.find_elements_by_css_selector("div[class='_2yfv _2yfv FriendButton']")
        try:
            links = div[0].find_elements_by_tag_name('a')
            button = links[0]
            button.click()
            sleep(3)
            Unfriend_button = driver.find_element_by_link_text('Unfriend')
            Unfriend_button.click()
            count = count + 1
            last_undriended = friend
        except IndexError:
            print("[INDEX ERROR] Could'nt Unfriend: " + friend)
        except NoSuchElementException:
            print("[UNFRIEND BUTTON NOT FOUND] Could'nt unfriend: " + friend)
        except Exception:
            print("Could'nt Unfriend: " + friend)
    print("Unfriended count: " + str(count) + " out of tried: " + str(trial))

    #adding 90 mins of pause to prevent getting blocked xD

    if count > 85 or trial > 130:
        pickle_out = open("last_unfriended.pickle", "wb")
        pickle.dump(last_undriended, pickle_out)
        for i in range(90):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(current_time)
            driver.get('https://www.facebook.com/')
            sleep(60)
        count = 0
        trial = 0

driver.quit()
