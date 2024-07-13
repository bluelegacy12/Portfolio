import puppeteer from "puppeteer";

const url = 'http://127.0.0.1:8000/';

(async()=>{
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();

    await page.goto(url);
    const title = await page.evaluate(()=>{
        const divs = document.querySelectorAll('div');
        for (let div of divs) {
            if (div.innerText == 'Sweet Abundance'){
                return div.innerText;
            }
        }
        return null
    });

    await browser.close();

    if (title != null){
        console.log('Success!');
        return 0;
    } else {
        console.log('Failure');
        return 1;
    }
    
})();