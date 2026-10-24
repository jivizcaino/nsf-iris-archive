<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<!-- start #header --><head><!-- Start Wayback Rewrite JS Include -->
<script type="text/javascript" src="/static/js/wombat.js?v=uVfyaniA" charset="utf-8"></script>
<script type="text/javascript">
if (window._WBWombatInit) {
  _wb_uc = new URL("https://www.nsf.gov/statistics/iris/errata.cfm");
  wbinfo = {}
  wbinfo.url = "https://www.nsf.gov/statistics/iris/errata.cfm";
  wbinfo.timestamp = "20181004030308";
  wbinfo.request_ts = "20181004030308";
  wbinfo.prefix = "https://wayback.archive-it.org/5902/";
  wbinfo.mod = "";
  wbinfo.is_framed = false;
  wbinfo.is_live = false;
  wbinfo.coll = "5902";
  wbinfo.proxy_magic = "";
  wbinfo.static_prefix = "/static/";
  wbinfo.enable_auto_fetch = true;
  wbinfo.auto_fetch_worker_prefix = "https://wayback.archive-it.org/5902/";
  wbinfo.wombat_ts = "20181004030308";
  wbinfo.wombat_sec = "1538622188";
  wbinfo.wombat_scheme = ( _wb_uc.protocol || 'http').replace(/:$/, '');
  wbinfo.wombat_host = _wb_uc.host;
  wbinfo.wombat_opts = {
    no_rewrite_prefixes: [
                            "https://wayback.archive-it.org/5902/",
                            "//archive-it.org/",
                            "https://partner.archive-it.org/",
                          ]
  };
  window._WBWombatInit(wbinfo);

  // variables useful for rulesengine rewrites from old ait-client_rewrite.js
  WB_RewriteUrl = _wb_wombat.rewrite_url;
  WB_ExtractOrig = _wb_wombat.extract_orig;
  WB_wombat_self_location = window.WB_wombat_location
}
</script>
<script type="text/javascript" src="https://partner.archive-it.org/static/AIT_Analytics.js" async="async"></script>
<!-- End Wayback Rewrite JS Include -->

