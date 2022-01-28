"""
tags:
    {"weighted", "single"} - The type of case it is
"""

from typing import Any, Callable, Iterable, Tuple, TypeVar, Union

from functools import reduce

import numpy as np
from pytest_cases import case, parametrize

from automl_common.util.types import SupportsEqualty

T = TypeVar("T", bound=SupportsEqualty)


def metric_acc(x: np.ndarray, y: np.ndarray) -> float:
    """Accuracy metric"""
    return sum(x == y) / len(x)


def metric_distance(x: np.ndarray, y: np.ndarray) -> float:
    """Distance metric"""
    return np.linalg.norm(x - y)  # type: ignore


def metric_multi_out(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """Multi-objective metric"""
    return (metric_acc(x, y), metric_distance(x, y))


def best_multi_out(scores: Iterable[Tuple[float, float]]) -> Tuple[float, float]:
    """A corresponding best function for multi object"""
    score = lambda acc, dist: (-acc + dist)
    return reduce(lambda s, sn: s if score(*s) < score(*sn) else sn, scores)


@case(tags=["single"])
@parametrize("metric", [metric_acc, metric_distance, metric_multi_out])
@parametrize("best", ["min", "max", lambda scores: next(scores)])
def case_single_one_model_to_choose(
    metric: Callable[..., T],
    best: Union[str, Callable[[Iterable[T]], T]],
) -> Any:
    """The case where the is only one model to choose from

    Should be the same model expected no matter what the metric or however the
    best is chosen from the metric.

    Parameters
    ----------
    metric: (preds, targets) -> T
        The metric that should be used

    best: Union[str, Callable[[Iterable[T]], T]]
        How to select the best from the list of scores
    """
    model_predictions = {"a": np.asarray([1, 1, 1])}
    targets = np.asarray([0, 0, 0])
    expected = "a"

    return model_predictions, targets, metric, best, expected


@case(tags=["weighted"])
@parametrize("metric", [metric_acc, metric_distance, metric_multi_out])
@parametrize("best", ["min", "max", lambda scores: next(scores)])
@parametrize("size", [1, 5, 10])
def case_weighted_one_model_to_choose(
    metric: Callable[..., T],
    best: Union[str, Callable[[Iterable[T]], T]],
    size: int,
) -> Any:
    """The case where the is only one model to choose from

    Should be the same model expected no matter what the metric or however the
    best is chosen from the metric.

    Parameters
    ----------
    metric: (preds, targets) -> T
        The metric that should be used

    best: Union[str, Callable[[Iterable[T]], T]]
        How to select the best from the list of scores

    size: int
        How many members in the enseble
    """
    model_predictions = {"a": np.asarray([1, 1, 1])}
    targets = np.asarray([0, 0, 0])
    expected_weights = {"a": 1.0}

    res = metric(model_predictions["a"], targets)

    # Should expect that we get the same model and result n times
    expected_trajectory = [("a", res)] * size

    return (
        model_predictions,
        targets,
        metric,
        size,
        best,
        expected_weights,
        expected_trajectory,
    )


@case(tags=["single"])
@parametrize("n", [2, 5, 10])
@parametrize(
    "metric, best",
    [
        (metric_acc, "max"),
        (metric_distance, "min"),
        (metric_multi_out, best_multi_out),
    ],
)
def case_single_n_models(
    n: int,
    metric: Callable[..., T],
    best: Union[str, Callable[[Iterable[T]], T]],
) -> Any:
    """The case where there is n models to choose from

    We randomly select the best model to ensure some fairness

    Parameters
    ----------
    n: int
        How many models to choose from

    metric: (preds, targets) -> T
        Metric to use to produce a score for a prediction

    best: Union[str, Callable[[Iterable[T]], T]]
        How to choose the best score
    """
    targets = np.asarray([0, 0, 0])
    model_predictions = {str(i): np.asarray([1, 1, 0]) for i in range(n)}

    expected = np.random.choice(list(model_predictions))

    # The expected model is given the targets so they match exactly
    model_predictions[expected] = targets

    return model_predictions, targets, metric, best, expected