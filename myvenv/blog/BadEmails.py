<?php

$url1 = "https://eclipseprod.phila.gov/phillylmsprod/int/lms/Default.aspx#presentationId=1238903&objectHandle=";
$url2 = "&processHandle=";
$i = 0;

//Connect to Corral
$c = oci_connect('phillyit', 'ECL1PSESUPP0RT', '192.168.30.93:1521/PHLMSPD');

//Build query
$drafts = oci_parse($c, "select lic.externalfilenum, biz.objectid, lic.expirationdate, biz.preferredcontactmethod \"Contact Method\", biz.businesscontactname \"Contact Name\", biz.businesscontactemail \"Contact Email\"
from query.o_bl_license lic, query.o_bl_business biz
where lic.businessobjectid = biz.objectid
and biz.preferredcontactmethod = 'Email'
and (biz.businesscontactemail not like '%@%' OR biz.businesscontactemail like '%dispostable%' OR (biz.businesscontactemail like '%@%' AND biz.businesscontactemail not like '%.%'))
order by lic.expirationdate desc, biz.businesscontactemail asc");

//Execute query
oci_execute($drafts);

echo "These are Businesses with Email chosen as their contact method, but the email address on record is bad.<br/><table>";

//First Time Split
	while (oci_fetch($drafts)) {
		$licNum = oci_result($drafts, 'EXTERNALFILENUM');
		$bizID = oci_result($drafts, 'OBJECTID');
		$licExp = oci_result($drafts, 'EXPIRATIONDATE');
		$bizMethod = oci_result($drafts, 'Contact Method');
		$bizContact = oci_result($drafts, 'Contact Name');
		$bizEmail = oci_result($drafts, 'Contact Email');
		$bizurl = $url1.$bizID.$url2;
		echo "<tr><td>$licNum</td><td>$licExp</td><td>$bizMethod</td><td>$bizContact</td><td><a href='".$bizurl."' target='new'>".$bizEmail."</a></td></tr>";
		$i++;
	}


echo "</table></br>".$i." records found.<br/>";
echo "<br/>-End-";
echo "<br/><br/><b>Instructions:</b><br/>";
echo "Click a link at the end of a row. This will take you to the Business record. <br/>Click edit, select Mail instead of Email. <br/>If the Email field is the same name as the contact field, remove the value from the Email field. Otherwise, leave the bad email for historical records.<br/>You can then click the Finish Editing button and close that tab and return to this list."

?>