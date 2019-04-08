from channels.generic.websocket import WebsocketConsumer 
import json
from asgiref.sync import async_to_sync
from .models import Order, OrderedItem, FoodItem, CustomUser

GROUP_NAME = 'reception'

class StaffConsumer(WebsocketConsumer):

    def send_response(self,response):
        print('sending response for',response['type'])
        async_to_sync (self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': 'staff_message',
                'message': response,
            }
        )

    def get_order(self,data):
        response = {'type':'getOrderResponse','state':data['state'], 'order': []}
        orders = Order.objects.filter(
            state = data['state']
        )
        for order in orders:
            order_items = OrderedItem.objects.filter(
                order = order
            )
            food_items = []
            for order_item in order_items:
                food_item = {
                    'food_name': order_item.food_item.name,
                    'food_price': order_item.food_item.price,
                    'qunatity': order_item.quantity,
                }
                food_items.append(food_item)
            response['order'].append({
                'id': order.id,
                'timestamp': str(order.timestamp),
                'table_number':order.table_number,
                'food_item': food_items
            })
        self.send_response(response)
    
    def set_order(self,data):
        pass

    def modify_order(self,data):
        pass
    
    def handle_error(self,data):
        pass

    def get_menu(self,data):
        pass
    

    def connect(self):
        async_to_sync (self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name
        )
        print("Connecting Incommnig")
        self.accept()
        print("Connection Accepted")
    
    def disconnect(self, close_code):
        async_to_sync (self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name
        )
    
    def receive(self, text_data):        
        data = json.loads(text_data)
        type = data['type']
        if type == "getOrder":
            self.get_order(data)
        elif type == "modifyOrder":
            self.modify_order(data)
        elif type == "setOrder":
            self.set_order()
        elif type == "getMenu":
            self.get_menu()
        else:
            self.handle_error()
    
    def staff_message(self,event):
        print("send staff")
        message = event['message']
        async_to_sync (self.send(text_data = json.dumps({
            'message':message
        })))

    #imporvise this code make it adapt
    def order(data):
        #data is send as a set of arrays wrapped in a dict.
        #eg. data = {type: "setOrder", table_number: 2,order:[{food_code:2,quantity:3},{food_code:1,quantity:3},{food_code:3,quantity:1}]}
        response = {}
        response['type'] = "order_response"
        table_number = data['table_number']
        ordered_food_items = data['order']
        current_order = Order.objects.create(table_number = table_number)
        for x in ordered_food_items:
            try:
                food_item = FoodItem.objects.get(code = int(x['food_code']))
                print("good food")
            except:
                #write a proper failure action
                response['']
            OrderedItem.objects.create(order = current_order,food_item = food_item,quantity = int(x['quantity']))
            # total_cost = int(food_item.price)*x['quantity']+total_cost
        