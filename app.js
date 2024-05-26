const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const userAgent = require('user-agents');

const path = require('path');
const { Pool } = require('pg');

puppeteer.use(StealthPlugin());

const connectionString = 'postgres://postgres.omszflfpoxotqapvioim:ZFh1QKUYHhCDkYJ3@aws-0-us-east-1.pooler.supabase.com:5432/postgres';

const pool = new Pool({
    connectionString,
});

async function insertListing(listing) {
    const { listing_id, url, price, address, neighborhood } = listing; 
    const query = `
        INSERT INTO listings (listing_id, url, price, address, neighborhood)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (listing_id) DO NOTHING;
    `;
    const values = [listing_id, url, price, address, neighborhood];

    try {
        await pool.query(query, values);
    } catch (err) {
        console.error('Error inserting listing:', err);
    }
}

async function getListings() {
    try {
        const query = 'SELECT listing_id FROM listings';
        const result = await pool.query(query);
        return result.rows;
    } catch (err) {
        console.error('Error retrieving listings:', err);
        return [];
    }
}

const searchUrl = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3';
const testUrl = 'https://www.zillow.com/homes/for_rent/condo,apartment_duplex_type/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-75.4456884765625%2C%22east%22%3A-72.5343115234375%2C%22south%22%3A39.54196992713169%2C%22north%22%3A41.85299742972416%7D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A8%7D';
const botUrl = 'https://bot.sannysoft.com/';

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--disable-extensions', '--enable-automation=false'],
    });
    const page = await browser.newPage();

    await page.evaluate(() => {
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
      });

    const randomUserAgent = userAgent.random().toString();
    const defaultUserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36';

    await page.setUserAgent(randomUserAgent || defaultUserAgent);

    await page.setCacheEnabled(false);

    // await page.goto(searchUrl);
    await page.goto(testUrl);
    // await page.goto(`file:${path.join(__dirname, 'listings.html')}`, { waitUntil: 'networkidle0' });
    
    //Randomize viewport size
    await page.setViewport({
        width: 1920 + Math.floor(Math.random() * 100),
        height: 3000 + Math.floor(Math.random() * 100),
        deviceScaleFactor: 1,
        hasTouch: false,
        isLandscape: false,
        isMobile: false,
    });

    await page.screenshot({
            path: 'screenshot.jpg'
        });

    // sort listings by newest
    await page.select("select#sort-by", "listed_desc");

    const oldListings = await getListings();
    const existingIds = oldListings.map(listing => {
        return listing.listing_id;
    });
            
    const newListings = await page.evaluate(() => {
        const listItems = document.querySelectorAll('li.searchCardList--listItem');
        const containers = Array.from(listItems);
        return containers.map(container => {
            const listing_id = container
                .querySelector('div.SRPCarousel-container')
                .getAttribute('data-listing-id');
            const url = container
                .querySelector('a.listingCard-globalLink')
                .getAttribute('href');
            const price = Number(
                container
                    .querySelector('span.price')
                    .textContent.trim().replace(/[$,]/g, '')
                );
            const address = container
                .querySelector('address.listingCard-addressLabel a')
                .textContent.trim();
            const neighborhood = container
                .querySelector('p.listingCardLabel')
                .textContent
                .replace('Rental Unit in', '').trim();
            
            return {
                listing_id,
                url,
                price,
                address,
                neighborhood,
            };

        })
    });

    const filteredListings = newListings.filter(listing => {
        return !existingIds.includes(listing.listing_id);
    });
    
    console.log('existingIds:', existingIds);
    console.log('newListings:', newListings);
    
    console.log('filteredListings:', filteredListings);
    
    // for each remaining listing in newListings,
    filteredListings.forEach(async (listing) => {
        // navigate to the url
        console.log(listing.url);

        const randomUserAgent = userAgent.random().toString();
        const defaultUserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36';
    
        await page.setUserAgent(randomUserAgent || defaultUserAgent);

        await page.goto(listing.url);

        //Randomize viewport size
        await page.setViewport({
            width: 1920 + Math.floor(Math.random() * 100),
            height: 3000 + Math.floor(Math.random() * 100),
            deviceScaleFactor: 1,
            hasTouch: false,
            isLandscape: false,
            isMobile: false,
        });

        await page.screenshot({
            path: `${listing.listing_id}.jpg`
        })
        // submit the contact form
        // insert into database
        await insertListing(listing);
    });

    // await page.goto(`file:${path.join(__dirname, 'listing.html')}`, { waitUntil: 'networkidle0' });
    // await page.screenshot({
    //     path: 'screenshot.jpg'
    // });



    await browser.close();
})();