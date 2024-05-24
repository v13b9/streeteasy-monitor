const puppeteer = require('puppeteer');
const path = require('path');
const { Pool } = require('pg');

const connectionString = 'postgres://postgres.omszflfpoxotqapvioim:ZFh1QKUYHhCDkYJ3@aws-0-us-east-1.pooler.supabase.com:5432/postgres'

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

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // test different user agent
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36');

    // await page.goto(testUrl);
    await page.goto(`file:${path.join(__dirname, 'sample.html')}`);
    await page.setViewport({width: 1080, height: 1024});

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
        // await page.goto(listing.url);
        // await page.screenshot({
        //     path: 'screenshot.jpg'
        // })
        // submit the contact form
        // insert into database
        await insertListing(listing);
    });

    await browser.close();
})();