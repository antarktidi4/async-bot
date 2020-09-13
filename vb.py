import requests, os, datetime, asyncio 
from vkwave.bots import SimpleLongPollBot, TaskManager, ClonesBot
from bs4 import BeautifulSoup as BS
from random import randint

s = 0
gId = 189021062
token = os.environ.get('BOT_TOKEN')

bot = SimpleLongPollBot(tokens = token, group_id = gId)


@bot.message_handler(lambda e: 'дней до школы' in e.object.object.message.text)
async def dateBeforeSc(event: bot.SimpleBotEvent):
	now = datetime.date.today()
	sept = datetime.date(2021, 9, 1)
	date = sept - now
	date = str(date)
	if date >= datetime.date(2020, 9, 1) and date <= datetime.date(2021, 6, 1):
		await event.answer('дней до конца учебного года: ' + datetime.date(2021, 6, 1) - now)
	else:
		await event.answer('дней до учебного года: ' + date[:3])


@bot.message_handler(lambda e: 'дата регистрации' in e.object.object.message.text)
async def DateOfReg(event: bot.SimpleBotEvent):
	fId = event.object.object.message.from_id
	r = requests.get('https://vk.com/foaf.php?id=' + str(fId))
	html = BS(r.content, 'html.parser')
	tag = html.findAll('ya:created')
	time = tag[0]['dc:date']
	await event.answer("твоя дата регистрации: " + str(time[:10]))


@bot.message_handler(lambda e: 'анекдот про замая' in e.object.object.message.text)
async def zamayAnec(event: bot.SimpleBotEvent):
	await event.answer('Как-то Бог и Дьявол пошли получать зарплату. Бог должен был получить апрельскую зарплату, а дьявол майскую. Но в бухгалтерии всё перепутали и за апрель получил дьявол, а ЗАМАЙ БОГ.')


@bot.message_handler(lambda e: 'смешной анекдот' in e.object.object.message.text)
async def holoc1(event: bot.SimpleBotEvent):
	global s
	await event.answer('что может быть страшнее, чем откусить от яблока и обнаружить в нем червя?')
	s = 1


@bot.message_handler(lambda e: 'что' in e.object.object.message.text and s == 1 or 'чё' in e.object.object.message.text and s == 1)
async def holoc2(event: bot.SimpleBotEvent):
	global s
	await event.answer('холокост')
	s = 0



@bot.message_handler(lambda e: 'анекдот' in e.object.object.message.text)
async def anec(event: bot.SimpleBotEvent):
	page = randint(1, 27)
	randanec = randint(0, 29)
	r = requests.get('https://4tob.ru/anekdots/tag/short/page' + str(page))
	html = BS(r.content, 'html.parser')
	text = html.select('.text')
	await event.answer(text[randanec].text)


@bot.message_handler(lambda e: 'помощь' in e.object.object.message.text or 'help' in e.object.object.message.text or 'привет' in e.object.object.message.text)
async def help(event: bot.SimpleBotEvent):
	await event.answer('что? может ты имел ввиду:\nанекдот \nанекдот про замая \nдата регистрации \nдней до школы \nсмешной анекдот \n  ')





bot.run_forever()
