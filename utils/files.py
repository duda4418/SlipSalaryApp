import os, csv, zipfile
from typing import Iterable

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def write_csv(path: str, headers: list[str], rows: Iterable[Iterable]):
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    return path

def zip_paths(paths: list[str], zip_path: str):
    ensure_dir(os.path.dirname(zip_path))
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            arcname = os.path.basename(p)
            z.write(p, arcname)
    return zip_path
