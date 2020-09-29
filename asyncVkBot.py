import requests, os, datetime, asyncio 
from vkwave.bots import SimpleLongPollBot
from bs4 import BeautifulSoup as BS
from random import randint

s = 0
gId = 189021062
token = os.environ.get('BOT_TOKEN')
bot = SimpleLongPollBot(tokens = token, group_id = gId)


@bot.message_handler(bot.text_contains_filter('дней до школы'))
async def dateBeforeSc(event: bot.SimpleBotEvent):
	now = datetime.date.today()
	sept = datetime.date(2021, 9, 1)
	date = sept - now
	if now >= datetime.date(2020, 9, 1) and now <= datetime.date(2021, 6, 1):
		await event.answer(f'дней до конца учебного года: {str(datetime.date(2021, 6, 1) - now)[:3]}')
	else:
		await event.answer(f'дней до учебного года: {str(date)[:3]}')


@bot.message_handler(bot.text_contains_filter('дата регистрации'))
async def DateOfReg(event: bot.SimpleBotEvent):
	r = requests.get(f'https://vk.com/foaf.php?id={event.object.object.message.from_id}')
	html = BS(r.content, 'html.parser')
	tag = html.findAll('ya:created')
	time = tag[0]['dc:date']
	await event.answer(f'твоя дата регистрации: {str(time)[:10]}')


@bot.message_handler(bot.text_contains_filter('анекдот про замая'))
async def zamayAnec(event: bot.SimpleBotEvent):
	await event.answer('Как-то Бог и Дьявол пошли получать зарплату. Бог должен был получить апрельскую зарплату, а дьявол майскую. Но в бухгалтерии всё перепутали и за апрель получил дьявол, а ЗАМАЙ БОГ.')


@bot.message_handler(bot.text_contains_filter('смешной анекдот'))
async def holoc1(event: bot.SimpleBotEvent):
	global s
	await event.answer('что может быть страшнее, чем откусить от яблока и обнаружить в нем червя?')
	s = 1


@bot.message_handler(bot.text_contains_filter(['что', 'чё', 'чо']))
async def holoc2(event: bot.SimpleBotEvent):
	global s
	await event.answer('холокост')
	s = 0


@bot.message_handler(bot.text_contains_filter('анекдот'))
async def anec(event: bot.SimpleBotEvent):
	r = requests.get(f'https://4tob.ru/anekdots/tag/short/page{randint(1, 27)}')
	html = BS(r.content, 'html.parser')
	text = html.select('.text')
	await event.answer(text[randint(0, 29)].text)


@bot.message_handler(bot.text_contains_filter(['калькулятор', 'calc']))
async def calc(event: bot.SimpleBotEvent):
	try:
		if len(str(eval(event.object.object.message.text[12:]))) < 1000:
			await event.answer(eval(event.object.object.message.text[12:]))
		else:
			await event.answer('в ответе более 1000 символов')
	except:
		await event.answer('eval except')


@bot.message_handler(bot.text_contains_filter(['помощь', 'help']))
async def help(event: bot.SimpleBotEvent):
	await event.answer('команды бота:\nанекдот \nанекдот про замая \nдата регистрации \nдней до школы \nсмешной анекдот \n  ')


bot.run_forever()
