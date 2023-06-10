import csv
import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import Union, List, TypedDict, Optional, Tuple

StrOrPathLike = Union[Path, str]

logger = logging.root
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

__package_name__ = "txr"
__version__ = '1.0.0'
__author__ = "Idan Miara"
__author_email__ = "idan@miara.com"
__license__ = "GPL3"
__url__ = r"https://github.com/idanmiara/txr"
__description__ = "Stylish merge/split files (tar-like with txt output)"

txr_ver = __version__
txr_fmt = 1
sentinel = '!@#$!@#$!@#$'


class FileMeta(TypedDict):
    idx: int
    sha256: str
    offset: int
    filesize: int
    filename: str


meta_fileds = list(FileMeta.__annotations__)


class MetaHeader(TypedDict):
    txr_ver: str
    txr_fmt: int
    sentinel: str
    files: int
    total_bytes: int


def txr(
        root: StrOrPathLike, files: List[StrOrPathLike],
        txr_filename: Optional[StrOrPathLike] = None, txd_filename: Optional[StrOrPathLike] = None,
        write_txr: bool = True, write_txd: bool = True,
        encoding='utf-8', **kwargs
) -> Tuple[Path, Path]:
    if txr_filename is None:
        txr_filename = str(root) + '.txr'
    if txd_filename is None:
        txd_filename = str(root) + '.txd'

    total_bytes = 0
    meta = []
    root = Path(root)
    b_sentinal = bytes(sentinel, 'ascii')
    f_txd = open(txd_filename, mode='bw', **kwargs) if write_txd else None
    if write_txd:
        logger.info(f'writing {txd_filename}')

    for idx, filename in enumerate(files):
        filename = Path(filename)
        filename = filename.relative_to(root)
        with open(root / filename, mode='br', **kwargs) as f:
            file_data = f.read()
        file_size = len(file_data)
        hash = hashlib.sha256(file_data).hexdigest()
        m = FileMeta(
            idx=idx,
            offset=total_bytes,
            filesize=file_size,
            sha256=str(hash),
            filename=str(filename),
        )
        logger.debug(m)
        meta.append(m)
        if write_txd:
            f_txd.write(file_data)
            f_txd.write(b_sentinal)
        total_bytes += file_size + len(sentinel)
    if write_txd:
        f_txd.close()

    meta_header = MetaHeader(
        txr_ver=txr_ver,
        txr_fmt=txr_fmt,
        sentinel=sentinel,
        files=len(files),
        total_bytes=total_bytes,
    )
    logger.info(meta_header)

    if write_txr:
        logger.info(f'writing {txr_filename}')
        with open(txr_filename, mode='w', newline='', encoding=encoding) as f_txr:
            meta_header = json.dumps(meta_header)
            f_txr.write(f'{meta_header}\n')
            w = csv.DictWriter(f_txr, meta_fileds)
            w.writeheader()
            w.writerows(meta)

    return txr_filename, txd_filename


def un_txr(
        txr_filename: StrOrPathLike,
        txd_filename: Optional[StrOrPathLike] = None,
        root: Optional[StrOrPathLike] = None,
        enforce_hash: Optional[bool] = None,
        encoding='utf-8', **kwargs
):
    txr_filename = Path(txr_filename)
    if root is None:
        root = txr_filename.with_name(txr_filename.stem)
    txr_filename = Path(txr_filename)
    if txd_filename is None:
        txd_filename = txr_filename.with_suffix('.txd')
    txd_filename = Path(txd_filename)

    with open(txr_filename, mode='r', encoding=encoding, newline='', **kwargs) as f_txr:
        meta_header = f_txr.readline().strip()
        meta_header = json.loads(meta_header)
        r = csv.DictReader(f_txr)
        meta = list(r)
        compare_hash = enforce_hash or enforce_hash is None

        logger.info(f'reading {txd_filename}')
        with open(txd_filename, mode='br', **kwargs) as f_txd:
            for m in meta:
                offset = int(m['offset'])
                filesize = int(m['filesize'])
                filename = m['filename']
                hash_org = m['sha256']
                full_filename = root / filename
                full_filename.parent.mkdir(exist_ok=True, parents=True)
                f_txd.seek(offset)
                file_data = f_txd.read(filesize)
                logger.debug(m)
                with open(full_filename, mode='bw', **kwargs) as f:
                    if compare_hash:
                        hash_new = hashlib.sha256(file_data).hexdigest()
                        if hash_new != hash_org:
                            s = f'hash mismatch: {filename}: {hash_new} != {hash_org}'
                            if enforce_hash:
                                raise Exception(s)
                            else:
                                logger.error(s)
                    f.write(file_data)

    return meta


def txr_dir(root: StrOrPathLike, pattern: str = '**/*', **kwargs):
    filenames = list([f for f in Path(root).glob(pattern) if f.is_file()])
    if not filenames:
        raise Exception(f'No files found for {root}/{pattern}')
    return txr(root=root, files=filenames, **kwargs)


def test(root: StrOrPathLike, new_root: Optional[StrOrPathLike] = None, pattern: str = '**/*.*', **kwargs):
    root = Path(root)
    simulate = False
    txr_filename, txd_filename = txr_dir(
        root,
        write_txr=not simulate,
        write_txd=not simulate,
        pattern=pattern,
        **kwargs)
    if new_root is None:
        new_root = root.with_suffix('.test')
    un_txr(txr_filename=txr_filename, root=new_root)


if __name__ == '__main__':
    test(root=r'd:\tmp\txr_test')
