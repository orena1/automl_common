from typing import Generic, TypeVar

import pickle
from pathlib import Path

from automl_common.backend.contexts import Context, PathLike
from automl_common.backend.stores import PredictionsStore

Model = TypeVar("Model")


# TODO assuming a picklable Model
#   Trying to parametrize the saveing and loading functions would
#   lead to any framework using automl_common to not be picklalbe.
class ModelAccessor(Generic[Model]):
    """Access state of a Model with a directory on a filesystem

    Manages a directory:
    /<dir>
        / predictions_train.npy
        / predictions_test.npy
        / predictions_val.npy
        / model
        / ...

    Any implementing class can add more state that can be managed about this model.

    A ModelView must implement:
    * `save` - Save a model to a backend
    * `load` - Load a model from a backend
    """

    def __init__(
        self,
        dir: PathLike,
        context: Context,
    ):
        """
        Parameters
        ----------
        dir: PathLike
            The directory to load and store from

        context: Context
            A context object to iteract with a filesystem
        """
        self.context = context

        self.dir: Path
        if isinstance(dir, Path):
            self.dir = dir
        else:
            self.dir = self.context.as_path(dir)

        self.predictions_store = PredictionsStore(dir, context)

    @property
    def path(self) -> Path:
        """Path to the model object"""
        return self.dir / "model"

    @property
    def predictions(self) -> PredictionsStore:
        """Return the predictions store for this model

        Returns
        -------
        PredictionsStore
            A store of predicitons for the model encapsulated by this ModelBackend

        """
        return self.predictions_store

    def load(self) -> Model:
        """Get the model in this model store

        Returns
        -------
        Model
            The loaded model
        """
        with self.context.open(self.path, "rb") as f:
            return pickle.load(f)

    def save(self, model: Model) -> None:
        """Save the model

        Parameters
        ----------
        model: Model
            The model to save
        """
        with self.context.open(self.path, "wb") as f:
            pickle.dump(model, f)
