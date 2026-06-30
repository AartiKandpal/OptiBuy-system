import asyncio
from playwright.async_api import async_playwright

async def get_site_data(site, query):
    search_q = query.replace(' ', '+')
    urls = {
        "amazon": f"https://www.amazon.in/s?k={search_q}",
        "flipkart": f"https://www.flipkart.com/search?q={search_q}",
        "myntra": f"https://www.myntra.com/{search_q}",
        "savana": f"https://www.savana.com/search/{search_q}",
        "purplle": f"https://www.purplle.com/search?q={search_q}"
    }

    url = urls.get(site, f"https://www.google.com/search?q={site}+{search_q}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=6000)
            await page.wait_for_load_state("networkidle")
            
            price = "Check Deal"
            if site == "amazon":
                price_element = await page.locator("span.a-price-whole").first.text_content()
                price = "₹" + price_element
            elif site == "flipkart":
                price_element = await page.locator("div._30jeq3").first.text_content()
                price = price_element
            elif site == "myntra":
                price_element = await page.locator("span.product-discountedPrice").first.text_content()
                price = price_element

            await browser.close()
            return {"site": site.capitalize(), "price": price, "link": url}
            
        except:
            await browser.close()
            return {"site": site.capitalize(), "price": "View on Site", "link": url}

def get_all_prices(product_name):
    sites = ["amazon", "flipkart", "myntra", "savana", "purplle"]
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tasks = [get_site_data(site, product_name) for site in sites]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    
    return results