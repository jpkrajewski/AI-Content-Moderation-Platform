import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class PipelineStage:
    def __init__(self, func: Callable[[Any], Any], name: str):
        self.func = func
        self.name = name

    async def run(self, data: Any) -> Any:
        logger.info(f"Starting stage '{self.name}' with data: {data}")
        try:
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(data)
            else:
                result = self.func(data)
            logger.info(f"Completed stage '{self.name}' with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in stage '{self.name}': {e}", exc_info=True)
            raise


class Pipeline:
    def __init__(
        self,
        extractors: List[PipelineStage],
        preprocessors: Dict[int, List[PipelineStage]],
        runners: Dict[int, PipelineStage],
        postprocessors: Optional[Dict[int, List[PipelineStage]]] = None,
    ):
        self.extractors = extractors
        self.preprocessors = preprocessors
        self.runners = runners
        self.postprocessors = postprocessors or defaultdict(list)

    async def process(self, input_data: Any) -> list:
        logger.info(f"Starting pipeline processing with input data: {input_data}")
        data = input_data

        # Extraction
        for extractor in self.extractors:
            logger.info(f"Running extractor: {extractor.name}")
            data = await extractor.run(data)

        # Preprocessing per runner index
        preprocessed_data = {}
        for idx, stages in self.preprocessors.items():
            logger.info(f"Running preprocessors for runner index {idx}")
            temp_data = data
            for stage in stages:
                logger.info(f"Running preprocessor: {stage.name}")
                temp_data = await stage.run(temp_data)
            preprocessed_data[idx] = temp_data
            logger.info(f"Preprocessed data for index {idx}: {temp_data}")

        results = []
        for idx, runner in self.runners.items():
            logger.info(f"Running runner: {runner.name} for index {idx}")
            input_for_runner = preprocessed_data.get(idx, data)

            # Normalize input to list if it isn't already
            if not isinstance(input_for_runner, list):
                input_for_runner = [input_for_runner]

            try:
                # Run runner on each item sequentially and collect results
                result = []
                for item in input_for_runner:
                    r = await runner.run(item)
                    result.append(r)

                logger.info(f"Runner '{runner.name}' completed with result: {result}")

                # Run postprocessors if any
                if idx in self.postprocessors:
                    logger.info(f"Running postprocessor(s) for index {idx}")
                    for i, res in enumerate(result):
                        for postprocessor in self.postprocessors[idx]:
                            res = await postprocessor.run(res)
                        result[i] = res
                    logger.info(f"Postprocessor(s) for index {idx} completed with result: {result}")

                results.extend(result)  # always extend because result is list

            except Exception as e:
                logger.error(f"Error in runner '{runner.name}' at index {idx}: {e}", exc_info=True)
                raise

        logger.info(f"Pipeline processing completed with results: {results}")
        return results

