from playwright.sync_api import sync_playwright

import time
from pprint import pprint
def get_info(url):
    

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        # Open the URL
        page.goto(url)

        def name():
            return page.inner_text('.css-1hb0db8').strip()

        def address():
            return page.inner_text('.css-1ml6wus').strip()

        def price():
            return page.inner_text('.price').strip()

        def info():
            return page.inner_text('.css-186kfow').strip()
        


        def id():
            listing_number_locator = page.locator('div.css-s5xdrg span.css-1qahy2z')
            listing_number_locator.wait_for(state="visible")
            listing_text = listing_number_locator.text_content()
            id = listing_text.split(":")[-1].strip()
            return id
        """ Apartments ID """
        

        def get_phonenumber():
    
            button_selector = '.btnShowPhone '  
            button = page.locator(button_selector)
        
            button.click()  # Click 
        
            
            li_elements_selector = 'ul.css-zjmoec > li.css-1249jn7'
            li_elements = page.query_selector_all(li_elements_selector)
            phone_numbers = []
            
            for li_element in li_elements:
            
                span_element = li_element.query_selector('span.css-s5xdrg')
            
                if span_element:
                    phone_numbers.append(span_element.inner_text())  
                    
                else:
                    print("No <span> element found within <li>")

            phone_numbers_str = ', '.join(phone_numbers)
            print("Done for Phone number ___ !")
            return phone_numbers_str
        
        """Get phone number by clicking on Phone number button"""


        def image(url):
            gallery = page.locator('li:has-text("Gallery")')
            gallery.wait_for(state="visible") # wait for visible 
            
            gallery.click()
            time.sleep(2)
            

            img_xpath = '//*[@id="__next"]/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div//img'
            # element matching the XPath
            images = page.query_selector_all(img_xpath)
            if  images:
                print("images found")
            image_sources = []
            image_elements = page.query_selector_all('.embla__slide img')
            image_sources = [element.get_attribute('src') for element in image_elements]
            print(f"Image sources from {url} is scraped")
            print("="*80)
            print(len(image_sources))
            return image_sources
        
        """ Some page have View Tour , So click on Gallery Tab and get all Gallery and save as link """
        
        details = {}
        parent_elements = page.query_selector_all('ul.css-1g8zdg0')
        for parent in parent_elements:
            list_items = parent.query_selector_all('li')
            for li in list_items:
                text_content = li.inner_text().strip()
                if ':' in text_content:
                    key, value = text_content.split(':', 1)
                    details[key.strip()] = value.strip()

        print("Done for details __ !")

        """Details of apartment that contain , 
        - Monthly or Daily price
        - Water price / Electric price
        - Services fees
        - etc ....
        """
        

        def amentities():
            result={}
            
            page.wait_for_selector("div.css-1cfffqj , div.css-a2bpvb")

            divs_true = page.query_selector_all('div.css-1cfffqj')
        
            divs_false = page.query_selector_all('div.css-a2bpvb')

            for div in divs_true:
                text =  div.text_content()
                if text:
                    text = text.strip()
                    result[text] = True
                    

            for div in divs_false:
                text =  div.text_content()
                if text:
                    text = text.strip()
                    result[text] = False
                    

            print("Done for ammenitity __ !")
            
            return result
        
        """ Get all Amentities valuse as , True / False """
        
        def get_category():  # get category for near_by function
            cato = 'div.css-m9n4sa h3.css-1na3dq1'
            eles = page.query_selector_all(cato)
            categories = [ele.text_content().strip() for ele in eles]
            return categories

        nearby_places = {}

        def near_by(): 
            categories = get_category()
            for category in categories:
                category_header = page.locator(f"h3:has-text('{category}')")
                if category_header.count() > 0:
                    elements = page.locator(f"h3:has-text('{category}') + ul > li")
                    places = []
                    for i in range(elements.count()):
                        element = elements.nth(i)
                        place_name_locator = element.locator(".css-zibm5m")
                        if place_name_locator.count() > 0:
                            span_elements = element.locator("span")
                            span_texts = [span.inner_text().split('\n')[0] for span in span_elements.element_handles()]
                        
                            if len(span_texts) >= 2:
                                places.append({span_texts[0].split('(')[0]: span_texts[1].split('(')[0]})
                            elif len(span_texts) == 1:
                                places.append({span_texts[0].split('(')[0]: None})  # Or some other default value
                        

                    nearby_places[category] = places

            print("Done for Near by __ !")
        
            return nearby_places

        def room_info():
            room_data_elements = page.query_selector_all('div.css-dutwp4')
        
            room_infos={

            }
            for i,room_elem in enumerate(room_data_elements):
            # Extract room information
                roomR_elem = room_elem.query_selector('div.css-1223njl:nth-of-type(2)')
                room_type_elem = room_elem.query_selector('div.css-1223njl:nth-of-type(3)')  
                room_size_elem = room_elem.query_selector('div.css-1hadurm') 
                monthly_rental_elem = room_elem.query_selector('div.css-y9jx00:nth-of-type(5)') 
                daily_rental_elem = room_elem.query_selector('div.css-y9jx00:nth-of-type(6)') 
                short_contract_ele = room_elem.query_selector('div.css-y9jx00:nth-of-type(7)')
                room_status_elem = room_elem.query_selector('div.css-ux0rdj') 

                room = roomR_elem.inner_text().strip() if roomR_elem else "-"
                room_type = room_type_elem.inner_text().strip() if room_type_elem else "-"
                room_size = room_size_elem.inner_text().strip() if room_size_elem else "-"
                monthly_rental = monthly_rental_elem.inner_text().strip() if monthly_rental_elem else "-"
                daily_rental = daily_rental_elem.inner_text().strip() if daily_rental_elem else "-"
                short_contract = short_contract_ele.inner_text().strip() if short_contract_ele else "-"
                room_status = room_status_elem.inner_text().strip() if room_status_elem else "-"

                room_info = {
                "Room " : room,
                "Room Type": room_type,
                "Size": room_size,
                "Monthly Rental": monthly_rental,
                "Daily Rental": daily_rental,
                "Short Contract" :short_contract,
                "Room Status": room_status
            }
                room_infos[f"Room{i+1}"]=(room_info)

            return room_infos
        """ 
        Get all data of rooms , 
        That are room type , room size , room status , Monthly or Daily  Rental
        """

        Room_info= room_info()
        ammenitity = amentities()
        place = near_by()
        data = {
            'ID': id(),
            'Name': name(),
            'Address': address(),
            'phone Number':get_phonenumber(),
            'Price': price(),
            'Info': info(),
            'Image':image(url),
            'Ammenitity': ammenitity,
            'Rooms':Room_info,
            **details ,
             
             **place# Add details dictionary keys as additional columns
        }


        # Close the browser
        browser.close()
        print(f"All data from {url} is scraped!")

        return data




