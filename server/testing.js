import axios from 'axios';
import * as cheerio from 'cheerio';
async function handler(){
    const url = "https://events.umich.edu/list?filter=alltypes%3A20";
    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    };

    try {
        // 1. Fetch the page (equivalent to requests.get)
        const { data: html } = await axios.get(url, { headers, timeout: 10000 });

        // 2. Load HTML into Cheerio (equivalent to BeautifulSoup)
        const $ = cheerio.load(html);
        const events = [];

        // 3. Find all event containers (equivalent to find_all)
        // Selects every <div> with class "event-listing-grid"
        $('.event-listing-grid').each((index, element) => {
            const item = $(element);

            // 1. Extract Title and Link
            const titleTag = item.find('.event-title a');
            const title = titleTag.text().trim();
            const link = "https://events.umich.edu" + titleTag.attr('href');

            // 2. Extract DateTime from the <time> tag
            const timeTag = item.find('time.time-banner');
            const eventDatetime = timeTag.attr('datetime') || "N/A";
            const readableTime = timeTag.text().trim() || "N/A";

            // 3. Extract Location
            // Find the first <li> inside the .event-details <ul>
            const details = item.find('ul.event-details');
            let location = "TBD";
            if (details.length > 0) {
                const locLi = details.find('li').first();
                location = locLi.text().trim();
            }

            // Add to our list
            events.push({
                title,
                link,
                datetime: eventDatetime,
                time_display: readableTime,
                location
            });
        });
        console.log(events)
        
        return events;

    } catch (error) {
        console.error(`Error scraping: ${error.message}`);
        return [];
    }
};