<!DOCTYPE html>
<html lang="en" >

<head>
	<noscript><meta http-equiv="refresh" content="0; URL=/?redir=%2Ffiles%2Fdustin%2FF0510DKBS%2Fechoserver-simple.py&amp;nojsmode=1" /></noscript>
<script type="text/javascript">
window.load_start_ms = new Date().getTime();
window.load_log = [];
window.logLoad = function(k) {
	var ms = new Date().getTime();
	window.load_log.push({
		k: k,
		t: (ms-window.load_start_ms)/1000
	})
}
if(self!==top)window.document.write("\u003Cstyle>body * {display:none !important;}\u003C\/style>\u003Ca href=\"#\" onclick="+
"\"top.location.href=window.location.href\" style=\"display:block !important;padding:10px\">Go to Slack.com\u003C\/a>");
</script>


<script type="text/javascript">
window.callSlackAPIUnauthed = function(method, args, callback) {
	var url = '/api/'+method+'?t='+new Date().getTime();
	var req = new XMLHttpRequest();
	
	req.onreadystatechange = function() {
		if (req.readyState == 4) {
			req.onreadystatechange = null;
			var obj;
			
			if (req.status == 200) {
				if (req.responseText.indexOf('{') == 0) {
					try {
						eval('obj = '+req.responseText);
					} catch (err) {
						console.warn('unable to do anything with api rsp');
					}
				}
			}
			
			obj = obj || {
				ok: false	
			}
			
			callback(obj.ok, obj, args);
		}
	}
	
	req.open('POST', url, 1);
	req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var args2 = [];
	for (i in args) {
		args2[args2.length] = encodeURIComponent(i)+'='+encodeURIComponent(args[i]);
	}

	req.send(args2.join('&'));
}
</script>
			<meta name="referrer" content="no-referrer">
			<meta name="superfish" content="nofish">
	<script type="text/javascript">



var TS_last_log_date = null;
var TSMakeLogDate = function() {
	var date = new Date();

	var y = date.getFullYear();
	var mo = date.getMonth()+1;
	var d = date.getDate();

	var time = {
	  h: date.getHours(),
	  mi: date.getMinutes(),
	  s: date.getSeconds(),
	  ms: date.getMilliseconds()
	};

	Object.keys(time).map(function(moment, index) {
		if(time[moment] < 10) {
			time[moment] = '0' + time[moment];
		}
	});

	var str = y + '/' + mo + '/' + d + ' ' + time.h + ':' + time.mi + ':' + time.s + '.' + time.ms;
	if (TS_last_log_date) {
		var diff = date-TS_last_log_date;
		//str+= ' ('+diff+'ms)';
	}
	TS_last_log_date = date;
	return str+' ';
}

var TSSSB = {
	

	call: function() {
		return false;
	}

	
}

</script>	<script type="text/javascript">TSSSB.call('didFinishLoading');</script>
	    <meta charset="utf-8">
    <title>Slack</title>
    <meta name="author" content="Slack">
    <meta name="robots" content="noindex,nofollow">

	
						
																				
    									
		
		<!-- output_css "core" -->
    <link href="https://slack.global.ssl.fastly.net/fffa/style/rollup-plastic.css" rel="stylesheet" type="text/css">

	<!-- output_css "regular" -->
    <link href="https://slack.global.ssl.fastly.net/1e63/style/libs/lato-1.css" rel="stylesheet" type="text/css">

		<style>
	
		@media only screen and (max-width: 480px) {
			h1 {
				font-size: 1.5rem;
				margin-left: -0.5rem;
				margin-right: -0.5rem;
			}
		}
	
	</style>


	
	
	

	<!--[if lt IE 9]>
	<script src="https://slack.global.ssl.fastly.net/ef0d/js/libs/html5shiv.js"></script>
	<![endif]-->

	
<link id="favicon" rel="shortcut icon" href="https://slack.global.ssl.fastly.net/272a/img/icons/favicon-32.png" sizes="16x16 32x32 48x48" type="image/png" />

