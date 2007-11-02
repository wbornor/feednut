import re, sys, subprocess, shutil, glob, os, tempfile


def compress(files, outfile, use_packer=False):
    temp, tempname = tempfile.mkstemp()
    for f in files:
        fo = open(f, 'r')
        os.write(temp, fo.read())
        fo.close()
    os.close(temp)
    
    #now, compress it -- commented out cuz jquery was having problems w/it
    if use_packer:
        if sys.platform == 'win32':
            p = subprocess.Popen(
                ['CScript', '/nologo', 'packer\pack.wsf', tempname],
                stdout=subprocess.PIPE,
            )
        else:
            p = subprocess.Popen(
                ['perl', '-Ipacker', 'packer/jsPacker.pl', '-q', '-i', tempname],
                stdout=subprocess.PIPE,
            )
    else:
        p = subprocess.Popen(
            ['java', '-jar', 'custom_rhino.jar', '-c', tempname],
            stdout=subprocess.PIPE,
        )
    
    outf = file(outfile, 'w')
    #print >>outf, """/***\n(c) 2006 Westom LLC.  All rights Reserved.\n***/
    shutil.copyfileobj(p.stdout, outf)
    os.unlink(tempname)

    outf.write('\n')
    outf.flush()
    outf.close()



def make_jquery():
    """ this is separate cuz we might want to combine several into one """
    files = ['../feednut/media/js/raw/jquery.js']
#    files.append('../feednut/media/js/raw/jquery/plugins/dom.js')
#    files.append('../feednut/media/js/raw/jquery/plugins/interface/ifx.js')
#    files.append('../feednut/media/js/raw/jquery/plugins/interface/idrag.js')
#    files.append('../feednut/media/js/raw/jquery/plugins/interface/idrop.js')
#    files.append('../feednut/media/js/raw/jquery/plugins/interface/iselect.js')
#    files.extend(glob.glob('../db/media/js/raw/jquery/plugins/interface/*.js'))
    compress(files, '../feednut/media/js/jquery.js')



if __name__ == '__main__':
    
    #rhino is having trouble w/feednut, so using packer
    compress(['../feednut/media/js/raw/feednut.js'], '../feednut/media/js/feednut.js', use_packer=True)
    
    make_jquery()
    
    #and some others.. each of these, just move up one dir
    files = ['thickbox.js', 'dragdrop.js', 'drag.js', 'thickbox.js',
             'lightbox.js', 'nifty.js', 'pngfix.js', 'MochiKit.js',
             'coordinates.js']
    for f in files:
        compress(['../feednut/media/js/raw/%s' % f], '../feednut/media/js/%s' % f)
    
