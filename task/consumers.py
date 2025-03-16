import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TaskTable
from .serializers import TaskSerializer
from channels.db import database_sync_to_async


class TaskConsumer(AsyncWebsocketConsumer):
    
    
    async def connect(self):    
        
       
        self.room_name = 'tasks'
        self.room_group_name = f'task_{self.room_name}'
        # print(self.user)
        # if self.user.is_authenticated:
        #     print(self.user)
            

            # Add the user to the group
        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        await self.accept()
        # else:
        #     await self.close()
        
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        
    # Receive message from WebSocket (This can be for task updates)  
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        
        action =  text_data_json['action']
        task_id = text_data_json.get('task_id',None)
        
        if action =="update" and task_id:
            # Use sync_to_async for ORM calls
            task = await self.get_task(task_id)
            
            task_serializer =  TaskSerializer(task)
            
             # Ensure we await group_send properly
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'task_update',
                'task': task_serializer.data
            }
        )
            
        if action =='delete' and task_id:
            
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'task_delete',
                'task_id': task_id
            }
        )
            
            
            
    async def task_update(self,event):
        task=event['task']
        
        # print('updated task chanmel')
        
        await self.send(
            text_data=json.dumps(
                {
                    'action':'update',
                    'task':task
                }
            )
        )
        
    async def task_create(self,event):
        task=event['task']
        
 
        
        await self.send(
            text_data=json.dumps(
                {
                    'action':'created',
                    'task':task
                }
            )
        )
        
    async def task_delete(self, event):
        task_id= event['task_id']
        
        await self.send(text_data=json.dumps(
            {
                'action':'deleted',
                'task_id':task_id,
                
            }
        ))
        
    @database_sync_to_async
    def get_task(self, task_id):
        return TaskTable.objects.get(id=task_id)