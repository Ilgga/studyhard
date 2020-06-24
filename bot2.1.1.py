import telebot
import openpyxl
import time

wb = openpyxl.load_workbook('1111.xlsx')
fout = open('out.txt','w')

predmets = wb.sheetnames
mid,count=0,0
a=dict()
t0 = time.time()

bot = telebot.TeleBot('1159532742:AAF40D9hcZ3OFDaC8DZ3nSjDj52hcvkOOTQ')

def out(mid,s):
    bot.send_message(mid,s)

def give_all(mid):
    global a
    column=2
    level = a[mid][1]
    sheet = wb[a[mid][0]]
    kniga = sheet[level + str(column)].value
    while kniga:
        out(mid,kniga)
        column += 1
        kniga = sheet[level + str(column)].value

def make_otshet(mid,t1):
    global t0
    with open('fout.txt','a') as f:
        f.write(time.ctime(time.time())+'\n')
        f.write("      посетило всего "+str(count)+ " человек")
        f.write('\n')
    print("poop")
    out(mid, "Внимание! Вы попали под очистку:). Начните сначала пожалуйста /start")
    for keys in a:
        out(keys, "Внимание! Вы попали под очистку:). Начните сначала пожалуйста /start")
    a.clear()
    t0 = time.time()

def proverka(mid):
    t1 = time.time()
    if (t1 - t0)/3600 > 6:
        make_otshet(mid,t1)
        return False
    return True

def give_choise(mid,mas):
    for pr in mas:
        out(mid,pr)

def add_people(mid):
    a[mid] = ['', '',{}]

def make_levels(mid):
    global a
    sheet = wb[a[mid][0]]
    for i in range(26):
        k = chr(i+ord('A')).upper()
        if sheet[k+'1'].value:
            a[mid][2][sheet[k+'1'].value.lower()]=k

@bot.message_handler(commands=['start'])
def start_message(message):
    global t0,a,count
    mid = message.chat.id
    count +=1
    if proverka(mid):
        add_people(mid)
        st = 'Привет, Я - бот, выдающий материалы для учебы. Давай начнем '+ message.from_user.first_name +'. Выбери предмет:'
        out(mid,st)
        give_choise(mid,predmets)

@bot.message_handler(commands=['cont'])
def cont_message(message):
    global t0, a, count
    mid = message.chat.id
    count += 1
    if proverka(mid):
        add_people(mid)
        out(mid, 'Итак, продолжаем. Выбери предмет:')
        give_choise(mid,predmets)

@bot.message_handler(content_types=['text'])
def start(message):
    global a
    mid = message.from_user.id
    if message.text.lower() in predmets:
        a[mid][0] = message.text.lower()
        s = 'Ты выбрал ' + a[mid][0] + '. Теперь выбери уровень подготовки:'
        out(mid, s)
        make_levels(mid)
        give_choise(mid,a[mid][2].keys())
        bot.register_next_step_handler(message, get_level);
    else:
        out(mid, 'введи правильно!');

def get_level(message):
    global a;
    mid = message.from_user.id
    if message.text.lower() in a[mid][2]:
        a[mid][1] = a[mid][2][message.text.lower()]
        s = 'Ты выбрал все, что нужно. Теперь держи курсы: '
        print(a)
        if a[mid][0]!='' and a[mid][1]!='':
            out(mid, s)
            give_all(mid)
            s = 'Ну вот '+ message.from_user.first_name +' у тебя есть курсы и материалы для подготовки. Твой результат в учебе зависит только от твоих действий, так что дерзай гранит науки:)'
            out(mid,s)
            out(mid,'напиши /cont чтобы снова взять материалы:)')
            a.pop(mid)
        else:
            out(mid, "что-то не так попробуй снова ")
            start_message(message)
    else:
        out(mid,'Введи правильно!')

bot.polling()


