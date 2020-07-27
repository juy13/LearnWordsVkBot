import os
import sys
import random as rnd
from time import sleep
import serial
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

messAPI = 3
bot = 0
users = []
#token = "31a185a685902949a4c938bc2abedc5b8823c51b7b727edd11d588701ee7973bd709c218c90f3ee65388f"
tokenhandle = open('token.txt', 'r', encoding="utf8")
token = tokenhandle.readline()

clear = lambda: os.system('cls')
quest = {}
transl = {}
base = {}
i = 0
j = 0

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def read_files():
	global i
	filehandle = open('words.txt', 'r', encoding="utf8")  
	filehandle2 = open('translate.txt', 'r', encoding="utf8") 
	i_l = 0
	while True:  
		# читаем одну строку
		line = filehandle.readline()
		line2 = filehandle2.readline()
		if not line:
			break
	
		quest[i_l] = line2
		transl[i_l] = line
		base[i_l] = 0
		i_l += 1
		#print(line)
	i = i_l
	#return filehandle, filehandle2


def change_lang(dict1, dict2):
	return dict2, dict1


def create_keyboard(code):
	keyboard = VkKeyboard(one_time=False)

	if code == 1:
		keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)
	if code == 2:
		keyboard.add_button('Ответ', color=VkKeyboardColor.POSITIVE)
		keyboard.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)
	if code == 3:
		keyboard.add_button('Далее', color=VkKeyboardColor.POSITIVE)
		keyboard.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)
	#keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
	#False Если клавиатура должна оставаться откртой после нажатия на кнопку
	#True если она должна закрваться
	
	#keyboard.add_button("Включить лампу", color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
	#keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
	
	#keyboard.add_line()#Обозначает добавление новой строки
	#keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)
	#
	#keyboard.add_line()
	#keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	#keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	
	return keyboard.get_keyboard()
	#Возвращает клавиатуру


#while True:
#	if j == i:
#		print('Вопросы закончились')
#		break
#	ans = str(input("Continue? y/n: "))
#	if ans == 'n':
#		break
#	if ans != 'y':
#		continue
#	if ans == 'y':
#		clear()
#	while True:
#		rand = rnd.randint(0, i - 1)
#		if base[rand] == 1:
#			continue
#		else:
#			base[rand] = 1
#			j += 1
#			break
#	print("Генерируем вопрос: ")
#	print(quest[rand])
#	ans2 = str(input("Show answer? y/n: "))
#	if ans == 'n':
#		continue
#	if ans == 'y':
#		print(transl[rand])
	

def ask_word(event):
	global j
	global i
	global quest
	global base
	rand = 0
	rand_id = random.randint(100000, 999999)
	if j == i:
		for k in base:
			k = 0
	while True:
		rand = rnd.randint(0, i - 1)
		if base[rand] == 1:
			continue
		else:
			base[rand] = 1
			j += 1
			break	
	vk.method('messages.send', {'user_id': event.user_id, 'message': quest[rand], 'keyboard' : create_keyboard(2), 'random_id': rand_id})
	
	return rand

def show_ans(place, event):
	global transl
	rand_id = random.randint(100000, 999999)
	vk.method('messages.send', {'user_id': event.user_id, 'message': transl[place], 'keyboard' : create_keyboard(3), 'random_id': rand_id})
	return 0

def check_word(place, word, event):
	global transl
	rand_id = random.randint(100000, 999999)
	
	word = word.lower()
	word_ans = transl[place].lower()[:-1]
	if(word == word_ans):
		vk.method('messages.send', {'user_id': event.user_id, 'message': "Верно", 'keyboard' : create_keyboard(3), 'random_id': rand_id})
	else:
		vk.method('messages.send', {'user_id': event.user_id, 'message': "Не верно, попробуйте еще раз", 'keyboard' : create_keyboard(2), 'random_id': rand_id})
	return 0

def stop_bot(event):
	rand_id = random.randint(100000, 999999)
	vk.method('messages.send', {'user_id': event.user_id, 'message': "Удачи Вам!", 'keyboard' : create_keyboard(1), 'random_id': rand_id})
	return 0

keyboard = create_keyboard(1)
first_fl = False
place_w = 0

for event in longpoll.listen():
	# Если пришло новое сообщение
	if event.type == VkEventType.MESSAGE_NEW:
		# Если оно имеет метку для меня( то есть бота)
		if event.to_me:
			# Сообщение от пользователя
			if first_fl is False:
				read_files()
				first_fl = True
			request = event.text
			print('User: ', event.user_id, 'Request: ', request)
			# Каменная логика ответа
			if request == "Начать" or request == "Далее" or  request == "Ответ" or request == "Стоп":
				if request == "Начать" or request == "Далее":
					place_w = ask_word(event)
				if request == "Ответ":
					show_ans(place_w, event)
				if request == "Стоп":
					stop_bot(event)
			else:
				check_word(place_w, request, event)
			
			#elif request == "пока":
			#    write_msg(event.user_id, "Пока((", event)
			#else:
			#    write_msg(event.user_id, "Не поняла вашего ответа...", event)