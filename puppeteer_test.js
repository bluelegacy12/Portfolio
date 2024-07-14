import puppeteer from "puppeteer";
import * as child from 'child_process';

const url = 'http://127.0.0.1:8000/';

// run the `runserver` command using exec
child.exec('python "Web Apps/sweetAbunance/sweetAbundance/manage.py" runserver', (err, output) => {
    // once the command has completed, the callback function is called
    if (err) {
        // log and return if we encounter an error
        console.error("could not execute command: ", err);
        return;
    }
    // log the output received from the command
    console.log("Starting server" );
});

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