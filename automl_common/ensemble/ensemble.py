from abc import ABC, abstractmethod
from typing import Any, Iterator, List, Mapping, TypeVar

import copy

import numpy as np

from automl_common.backend import Backend
from automl_common.backend.accessors import ModelAccessor
from automl_common.model import Model

ModelT = TypeVar("ModelT", bound=Model)


class Ensemble(ABC, Mapping[str, ModelAccessor[ModelT]]):
    """Manages functionality around using multiple models ensembled in some fashion"""

    def __init__(self, backend: Backend[ModelT], identifiers: List[str]):
        """
        Parameters
        ----------
        identifiers: List[str]
            The identifiers of the models in the ensemble

        backend: Backend
            The context to work from
        """
        self.backend = backend
        self.identifiers = identifiers

    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        """The prediction of the ensemble on values x

        Parameters
        ----------
        x: np.ndarray
            The values to predict on

        Returns
        -------
        np.ndarray
            The prediction for the given values
        """
        ...

    def __getitem__(self, key: str) -> ModelAccessor[ModelT]:
        if key not in self.identifiers:
            raise ValueError(f"Model with {key} not in ensemble, {self.identifiers}")
        return self.backend.models[key]

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False

        return key in self.identifiers

    def __iter__(self) -> Iterator[str]:
        return iter(self.identifiers)

    def __getstate__(self) -> Any:
        state = copy.deepcopy(self.__dict__)
        del state["backend"]
        return state
