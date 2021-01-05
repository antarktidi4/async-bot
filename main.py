from vkwave.bots import BaseEvent, PayloadFilter, Keyboard
from vkwave.bots import SimpleLongPollBot
from bs4 import BeautifulSoup as BS
import requests, os, datetime, json



gId = 189021062
token = os.environ.get('BOT_TOKEN')
bot = SimpleLongPollBot(tokens = token, group_id = gId)



@bot.message_handler(bot.text_contains_filter('start'))
async def kb_handler(event: BaseEvent):
	kb = Keyboard(one_time=False)

	kb.add_text_button(text='анекдот', payload={"anec": "default"})
	kb.add_text_button(text='анекдот про замая', payload={"anec": "zamai"})
	kb.add_row()
	kb.add_text_button(text='дней до школы', payload={"date": "school"})
	kb.add_text_button(text='дата регистрации', payload={"date": "reg"})

	await event.answer(message="[d34th1sn34r|боты дёшево куда угодно]", keyboard=kb.get_keyboard())



@bot.message_handler(PayloadFilter({"anec": "default"}))
async def anec(event: BaseEvent):
	rawcontent = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1').text
	await event.answer(json.loads(rawcontent, strict=False)['content'])


@bot.message_handler(PayloadFilter({"anec": "zamai"}))
async def zamayAnec(event: BaseEvent):
	await event.answer('Как-то Бог и Дьявол пошли получать зарплату. Бог должен был получить апрельскую зарплату, а дьявол майскую. Но в бухгалтерии всё перепутали и за апрель получил дьявол, а ЗАМАЙ БОГ.')


@bot.message_handler(PayloadFilter({"date": "reg"}))
async def DateOfReg(event: BaseEvent):
	r = requests.get(f'https://vk.com/foaf.php?id={event.object.object.message.from_id}')
	html = BS(r.content, 'html.parser')
	tag = html.findAll('ya:created')
	time = tag[0]['dc:date']
	await event.answer(f'твоя дата регистрации: {str(time)[:10]}')


@bot.message_handler(PayloadFilter({"date": "school"}))
async def dateBeforeSc(event: BaseEvent):
	now = datetime.date.today()
	sept = datetime.date(2020, 9, 1)
	june = datetime.date(2021, 6, 1)
	date = str(june - now)[:3] if now >= sept and now <= june else str(sept - now)[:3]
	await event.answer(f'дней до учебного года: {date}')



bot.run_forever()
