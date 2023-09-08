from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800


def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)

    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait)

    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(
            filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    driver.quit()


def __takeScreenshot(filePrefix, driver, wait, handle="Post"):
    method = By.CLASS_NAME if (handle == "Post") else By.ID
    search = wait.until(
        EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName


def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False

    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.cookie.cookieBehavior', 1)

    driver_path = r'C:\Geckodriver\geckodriver.exe'
    driver = webdriver.Firefox(
        executable_path=driver_path,
        options=options,
        firefox_profile=profile
    )

    wait = WebDriverWait(driver, 10)
    driver.get(url)
    driver.implicitly_wait(10)
    print("Trying to click Cookies...")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[class='_1tI68pPnLBjR1iHcL7vsee _2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 ']")
    )).click()
    print("Clicked Cookies")

    driver.set_window_size(width=screenWidth, height=screenHeight)

    return driver, wait
