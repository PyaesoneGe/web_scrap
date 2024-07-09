from playwright.sync_api import sync_playwright
import time
def get_url():
    # URL of the Google Map you want to render
    google_map_url = "https://www.google.com/maps"
    place='Don Muang Hotel'

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()

        # Navigate to Google Maps
        page.goto(google_map_url)
        page.wait_for_selector('div.widget-scene')

        # Take a screenshot of the entire page
        screenshot_file = "google_map_screenshot.png"
        

        page.fill('//*[@id="searchboxinput"]', place)
        page.screenshot(path=screenshot_file)

        page.click('//*[@id="searchbox-searchbutton"]/span')
        time.sleep(3)
        page.screenshot(path="result.png")

        page.wait_for_load_state("networkidle")

        nexturl = page.url

        check =page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div/div[1]')
        if check:
            print("flase")
        else:
            print('true')
            print(f"Screenshot saved as {screenshot_file}")
            print(f"Screenshot saved result")
            print(nexturl)
            return nexturl

        browser.close()



if __name__ == "__main__":
    get_url()
