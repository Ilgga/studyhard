
import requests
from tree import LoadTree
from users import users
import telebot
from telebot import types
import keys

API_TOKEN = keys.API_TOKEN
user = users()
def bob():


    hello_message=str('Привет,я - бот,сохраняю записи, заготвка для другого бота\n при '+
                      'нажатии /start создается запись, в которой вы можете создавать другие записи(файлы)\n'+
                      '#По некоторым пунктам:\n    *\'del запись\'-удаляет запись, в которой вы находитесь(не относится к root)\n'+
                      '    *\'корень\' - возрващает вас в root\n    *кнопка с названием записи открывает её\n'+
                      '    *\'saved\' внизу показывает сохранена ли запись\n'+
                      '    *если вы сохраните файл и выйдете, то ваши записи остаются\n'+
                      '!!все записи, не подходящие под условия запроса от бота игнорируются и удаляются без объяснения,'+
                      ' тк объяснения нужно сделать,а у меня скоро егэ:)!!\n'+
                      '    P.S.: to_do_list: добавить: удаление всей записи,завершение сеанса, значки в описание и ...переделать все ')

    main_keyboard = types.InlineKeyboardMarkup()
    main_keyboard.add(
        types.InlineKeyboardButton(text='доб запись', callback_data='add_dir'),
        types.InlineKeyboardButton(text='доб текст', callback_data='add_text'),
        types.InlineKeyboardButton(text='del запись', callback_data='del_dir'),
        types.InlineKeyboardButton(text='корень', callback_data='start'),
        types.InlineKeyboardButton(text='назад', callback_data='back'),
        types.InlineKeyboardButton(text='сохр', callback_data='save'),
        types.InlineKeyboardButton(text="загрузить", callback_data='download')
            )

    bot = telebot.TeleBot(API_TOKEN)
    bot_id = '1027087278'

    def give_mess(mid,text):
        return bot.send_message(chat_id=mid,text=text).message_id

    def update_text(mid):
        te = 'Ты в записи ' + user.tree(mid).name + ':\n'+user.tree(mid).text+'\n\n Saved: ' + str(user.saved(mid))
        if te!=user.text(mid):
            user.apd(mid,'text',te)
            bot.edit_message_text(text=te,chat_id=bot_id,message_id=user.msg(mid)[2])


    def update_main(mid):
        li = user.tree(mid).get_child()
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i in li:
            buttons.append(types.InlineKeyboardButton(text=li[i].name, callback_data=li[i].name))
        keyboard.add(*buttons)
        if user.msg(mid)[0]==0:
            user.msg(mid)[0]=1
            te = 'Ты в записи ' + user.tree(mid).name + ':\n'+user.tree(mid).text+'\n\n Saved: ' + str(user.saved(mid))
            user.msg(mid)[2] = bot.send_message(mid, text=te).message_id
            user.msg(mid)[1] = bot.send_message(mid,text='dirs', reply_markup=keyboard).message_id
        else:
            bot.edit_message_reply_markup(chat_id=bot_id, message_id=user.msg(mid)[1], reply_markup=keyboard)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        mid = message.chat.id
        if message.text == '/start':
            if not(mid in user.users.keys()):
                user.add_user(mid)
            give_mess(mid,hello_message)
            give_mess(mid, 'приветствую тебя, ' + str(message.from_user.username))
            update_main(mid)
            bot.send_message(mid,text='commands:', reply_markup=main_keyboard)
        else:
            bot.send_message(mid,'Напиши /start, чтобы заработало')
        bot.delete_message(message.chat.id,message.message_id)

    @bot.callback_query_handler(func= lambda call:True)
    def callback(call):
        mid = call.message.chat.id
        if call.data in user.tree(mid).get_child():
            user.upd_tree(mid,user.tree(mid).go_to(call.data))
            update_text(mid)
            if user.tree(mid).get_child().keys() != user.tree(mid).get_parent().get_child().keys():
                update_main(mid)

        elif call.data == 'start' and user.tree(mid).get_parent:
            tr = user.tree(mid).get_child().keys()
            user.upd_tree(mid,user.root(mid))
            update_text(mid)
            if tr != user.root(mid).get_child().keys():
                update_main(mid)
        elif call.data == 'add_dir':
            user.apd(mid,'adding',True)
            user.msg(mid)[3] = give_mess(mid, 'Введите имя записи, ограничения на ее неё: не должно называться как один местный файл')

        elif call.data == 'add_text':
            user.apd(mid,'add_text',True)
            user.msg(mid)[3] = give_mess(mid, 'Введите описание записи:')

        elif call.data == 'back':
            if user.tree(mid).get_parent():
                name = user.tree(mid).name
                user.upd_tree(mid,user.tree(mid).go_back())
                update_text(mid)
                if user.tree(mid).get_child().keys()!=user.tree(mid).go_to(name).get_child().keys():
                    update_main(mid)

        elif call.data == 'save':
            user.apd(mid,'saved',True)
            user.tree(mid).save_tree(str(mid)+'-'+user.tree(mid).name+'.txt')
            doc = open(str(mid)+'-'+user.tree(mid).name+'.txt','rb')
            give_mess(mid,"Держи файл, скормив его мне люди смогут прогрузить дерево")
            bot.send_document(mid,doc)
            doc.close()
            user.msg(mid)[0] = 0
            update_main(mid)
            bot.send_message(mid,text='commands:', reply_markup=main_keyboard)

        elif call.data == 'del_dir' and user.tree(mid).get_parent:
            user.apd(mid,'dell_dir',True)
            user.msg(mid)[3] = give_mess(mid, 'Уверен, что хочешь'+
                                              ' удалить папку и её содержимое? \n Если да, то напиши \'Yes\':)')
        elif call.data == 'download':
            user.msg(mid)[3] = give_mess(mid,"Отправь сделанный мной файл.При ошибке переделки файла он не будет добавлен")

        else:
            bot.send_message(mid,'Напиши /start, чтобы заработало')

    @bot.message_handler(content_types=['text'])
    def mes(message):
        mid = message.chat.id
        if mid in user.users:
            mes = message.text
            if user.adding(mid):
                if not(mes in user.tree(mid).get_child()):
                    user.tree(mid).add(mes)
                    if user.saved(mid):
                        user.apd(mid,'saved',False)
                        update_text(mid)
                    update_main(mid)
                    bot.delete_message(bot_id, user.msg(mid)[3])
                    user.apd(mid,'adding',False)
                else:
                    bot.delete_message(bot_id,user.msg(mid)[3])
                    user.msg(mid)[3] = give_mess(mid,'Введи коррректное название файла!')
            if user.add_text(mid):
                if user.tree(mid).text!=message.text:
                    user.tree(mid).text=message.text
                    update_text(mid)
                user.apd(mid,'add_text',False)
                bot.delete_message(bot_id,user.msg(mid)[3])
            if user.dell_dir(mid):
                if not(user.tree(mid).get_parent()==None):
                    name = user.tree(mid).name
                    user.upd_tree(mid,user.tree(mid).get_parent())
                    user.tree(mid).delete(name)
                    update_text(mid)
                    update_main(mid)
                user.apd(mid,'dell_dir',False)
                bot.delete_message(bot_id,user.msg(mid)[3])

        bot.delete_message(message.chat.id, message.message_id)

    @bot.message_handler(content_types=['document'])
    def get_dok(dok):
        mid = dok.chat.id
        if dok.forward_from:
            try:
                file_info = bot.get_file(dok.document.file_id)
                file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
                a = LoadTree(file.text,'tr').tree
                a.put_parent(user.tree(mid))
                user.tree(mid).put_child(a)
                bot.delete_message(bot_id, user.msg(mid)[3])
                update_main(mid)
            except:
                user.msg(mid)[3] = give_mess(mid,"кажется файл поврежден")
        else:
            give_mess(mid,'отправь мой файл')
        bot.delete_message(mid, dok.message_id)

    bot.polling(none_stop=True)

def start():
    try:
        bob()
    except:
        print('СЛОМАЛСЯ')
        start()

start()