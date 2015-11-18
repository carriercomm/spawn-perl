#!/usr/bin/env perl
use CGI;
my $cgi = new CGI;
print $cgi->header();
print <<"EOF";
<HTML>

<HEAD>
<TITLE>Hello, world!</TITLE>
</HEAD>

<BODY>
<H1>Hello, world!</H1>
</BODY>

</HTML>
EOF
