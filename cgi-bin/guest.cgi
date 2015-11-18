#!/user/bin/perl -w
#use strict;

    my(%fields);
    my($sec, $min, $hour, $mday, $mon, $year) = (localtime(time))[0..5];
    my($dataFile) = $ENV{'PATH_INFO'}."guestbook.dat";

    $mon  = zeroFill($mon, 2);
    $hour = zeroFill($hour, 2);
    $min  = zeroFill($min, 2);
    $sec  = zeroFill($sec, 2);
    $fields{'timestamp'} = "$mon/$mday/$year, $hour:$min:$sec";

    getFormData(\%fields);

    if ($ENV{'QUERY_STRING'}) {
        if ($ENV{'QUERY_STRING'} eq 'display') {
            displayPage();
        }
        elsif ($ENV{'QUERY_STRING'} eq 'add') {
            printGuestForm();
        }
        else {
            displayError("Unknown Command: <B>$ENV{'QUERY_STRING'}</B>");
        }
    }
    else {
        if (length($fields{'name'}) == 0) {
            displayError("Please fill the name field,<BR>\n");
        }
        if (length($fields{'comments'}) == 0) {
            displayError("Please fill the comments field,<BR>\n");
        }
        saveFormData(\%fields, $dataFile);
        displayPage();
    }

    exit(0);

sub displayError {
    print("Content-type: text/html;charset=ISO-8859-1\nCache-Control: max-age=3600\n\n");
    print("<HTML>\n");
    print("<HEAD><TITLE>Guestbook Error</TITLE></HEAD>\n");
    print("<H1>Guestbook</H1>\n");
    print("<HR>\n");
    print("@_<BR>\n");
    print("<HR>\n");
    printENV();
    print("</BODY>\n");
    print("</HTML>\n");
    exit(0);
}

sub displayPage {
    my(%entries);

    readFormData($dataFile, \%entries);

    print("Content-type: text/html;charset=ISO-8859-1\n\n");
    print("<HTML>\n");
    print("<HEAD><TITLE>Guestbook</TITLE></HEAD>\n");
    print("<TABLE><TR><TD VALIGN=top><H1>Guestbook</H1></TD>\n");

    print("<TD VALIGN=top><UL><LI><A HREF=\"guest.cgi?add\">Add an Entry</A>\n");
    print("<LI><A HREF=\"guest.cgi?display\">Refresh</A></UL></TD></TR></TABLE>\n");
    print("<HR>\n");

    foreach (sort(keys(%entries))) {
        my($arrayRef) = $entries{$_};
        my($timestamp, $name, $email, $comments) = ($_, @{$arrayRef});

        print("$timestamp: <B>$name</B> <A HREF=mailto:$email>$email</A>\n");
        print("<OL>$comments</OL>\n");
        print("<HR>\n");
    }
    print("</BODY>\n");
    print("</HTML>\n");
}

sub readFormData {
    my($file)    = shift;
    my($hashRef) = shift;

    open(FILE, "<$file") or displayError("Unable to open Guestbook data file.");
    while (<FILE>) {
        my($timestamp, $name, $email, $comments) = split(/~/, $_);

        $hashRef->{$timestamp} = [ $name, $email, $comments ];
    }
    close(FILE);
}

sub getFormData {
    my($hashRef) = shift;
    my($buffer) = "";

    if ($ENV{'REQUEST_METHOD'} eq "GET") {
        $buffer = $ENV{'QUERY_STRING'};
    }
    else {
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    }

    foreach (split(/&/, $buffer)) {
        my($key, $value) = split(/=/, $_);
        $key   = decodeURL($key);
        $value = decodeURL($value);

        $value =~ s/(<P>\s*)+/<P>/g;   # compress multiple <P> tags.
        $value =~ s/</&lt;/g;           # turn off all HTML tags.
        $value =~ s/>/&gt;/g;
        $value =~ s/&lt;b&gt;/<b>/ig;    # turn on the bold tag.
        $value =~ s!&lt;/b&gt;!</b>!ig;
        $value =~ s/&lt;i&gt;/<b>/ig;    # turn on the italic tag.
        $value =~ s!&lt;/i&gt;!</b>!ig;
        $value =~ s!\cM!!g;            # Remove unneeded carriage returns.
        $value =~ s!\n\n!<P>!g;        # Convert 2 newlines into paragraph.
        $value =~ s!\n! !g;            # convert newline into space.
        $hashRef->{$key} = $value;
    }
}

sub decodeURL {
    $_ = shift;
    tr/+/ /;
    s/%(..)/pack('c', hex($1))/eg;
    return($_);
}

sub zeroFill {
    my($temp) = shift;
    my($len)  = shift;
    my($diff) = $len - length($temp);

    return($temp) if $diff <= 0;
    return(('0' x $diff) . $temp);
}

sub saveFormData {
    my($hashRef) = shift;
    my($file)    = shift;

    open(FILE, ">>$file") or die("Unable to open Guestbook data file.");
    print FILE ("$hashRef->{'timestamp'}~");
    print FILE ("$hashRef->{'name'}~");
    print FILE ("$hashRef->{'email'}~");
    print FILE ("$hashRef->{'comments'}");
    print FILE ("\n");
    close(FILE);
}

sub printENV {
    print "The Environment report<BR>\n";
    print "----------------------<BR><PRE>\n";
    print "REQUEST_METHOD:  *$ENV{'REQUEST_METHOD'}*\n";
    print "SCRIPT_NAME:     *$ENV{'SCRIPT_NAME'}*\n";
    print "QUERY_STRING:    *$ENV{'QUERY_STRING'}*\n";
    print "PATH_INFO:       *$ENV{'PATH_INFO'}*\n";
    print "PATH_TRANSLATED: *$ENV{'PATH_TRANSLATED'}*</PRE>\n";

    if ($ENV{'REQUEST_METHOD'} eq 'POST') {
        print "CONTENT_TYPE:    $ENV{'CONTENT_TYPE'}<BR>\n";
        print "CONTENT_FILE:    $ENV{'CONTENT_FILE'}<BR>\n";
        print "CONTENT_LENGTH:  $ENV{'CONTENT_LENGTH'}<BR>\n";
    }
    print("<BR>");

    foreach (sort(keys(%ENV))) {
        print("$_: $ENV{$_}<BR>\n");
    }
    print("<BR>");

    foreach (sort(keys(%fields))) {
        print("$_: $fields{$_}<BR>\n");
    }
    print("<BR>");
}
sub printGuestForm{
 print qq{<HTML>
<HEAD><TITLE>Add to our Guestbook</TITLE></HEAD>
<BODY>
<CENTER><H1>Add to our Guestbook</H1></CENTER>
Fill in the blanks below to add to our Guestbook.  The only fields that you
have to fill in are the comments and name section.  Thanks!
<HR>
<FORM METHOD=POST ACTION="/cgi-bin/guest.cgi">
  <TABLE BORDER=0 CELLPADDING=10>
    <TR>
      <TD>Your Name:</TD>
      <TD><INPUT TYPE=text NAME=name SIZE=30></TD>
    </TR>
    <TR>
      <TD>Email:</TD>
      <TD><INPUT TYPE=text NAME=email SIZE=40></TD>
    </TR>
    <TR>
      <TD VALIGN=top>Comments:</TD>
      <TD><TEXTAREA NAME=comments COLS=60 ROWS=4></TEXTAREA></TD>
    </TR>
  </TABLE>
  <INPUT TYPE=submit VALUE="Add Entry"> <INPUT TYPE=reset>
</FORM>
</BODY>
</HTML>};

}