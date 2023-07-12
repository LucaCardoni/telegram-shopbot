# Shop Bot 🛍

ShopBot is a Telegram bot that allows users to purchase products easily and automatically through Telegram. It provides a convenient way for shop owners to manage their products and interact with customers.

This code uses the [EzTG](https://github.com/peppelg/EzTG) script to communicate with the Telegram API. It is a simple and intuitive library because it allows you to use the official methods of the Telegram API and work directly with raw data.
Therefore, I am very grateful to @peppelg, the creator of this library.

## Features

- Browse products and view their descriptions, prices, and media (images or videos).
- Confirm purchases.
- Shop owners can manage their products, including adding, editing, and removing items.
- Integration with a feeds channel to provide updates and announcements.
- Integration with Terms of Service (ToS) for users to review before making a purchase.

## ⬇️ Setup

Downoad the repo, or clone it with git

`git clone https://github.com/Rickionee/telegram-shopbot`

Update the owner, owner_id, tokenbot, feeds, and ToS variables in the script (row 4-9) with your own values.

## 🏃‍♂️ Usage
Run the `shopbot.py` script:

When you start the bot, if you are the owner, you will see the control panel to modify your shop. From there, you can use the buttons to fully manage the shop. You can add, remove, or modify your products, and you can add a name, description, image, video, and price.

However, if someone else starts the bot, they will have access to your contacts, shop, terms of service (ToS), and feedbacks. They can purchase items, but for security reasons, a message will be sent to the owner notifying them of the placed order. The message will contain all the necessary information to contact the customer to arrange payment and product delivery.

To access the user menu, even as the owner, simply type `/test`. This will allow you to see how users view the shop.

## CONTRIBUTING
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## LICENSE
This project is licensed under the [GPL-2.0 license](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).
