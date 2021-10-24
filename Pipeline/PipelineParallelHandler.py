import threading
from .Pipeline import PipelineHandler
from threading import Thread

class PipelineParallelHandler(PipelineHandler):
	def __init__(self) -> None:
		super().__init__()
		self.__clear_state()
	def addHandler(self,handler : PipelineHandler) -> None:
		self.handlers_list.append( handler )
	def handler(self, workspace: dict = None) -> dict:
		for handler in self.handlers_list:
			thread = Thread(target= handler.execute , args= (self.pipeline_handler_id , workspace) ) 
			self.tasks_list.append( thread )
			thread.start()
		at_least_one_alive = True
		while( at_least_one_alive ):
			at_least_one_alive = False
			for task in self.tasks_list:
				if( task.is_alive() ):
					at_least_one_alive = True
					break
		# Wait for all tasks to complete
		# and remove those from the list
		self.tasks_list.clear()
	def __clear_state(self):
		self.handlers_list = []
		self.tasks_list = []

