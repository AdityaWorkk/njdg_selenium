from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import threading


# ✅ Setup WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("drivers\\chromedriver.exe")  # Ensure correct ChromeDriver path
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://njdg.ecourts.gov.in/njdg_v3/")
wait = WebDriverWait(driver, 30)  # ✅ Wait object for dynamic elements

try:
    

    # ✅ Validate modal opens
    time.sleep(10)
    wait.until(EC.visibility_of_element_located((By.ID, "modal_estwiseCase_data")))
    print("✅ City-wise Modal opened.")

    from selenium.webdriver.support.ui import Select

    # ✅ Locate the dropdown inside the specific div
    dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tblestwisecount_length select")))
    
    # ✅ Select value "100"
    select = Select(dropdown)
    select.select_by_value("100")  # Select option with value="100"

    # ✅ Extract total entries
    time.sleep(5)
    entries_text = wait.until(EC.presence_of_element_located((By.ID, "tblestwisecount_info"))).text
    total_entries = int(entries_text.split()[-2])
    print(f"✅ Total establishments: {total_entries}")

    # ✅ Load existing data
    try:
        with open("case_details_final.json", "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    # ✅ Function to handle input with timeout
    def get_user_input():
        global est_input
        try:
            est_input = int(input(f"Enter the establishment number, from 0 to {total_entries}, (or wait 5 sec to continue from 1): ").strip())
        except:
            est_input = None
    # ✅ Default case number
    case_wise_input = 0

    # ✅ Start the input thread with a 5-second timeout
    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()
    input_thread.join(timeout=30)  # Wait for max 15 seconds

    # ✅ Loop through all establishments
    for i in range(est_input, total_entries):
        time.sleep(2)

        # ✅ Find and Click the i-th instance of "Case-wise details"
        case_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[onclick*='casewise_case_details']")))

        if i < len(case_links):
            driver.execute_script("arguments[0].click();", case_links[i])
            print(f"✅ Clicked {i}th case details link.")
        else:
            print("❌ No more cases to process.")
            break

        # ✅ Validate case modal
        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.ID, "modal_dashcaselist")))
        print("✅ Case-wise Modal opened.")

        ############
        import json
        import os

        # ✅ Load existing data
        try:
            # ✅ Locate the dropdown inside the specific div
            dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tbl_cases_dash_length select")))

            # ✅ Select value "1000"
            select = Select(dropdown)
            select.select_by_value("1000")  # Select option with value="1000"

            time.sleep(5)

            # ✅ Starting to scrap from specific page
            import threading

            # ✅ Extract total cases dynamically
            import re

            # ✅ Extract text from the webpage
            case_wise_text = wait.until(EC.presence_of_element_located((By.ID, "tbl_cases_dash_info"))).text
            print(f"✅ Extracted text: {case_wise_text}")

            # ✅ Use regex to extract the second number (1000)
            match = re.search(r"to ([\d,]+)", case_wise_text)

            if match:
                cw_entries = int(match.group(1).replace(",", ""))  # Remove comma and convert to integer
                print(f"✅ Extracted number: {cw_entries}")  # Output: 1000
            else:
                print("❌ Number not found!")


            # ✅ Function to handle input with timeout
            def get_user_input():
                global case_wise_input
                try:
                    case_wise_input = int(input("Enter the page number(1000 entries per page), (or wait 5 sec to continue from 1): ").strip())
                except:
                    case_wise_input = None

            # ✅ Default case number
            case_wise_input = 0

            # ✅ Start the input thread with a 5-second timeout
            input_thread = threading.Thread(target=get_user_input)
            input_thread.start()
            input_thread.join(timeout=40)  # Wait for max 15 seconds

            i = 0

            if case_wise_input != 0:
                for i in range(case_wise_input):  # Assuming 1000 cases per page
                    next_button = driver.find_element(By.ID, "tbl_cases_dash_next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("✅ Reached the last page. Stopping pagination.")
                        break
                    
                    driver.execute_script("arguments[0].click();", next_button)
                    print("✅ Clicked 'Next' button. Fetching more data...")
                    print(f"✅ Reached page {i+1}.")
    
                    time.sleep(3)  # Wait for new data to load
                
            print(f"✅ Reached case {case_wise_input}. Starting data extraction from here.")



            #######
            save_file = "case_details_final.json"
            with open(save_file, "r", encoding="utf-8") as file:
                print(f"saving in {save_file}")
                existing_data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = []

        # ✅ Use JavaScript Executor to get only the 2nd <td> (Establishment Name) from each row
        establishment_names = driver.execute_script("""
            return Array.from(document.querySelectorAll('#tblestwisecount tbody tr')).map(row => 
                row.children[1] ? row.children[1].textContent.trim() : ''
            );
        """)

        # ✅ Check if the i-th establishment exists
        if i < len(establishment_names):
            establishment_name = establishment_names[i]  # Get the i-th establishment name
            print(f"✅ Extracted {i+1}th Court Name: {establishment_name}")
        else:
            establishment_name = "Unknown"  # Fallback if i is out of range
            print(f"❌ Establishment {i+1} not found. Using 'Unknown'.")




        # ✅ Extract table headers dynamically
        header_elements = driver.find_elements(By.CSS_SELECTOR, "#tbl_cases_dash thead th")
        headers = [header.text.strip() for header in header_elements]
        print("✅ Extracted headers:", headers)

        # ✅ Find if establishment already exists
        establishment_entry = next((item for item in existing_data if item["Establishment"] == establishment_name), None)

        if not establishment_entry:
            # ✅ If establishment does not exist, create a new one with an incremented Sr. No
            establishment_sr_no = len(existing_data) + 1
            establishment_entry = {
                "Sr. No": establishment_sr_no,
                "Establishment": establishment_name,
                "Count": []
            }
            existing_data.append(establishment_entry)
        else:
            establishment_sr_no = establishment_entry["Sr. No"]  # Keep existing Sr. No

        # ✅ Get the next available "Sr. No." for cases in "Count"
        next_case_sr_no = len(establishment_entry["Count"]) + 1

        # ✅ Function to extract and append JSON
        def extract_and_append_json():
            global next_case_sr_no  # Ensure the Sr. No. continues across pages

            rows = driver.find_elements(By.CSS_SELECTOR, "#tbl_cases_dash tbody tr")

            extracted_cases = []
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                case_data = {headers[i]: columns[i].text.strip() for i in range(len(columns))}

                # ✅ Assign unique "Sr. No." to each case
                case_data["Sr. No."] = str(next_case_sr_no)
                next_case_sr_no += 1  # Increment for next case

                extracted_cases.append(case_data)

            # ✅ Append new cases to the correct establishment
            establishment_entry["Count"].extend(extracted_cases)

            # ✅ Save JSON to file
            with open(save_file, "w", encoding="utf-8") as json_file:
                json.dump(existing_data, json_file, indent=4)

            print(f"✅ JSON Data Extracted and Appended for {establishment_name}!")

        # ✅ Extract first page data before pagination
        extract_and_append_json()

        # ✅ Click "Next" button until disabled
        while True:
            try:
                next_button = driver.find_element(By.ID, "tbl_cases_dash_next")
                if "disabled" in next_button.get_attribute("class"):
                    print("✅ Reached the last page. Stopping pagination.")
                    break
                
                driver.execute_script("arguments[0].click();", next_button)
                print("✅ Clicked 'Next' button. Fetching more data...")

                time.sleep(3)  # Wait for new data to load
                extract_and_append_json()

            except Exception as e:
                print("❌ No 'Next' button found or pagination ended.", e)
                break
        
        print("✅ Pagination completed. All pages processed.")


        ##########################################
        # # Wait for the button to be present in the DOM
        back_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-bs-target='#modal_estwiseCase_data']")))

        # Click the button using JavaScript Executor
        driver.execute_script("arguments[0].click();", back_button)

        print("✅ Clicked the 'Back' button using JavaScript Executor.")

except Exception as e:
    print("❌ Error:", e)
    driver.save_screenshot("error.png")

# ✅ Keep browser open until exit
input("Press Enter to exit...")
driver.quit()
