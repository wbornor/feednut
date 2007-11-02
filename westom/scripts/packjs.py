import re, sys, subprocess, shutil

if __name__ == '__main__':
    infile = file('media/js/westom.js')
#    outf = file('media/js/fn.js')
    outf = sys.stdout
    
    p = subprocess.Popen(
        ['java', '-jar', 'scripts/custom_rhino.jar', '-c', infile.name],
        stdout=subprocess.PIPE,
    )
    print >>outf, """/***\n(c) 2006 Westom LLC.  All rights Reserved.\n***/
    """ % locals()
    
    shutil.copyfileobj(p.stdout, outf)
    outf.write('\n')
    outf.flush()
    outf.close()

