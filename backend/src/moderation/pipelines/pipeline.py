from typing import Callable, List, Any, Dict, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class PipelineStage:
    def __init__(self, func: Callable[[Any], Any], name: str):
        self.func = func
        self.name = name

    async def run(self, data: Any) -> Any:
        try:
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(data)
            else:
                result = self.func(data)
            return result
        except Exception as e:
            logger.error(f"Error in stage '{self.name}': {e}")
            raise

class Pipeline:
    def __init__(
        self,
        extractors: List[PipelineStage],
        preprocessors: Dict[int, List[PipelineStage]],
        runners: Dict[int, PipelineStage],
        postprocessors: Optional[Dict[int, PipelineStage]] = None,
    ):
        self.extractors = extractors
        self.preprocessors = preprocessors
        self.runners = runners
        self.postprocessors = postprocessors or dict()


    async def process(self, input_data: Any) -> Dict[int, Any]:
        data = input_data

        # Extraction
        for extractor in self.extractors:
            data = await extractor.run(data)

        # Preprocessing per runner index
        preprocessed_data = {}
        for idx, stages in self.preprocessors.items():
            temp_data = data
            for stage in stages:
                temp_data = await stage.run(temp_data)
            preprocessed_data[idx] = temp_data

        # Running processors
        results = {}
        for idx, runner in self.runners.items():
            input_for_runner = preprocessed_data.get(idx, data)
            results = await runner.run(input_for_runner)
            if idx in self.postprocessors:
                result = await self.postprocessors[idx].run(result)
            results[idx] = result

        return results
