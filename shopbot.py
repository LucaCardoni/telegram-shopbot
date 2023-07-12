import EzTG
import json

owner = "" # Owner's telegram username (without @)
owner_id = 0 # Owner's telegram id
tokenbot = "" # bot's token
feeds = "https://t.me/" # feeds channel link
ToS = "asofoe" # telegra.ph link to your ToS
currency = "€" # currency that you want your price to be in

with open('products.json') as json_products:
    products = json.load(json_products)

products = dict(products)
new_name = ''
new_description = ''
new_price = ''
atchtype = ""
file_id = ""

def callback(bot, update):

    if 'message' in update:
        global new_name, new_description, new_price, text, atchtype, file_id, text_message_id
        text_message_id = update['message']['message_id']
        user_id = update['message']['from']['id']
        chat_id = update['message']['chat']['id']
        username = update['message']['from']['username']
        text = ""
        try:
            text = update['message']['caption']
        except:
            pass
        if 'text' in update['message']:
            atchtype = ""
            text = update['message']['text']
        elif 'photo' in update['message']:
            atchtype = "img"
            file_id = update['message']['photo'][-1]['file_id']
        elif 'video' in update['message']:
            atchtype = "vid"
            file_id = update['message']['video']['file_id']
        else:
            atchtype = "other"

        if text == '/start' and chat_id != owner_id or text == '/test' and chat_id == owner_id:
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('💬Contact Me', f"http://t.me/{owner}")
            keyboard.add('🛍Shop', 'shop')
            keyboard.newLine()
            keyboard.add('⚠️ToS', f'{ToS}')
            keyboard.add('🧾Feeds', f'{feeds}')
            bot.sendMessage(chat_id=chat_id, text=f"<i>Hello @{username}</i> [<code>{user_id}</code>] 👋\n<b>Welcome to @{owner}'s shopbot!</b>\n\n<b>Here you can purchase my products easily and automatically</b>\n\nNavigate with the buttons below🎛", reply_markup=keyboard, parse_mode='HTML')

        if text == '/start' and chat_id == owner_id:
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Edit shop🛍', 'edit-shop')
            keyboard.newLine()
            bot.sendMessage(chat_id=chat_id, text=f"<i>Hello @{username}</i> [<code>{user_id}</code>] 👋\n<b>Welcome to your shopbot control panel!</b>\n\n<b>Here you can add, remove, or modify your products and information.</b>\n\nNavigate with the buttons below🎛", reply_markup=keyboard, parse_mode='HTML')

    if 'callback_query' in update:
        cb_message_id = update['callback_query']['message']['message_id']
        user_id = update['callback_query']['from']['id']
        chat_id = update['callback_query']['message']['chat']['id']
        username = update['callback_query']['from']['username']
        cb_id = update['callback_query']['id']
        cb_data = update['callback_query']['data']

        if cb_data == 'edit-shop':
            keyboard = EzTG.Keyboard('inline')
            for product in list(products.keys()):
                keyboard.add(f'{product}', f'edititem-{product}')
                keyboard.newLine()
            keyboard.add('➕Add item', 'additem')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'menu-admin')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.SendMessage(chat_id=chat_id, text='which item do you want to edit?', reply_markup=keyboard)
            except:
                pass

        if cb_data == 'additem':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm', f'confirmadd')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text= f'Send a message formatted like this then confirm, if you write it in any other way it wont work:\n\nNAME: <i>product name</i>\nDESCRIPTION: <i>product description</i>\nPRICE: <i>product price(just number)</i>', reply_markup=keyboard, parse_mode='HTML')
            except:
                pass

        if cb_data == 'confirmadd':
            try:
                name = str(text).split("NAME: ")[1].split("\nDESCRIPTION")[0]
                description = str(text).split("DESCRIPTION: ")[1].split("\nPRICE")[0]
                price = str(text).split("PRICE: ")[1]
                if atchtype == "":
                    products[name] = {"description" : description, "price": price, "atchtype": atchtype}
                    bot.answerCallbackQuery(callback_query_id=cb_id, text='New item added to the shop!✅', show_alert=True)
                    done = True
                elif atchtype == "img" or atchtype == "vid":
                    products[name] = {"description" : description, "price" : price, "atchtype" : atchtype, "file_id" : file_id}
                    bot.answerCallbackQuery(callback_query_id=cb_id, text='New item added to the shop!✅', show_alert=True)
                    done = True
                else:
                    bot.answerCallbackQuery(callback_query_id=cb_id, text='Error: file not supported, send a photo or a video with the text as caption', show_alert=True)
                    done = False

                bot.deleteMessage(chat_id=chat_id, message_id=text_message_id)

                if done == True:
                    keyboard = EzTG.Keyboard('inline')
                    keyboard.add('🔙Main menu', 'menu-admin')
                    with open("products.json", "w") as f:
                        json.dump(products, f)
                    try:
                        bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='New item added to the shop!✅', reply_markup=keyboard)
                    except:
                        pass
            except:
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: you may have formatted the message incorrectly, check and resend it, do not edit it", show_alert=True)

        if cb_data[:9] == 'edititem-':
            product = cb_data[9:]
            description = products[product]['description']
            price = products[product]['price']
            atchtype = products[product]['atchtype']
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Edit name', f'editname-{product}')
            keyboard.add('Edit description', f'editdesc-{product}')
            keyboard.newLine()
            keyboard.add('Edit price', f'editprice-{product}')
            keyboard.add('Edit media', f'editmedia-{product}')
            keyboard.newLine()
            keyboard.add('❌Remove item❌', f'rmitem-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            if atchtype == "":

                try:
                    bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text=f'✏️Editor mode\n\n<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass
            elif atchtype == "img":
                file_id = products[product]['file_id']
                try:
                    bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                    bot.sendPhoto(chat_id=chat_id, photo=file_id, caption=f'✏️Editor mode\n\n<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass
            elif atchtype == "vid":
                file_id = products[product]['file_id']
                try:
                    bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                    bot.sendVideo(chat_id=chat_id, video=file_id, caption=f'✏️Editor mode\n\n<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass

        if cb_data[:9] == 'editname-':
            product = cb_data[9:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm edit', f'confirmeditname-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text=f"Send the new name and confirm", reply_markup=keyboard)
            except:
                pass

        if cb_data[:16] == 'confirmeditname-':
            product = cb_data[16:]
            try:
                new_name = text
                products[new_name] = products[product]
                del products[product]
                keyboard = EzTG.Keyboard('inline')
                for product in list(products.keys()):
                    keyboard.add(f'{product}', f'edititem-{product}')
                    keyboard.newLine()
                keyboard.add('➕Add item', 'additem')
                keyboard.newLine()
                keyboard.add('🔙 Go back', 'menu-admin')

                bot.deleteMessage(chat_id=chat_id, message_id=text_message_id)

                try:
                    bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='which item do you want to edit?', reply_markup=keyboard)
                except:
                    pass
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"name changed in '{new_name}'! ✅", show_alert=True)
                with open("products.json", "w") as f:
                    json.dump(products, f)
            except:
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: no new message found, write the new name and try again.", show_alert=True)

        if cb_data[:9] == 'editdesc-':
            product = cb_data[9:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm edit', f'confirmeditdesc-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text=f"Send the new description and confirm", reply_markup=keyboard)
            except:
                pass

        if cb_data[:16] == 'confirmeditdesc-':
            product = cb_data[16:]
            try:
                new_description = text
                products[product]['description'] = new_description
                keyboard = EzTG.Keyboard('inline')
                for product in list(products.keys()):
                    keyboard.add(f'{product}', f'edititem-{product}')
                    keyboard.newLine()
                keyboard.add('➕Add item', 'additem')
                keyboard.newLine()
                keyboard.add('🔙 Go back', 'menu-admin')

                bot.deleteMessage(chat_id=chat_id, message_id=text_message_id)

                try:
                    bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='which item do you want to edit?', reply_markup=keyboard)
                except:
                    pass
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"description changed! ✅", show_alert=True)
                with open("products.json", "w") as f:
                    json.dump(products, f)
            except:
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: no new message found, write the new name and try again.", show_alert=True)

        if cb_data[:10] == 'editprice-':
            product = cb_data[10:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm edit', f'confirmeditprice-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text=f"Send the new price and confirm", reply_markup=keyboard)
            except:
                pass

        if cb_data[:17] == 'confirmeditprice-':
            product = cb_data[17:]
            try:
                new_price = text
                products[product]['price'] = new_price
                keyboard = EzTG.Keyboard('inline')
                for product in list(products.keys()):
                    keyboard.add(f'{product}', f'edititem-{product}')
                    keyboard.newLine()
                keyboard.add('➕Add item', 'additem')
                keyboard.newLine()
                keyboard.add('🔙 Go back', 'menu-admin')

                bot.deleteMessage(chat_id=chat_id, message_id=text_message_id)

                try:
                    bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='which item do you want to edit?', reply_markup=keyboard)
                except:
                    pass
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"price changed in '{new_price}'! ✅", show_alert=True)
                with open("products.json", "w") as f:
                    json.dump(products, f)
            except:
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: no new message found, write the new name and try again.", show_alert=True)

        if cb_data[:10] == 'editmedia-':
            product = cb_data[10:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm edit', f'confirmeditmedia-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text=f"Send the new media and confirm", reply_markup=keyboard)
            except:
                pass

        if cb_data[:17] == 'confirmeditmedia-':
            product = cb_data[17:]
            try:
                if atchtype == 'img' or atchtype == 'vid':
                    new_atchtype = atchtype
                    new_file_id = file_id
                    products[product]['atchtype'] = new_atchtype
                    products[product]['file_id'] = new_file_id
                    done = True
                else:
                    bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: file not supported, send a photo or a video with the text as caption", show_alert=True)
                    done = False

                bot.deleteMessage(chat_id=chat_id, message_id=text_message_id)

                if done == True:
                    keyboard = EzTG.Keyboard('inline')
                    for product in list(products.keys()):
                        keyboard.add(f'{product}', f'edititem-{product}')
                        keyboard.newLine()
                    keyboard.add('➕Add item', 'additem')
                    keyboard.newLine()
                    keyboard.add('🔙 Go back', 'menu-admin')
                    try:
                        bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='which item do you want to edit?', reply_markup=keyboard)
                    except:
                        pass
                    bot.answerCallbackQuery(callback_query_id=cb_id, text=f"media changed! ✅", show_alert=True)
                    with open("products.json", "w") as f:
                        json.dump(products, f)
            except:
                bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Error: no new message found, send the new media and try again.", show_alert=True)

        if cb_data[:7] == 'rmitem-':
            product = cb_data[7:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅Confirm', f'confirmrm-{product}')
            keyboard.newLine()
            keyboard.add('🔙 Go back', 'edit-shop')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text=f"Are you 100% sure you want to remove this item from your shop?", reply_markup=keyboard)
            except:
                pass

        if cb_data[:10] == 'confirmrm-':
            product = cb_data[10:]
            del products[product]
            bot.answerCallbackQuery(callback_query_id=cb_id, text=f"Item '{product}' removed from the shop✅", show_alert=True)
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('🔙Main menu', 'menu-admin')
            with open("products.json", "w") as f:
                json.dump(products, f)
            try:
                bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text= f"Item '{product}' removed from the shop✅", reply_markup=keyboard)
            except:
                pass

        if cb_data == 'shop':
            keyboard = EzTG.Keyboard('inline')
            for product in list(products.keys()):
                keyboard.add(f'{product}', f'info-{product}')
                keyboard.newLine()
            keyboard.add('🔙 Go back', 'menu')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text='what do you want to buy?', reply_markup=keyboard)
            except:
                pass

        if cb_data[:5] == 'info-':
            product = cb_data[5:]
            description = products[product]['description']
            price = products[product]['price']
            atchtype = products[product]['atchtype']
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('💸 Buy', f'buy-{product}')
            keyboard.newLine()
            if atchtype == "":
                keyboard.add('🔙 Go back', 'shop')
                try:
                    bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text=f'<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass
            elif atchtype == "img":
                keyboard.add('🔙 Go back', 'shop')
                file_id = products[product]['file_id']
                try:
                    bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                    bot.sendPhoto(chat_id=chat_id, photo=file_id, caption=f'<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass
            elif atchtype == "vid":
                keyboard.add('🔙 Go back', 'shop')
                file_id = products[product]['file_id']
                try:
                    bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                    bot.sendVideo(chat_id=chat_id, video=file_id, caption=f'<b>{product}</b>\n\n{description}\n\n<b>Price:</b> <i>{currency}{price}</i>', reply_markup=keyboard, parse_mode='HTML')
                except:
                    pass

        if cb_data[:4] == 'buy-':
            product = cb_data[4:]
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('✅ Confirm purchase ', f'confirm-{product}')
            keyboard.newLine()
            keyboard.add('❌ Cancel', 'menu')
            try:
                bot.deleteMessage(chat_id=chat_id, message_id=cb_message_id)
                bot.sendMessage(chat_id=chat_id, text='Are you completely sure?', reply_markup=keyboard, parse_mode='HTML')
            except:
                pass

        if cb_data[:8] == 'confirm-':
            product = cb_data[8:]
            bot.sendMessage(chat_id=owner_id, text=f"@{username} [<code>{chat_id}</code>]\nhas just confirmed the purchase of: <b>{product}</b>", parse_mode='HTML')
            bot.answerCallbackQuery(callback_query_id=cb_id, text='Purchase confirmed! ✅', show_alert=True)
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('🔙Main menu', 'menu')
            try:
                bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text='Purchase confirmed! ✅', reply_markup=keyboard)
            except:
                pass

        if cb_data == 'menu':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('💬Contattami', f"http://t.me/{owner}")
            keyboard.add('🛍Shop', 'shop')
            keyboard.newLine()
            keyboard.add('⚠️ToS', f'{ToS}')
            keyboard.add('🧾Feed', f'{feeds}')
            try:
                bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text=f"<i>Hello @{username}</i> [<code>{user_id}</code>] 👋\n<b>Welcome to @{owner}'s shopbot!</b>\n\n<b>Here you can purchase my products easily and automatically</b>\n\nNavigate with the buttons below🎛", reply_markup=keyboard, parse_mode='HTML')
            except:
                pass

        if cb_data == 'menu-admin':
            keyboard = EzTG.Keyboard('inline')
            keyboard.add('Edit shop🛍', 'edit-shop')
            try:
                bot.editMessageText(chat_id=chat_id, message_id=cb_message_id, text=f"<i>Hello @{username}</i> [<code>{user_id}</code>] 👋\n<b>Welcome to your shopbot control panel!</b>\n\n<b>Here you can add, remove, or modify your products and information.</b>\n\nNavigate with the buttons below🎛", reply_markup=keyboard, parse_mode='HTML')
            except:
                pass

bot = EzTG.EzTG(token=tokenbot, callback=callback)