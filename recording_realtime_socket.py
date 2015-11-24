import bpy
import time
from socket import *

time_start = time.time()

scn = bpy.context.scene
obj = bpy.context.active_object
obj_each = obj

class TcpClient:
	HOST='127.0.0.1'
	PORT=12345
	BUFSIZ=1024
	ADDR=(HOST, PORT)
	def __init__(self):
		self.client=socket(AF_INET, SOCK_STREAM)
		self.client.connect(self.ADDR)

	def SendMassage(self, message):
		data='Hello'
		data=message
		self.client.send(data.encode('utf8'))
		data=self.client.recv(self.BUFSIZ)
		print(data.decode('utf8'))
		self.client.close()

class ModalTimerOperator(bpy.types.Operator):
	"""Operator which runs its self from a timer"""
	bl_idname = "wm.modal_timer_operator"
	bl_label = "Modal Timer Operator"
	
	_timer = None
	
	def op_coor(self, obj_each):
		"Output coordinates of each object"
		print(obj_each.name, obj_each.location)
		DroneData = str(obj_each.name)	+'	'+ str(obj_each.location)
		client=TcpClient()
		client.SendMassage(DroneData)
		return 

	def modal(self, context, event):
		if event.type in {'ESC'}:
			self.cancel(context)
			return {'CANCELLED'}
			
		if event.type == 'TIMER':
			# change theme color, silly!
			print("Time: {0} secends".format(time.time()-time_start))
			for obj_each in scn.objects:
				self.op_coor(obj_each)

		
		return {'PASS_THROUGH'}
	
	def execute(self, context):
		wm = context.window_manager
		self._timer = wm.event_timer_add(0.1, context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
	def cancel(self, context):
		wm = context.window_manager
		wm.event_timer_remove(self._timer)
	
def register():
	bpy.utils.register_class(ModalTimerOperator)


def unregister():
	bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
	register()

	# test call
	bpy.ops.wm.modal_timer_operator()