<link rel="icon" href="https://slack.global.ssl.fastly.net/ba3c/img/icons/app-256.png" sizes="256x256" type="image/png" />

<link rel="apple-touch-icon-precomposed" sizes="152x152" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-152.png" />
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-144.png" />
<link rel="apple-touch-icon-precomposed" sizes="120x120" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-120.png" />
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-114.png" />
<link rel="apple-touch-icon-precomposed" sizes="72x72" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-72.png" />
<link rel="apple-touch-icon-precomposed" href="https://slack.global.ssl.fastly.net/0dc1/img/icons/ios-57.png" />

<meta name="msapplication-TileColor" content="#FFFFFF" />
<meta name="msapplication-TileImage" content="https://slack.global.ssl.fastly.net/272a/img/icons/app-144.png" />	<script>
!function(a,b){function c(a,b){try{if("function"!=typeof a)return a;if(!a.bugsnag){var c=e();a.bugsnag=function(d){if(b&&b.eventHandler&&(u=d),v=c,!y){var e=a.apply(this,arguments);return v=null,e}try{return a.apply(this,arguments)}catch(f){throw l("autoNotify",!0)&&(x.notifyException(f,null,null,"error"),s()),f}finally{v=null}},a.bugsnag.bugsnag=a.bugsnag}return a.bugsnag}catch(d){return a}}function d(){B=!1}function e(){var a=document.currentScript||v;if(!a&&B){var b=document.scripts||document.getElementsByTagName("script");a=b[b.length-1]}return a}function f(a){var b=e();b&&(a.script={src:b.src,content:l("inlineScript",!0)?b.innerHTML:""})}function g(b){var c=l("disableLog"),d=a.console;void 0===d||void 0===d.log||c||d.log("[Bugsnag] "+b)}function h(b,c,d){if(d>=5)return encodeURIComponent(c)+"=[RECURSIVE]";d=d+1||1;try{if(a.Node&&b instanceof a.Node)return encodeURIComponent(c)+"="+encodeURIComponent(r(b));var e=[];for(var f in b)if(b.hasOwnProperty(f)&&null!=f&&null!=b[f]){var g=c?c+"["+f+"]":f,i=b[f];e.push("object"==typeof i?h(i,g,d):encodeURIComponent(g)+"="+encodeURIComponent(i))}return e.join("&")}catch(j){return encodeURIComponent(c)+"="+encodeURIComponent(""+j)}}function i(a,b){if(null==b)return a;a=a||{};for(var c in b)if(b.hasOwnProperty(c))try{a[c]=b[c].constructor===Object?i(a[c],b[c]):b[c]}catch(d){a[c]=b[c]}return a}function j(a,b){a+="?"+h(b)+"&ct=img&cb="+(new Date).getTime();var c=new Image;c.src=a}function k(a){var b={},c=/^data\-([\w\-]+)$/;if(a)for(var d=a.attributes,e=0;e<d.length;e++){var f=d[e];if(c.test(f.nodeName)){var g=f.nodeName.match(c)[1];b[g]=f.value||f.nodeValue}}return b}function l(a,b){C=C||k(J);var c=void 0!==x[a]?x[a]:C[a.toLowerCase()];return"false"===c&&(c=!1),void 0!==c?c:b}function m(a){return a&&a.match(D)?!0:(g("Invalid API key '"+a+"'"),!1)}function n(b,c){var d=l("apiKey");if(m(d)&&A){A-=1;var e=l("releaseStage"),f=l("notifyReleaseStages");if(f){for(var h=!1,k=0;k<f.length;k++)if(e===f[k]){h=!0;break}if(!h)return}var n=[b.name,b.message,b.stacktrace].join("|");if(n!==w){w=n,u&&(c=c||{},c["Last Event"]=q(u));var o={notifierVersion:H,apiKey:d,projectRoot:l("projectRoot")||a.location.protocol+"//"+a.location.host,context:l("context")||a.location.pathname,userId:l("userId"),user:l("user"),metaData:i(i({},l("metaData")),c),releaseStage:e,appVersion:l("appVersion"),url:a.location.href,userAgent:navigator.userAgent,language:navigator.language||navigator.userLanguage,severity:b.severity,name:b.name,message:b.message,stacktrace:b.stacktrace,file:b.file,lineNumber:b.lineNumber,columnNumber:b.columnNumber,payloadVersion:"2"},p=x.beforeNotify;if("function"==typeof p){var r=p(o,o.metaData);if(r===!1)return}return 0===o.lineNumber&&/Script error\.?/.test(o.message)?g("Ignoring cross-domain script error. See https://bugsnag.com/docs/notifiers/js/cors"):(j(l("endpoint")||G,o),void 0)}}}function o(){var a,b,c=10,d="[anonymous]";try{throw new Error("")}catch(e){a="<generated>\n",b=p(e)}if(!b){a="<generated-ie>\n";var f=[];try{for(var h=arguments.callee.caller.caller;h&&f.length<c;){var i=E.test(h.toString())?RegExp.$1||d:d;f.push(i),h=h.caller}}catch(j){g(j)}b=f.join("\n")}return a+b}function p(a){return a.stack||a.backtrace||a.stacktrace}function q(a){var b={millisecondsAgo:new Date-a.timeStamp,type:a.type,which:a.which,target:r(a.target)};return b}function r(a){if(a){var b=a.attributes;if(b){for(var c="<"+a.nodeName.toLowerCase(),d=0;d<b.length;d++)b[d].value&&"null"!=b[d].value.toString()&&(c+=" "+b[d].name+'="'+b[d].value+'"');return c+">"}return a.nodeName}}function s(){z+=1,a.setTimeout(function(){z-=1})}function t(a,b,c){var d=a[b],e=c(d);a[b]=e}var u,v,w,x={},y=!0,z=0,A=10;x.noConflict=function(){return a.Bugsnag=b,x},x.refresh=function(){A=10},x.notifyException=function(a,b,c,d){b&&"string"!=typeof b&&(c=b,b=void 0),c||(c={}),f(c),n({name:b||a.name,message:a.message||a.description,stacktrace:p(a)||o(),file:a.fileName||a.sourceURL,lineNumber:a.lineNumber||a.line,columnNumber:a.columnNumber?a.columnNumber+1:void 0,severity:d||"warning"},c)},x.notify=function(b,c,d,e){n({name:b,message:c,stacktrace:o(),file:a.location.toString(),lineNumber:1,severity:e||"warning"},d)};var B="complete"!==document.readyState;document.addEventListener?(document.addEventListener("DOMContentLoaded",d,!0),a.addEventListener("load",d,!0)):a.attachEvent("onload",d);var C,D=/^[0-9a-f]{32}$/i,E=/function\s*([\w\-$]+)?\s*\(/i,F="https://notify.bugsnag.com/",G=F+"js",H="2.4.7",I=document.getElementsByTagName("script"),J=I[I.length-1];if(a.atob){if(a.ErrorEvent)try{0===new a.ErrorEvent("test").colno&&(y=!1)}catch(K){}}else y=!1;if(l("autoNotify",!0)){t(a,"onerror",function(b){return function(c,d,e,g,h){var i=l("autoNotify",!0),j={};!g&&a.event&&(g=a.event.errorCharacter),f(j),v=null,i&&!z&&n({name:h&&h.name||"window.onerror",message:c,file:d,lineNumber:e,columnNumber:g,stacktrace:h&&p(h)||o(),severity:"error"},j),b&&b(c,d,e,g,h)}});var L=function(a){return function(b,d){if("function"==typeof b){b=c(b);var e=Array.prototype.slice.call(arguments,2);return a(function(){b.apply(this,e)},d)}return a(b,d)}};t(a,"setTimeout",L),t(a,"setInterval",L),a.requestAnimationFrame&&t(a,"requestAnimationFrame",function(a){return function(b){return a(c(b))}}),a.setImmediate&&t(a,"setImmediate",function(a){return function(){var b=Array.prototype.slice.call(arguments);return b[0]=c(b[0]),a.apply(this,b)}}),"EventTarget Window Node ApplicationCache AudioTrackList ChannelMergerNode CryptoOperation EventSource FileReader HTMLUnknownElement IDBDatabase IDBRequest IDBTransaction KeyOperation MediaController MessagePort ModalWindow Notification SVGElementInstance Screen TextTrack TextTrackCue TextTrackList WebSocket WebSocketWorker Worker XMLHttpRequest XMLHttpRequestEventTarget XMLHttpRequestUpload".replace(/\w+/g,function(b){var d=a[b]&&a[b].prototype;d&&d.hasOwnProperty&&d.hasOwnProperty("addEventListener")&&(t(d,"addEventListener",function(a){return function(b,d,e,f){return d&&d.handleEvent&&(d.handleEvent=c(d.handleEvent,{eventHandler:!0})),a.call(this,b,c(d,{eventHandler:!0}),e,f)}}),t(d,"removeEventListener",function(a){return function(b,d,e,f){return a.call(this,b,d,e,f),a.call(this,b,c(d),e,f)}}))})}a.Bugsnag=x,"function"==typeof define&&define.amd?define([],function(){return x}):"object"==typeof module&&"object"==typeof module.exports&&(module.exports=x)}(window,window.Bugsnag);
Bugsnag.apiKey = "2a86b308af5a81d2c9329fedfb4b30c7";
Bugsnag.appVersion = "911b9f8e49d2575c10338f8c585ea4a4ab3c7a36-1432427687";
Bugsnag.endpoint = "https://errors.slack-core.com/js";
Bugsnag.releaseStage = "prod";
Bugsnag.autoNotify = false;
Bugsnag.metaData = {};
Bugsnag.metaData.team = {id:"T048Y0J0L",name:"179KTeam4",domain:"team-badger"};
Bugsnag.refresh_interval = setInterval(function () { (window.TS && window.TS.client) ? Bugsnag.refresh() : clearInterval(Bugsnag.refresh_interval); }, 15 * 60 * 1000);
</script>			<script type="text/javascript">

	(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
	ga('create', 'UA-106458-17', 'slack.com');
	ga('send', 'pageview');


	(function(e,c,b,f,d,g,a){e.SlackBeaconObject=d;
	e[d]=e[d]||function(){(e[d].q=e[d].q||[]).push([1*new Date(),arguments])};
	e[d].l=1*new Date();g=c.createElement(b);a=c.getElementsByTagName(b)[0];
	g.async=1;g.src=f;a.parentNode.insertBefore(g,a)
	})(window,document,"script","https://slack.global.ssl.fastly.net/dcf8/js/libs/beacon.js","sb");
	sb('set', 'token', '3307f436963e02d4f9eb85ce5159744c');
	sb('track', 'pageview');

	function track(a){ga('send','event','web',a);sb('track',a);}


	
	(function(f,b){if(!b.__SV){var a,e,i,g;window.mixpanel=b;b._i=[];b.init=function(a,e,d){function f(b,h){var a=h.split(".");2==a.length&&(b=b[a[0]],h=a[1]);b[h]=function(){b.push([h].concat(Array.prototype.slice.call(arguments,0)))}}var c=b;"undefined"!==typeof d?c=b[d]=[]:d="mixpanel";c.people=c.people||[];c.toString=function(b){var a="mixpanel";"mixpanel"!==d&&(a+="."+d);b||(a+=" (stub)");return a};c.people.toString=function(){return c.toString(1)+".people (stub)"};i="disable track track_pageview track_links track_forms register register_once alias unregister identify name_tag set_config people.set people.set_once people.increment people.append people.track_charge people.clear_charges people.delete_user".split(" ");
	for(g=0;g<i.length;g++)f(c,i[g]);b._i.push([a,e,d])};b.__SV=1.2;a=f.createElement("script");a.type="text/javascript";a.async=!0;a.src="//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";e=f.getElementsByTagName("script")[0];e.parentNode.insertBefore(a,e)}})(document,window.mixpanel||[]);
	
	mixpanel.init("12d52d8633a5b432975592d13ebd3f34");

	function mixpanel_track(event_name){if(window.mixpanel&&event_name)mixpanel.track(event_name);}

</script>	
</head>

  <body >

		  			<script>
		
			var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
			if (w > 1440) document.querySelector('body').classList.add('widescreen');
		
		</script>
	
  	
	

	
			<header>
							<a href="https://slack.com/"  id="header_logo"><img src="https://slack.global.ssl.fastly.net/558b/img/slack_logo_240.png" /></a>
				<div class="header_nav">
																	<div class="header_links float_right">
							<a href="/is">Tour</a>
							<a href="http://slackhq.com" target="new">Blog</a>
							<a href="http://twitter.com/@slackhq" target="new">Twitter</a>
						</div>
									</div>
			
			
		</header>
	
	<div id="page" >

		<div id="page_contents" >

<div class="span_4_of_6 col float_none margin_auto no_right_padding">
			<p class="alert alert_info"><i class="ts_icon ts_icon_info_circle"></i> You need to sign in to see this page.</p>

	
											<p id="error_ratelimit" class="alert alert_warning" style="display: none;"><i class="ts_icon ts_icon_warning"></i> <strong>Too many login failures!</strong><br class="hide_on_mobile" /> For your team’s security complete the reCAPTCHA.</p>							<p id="error_unknown" class="alert alert_error" style="display: none;"><i class="ts_icon ts_icon_warning"></i> Hmmm... something went wrong. Please try again.</p>
</div>

<div class="real_content card align_center span_4_of_6 col float_none margin_auto large_bottom_margin right_padding">

	<h1> Sign in to <span class="break_word">team-badger.slack.com</span></h1>

	
		<div class="col span_4_of_6 float_none margin_auto large_bottom_margin">

			<form id="signin_form" action="/" method="post" accept-encoding="UTF-8">

				<input type="hidden" name="signin" value="1" />
				<input type="hidden" name="redir" value="/files/dustin/F0510DKBS/echoserver-simple.py" />
								<input type="hidden" name="crumb" value="s-1432523600-fcbd6075a8-☃" />

				<p>Enter your <strong>email address</strong> and <strong>password</strong>.</p>

				<p class=" no_bottom_margin">
					<input type="email" id="email" name="email" size="40" value="" placeholder="you@domain.com" />
				</p>

				<p class=" small_bottom_margin">
					<input type="password" id="password" name="password" size="40" placeholder="password" />
				</p>
				
				
					
									
				<p><button id="signin_btn" type="submit" class="btn btn_large full_width ladda-button" data-style="expand-right" /><span class="ladda-label">Sign in</span></button></p>

				<p><label class="checkbox"><input type="checkbox" name="remember" checked /> Keep me signed in</label></p>

									<p class="small"><a href="/forgot" class="bold">I forgot my password</a></p>
				
			</form>

			<div id="signup_prompt" class="signin_msg large_top_margin large_bottom_margin" style="display: none;">
				<hr class="half_width no_top_margin" />
				<p class="align_left">You don't have an account set up yet. But you can sign up with your <strong class="email_output"></strong> email address.</p>
				<p><a id="signup_link" href="/signup?email=" class="btn btn_large btn_info full_width">Create Account</a></p>
				<p class="small"><a class="restart_link bold">Or use a different email address</a></p>
			</div>

			<div id="user_not_found" class="signin_msg large_top_margin large_bottom_margin" style="display: none;">
				<hr class="half_width no_top_margin" />
				<p>We couldn't find an account matching <strong class="email_output"></strong></p>
				<p><a class="restart_link btn btn_outline full_width normal_wrap">Try a different email address</a></p>
			</div>

			<div id="user_disabled" class="signin_msg large_top_margin large_bottom_margin" style="display: none;">
				<hr class="half_width no_top_margin" />
				<p>It looks like the account matching <strong class="email_output"></strong> has been disabled. Contact your team administrator.</p>
				<p><a class="restart_link btn btn_outline full_width normal_wrap">Try a different email address</a></p>
			</div>

		</div>

		<p class="subtle_silver small">
					</p>

	
</div>

<div class="real_content align_center">
			<p>If you have an <strong>@ucr.edu</strong> email address, you can <a href="/signup/" class="bold">create an account</a>.</p>
	
	
			<p>Trying to create a team? <a href="https://slack.com/" class="bold">Sign up on the home page</a> to get started.</p>
	</div>


			
	</div>
	<div id="overlay"></div>
</div>




<script type="text/javascript">
var cdn_url = 'https://slack.global.ssl.fastly.net';
</script>

		
	<!-- output_js "core" -->
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/1852/js/libs/jquery-2.1.3.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/c212/js/libs/bootstrap_plastic.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/f66c/js/libs/flash_detect.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/4bdd/js/libs/fastclick.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/8556/js/libs/headroom.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/c15e/js/plastic.js" crossorigin="anonymous"></script>

			<!-- output_js "secondary" -->

		<!-- output_js "regular" -->
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/78f3/js/libs/warn_capslock.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/99d9/js/libs/spin.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://slack.global.ssl.fastly.net/f60e/js/libs/ladda.js" crossorigin="anonymous"></script>

		<script type="text/javascript">
					
				$('input[name="email"]').val() ? $('input[name="password"]').focus() : $('input[name="email"]').focus();
			
						
			if (navigator.userAgent.match(/windows phone/i)) {
				$('input[name="password"]').css('font-family', 'sans-serif,arial,verdana,tahoma');
			}
		

		

		var $signin_btn = $('#signin_btn');
		$signin_btn.data('ladda', Ladda.create(document.querySelector('#signin_btn')));

		var no_sso = false;
		var team_id = 'T048Y0J0L';
		var email_regex = new RegExp("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", 'i');

		// signin form
		$('#signin_form').on('submit', function(e) {

			var email = $.trim($('#email').val());
			var password = $.trim($('#password').val());

			// no email or invalid email
			if (!email || !email_regex.test(email)) {
				$('#email').focus().closest('p').addClass('error');
				e.preventDefault();
			} else {

				// no password
				if (!password) {
					$('#password').focus().closest('p').addClass('error');
					e.preventDefault();
				} else {
					$signin_btn.data('ladda').start();
				}

			}

		});

		// email check
		$('#email').on('blur', function(e) {

			var email = $.trim($('#email').val());

			// no email or invalid email
			if (!email || !email_regex.test(email)) return;

			$('.signin_msg').hide();

			$('.email_output').text(email);

			var api_args = {
				email: email,
				team: team_id
			};

			window.callSlackAPIUnauthed('auth.findUser', api_args, function(ok, data, args) {

					if (!ok) {

						if (data.error == 'user_not_found') {

							$('#user_not_found').slideDown(150);

						} else if (data.error == 'user_disabled') {

							$('#user_disabled').slideDown(150);

						} else if (data.error == 'ratelimited') {

							$('#error_ratelimit').slideDown(150);

						} else {

							$('#error_unknown').slideDown(150);

						}

						return;

					}

					if (data.found) {

						// do nothing: let the form submit

					} else if (data.can_join) {

						// no match found, but email matches whitelisted domain: show create account option
						$('#signup_prompt').slideDown(150);
						$('#signup_link').prop('href', '/signup?email='+encodeURIComponent(email)+(no_sso ? '&no_sso=1' : ''));

					}

				}

			);

		});

		// restart flow
		$('.restart_link').on('click', function() {

			$('.signin_msg').slideUp(150, function() {
				$('#email').val('').focus();
				$('.signin_msg').hide();
			});

		});

		
	</script>

	<!-- slack-www267 / 2015-05-24 20:13:20 / v911b9f8e49d2575c10338f8c585ea4a4ab3c7a36 -->

</body>
</html>