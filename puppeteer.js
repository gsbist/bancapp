const puppeteer = require('puppeteer');
global.ReadableStream = require('web-streams-polyfill').ReadableStream;

var pageUrl = process.argv[2];

(async () => {
  try{
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(80000);
    await page.setDefaultTimeout(80000);

    await page.goto(`file://${pageUrl}`,{waitUntil: 'networkidle2'});
    await page.emulateMediaType('screen');

    await page.pdf(
      {
        path: process.argv[3],
        format: 'A4',
        displayHeaderFooter: true,
        headerTemplate: ' ',
        footerTemplate: " ",
        margin: {
          top: '30px',
          bottom: '60px',
          right: '30px',
          left: '30px'
        }
      });

    await browser.close();
  }
  catch(e){
    console.log(e);
    process.exit(0);
  }
})();

