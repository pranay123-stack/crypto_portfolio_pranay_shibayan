from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Initialize the webdriver
driver = webdriver.Chrome()
driver.get("https://www.binance.com/en/copy-trading")
wait = WebDriverWait(driver, 20)

# Open CSV file to save data
with open("binance_copy_trading_details.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Card Title", "Section", "Days Trading", "Copiers", "Total Copiers", "Mock Copier", 
                     "Closed Portfolios", "90 Days ROI", "PnL", "Sharpe Ratio", "MDD", 
                     "Win Rate", "Win Positions", "Total Positions"])  

    # Loop through pages
    for page in range(1, 261):
        print(f"Scraping page {page}")

        # Retry mechanism for page loading with scroll
        attempts = 3
        page_loaded = False
        for attempt in range(attempts):
            try:
                # Wait and scroll to load cards fully
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card-container')]")))  # Update with stable selector
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Allow time for lazy-loaded elements
                page_loaded = True
                break
            except Exception as e:
                print(f"Error loading page {page}, attempt {attempt + 1}: {e}")
                driver.refresh()  # Reload the page and try again
                time.sleep(5)  # Wait before retrying

        if not page_loaded:
            print(f"No cards found on page {page}. Skipping to next page.")
            continue

        # Extract and click each card
        try:
            # Adjust selector if needed to capture all cards after scrolling
            cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'card-container')]")  # Replace with actual card container selector
            if not cards:
                print(f"No cards found on page {page}. Skipping to next page.")
                continue

            for card in cards:
                try:
                    # Get card title to identify the card
                    card_title = card.find_element(By.XPATH, ".//div[contains(@class, 'title')]").text  # Adjust XPath as needed
                    card.click()  # Click to go to the detail page
                    time.sleep(3)  # Wait for the details page to load

                    # Loop through sections (Futures Public and Spot)
                    for section in ["Futures Public", "Spot"]:
                        try:
                            # Click on the section tab
                            section_tab = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{section}')]")))
                            section_tab.click()
                            time.sleep(2)  # Wait for the section to load

                            # Extract details from the selected section
                            days_trading = driver.find_element(By.XPATH, ".//span[contains(@class, 'days-trading')]").text
                            copiers = driver.find_element(By.XPATH, ".//span[contains(@class, 'copiers')]").text
                            total_copiers = driver.find_element(By.XPATH, ".//span[contains(@class, 'total-copiers')]").text
                            mock_copier = driver.find_element(By.XPATH, ".//span[contains(@class, 'mock-copier')]").text
                            closed_portfolios = driver.find_element(By.XPATH, ".//span[contains(@class, 'closed-portfolios')]").text
                            roi_90_days = driver.find_element(By.XPATH, ".//span[contains(@class, 'roi-90-days')]").text
                            pnl_90_days = driver.find_element(By.XPATH, ".//span[contains(@class, 'pnl-90-days')]").text
                            sharpe_ratio = driver.find_element(By.XPATH, ".//span[contains(@class, 'sharpe-ratio')]").text
                            mdd = driver.find_element(By.XPATH, ".//span[contains(@class, 'mdd')]").text
                            win_rate = driver.find_element(By.XPATH, ".//span[contains(@class, 'win-rate')]").text
                            win_positions = driver.find_element(By.XPATH, ".//span[contains(@class, 'win-positions')]").text
                            total_positions = driver.find_element(By.XPATH, ".//span[contains(@class, 'total-positions')]").text

                            # Write the data for this card's section details
                            writer.writerow([card_title, section, days_trading, copiers, total_copiers, mock_copier, 
                                             closed_portfolios, roi_90_days, pnl_90_days, sharpe_ratio, 
                                             mdd, win_rate, win_positions, total_positions])

                        except Exception as e:
                            print(f"Error scraping {section} section for {card_title}: {e}")

                    # Navigate back to the main list
                    driver.back()
                    time.sleep(3)  # Wait for the main list page to load
                except Exception as e:
                    print(f"Error scraping card details: {e}")
                    driver.back()  # Ensure we return to the main page if an error occurs
        except Exception as e:
            print(f"Error processing cards on page {page}: {e}")

        # Move to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'next-page-button')]")))
            next_button.click()
            time.sleep(3)  # Allow time for the next page to load
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break

# Close the driver after scraping
driver.quit()
