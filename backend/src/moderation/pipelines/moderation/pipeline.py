import asyncio
import logging
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional

from moderation.pipelines.moderation.postprocessors import ReturnSame

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


def fill_empty_stages(
    runners: Dict[int, PipelineStage], stage: Dict[int, PipelineStage] | None
) -> Dict[int, List[PipelineStage]]:
    if stage is None:
        stage = {}
    for index in runners:
        if index not in stage:
            stage[index] = [PipelineStage(ReturnSame(), "return_same")]
    return stage


async def yield_results_from_runner(runner: PipelineStage, input_for_runner: List[Any]) -> AsyncGenerator:
    for item in input_for_runner:
        result = await runner.run(item)
        if result is not None:
            yield result
        else:
            logger.error(f"Error in runner '{runner.name}' at index {runner.index}: {item}")


class Pipeline:
    def __init__(
        self,
        extractors: List[PipelineStage],
        preprocessors: Dict[int, List[PipelineStage]],
        runners: Dict[int, PipelineStage],
        postprocessors: Optional[Dict[int, List[PipelineStage]]] = None,
        aggregator: Optional[Dict[int, PipelineStage]] = None,
    ):
        self.extractors = extractors
        self.preprocessors = preprocessors
        self.runners = runners
        self.postprocessors = fill_empty_stages(self.runners, postprocessors)
        self.aggregator = aggregator or {}

    async def process(self, input_data: Any) -> list:
        logger.info(f"Starting pipeline processing with input data: {input_data}")
        data = await self.extract(input_data)
        preprocessed_data = await self.preprocess(data)
        results_total = []
        for idx, runner in self.runners.items():
            logger.info(f"Running runner: {runner.name} for index {idx}")
            input_for_runner = preprocessed_data.get(idx, data)
            if not isinstance(input_for_runner, list):
                input_for_runner = [input_for_runner]
            try:
                results = []
                async for result in yield_results_from_runner(runner, input_for_runner):
                    postprocessor_input = result
                    for postprocessor in self.postprocessors[idx]:
                         postprocessor_input = await postprocessor.run(postprocessor_input)
                    results.append(postprocessor_input)
                aggregator_input = results
                if idx in self.aggregator:
                    aggregator_input = await self.aggregator[idx].run(aggregator_input)
                if isinstance(aggregator_input, list):
                    results_total.extend(aggregator_input)
                else:
                    results_total.append(aggregator_input)

            except Exception as e:
                logger.error(f"Error in runner '{runner.name}' at index {idx}: {e}", exc_info=True)
                raise

        logger.info(f"Pipeline processing completed with results: {results_total}")
        return [result for result in results_total if result is not None]

    async def extract(self, data: Any) -> Any:
        logger.info(f"Starting extract for data: {data}")
        for extractor in self.extractors:
            logger.info(f"Running extractor: {extractor.name}")
            data = await extractor.run(data)
        return data

    async def preprocess(self, data: Any) -> Dict[int, Any]:
        logger.info(f"Starting preprocess for data: {data}")
        preprocessed_data = {}
        for idx, stages in self.preprocessors.items():
            logger.info(f"Running preprocessors for runner index {idx}")
            temp_data = data
            for stage in stages:
                logger.info(f"Running preprocessor: {stage.name}")
                temp_data = await stage.run(temp_data)
            preprocessed_data[idx] = temp_data
            logger.info(f"Preprocessed data for index {idx}: {temp_data}")
        return preprocessed_data
