const puppeteer = require('puppeteer');
const path = require('path');

sample = 'sample.html';

const searchUrl = 'https://streeteasy.com/for-rent/nyc/status:open%7Cprice:-3001%7Carea:321,364,322,325,304,320,301,319,326,329,302,310,306,307,303,412,305,109%7Cbeds:1-3';

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // test different user agent
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36');

    // await page.goto(testUrl);
    await page.goto(`file:${path.join(__dirname, sample)}`);
    await page.setViewport({width: 1080, height: 1024});

    // sort listings by newest
    await page.select("select#sort-by", "listed_desc");

    // listings are rendered as a ul with class="searchCardList"
        // ul contains li with class="searchCardList--listItem"
            // li contains div with class="listingCard"
                // div contains a with class="listingCard-globalLink" and href for listing url

    const newRentals = await page.evaluate(() => {
        const listItems = document.querySelectorAll('li.searchCardList--listItem');
        const containers = Array.from(listItems);
        return containers.map(container => {
            const id = container
                .querySelector('div.SRPCarousel-container')
                .getAttribute('data-listing-id');
            const link = container
                .querySelector('a.listingCard-globalLink')
                .getAttribute('href');
            // const title = container
            //     .querySelector('span.u-displayNone')
            //     .textContent.trim();
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
                id,
                link,
                // title,
                price,
                address,
                neighborhood,
            };

        })
    });

    console.log(newRentals);

    // query database for already visited listings

    // for each listing,
        // check if id already in database
        // if not,
            // create object consisting of:
                // the listing id (primary key)
                // the listing name
                // the listing url
                // other info if useful - price, neighborhood, etc
            // add to new listings array

    // for each listing in the new listings array,
        // navigate to the url
        // submit the contact form
    // store the listing in a database

    await browser.close();
})();