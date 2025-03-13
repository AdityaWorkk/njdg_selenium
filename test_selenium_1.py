from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Setup WebDriver (Ensure ChromeDriver is installed & compatible)
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://njdg.ecourts.gov.in/njdg_v3/")

# ✅ Wait object for dynamic element handling
wait = WebDriverWait(driver, 30)

try:
    # ✅ Click the second Disposal Dashboard tab
    dashboard_buttons = wait.until(EC.presence_of_all_elements_located((By.ID, "penDash1-tab")))
    if len(dashboard_buttons) >= 2:
        driver.execute_script("arguments[0].scrollIntoView(true);", dashboard_buttons[1])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", dashboard_buttons[1])
        print("✅ Clicked the second instance of Disposal Dashboard.")

    # ✅ Click "Agewise Table Button"
    time.sleep(2)
    age_table_btn = wait.until(EC.element_to_be_clickable((By.ID, "agewiseTblbtn")))
    driver.execute_script("arguments[0].click();", age_table_btn)
    print("✅ Clicked Agewise Table Button.")

    # ✅ Click "Agewise Chart Button"
    time.sleep(2)
    chart_btn = wait.until(EC.element_to_be_clickable((By.ID, "agewisechartbtn")))
    driver.execute_script("arguments[0].click();", chart_btn)
    print("✅ Clicked Agewise Chart Button.")

    # ✅ Switch back to table view
    time.sleep(2)
    driver.execute_script("arguments[0].click();", age_table_btn)
    print("✅ Reopened Agewise Table after switching views.")

    time.sleep(5)  # Wait for the search filter to load

    # ✅ Locate the search filter and enter "2024"
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tblAgewisecount_filter input")))
    search_box.clear()
    search_box.send_keys("2024")
    print("✅ Entered '2024' in the search filter.")

    time.sleep(5)  # Wait for table update

    # ✅ Click on statewise case details link
    statewise_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[onclick*='statewise_case_details']")))
    hidden_text = driver.execute_script("return arguments[0].textContent;", statewise_link)
    print(f"🔍 Extracted Hidden Link Text: {hidden_text.strip()}")

    driver.execute_script("arguments[0].style.display = 'block';", statewise_link)
    driver.execute_script("arguments[0].click();", statewise_link)
    print("✅ Clicked statewise details link.")

    time.sleep(5)
    modal = wait.until(EC.visibility_of_element_located((By.ID, "modal_statewiseCase_data")))
    print("✅ Modal opened successfully!")

    statewise_table = wait.until(EC.presence_of_element_located((By.ID, "tblStatewisecount_wrapper")))
    print("✅ Statewise table detected in the modal!")

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "dataTables_processing")))
    print("✅ Statewise table loaded successfully.")

    search_statewise = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tblStatewisecount_filter input")))
    search_statewise.clear()
    search_statewise.send_keys("Karnataka")
    print("✅ Entered 'Karnataka' in the Statewise Table search filter.")

    time.sleep(5)

    # ✅ Click on district-wise case details link
    districtwise_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[onclick*='distwise_case_details']")))
    hidden_text = driver.execute_script("return arguments[0].textContent;", districtwise_link)
    print(f"🔍 Extracted Hidden Districtwise Link Text: {hidden_text.strip()}")

    driver.execute_script("arguments[0].style.display = 'block';", districtwise_link)
    driver.execute_script("arguments[0].click();", districtwise_link)
    print("✅ Clicked district-wise details link.")

    time.sleep(5)
    dist_modal = wait.until(EC.visibility_of_element_located((By.ID, "modal_distwiseCase_data")))
    print("✅ District-wise Modal opened successfully!")

    distwise_table = wait.until(EC.presence_of_element_located((By.ID, "tblDistwisecount_wrapper")))
    print("✅ District-wise table detected in the modal!")

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "dataTables_processing")))
    print("✅ District-wise table loaded successfully.")

    search_distwise = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tblDistwisecount_filter input")))
    search_distwise.clear()
    search_distwise.send_keys("Bangalore")
    print("✅ Entered 'Bangalore' in the District-wise Table search filter.")

    time.sleep(5)

    driver.save_screenshot("districtwise_table_bangalore.png")
    print("✅ Captured screenshot of district-wise results.")

except Exception as e:
    print("❌ Error:", e)
    driver.save_screenshot("error.png")

# ✅ Pause and close
time.sleep(10)
driver.quit()
