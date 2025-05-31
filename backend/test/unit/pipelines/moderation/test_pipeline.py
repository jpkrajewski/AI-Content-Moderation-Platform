import asyncio

import pytest
from moderation.pipelines.moderation.pipeline import Pipeline, PipelineStage, fill_empty_stages
from moderation.pipelines.moderation.postprocessors import ReturnSame


def sync_function(data):
    return data + 1


async def async_function(data):
    await asyncio.sleep(0.1)
    return data * 2


@pytest.mark.asyncio
async def test_sync_stage():
    stage = PipelineStage(func=sync_function, name="SyncStage")
    result = await stage.run(3)
    assert result == 4


@pytest.mark.asyncio
async def test_async_stage():
    stage = PipelineStage(func=async_function, name="AsyncStage")
    result = await stage.run(5)
    assert result == 10


@pytest.mark.asyncio
async def test_stage_exception_handling():
    def failing_func(_):
        raise ValueError("Deliberate failure")

    stage = PipelineStage(func=failing_func, name="FailStage")
    with pytest.raises(ValueError, match="Deliberate failure"):
        await stage.run("test")


def test_fill_empty_stages_with_none():
    runners = {0: PipelineStage(ReturnSame(), "runner0")}
    result = fill_empty_stages(runners, None)

    assert 0 in result
    assert isinstance(result[0][0], PipelineStage)
    assert result[0][0].name == "return_same"


def test_fill_empty_stages_with_missing_indexes():
    runners = {0: PipelineStage(ReturnSame(), "runner0"), 1: PipelineStage(ReturnSame(), "runner1")}
    stage = {0: [PipelineStage(ReturnSame(), "custom_stage_0")]}

    result = fill_empty_stages(runners, stage)

    assert 0 in result and len(result[0]) == 1 and result[0][0].name == "custom_stage_0"
    assert 1 in result and result[1][0].name == "return_same"


def test_fill_empty_stages_all_present():
    runners = {0: PipelineStage(ReturnSame(), "runner0"), 1: PipelineStage(ReturnSame(), "runner1")}
    stage = {0: [PipelineStage(ReturnSame(), "custom_stage_0")], 1: [PipelineStage(ReturnSame(), "custom_stage_1")]}

    result = fill_empty_stages(runners, stage)

    assert result[0][0].name == "custom_stage_0"
    assert result[1][0].name == "custom_stage_1"


def sync_add_one(x):
    return x + 1


async def async_double(x):
    return x * 2


def sync_to_string(x):
    return f"val:{x}"


async def async_aggregate_sum(x):
    return sum(x)


@pytest.mark.asyncio
async def test_generic_pipeline():
    # Setup pipeline stages
    extractors = [PipelineStage(sync_add_one, "add_one")]
    preprocessors = {0: [PipelineStage(async_double, "double")]}
    runners = {0: PipelineStage(sync_to_string, "to_string")}
    postprocessors = {0: [PipelineStage(sync_add_one, "noop_len")]}  # add 1 to string length as dummy operation
    aggregator = {0: PipelineStage(async_aggregate_sum, "sum_strings")}

    # Override postprocessor to just pass-through for compatibility
    postprocessors[0] = [PipelineStage(lambda x: x, "noop")]

    # Override aggregator to count characters
    aggregator[0] = PipelineStage(lambda items: [f"count:{len(items)}"], "count_items")

    pipeline = Pipeline(extractors, preprocessors, runners, postprocessors, aggregator)

    # Run pipeline
    result = await pipeline.process(3)

    # Assert result
    assert isinstance(result, list)
    assert result == ["count:1"]
