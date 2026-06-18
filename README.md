# thuis-in-de-achterhoek-bot (Work in Progress)

## Description
A bot made with selenium that automates applying for housing via Thuis In De Achterhoek. (This project is still in the early stages)
## Status:
- Log in ✔️
- Check current amount of outgoing applications (max 3) ✔️
## TODO:
- If outgoing applications < 3:
    - Check listings for not yet applied housing ✔️
    - Submit Applications
- Add Error handling
- Sort listings by deadline
- Test program with different browsers

## Installation
- clone the repository, create a virtual environment and install dependencies:
```bash
git clone https://github.com/wnsnk/thuis-in-de-achterhoek-bot.git

cd thuis-in-de-achterhoek-bot

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
- Make sure you have installed Firefox (Future versions might support other browsers)
- add your own environment variables to a .env file (see .env.example)

- Run the app:
```bash
python main.py
```

## Tech Stack
- Python 3.14
- Selenium
