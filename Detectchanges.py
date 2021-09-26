import smtplib
from email.mime.text import MIMEText
import bs4
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver

sender = "scrappercrypto@gmail.com"
receivers = ["ghazi@napoleonx.ai"]
chromedriver_autoinstaller.install()

url = "https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&encryptedUid=8D27A8FA0C0A726CF01A7D11E0095577"

browser = webdriver.Chrome()
browser.get(url)
fastrack = WebDriverWait(browser, 10).until(
    ec.visibility_of_element_located((By.XPATH, "//div[@id='tab-MYPOSITIONS']"))
)
button = browser.find_element_by_xpath("//div[@id='tab-MYPOSITIONS']")
button.click()
fastrack = WebDriverWait(browser, 10).until(
    ec.visibility_of_element_located(
        (
            By.CSS_SELECTOR,
            "tbody tr[class='rc-table-row rc-table-row-level-0'] td:nth-child(4) div:nth-child(1)",
        )
    )
)
soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
previous_value = str(soup.select(".rc-table-row.rc-table-row-level-0"))

while True:
    browser.get(url)
    fastrack = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//div[@id='tab-MYPOSITIONS']"))
    )

    button = browser.find_element_by_xpath("//div[@id='tab-MYPOSITIONS']")
    button.click()

    fastrack = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "tbody tr[class='rc-table-row rc-table-row-level-0'] td:nth-child(4) div:nth-child(1)",
            )
        )
    )

    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    new_values = str(soup.select(".rc-table-row.rc-table-row-level-0"))
    if previous_value == new_values:
        continue

    previous_value = new_values
    NewMarkPrice = str(
        soup.select(
            "tbody tr[class='rc-table-row rc-table-row-level-0'] td:nth-child(4) div:nth-child(1)"
        )
    )
    NewPnl = str(soup.select(".css-13n52y"))
    body_of_email = (
        "Changemenet au niveau du site: https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&encryptedUid=8D27A8FA0C0A726CF01A7D11E0095577 <br>  valeur du Mark Price:  <br> "
        + NewMarkPrice
        + "<br> valeur du PNL (ROE %)<br>"
        + NewPnl
    )

    msg = MIMEText(body_of_email, "html")
    msg["Subject"] = "Changement au niveau des cryptos"
    msg["From"] = sender
    msg["To"] = ",".join(receivers)

    s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    s.login(user=sender, password="wjdlxvcsxnkbjetl")
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("email sent succesfully!")
