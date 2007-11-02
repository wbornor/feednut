import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
os.environ['PYTHONINSPECT'] = '1'

from westom.feednut.utils import search

if __name__ == '__main__':
       context = """<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=375><TR><TD><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=5 WIDTH=1 BORDER=0 ALT="pad"></TD></TR><TR VALIGN=TOP><TD WIDTH=375><IMG SRC="http://us.st11.yimg.com/us.st.yimg.com/I/paulgraham_1920_1059" WIDTH=12 HEIGHT=14 ALIGN=LEFT BORDER=0 HSPACE=0 VSPACE=0><FONT SIZE=2 FACE="verdana"><A HREF="gap.html">Mind the Gap</A><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=2 WIDTH=1 BORDER=0 ALT="pad"><BR></FONT></TD></TR><TR><TD><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=5 WIDTH=1 BORDER=0 ALT="pad"></TD></TR><TR VALIGN=TOP><TD WIDTH=375><IMG SRC="http://us.st11.yimg.com/us.st.yimg.com/I/paulgraham_1920_1059" WIDTH=12 HEIGHT=14 ALIGN=LEFT BORDER=0 HSPACE=0 VSPACE=0><FONT SIZE=2 FACE="verdana"><A HREF="startupmistakes.html">The 18 Mistakes That Kill Startups</A><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=2 WIDTH=1 BORDER=0 ALT="pad"><BR></FONT></TD></TR><TR><TD><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=5 WIDTH=1 BORDER=0 ALT="pad"></TD></TR><TR VALIGN=TOP><TD WIDTH=375><IMG SRC="http://us.st11.yimg.com/us.st.yimg.com/I/paulgraham_1920_1059" WIDTH=12 HEIGHT=14 ALIGN=LEFT BORDER=0 HSPACE=0 VSPACE=0><FONT SIZE=2 FACE="verdana"><A HREF="mit.html">A Student's Guide to Startups</A><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=2 WIDTH=1 BORDER=0 ALT="pad"><BR></FONT></TD></TR><TR><TD><img src="http://us.st1.yimg.com/store1.yimg.com/Img/trans_1x1.gif" HEIGHT=5 WIDTH=1 BORDER=0 ALT="pad"></TD></TR><TR VALIGN=TOP><TD WIDTH=375><IMG SRC="http://us.st11.yimg.com/us.st.yimg.com/I/paulgraham_1920_1059" WIDTH=12 HEIGHT=14 ALIGN=LEFT BORDER=0 HSPACE=0 VSPACE=0><FONT SIZE=2 FACE="verdana"><A HREF="investors.html">"""
               
       seed = ['Mind the Gap', "The 18 Mistakes That Kill Startups", "A Student's Guide to Startups"]
       
       search.generate_feed(context, seed)