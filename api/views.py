from django.shortcuts import render
import json
from django.http import HttpResponse
from .models import Order, OrderedItem, FoodItem


def order(request):
	if request.method == "POST":
		json_str = request.body.decode(encoding = 'UTF-8')
		data = json.loads(json_str)
		#data is send as a set of arrays wrapped in a dict.
		#eg. data = {table_number: 2,order:[{food_code:2,quantity:3},{food_code:1,quantity:3},{food_code:3,quantity:1}]}
		table_number = data['table_number']
		ordered_food_items = data['order']
		current_order = Order.objects.create(table_number = table_number)
		for x in ordered_food_items:
			try:
				food_item = FoodItem.objects.get(code = int(x['food_code']))
				print("good food")
			except:
				#write a proper failure action
				return HttpResponse("Bad food code.")
			OrderedItem.objects.create(order = current_order,food_item = food_item,quantity = int(x['quantity']))
			# total_cost = int(food_item.price)*x['quantity']+total_cost
		return HttpResponse("OK! Order saved and is in pending.")
	else:
		return render(request,"test.html")

