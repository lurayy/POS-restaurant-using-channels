from channels.generic.websocket import WebsocketConsumer 
import json
from asgiref.sync import async_to_sync
from .models import Order, OrderedItem, FoodItem, CustomUser

GROUP_NAME = 'reception'

class StaffConsumer(WebsocketConsumer):

    def send_response(self,response):
        print('send_response')
        print(response)
        async_to_sync (self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': 'staff_message',
                'message': response,
            }
        )

    def get_order(self,data):
        response = {'type':'get_order_response','state':data['state'], 'order': []}
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
    
    def modify_order(self,data):
        pass

    def connect(self):
        async_to_sync (self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name
        )
        print("Connecting Incommnig")
        self.accept()
        print("Connection Accepted")
        inital_data = {
            'type': 'get_order',
            'from':0,
            'to':10,
            'state':'PENDING'
        } 
        self.get_order(inital_data)
    
    def disconnect(self, close_code):
        async_to_sync (self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name
        )
    
    def receive(self, text_data):        
        data = json.loads(text_data)
        type = data['type']
        if type == "get_order":
            self.get_order(data)
        elif type == "modify_order":
            self.modify_order(data)
        else:
            print(text_data)
    
    def staff_message(self,event):
        print("send staff")
        message = event['message']
        async_to_sync (self.send(text_data = json.dumps({
            'message':message
        })))
