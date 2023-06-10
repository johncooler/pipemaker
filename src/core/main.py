import asyncio
import logging
import core.defaults as defaults


class Core:

    def __init__(self):
        self.logger = logging.basicConfig(level=logging.INFO)
        self.pipeline_queue = asyncio.PriorityQueue(
            maxsize=defaults.max_pipelines_queue_size
        )

    def add_pipeline(self, pipeline, priority=0):
        self.pipeline_queue.put(pipeline, priority=priority)
        
