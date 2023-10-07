"""
Python Selenium Code
Automation code to Make my trip ("https://www.makemytrip.com")
To Find Buses and their complete details
Save Buses List to Excel file
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tracemalloc
import warnings
import pandas


class MakeMyTripBusSearch(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        tracemalloc.start()

    def test_opan_site_check_buses(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://www.makemytrip.com")

        try:
            iframe = driver.find_element(By.ID, 'webklipper-publisher-widget-container-notification-frame')
            driver.switch_to.frame(iframe)
            # Perform actions inside the iframe
            iframe_element = driver.find_element(By.CLASS_NAME, 'close')
            iframe_element.click()
            driver.switch_to.default_content()
        except NoSuchElementException:
            pass

        try:
            driver.find_element(By.XPATH, '//*[@id="SW"]/div[1]/div[2]/div[2]/div/section/span').click()
        except NoSuchElementException:
            pass

        driver.find_element(By.CLASS_NAME, 'menu_Buses').click()
        driver.implicitly_wait(5)
        driver.find_element(By.ID, 'fromCity').click()
        inp_city = (driver.find_element
                    (By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div/div/input'))
        inp_city.clear()
        from_city = "Pune"
        inp_city.send_keys(from_city)

        sug_city = driver.find_elements(By.XPATH, f'//span[@class="sr_city blackText"]')
        for city in sug_city:
            city_name = city.text
            if from_city in city_name:
                city.click()
                break

        out_city = (driver.find_element
                    (By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div/input'))
        to_city = "Bangalore" or "Bengalore"
        out_city.send_keys(to_city)

        sug_city1 = driver.find_elements(By.XPATH, f'//span[@class="sr_city blackText"]')
        for city1 in sug_city1:
            city_name1 = city1.text
            if to_city in city_name1:
                city1.click()
                break
        x = driver.find_element(By.XPATH, '//*[@id="fromCity"]')
        y = driver.find_element(By.XPATH, '//*[@id="toCity"]')
        print(x.get_attribute('value'), "to", y.get_attribute('value'))
        print(f'_' * 30)

        while True:
            month = driver.find_element(By.CLASS_NAME, 'DayPicker-Caption').text
            if 'November 2023' == month:
                target_date_label = "Fri Nov 17 2023"
                target_date_element = driver.find_element(By.XPATH, f'//div[@aria-label="{target_date_label}"]')
                target_date_element.click()

                break
            else:
                button = "Next Month"
                nextbutton = driver.find_element(By.XPATH, f'//span[@aria-label="{button}"]')
                nextbutton.click()
        search = driver.find_element(By.XPATH, f'//button[@id="search_button"]')
        search.click()
        wait = WebDriverWait(driver, 10)
        bus_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'busCard')))

        bus_list = []
        for bus_card in bus_cards:
            bus_info = bus_card.find_element(By.CLASS_NAME, 'busInfo')
            bus_name = bus_info.find_element(By.TAG_NAME, 'p').text
            bus_type = bus_info.find_elements(By.TAG_NAME, 'p')[1].text

            time_info = bus_card.find_element(By.CLASS_NAME, 'makeFlex.row.appendBottom20.alignSelfStart.hrtlCenter')
            departure_time = time_info.find_elements(By.TAG_NAME, 'span')[0].text
            arrival_time = time_info.find_elements(By.TAG_NAME, 'span')[4].text

            price = bus_card.find_element(By.ID, 'price').text
            seats_left = bus_card.find_elements(By.CLASS_NAME, 'sc-fjdhpX.fXgCif')[0].text

            bus_list.append({"Bus Name": bus_name,
                             "Bus Type": bus_type,
                             "Departure Time": departure_time,
                             "Arrival Time": arrival_time,
                             "Price": price,
                             "Seats Left": seats_left})

        bus_results = pandas.DataFrame(bus_list)
        bus_results.to_excel("buses.xlsx", index=False)
        print(f'{len(bus_list)} Buses found')

    def tearDown(self):
        self.driver.quit()
        warnings.filterwarnings("ignore", category=ResourceWarning)


if __name__ == "__main__":
    unittest.main()
