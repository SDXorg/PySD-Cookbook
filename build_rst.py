import glob
from pathlib import Path
import subprocess
import shutil

_root = Path(__file__).parent.resolve()
_docs = _root / "docs"

notebooks = glob.glob('source/analyses/*/*.ipynb')
notebooks += glob.glob('source/data/*/*.ipynb')
# Remove 'workbook' files
notebooks = [Path(nbf) for nbf in notebooks if '_Workbook' not in nbf]
figures = glob.glob('source/analyses/*/*.png')
figures += glob.glob('source/data/*/*.png')
figures = [Path(file) for file in figures]

for infile in notebooks:
    # convert notebook in its local directory
    path = _root / infile.parent
    nbfile = infile.name
    rstfile = infile.with_suffix(".rst").name
    files = infile.with_suffix("").name + '_files'
    call_str = "jupyter nbconvert --to rst %(nbfile)s" % {'nbfile': nbfile}
    subprocess.call(call_str, cwd=path, shell=True)

    # move the .rst file
    movefiles = path / rstfile
    # pretty dependent on directory structure
    dest = _docs / Path(*infile.parent.parts[1:])
    # ! mv $movefiles $dest

    if not dest.exists():
        dest.mkdir()

    shutil.move(movefiles, dest / rstfile)

    # move supporting files, if there are any
    movedir = path / files
    if movedir.exists():
        destdir = dest / files
        if destdir.exists():
            # !rm - r $destdir
            shutil.rmtree(destdir)
        # !mv $movedir $dest
        shutil.move(str(movedir), str(dest))

for infile in figures:
    # Copy extra figures
    dest = _docs / Path(*infile.parts[1:])
    shutil.copy(infile, dest)
