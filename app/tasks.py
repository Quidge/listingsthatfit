import os
from json import loads, dumps
from time import sleep

from celery import Celery, group, chain
from celery.utils.log import get_task_logger
#from .ebay_api_scripts import f_api
from ebaysdk.exception import ConnectionError, ConnectionResponseError
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.finding import Connection as Finding
from sqlalchemy.orm.exc import NoResultFound

from .model_builders import build_ebay_item_model
from .models import Item

celery = Celery(
	'{}'.format(__name__),
	broker='amqp://localhost',
	backend='amqp://')

logger = get_task_logger(__name__)

env_app_id = os.environ['EBAY_PRODUCTION_APP_ID']

s_api = Shopping(
	domain="open.api.ebay.com",
	appid=env_app_id,
	config_file=None,
	debug=False
)

f_api = Finding(
	domain="svcs.ebay.com",
	appid=env_app_id,
	config_file=None,
	debug=False)


@celery.task(bind=True)
def create_item_model(
	self,
	json_api_response,
	ebay_seller_id=None,
	with_measurements=False,
	with_sizes=False,
	affiliate_url=None):
	"""Celery task wrapper for model_builders.build_ebay_item_model."""

	api_response = loads(json_api_response)
	try:
		item = build_ebay_item_model(
			api_response,
			ebay_seller_id,
			with_measurements,
			with_sizes,
			affiliate_url)
	except BaseException:
		raise
		self.update_state(state='FAILURE')

	return str(item)


@celery.task
def lookup_single_item(ebay_item_id, html_description=False):
	"""Task to lookup up a single item. Asking for additional HTML
	description information is option. Returns JSON.
	"""
	#logger = lookup_single_item.get_logger()
	#logger.info = ("""
	#	Running GetSingleItem API for ebay id <{}>. Description requested: <{}>
	#	""".format(ebay_item_id, html_description))
	payload = {'ItemID': ebay_item_id}
	if html_description:
		# setattr(payload, 'IncludeSelector', 'Description')
		payload['IncludeSelector'] = 'Description'
	try:
		response = s_api.execute('GetSingleItem', payload)
	except ConnectionError:
		raise
	return response.json()


@celery.task(bind=True)
def get_seller_items(self, seller_id, items_category=None):
	"""Returns a JSON response of all items a <seller_id> has available. Uses
	the findItemsAdvanced ebay API. If items_category is provided, that will be
	used as an item filter in the payload.

	Returns
	-------
	response : json
	"""
	payload = {'itemFilter': {'name': 'Seller', 'value': seller_id}}
	if items_category:
		payload['categoryId'] = items_category
	try:
		response = f_api.execute('findItemsAdvanced', payload)
	except ConnectionError:
		raise

	r_dict = response.dict()
	if r_dict['ack'] != 'Success':
		raise ConnectionResponseError(r_dict['errorMessage'], response=response)

	return response.json()


@celery.task
def get_list_of_items_not_present_in_db(json_findingAPI_response):
	resp_obj = loads(json_findingAPI_response)
	list_of_item_ids = [i['itemId'] for i in resp_obj['searchResult']['item']]
	not_present = []
	for item_id in list_of_item_ids:
		try:
			Item.query.filter(Item.ebay_item_id == item_id).one()
		except NoResultFound:
			not_present.append(item_id)

	return dumps(not_present)


def add_new_items_from_seller_to_db(
	seller_ebay_id,
	items_category=None,
	html_description=False):
	"""Does not yet create Item models with results."""

	new_items = chain(
		get_seller_items.s(seller_ebay_id, items_category),
		get_list_of_items_not_present_in_db.s()
	)()  # Calling it turns to a lazy-load AsyncResult

	# Calling .get() on an AsynchResult waits for the actual value (but is sync and blocking)
	new_items_obj = loads(new_items.get())

	#result_to_model_workflow = chain(lookup_single_item.s(ebay_item_id), create_item_model.s(ebay_seller_id=seller_ebay_id))

	#new_items_detail = group(
	#	lookup_single_item.s(item_id, html_description) for item_id in new_items_obj)

	lookup_and_create_models_job = []
	for item_id in new_items_obj:
		job = chain(
			lookup_single_item.s(item_id, html_description=html_description),
			create_item_model.s(ebay_seller_id=seller_ebay_id, with_measurements=html_description))
		lookup_and_create_models_job.append(job)
	lookup_and_create_models_job = group(lookup_and_create_models_job)

	return lookup_and_create_models_job()


def lookup_item_and_add(ebay_item_id):
	workflow = chain(
		lookup_single_item.s(ebay_item_id, html_description=True),
		create_item_model.s(ebay_seller_id='balearic1', with_measurements=True)
	)
	return workflow()


@celery.task
def add(x, y):
	sleep(5)
	#self.update_state(state='SUCCESS')
	return x + y




