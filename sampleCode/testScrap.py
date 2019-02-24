from lxml import html

doc = """<thead class='market-trans-head'>
<tbody>
<TABLE>
    <TR class="linedlist">
         <TD><a href="blahblah/somepage/anotherpage">Name</a></TD>
        <TD><P>Fees</P></TD>
        <TD><P>Awards</P></TD>
        <TD><P>Total</P></TD>
    </TR>
    <TR class='linedlist'>
        <TD><P>Tony</P></TD>
        <TD >7,800</TD>
        <TD >7</TD>
        <TD>15,400</TD>
    </TR>
    <TR>
        <TD><P>Paul</FONT></P></TD>
        <TD >7,800</TD>
        <TD >7</TD>
        <TD>15,400</TD>
    </TR>
    <TR>
        <TD><P>Richard</P></TD>
        <TD >7,800</TD>
        <TD >7</TD>
        <TD>15,400</TD>
    </TR>

    </TR>
    </TABLE>"""

root = html.fromstring(doc)
print(root.xpath('//tbody/table/tr[@class="linedlist"]/td//text()'))