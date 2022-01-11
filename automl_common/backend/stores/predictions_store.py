from typing import Iterator

import re
from pathlib import Path

from automl_common.backend.stores.numpy_store import NumpyStore


class PredictionsStore(NumpyStore):
    """A store for numpy based predictions"""

    pattern = r"predictions_(.*)\.npy"

    def path(self, key: str) -> Path:
        """Get the path for predictions with the given key

        Parameters
        ----------
        key: str
            The key of the predicitons

        Returns
        -------
        Path
            The path to the predictions
        """
        return self.dir / f"predictions_{key}.npy"

    def __iter__(self) -> Iterator[str]:
        files = self.context.listdir(self.dir)
        matches = iter(re.match(self.pattern, file) for file in files)
        return iter(match.group(1) for match in matches if match is not None)
