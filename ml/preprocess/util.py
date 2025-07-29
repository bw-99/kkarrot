from pathlib import Path
import pandas as pd
from typing import Callable
import logging
import numpy as np

logger = logging.getLogger(__name__)

def load_cache(fpath: str | Path, read: bool, write: bool, func: Callable[..., any], **kwargs) -> pd.DataFrame:
    ret = None
    if read:
        ret = pd.read_parquet(fpath) if fpath.exists() else None

    if ret is None:
        logger.info(f"call fn: {func}")
        ret = func(**kwargs)
        if write:
            ret.to_parquet(fpath)

    return ret


def pad_sequence(x: np.ndarray | list[int], pad_length: int, pad_value: int = 0, where: str = "left") -> np.ndarray:
    if where == "left":
        return np.concatenate([np.full(pad_length, pad_value), x])
    elif where == "right":
        return np.concatenate([x, np.full(pad_length, pad_value)])
    else:
        raise ValueError(f"invalid where: {where}")