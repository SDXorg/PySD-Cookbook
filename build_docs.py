import glob
import os.path
import subprocess
import shutil

notebooks = glob.glob('source/analyses/*/*.ipynb')
notebooks += glob.glob('source/data/*/*.ipynb')

# Remove 'workbook' files
notebooks = [nbf for nbf in notebooks if '_Workbook' not in nbf]
errors = []

for infile in notebooks:
    try:
        # convert notebook in its local directory
        path, nbfile = os.path.split(infile)
        call_str = "jupyter nbconvert --to rst %(nbfile)s" % {'nbfile': nbfile}
        subprocess.call(call_str, cwd=path, shell=True)

        # move the .rst file
        no_ext = os.path.splitext(nbfile)[0]
        movefiles = path + '/' + no_ext + '.rst'
        # pretty dependent on directory structure
        dest = 'docs/' + '/'.join(path.split('/')[1:])
        # ! mv $movefiles $dest
        shutil.move(movefiles, dest + '/' + no_ext + '.rst')

        # move supporting files, if there are any
        movedir = path + '/' + no_ext + '_files'
        if os.path.exists(movedir):
            destdir = 'docs/' + '/'.join(path.split('/')[1:])\
                + '/' + no_ext + '_files'
            if os.path.exists(destdir):
                # !rm - r $destdir
                shutil.rmtree(destdir)
            # !mv $movedir $dest
            shutil.move(movedir, dest)
    except (FileNotFoundError, NotADirectoryError):
        errors.append(f"'{infile}'")

print(f'Did not translate {", ".join(errors)}')


# Call 'Make' to build the tranlated files to HTML
# http://www.sphinx-doc.org/en/stable/tutorial.html#running-the-build
subprocess.call('make clean', cwd='docs/', shell=True)
subprocess.call('make html', cwd='docs/', shell=True)
