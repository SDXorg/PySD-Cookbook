import glob
import os.path
import subprocess
import shutil

notebooks = glob.glob('source/analyses/*/*.ipynb')
notebooks += glob.glob('source/data/*/*.ipynb')

# Remove 'workbook' files
notebooks = [nbf for nbf in notebooks if '_Workbook' not in nbf]




for infile in notebooks:
    try:
        #infile = infile.replace(' ', '\ ')

        # convert notebook in its local directory
        path, nbfile = os.path.split(infile)
        call_str = "jupyter nbconvert --to rst %(nbfile)s" % {'nbfile': nbfile}
        subprocess.call(call_str, cwd=path, shell=True)

        # move the .rst file
        no_ext = os.path.splitext(nbfile)[0]
        movefiles = path + '/' + no_ext + '.rst'
        dest = 'docs/' + '/'.join(path.split('/')[1:])  # pretty dependent on directory structure
        shutil.move(movefiles, dest + '/' + no_ext + '.rst')  # ! mv $movefiles $dest

        # move supporting files, if there are any
        movedir = path + '/' + no_ext + '_files'
        if os.path.exists(movedir):
            destdir = 'docs/' + '/'.join(path.split('/')[1:]) + '/' + no_ext + '_files'
            if os.path.exists(
                    destdir):  # check to see if the 'files' directory has already been created
                # if so, remove it, so we can have a clean slate...
                shutil.rmtree(destdir)  # !rm - r $destdir
            shutil.move(movedir, dest)  # !mv $movedir $dest
    except:
        print 'Did not translate', infile

# Call 'Make' to build the tranlated files to HTML
# http://www.sphinx-doc.org/en/stable/tutorial.html#running-the-build
subprocess.call('make clean', cwd='docs/', shell=True)
subprocess.call('make html', cwd='docs/', shell=True)