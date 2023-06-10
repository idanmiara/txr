from pathlib import Path
from typing import Optional

import pytest as pytest

from txr import StrOrPathLike, txr_archive, txr_extract, error_exception


@pytest.mark.parametrize("root", [r'd:\tmp\txr_test1\test_file.txt', r'd:\tmp\txr_test1'])
@pytest.mark.parametrize("compression", ['zlib', ''])
@pytest.mark.parametrize("password", ['abc', ''])
@pytest.mark.parametrize("encoding", ['ub64', ''])
def test_1(
        root: StrOrPathLike,
        compression: Optional[str],
        password: Optional[str],
        encoding: Optional[str],
        new_root: Optional[StrOrPathLike] = None,
        **kwargs
):
    root = Path(root)
    test = False
    txr_filename, txd_filename = txr_archive(
        root,
        # hash='sha512',
        test_txr=test,
        test_txd=test,
        compression=compression,
        password=password,
        encoding=encoding,
        error_call=error_exception,
        **kwargs)
    if new_root is None:
        new_root = root.with_suffix('.test')
    txr_extract(
        txr_filename=txr_filename,
        root=new_root,
        enforce_hash=True,
        test=test,
        password=password,
        error_call=error_exception,
    )

