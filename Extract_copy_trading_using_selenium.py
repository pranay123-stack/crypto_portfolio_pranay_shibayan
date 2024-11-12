from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get("https://www.binance.com/en/copy-trading")
wait = WebDriverWait(driver, 20)

# Open CSV file to save data
with open("binance_copy_trading_details.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Days Trading", "Copiers", "Total Copiers", "Mock Copier", 
                     "Closed Portfolios", "ROI", "PnL", "Sharpe Ratio", "MDD", 
                     "Win Rate", "Win Positions", "Total Positions"])

    # Locate and process each card on the first page
    try:
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-outline")))

        # Process each card
        for index in range(len(cards)):
            try:
                # Re-locate cards to avoid stale element references
                cards = driver.find_elements(By.CSS_SELECTOR, ".card-outline")
                card = cards[index]

                # Scroll the card into view and click it
                driver.execute_script("arguments[0].scrollIntoView();", card)
                time.sleep(1)
                card.click()
                time.sleep(3)  # Allow time for detail page to load

                # Extract details from the detail page
                details = {}

                # Title
                try:
                    details["title"] = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".t-headline5"))).text
                except:
                    details["title"] = "N/A"

                # Define the fields to scrape and their labels
                fields = [
                    ("Days Trading", "days_trading"),
                    ("Copiers", "copiers"),
                    ("Total Copiers", "total_copiers"),
                    ("Mock Copier", "mock_copier"),
                    ("Closed Portfolios", "closed_portfolios"),
                    ("ROI", "roi"),
                    ("PnL", "pnl"),
                    ("Sharpe Ratio", "sharpe_ratio"),
                    ("MDD", "mdd"),
                    ("Win Rate", "win_rate"),
                    ("Win Positions", "win_positions"),
                    ("Total Positions", "total_positions"),
                ]

                # Collect the data for each field
                for label, key in fields:
                    try:
                        details[key] = driver.find_element(By.XPATH, f"//div[text()='{label}']/following-sibling::div").text
                    except:
                        details[key] = "N/A"

                # Write the collected data to CSV
                writer.writerow([
                    details.get("title", "N/A"), details.get("days_trading", "N/A"), details.get("copiers", "N/A"),
                    details.get("total_copiers", "N/A"), details.get("mock_copier", "N/A"), 
                    details.get("closed_portfolios", "N/A"), details.get("roi", "N/A"), details.get("pnl", "N/A"),
                    details.get("sharpe_ratio", "N/A"), details.get("mdd", "N/A"), 
                    details.get("win_rate", "N/A"), details.get("win_positions", "N/A"), details.get("total_positions", "N/A")
                ])

                # Return to the main page
                driver.back()
                time.sleep(3)

            except Exception as e:
                print(f"Error scraping card {index + 1} details: {e}")
                driver.back()
                time.sleep(3)

    except Exception as e:
        print(f"Error loading page or locating cards: {e}")

# Close the WebDriver
driver.quit()
