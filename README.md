
# Steam-Discount-Checker

This is a python backend program to scrap steam discount game and save it in a database. Also it can send stats report of the database in a specific time


## Screenshots

![App Screenshot](https://i.postimg.cc/TYYrHKNw/Screenshot-20220805-220601.png)

![App Screenshot](https://i.postimg.cc/W4b5HmnR/Screenshot-20220805-221434.png)

![App Screenshot](https://i.postimg.cc/XJx40gMw/Screenshot-20220805-221702.png)
## Setup
🔴 First edit credentials.txt
```bash
  1. search_amount  - The amount of product you want to check from top seller section (1000 take 3-4 minutes) 
  2. sendmail       - This 24 hour time that is used to send the stats from the scraped data to a email
  3. gatherdata     - ["minutes",10] or ["hours",2] , index 0 is to choose whether you want to scrap data every hours or minutes and index 1 is to choose
                          every periodical amount of minute or hour
  4. gmailpass      - You need to enable 2-step verification of gmail and under 2-step verification there is a app password section.
                          From there password needs to be collected
  5. sender_email   - Enter the mail from where you want to send the stats data
  6. receiver_email - Enter the mail of the reciever
  7. subject        - Enter the subject of the mail
  8. body           - Enter message body here
```
## Deployment

To deploy this project run

```bash
  pyhon3 program.py
```


## Authors

- [@DeepProgram](https://github.com/DeepProgram)