<meta name="keywords" content=""/>
<meta name="description" content=""/>
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<title>NSF's Industrial Research and Development Information System</title>
<link href="/5902/20181004030308cs_/https://www.nsf.gov/statistics/iris/style.css" rel="stylesheet" type="text/css" media="screen"/>
<!-- 	NCSES GA tracking code  -->
<script>
	(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	})(window,document,'script','https://wayback.archive-it.org/5902/20181004030308/https://www.google-analytics.com/analytics.js','ga');

	/* Only send pageview if in PROD environments */
	if(window.location.hostname === "nsf.gov" || window.location.hostname === "www.nsf.gov" || window.location.hostname === "ncsesdata.nsf.gov"){
		ga('create', 'UA-74063859-1', 'auto', 'ncsesTracker');
		ga('ncsesTracker.send', 'pageview');
	}
  
	var ncsesGaConfig = {
		COOKIE_DOMAIN: location.hostname.replace('www.', '').toLowerCase(),
		EXTS: 'doc|docx|xls|xlsx|xlsm|ppt|pptx|exe|zip|pdf|js|txt|csv|dxf|dwgd|rfa|rvt|dwfx|dwg|wmv|jpg|msi|7z|gz|tgz|wma|mov|avi|mp3|mp4|csv|mobi|epub|swf|rar|sas7bdat|sav',
		SUBDOMAIN_BASED: true
	};
	
	/*
	* name: _sendNcsesEvent
	* usage: to set hit type to Event
	*/
	function _sendNcsesEvent(_cat, _act, _lbl, _val, _nonInteraction) {
		if (_cat != '' && _cat != undefined && _act != '' && _act != undefined) {
			/* Only send Events if in PROD environments */
			if(window.location.hostname === "nsf.gov" || window.location.hostname === "www.nsf.gov" || window.location.hostname === "ncsesdata.nsf.gov") {
				try
				{
					ga('ncsesTracker.send', 'event', _cat, _act, ((_lbl != undefined) ? _lbl : ''), ((_val != '' || !isNaN(_val) || _val != undefined) ? parseInt(_val) : 0), {'nonInteraction': _nonInteraction});
				}
				catch(err) {}
			}
		}
	}

	/*
	* name: _tagNcsesClicks
	* usage: 
	* add event listener to an HTML element
	*/	
	function _tagNcsesClicks(evObj, evCat, evAct, evLbl, evVal){
		if (evObj.addEventListener) { 
			evObj.addEventListener('mousedown', function() {
                _sendNcsesEvent(evCat, evAct, evLbl, evVal); });       
		} 
		else if (evObj.attachEvent) { 
			evObj.attachEvent('onmousedown', function() {
                _sendNcsesEvent(evCat, evAct, evLbl, evVal); });       
		} 
    }
	
	function _initNcsesGaTracker(){
		var mainDomain = ncsesGaConfig.COOKIE_DOMAIN;
		var extDoc = ncsesGaConfig.EXTS.split("|");
		var arr = document.getElementsByTagName("a");
		for(i=0; i < arr.length; i++)
		{
			var flag = 0;
			var flagExt = 0;
			var doname = ""; 
			var mailPattern = /^mailto\:[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}/;
			var urlPattern = /^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
			var telPattern = /^tel\:(.*)([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
			if(mailPattern.test(arr[i].href) || urlPattern.test(arr[i].href) || telPattern.test(arr[i].href)){
				try{
					if(urlPattern.test(arr[i].href)){
						doname = arr[i].hostname.toLowerCase().replace("www.","");			
					}else if(mailPattern.test(arr[i].href)){
						doname = arr[i].href.split('@')[1];
					}else if(telPattern.test(arr[i].href)){
						doname = arr[i].href;
						doname = doname.toLowerCase();
					}  
				}
				catch(err){
					continue;
				}
			}else{   
				continue; 
			}
		
			var condition = false;
			if (ncsesGaConfig.SUBDOMAIN_BASED) {
				condition = (doname.indexOf(mainDomain) != -1);
			} else {
				condition = (doname == mainDomain);
			}
		
			if(condition){
				// Tracking internal email clicks		
				if (arr[i].href.toLowerCase().indexOf("mailto:") != -1 && arr[i].href.toLowerCase().indexOf("tel:") == -1) {
					var gaUri = arr[i].href.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}/);
					_tagNcsesClicks(arr[i],'Mailto', gaUri[0], '', 0); 
				}
				else if (arr[i].href.toLowerCase().indexOf("mailto:") == -1 && arr[i].href.toLowerCase().indexOf("tel:") != -1) {
					_tagNcsesClicks(arr[i],'Telephone Clicks', arr[i].href.split("tel:")[1], '', 0); 
				}
				else if(arr[i].href.toLowerCase().indexOf("mailto:") == -1 && arr[i].href.toLowerCase().indexOf("tel:") == -1){
				
					for(var j = 0; j < extDoc.length; j++) 
					{
						var arExt = arr[i].href.split(".");
						var ext = arExt[arExt.length-1].split(/[#?&?]/);
						if(ext[0].toLowerCase() == extDoc[j]) {
							// Tracking internal downloads - doc, xls, pdf, exe, zip
							_tagNcsesClicks(arr[i],'Download', ext[0].toLowerCase(), arr[i].href.split(/[#?&?]/)[0], 0);
							break;
						}
					}
				}
			}
			else{
				for(var l = 0; l < extDoc.length; l++) 
				{
					var arExt = arr[i].href.split(".");
					var ext = arExt[arExt.length-1].split(/[#?]/);
					if(ext[0].toLowerCase() == extDoc[l]) {
						// Tracking outbound downloads - doc, xls, pdf, exe, zip
						var gaUri = arr[i].href.split(extDoc[l]);
						_tagNcsesClicks(arr[i],'Outbound Downloads', ext[0].toLowerCase(), arr[i].href.split(/[#?&?]/)[0], 0);
						break;
					}
					else if(ext[0].toLowerCase() != extDoc[l]){
						flagExt++;
						if(flagExt == extDoc.length){
							if(arr[i].href.toLowerCase().indexOf("mailto:") == -1 && arr[i].href.toLowerCase().indexOf("tel:") == -1){
								// Tracking outbound links 
								_tagNcsesClicks(arr[i],'Outbound', arr[i].hostname, arr[i].pathname, 0);
							}
							else if (extDoc.length && arr[i].href.toLowerCase().indexOf("mailto:") != -1 && arr[i].href.toLowerCase().indexOf("tel:") == -1){
								// Tracking outbound emails 
								var gaUri = arr[i].href.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}/);
								_tagNcsesClicks(arr[i],'Outbound MailTo', gaUri[0], '', 0); 
							}
							else if (extDoc.length && arr[i].href.toLowerCase().indexOf("mailto:") == -1 && arr[i].href.toLowerCase().indexOf("tel:") != -1){
								// Tracking Telephone clicks
								_tagNcsesClicks(arr[i],'Telephone Clicks', arr[i].href.split("tel:")[1], '', 0); 
							}
						}
					}
				}
			}
		}
	}
	if(document.addEventListener){
		document.addEventListener('DOMContentLoaded', function() {
			_initNcsesGaTracker();
		});
	}else if(document.attachEvent){
		document.attachEvent('onreadystatechange', function() {
			_initNcsesGaTracker();
		});
	}
  
</script>	

<!-- CrazyEgg script -->
<script>
setTimeout(function(){var a=document.createElement("script");
var b=document.getElementsByTagName("script")[0];
a.src=document.location.protocol+"//wayback.archive-it.org/5902/20181004030308/https://script.crazyegg.com/pages/scripts/0041/5508.js?"+Math.floor(new Date().getTime()/3600000);
a.async=true;a.type="text/javascript";b.parentNode.insertBefore(a,b)}, 1);
</script>


<!-- DigGov DAP tracking code. Change ver=true for production server -->
<script async id="_fed_an_ua_tag" src="https://wayback.archive-it.org/5902/20181004030308js_/https://dap.digitalgov.gov/Universal-Federated-Analytics-Min.js?agency=NSF&amp;subagency=NCSES&amp;dclink=true&amp;exts=sas7bdat,sav"></script>

</head>
	


<style>
.errataicon, a.errataicon:link, a.errataicon:visited, a.errataicon:hover, a.errataicon:active {
	background-position: left top;
	background-repeat: no-repeat;
	padding-bottom: 12px;
	padding-top: 10px;
}

.errata {
	background-image:url(/5902/20181004030308im_/https://www.nsf.gov/statistics/graphics/errata_icon.gif);
}
-->
</style>
<body>             
<!--
     FILE ARCHIVED ON 03:03:08 Oct 04, 2018 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 17:10:43 Oct 24, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
	urlKey(b'gov,nsf)/statistics/iris/errata.cfm')
-->

<div id="wrapper">
	<div id="header">
    	<div id="logo"><img src="/5902/20181004030308im_/https://www.nsf.gov/statistics/iris/images/IRIS.gif" alt="National Science Foundation's Industrial Research and Development Information System" width="730" height="113" usemap="#banner" border="0" title="National Science Foundation's Industrial Research and Development Information System"/>
<map name="banner">
	<area shape="poly" alt="Industrial Research and Development Information System" title="Industrial Research and Development Information System" coords="74,10,522,13,518,43,329,45,327,111,70,111,74,49" href="/5902/20181004030308/https://www.nsf.gov/statistics/iris/">
    <area shape="poly" alt="National Science Foundation" title="National Science Foundation" coords="7,18,18,11,34,10,47,11,58,21,63,30,65,45,63,57,55,69,46,75,34,76,19,75,9,67,1,57,1,43,3,30" href="https://wayback.archive-it.org/5902/20181004030308/http://www.nsf.gov/">
	<area shape="poly" alt="Browse tables by survey year" title="Browse tables by survey year" coords="443,79,529,81,531,111,444,111" href="history_pub.cfm">
	<area shape="poly" alt="Browse tables by data topic" title="Browse tables by data topic" coords="548,82,629,83,632,110,550,112" href="history_data.cfm">
	<area shape="poly" alt="Search for data tables" title="Search for data tables" coords="644,84,644,110,728,111,725,86" href="search_data.cfm">        
</map>
        </div>
	</div>
	<!-- end #header -->
    
<!-- start #menu -->
	<div id="menu">
		<ul>
			<li><a href="start.cfm">Home</a></li>
			<li><a href="about.cfm">About IRIS</a></li>
			<li><a href="/5902/20181004030308/https://www.nsf.gov/statistics/srvyindustry/">About the Survey</a></li>
			<li><a href="/5902/20181004030308/https://www.nsf.gov/statistics/industry/">Related Publications</a></li>
            <li class="current_page_item"><a href="errata.cfm">Errata</a></li>
			<li><a href="glossary.cfm">Glossary</a></li>
			<li><a href="contact.cfm">Contact Us</a></li>
			<li><a href="/5902/20181004030308/https://www.nsf.gov/help/">Help</a></li>
		</ul>
	</div>
<!-- end #menu -->


	<div id="page">

		<div id="content">
			<div class="post">
            	<div class="caption">Last updated July 2011</div><br/>    
				<h2 class="title">Errata</h2>
					

    <script type="text/javascript" src="/5902/20181004030308js_/https://www.nsf.gov/statistics/js/highslide-full.js"></script>
    <script type="text/javascript" src="/5902/20181004030308js_/https://www.nsf.gov/statistics/js/lightboxconfig.js"></script>
    <link rel="stylesheet" type="text/css" href="/5902/20181004030308cs_/https://www.nsf.gov/statistics/css/highslide.css"/>
    <script language="javascript"> 
    function toggle(rowNum) {
        var ele = document.getElementById("toggleText" + rowNum);
        var text = document.getElementById("displayText" + rowNum);
        if(ele.style.display == "none") {
                ele.style.display = "block";
                text.innerHTML = "close -";
        }
        else {
            ele.style.display = "none";
            text.innerHTML = "expand +";
        }
    } 
    </script>

    
    <div style="padding-bottom:1px; padding-right:8px; padding-top:0px;" align="left">
        
            <div class="errataicon" style="min-height:8px; padding-bottom: -10px;" title="Errata" alt="Errata">
                
                    <strong>Jul 26, 2011</strong> [<a id="displayText1" href="javascript:toggle('1');">close -</a>]<br/>
                    <div id="toggleText1" style="padding-left: 20px; padding-top:10px;" align="left">                        
                        Appendix table A-5 was replaced with a corrected version in the following reports: <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf06322/">NSF 06-322</a>, <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf07314/">NSF 07-314</a>, <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf09301/">NSF 09-301</a>, and <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf10319/">NSF 10-319</a>.
                       <br/>                
                
            </div>
            <br/><noscript>Appendix table A-5 was replaced with a corrected version in the following reports: <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf06322/">NSF 06-322</a>, <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf07314/">NSF 07-314</a>, <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf09301/">NSF 09-301</a>, and <a href="/5902/20181004030308/https://www.nsf.gov/statistics/nsf10319/">NSF 10-319</a>.</noscript>     
        </div>
    </div>
       
                        <div style="float:right"><a href="/5902/20181004030308/https://www.nsf.gov/statistics/errata.cfm">NCSES Errata</a></div>                
                   
             </div><!-- end #post -->  
               

			
		<div style="clear: both;">&nbsp;</div>
		</div>
		<!-- end #content -->
		
		<!-- end #sidebar -->
		<div style="clear: both;">&nbsp;</div>

</div>
	<!-- end #page -->
</div>
<!-- end #wrapper -->

<!-- start #footer -->
	<div id="footer">
    <table width="550" border="0" cellspacing="3" cellpadding="0" bgcolor="#E7ECFA">
	<tr>
		<td valign="middle">&nbsp; <a href="https://wayback.archive-it.org/5902/20181004030308/http://www.nsf.gov/"><img src="/5902/20181004030308im_/https://www.nsf.gov/statistics/iris/images/nsf3.gif" alt="National Science Foundation" title="National Science Foundation" width="45" height="45" border="0"/></a></td>
    	<td>
		<p>National Center for Science and Engineering Statistics<br/>
			The National Science Foundation <br/>
			2415 Eisenhower Avenue, Suite W14200 <br/>
			Alexandria, Virginia 22314<br/>
			Tel: (703) 292-8780, FIRS: (800) 877-8339 | TDD: (800) 281-8749<br/>
	  		<em>Celebrating 60 Years of Discovery </em><br/><br/>
        </p>
        
        </td>
	</table>

</div>
	<!-- end #footer -->
    
    <!-- START OF SmartSource Data Collector TAG -->
<!-- Copyright (c) 1996-2009 WebTrends Inc. All rights reserved. -->
<!-- Version: 8.6.2 -->
<!-- Tag Builder Version: 3.0 -->
<!-- Created: 5/7/2009 8:32:37 PM -->
<script src="/5902/20181004030308js_/https://www.nsf.gov/js/webtrends.js" type="text/javascript"></script>
<!-- ----------------------------------------------------------------------------------- -->
<!-- Warning: The two script blocks below must remain inline. Moving them to an external -->
<!-- JavaScript include file can cause serious problems with cross-domain tracking. -->
<!-- ----------------------------------------------------------------------------------- -->
<script type="text/javascript">
//<![CDATA[
var ncsesDcsid = "";
var isNcsesProdOrAcpt = false;
var ncsesServerHostName = window.location.hostname;
if (ncsesServerHostName.search(/(www(\-0[1-4])?\.)?nsf\.gov/i) == 0) {
	ncsesDcsid = "dcsngbilzcxafpc7vw2qgbbij_3j2v";
	isNcsesProdOrAcpt = true;
}
else if (ncsesServerHostName.search(/www(\-0[1-2])?\.acpt.nsf\.gov/i) >= 0) {
	ncsesDcsid = "dcshd2w31cxafp45smwqd9bij_5l5g";
	isNcsesProdOrAcpt = true;
}
var _tag=new WebTrends();
_tag.dcsid = ncsesDcsid;
if (isNcsesProdOrAcpt) {
	_tag.dcsCollect();
}
//]]>>
</script>
<noscript>
<div><img alt="DCSIMG" id="DCSIMG" width="1" height="1" src="https://wayback.archive-it.org/5902/20181004030308im_/https://wt.research.gov/dcsngbilzcxafpc7vw2qgbbij_3j2v/njs.gif?dcsuri=/nojavascript&amp;WT.js=No&amp;DCS.dcscfg=1&amp;WT.tv=8.6.2"/></div>
</noscript>
<!-- END OF SmartSource Data Collector TAG --> 

</body>
</html><!--
     FILE ARCHIVED ON 03:03:08 Oct 04, 2018 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 17:10:43 Oct 24, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
-->
