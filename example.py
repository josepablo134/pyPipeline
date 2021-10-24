from Pipeline.Pipeline import PipelineHandler,Pipeline
from Pipeline.PipelineParallelHandler import PipelineParallelHandler

class ExampleOfTask(PipelineHandler):
	def handler(self,workspace : dict = None) -> dict:
		print( workspace )
		workspace["message"] = "Task %d was here" % self.pipeline_handler_id
		print("Hello, this is an example of task %d" % self.pipeline_handler_id)
def main():
	pipeline = Pipeline()

	parallel_handler = PipelineParallelHandler()
	parallel_handler.addHandler( ExampleOfTask() )
	parallel_handler.addHandler( ExampleOfTask() )
	parallel_handler.addHandler( ExampleOfTask() )

	pipeline.addHandler( parallel_handler )
	pipeline.addHandler( parallel_handler )
	pipeline.execute()

if __name__ == "__main__":
	try:
		main()
	except Exception as error:
		print(error)