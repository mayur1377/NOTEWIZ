# cn_mini
# Telegram Bot

This is a Telegram bot implemented using the Telegram API and the python-telegram-bot library. The bot allows users to access PDF files based on their branch, semester, subject, and unit.

## Setup

1. Clone the repository.
2. Install the required dependencies:



## Usage

1. Start the bot by sending the `/start` command.
2. The bot will prompt you to enter your name. Enter your name and press Enter.
3. If you enter "Mayur" as the name, the bot will enter teacher mode and ask you to upload a PDF file. Upload a PDF file to save it on the server. (gotta make changes in this)
4. If you enter any other name, the bot will ask you to enter your USN (University Seat Number). Enter your USN in the specified format (e.g., `4SI18CS001`) and press Enter.
5. The bot will validate the USN and ask you to select a semester from the available options.
6. After selecting the semester, the bot will ask you to select a subject from the available options.
7. Once you select a subject, the bot will ask you to select a unit from the available options.
8. After selecting the unit, the bot will provide you with the corresponding PDF file if it exists on the server.
9. If the PDF file is found, the bot will send the file to you. Otherwise, it will notify you that the PDF file was not found.
10. You can continue selecting subjects and units or start a new search by selecting a different semester.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
