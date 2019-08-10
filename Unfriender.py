from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
SCROLL_PAUSE_TIME = 5

exec_path = input("Enter path for geckodriver executable: ")
driver = webdriver.Firefox(executable_path=exec_path)
driver.get('https://www.facebook.com/')

username_box = driver.find_element_by_id('email') 
email = input("Enter email-id: ")
username_box.send_keys(email) 
print ("Email Id entered") 
sleep(1) 
  
password_box = driver.find_element_by_id('pass') 
pwd = input("Enter your password")
password_box.send_keys(pwd) 
print ("Password entered") 
  
login_box = driver.find_element_by_id('loginbutton') 
login_box.click() 
sleep(1)

#take username as input
Profile = driver.find_element_by_link_text('Gujjar')
Profile = Profile.get_attribute('href')
driver.get(Profile)
sleep(1)
print("Switched to profile")

# Scroll down to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait to load page
sleep(SCROLL_PAUSE_TIME)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(SCROLL_PAUSE_TIME)
All_friends = driver.find_element_by_link_text('Friends')
All_friends = All_friends.get_attribute('href')
driver.get(All_friends)
sleep(1)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
count = 0
while count<100:
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
friends = []
friends_divs = driver.find_elements_by_css_selector("div[class='fsl fwb fcb']")
for friends_div in friends_divs:
    friends_as = friends_div.find_elements_by_tag_name("a")
    for friends_a in friends_as:
        friends.append(friends_a.get_attribute('href'))

real_friends = []
for friend in friends:
    if(friend.find("friends_tab") != -1):
        real_friends.append(friend)

for friend in real_friends:
    driver.get(friend)
    try:
        elem = driver.find_element_by_partial_link_text('India')
        elem2 = driver.find_element_by_partial_link_text('INDIA')
    except NoSuchElementException:
        #code for unfriending
        print("Being Unfriended:  "+friend)
        sleep(5)
        div = driver.find_elements_by_css_selector("div[class='_2yfv _2yfv FriendButton']")
        links = elem[0].find_elements_by_tag_name('a')
        button = links[0]
        button.click()
        sleep(1)
        Unfriend_button = driver.find_element_by_link_text('Unfriend')
        Unfriend_button.click()
    sleep(2)
    


driver.quit()
