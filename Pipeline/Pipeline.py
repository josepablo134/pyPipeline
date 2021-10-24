class PipelineException(Exception):
	def __init__(self,message : str, code : int = None) -> None:
	    self.message = message
	    self.code = code

class PipelineHandler:
	def __init__(self) -> None:
		self.pipeline_handler_id = None

	def handler(self,workspace : dict = None) -> dict:
		"""
		Process the workspace and updates it. On error throws a PipelineException
		"""
		pass

	def execute(self, handler_id : int = None, workspace : dict = None) -> dict:
		self.pipeline_handler_id = handler_id
		return self.handler( workspace )

class Pipeline:
	def __init__(self, workspace : dict = None) -> None:
	    self.__clear_state()
	    if( workspace != None ):
		    self.workspace = workspace
	def __len__(self):
		return len( self.pipes )
	def addHandler(self,handler : PipelineHandler) -> None:
		self.pipes.append( handler )
	def execute(self, from_step : int = None, until_step : int = None):
		"""
		Executes all the pipeline handlers until finishes or someone throws an Exception.

		@params from_step: controls the beginning handler of the pipeline
		@params until_step: controls the final handler of the pipeline

		If from_step == until_step, the pipeline will execute only one handler, the "from_step" one.
		If from_step == until_step == None, the pipeline will trigger all handlers.
		"""
		from_index = 0
		until_index = len( self.pipes )
		if( from_step != None ):
			if( len( self.pipes ) <= from_step ):
				raise PipelineException( "Invalid from_step id", code=0x01 )
			else:
				from_index = from_step
		if( until_step != None ):
			if( len( self.pipes ) <= until_step ):
				raise PipelineException( "Invalid until_step id", code=0x01 )
			else:
				until_index = until_step
		if( from_index > until_index ):
			raise PipelineException( "until_step should be bigger than from_step", code=0x01 )

		try:
			index_counter = from_index
			for handler in self.pipes[from_index : until_index]:
				handler.execute( handler_id=index_counter, workspace=self.workspace )
				index_counter += 1
		except Exception as error:
			self.failed_step_id = index_counter
			raise error
	def __clear_state(self) -> None:
		self.workspace = {}
		self.pipes = []
		self.failed_step_id = 0
