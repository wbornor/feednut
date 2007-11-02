function rand(){return Math.floor(Math.random() * 10000);}


function hide(element)
{
	MochiKit.DOM.addElementClass(element, 'invisible');
}

function show(element)
{
	MochiKit.DOM.removeElementClass(element, 'invisible');
}

function toggle_visible(element)
{
	if (MochiKit.DOM.hasElementClass(element, 'invisible'))
		show(element);
	else
		hide(element);
}

function toggle_visible_after_delay(element)
{
	MochiKit.Async.wait(3).addCallback(function(res){
		toggle_visible(element);
	});
}

function eval_after_delay(fn, delay)
{
	if(MochiKit.Base.isUndefinedOrNull(delay))
		delay = 3;
	MochiKit.Async.wait(delay).addCallback(function(fn, res){
		eval(fn());
	}, fn);
}

function setup_entries(parentQuery)
{
    $('div.entry_title', parentQuery).css('width', '100%').click(function(evt){
    if ((evt.srcElement && evt.srcElement.nodeName== 'DIV') || (evt.target && evt.target.nodeName == 'DIV'))
    {
      var elems = $(this).find('../div.sum').filter('.hidden');
      if (elems.size() > 0){
        elems.removeClass('hidden').show("slow");
      }else{
        $(this).find('../div.sum').hide("slow").addClass('hidden');
      }
    }
  });
}

function redirect(url)
{
	MochiKit.DOM.currentWindow().location = url;
}

function redirect_after_delay(url, seconds)
{
	if(MochiKit.Base.isUndefinedOrNull(seconds))
		seconds = 3;
		
	MochiKit.Async.wait(seconds).addCallback(function(res){
		redirect(url);
	});
}

function set_status(status, msg, delay)
{
	if(MochiKit.Base.isUndefinedOrNull(delay))
		delay = 3;
	
	status.innerHTML = msg; 
	
	//this allows us to not hide the status if we don't want to
	if (delay > 0)
	{
		MochiKit.Async.wait(delay).addCallback(function(res){
			MochiKit.DOM.addElementClass(status, 'invisible');
			status.innerHTML='';
		});
	}
}

function init_user_page()
{
	init_main_msg();
	if (document.all)
		window.onscroll = float_msg;
	else
		setInterval('float_msg()', 100);
		
	if(NiftyCheck()){
        Rounded("div.block","all","transparent","#c3d9ff", "small");
        Rounded("div#tb_block","all","transparent","#c3d9ff", "small");
    }
	setupPanes("toolbar", "tagsTab");
	make_draggable();
	//MochiKit.Signal.connect(MochiKit.DOM.currentDocument(), 'onmousemove', mouse_move);
	
}

//var mouse_coords; //global
//function mouse_move(e)
//{
//	mouse_coords = e.mouse();
//}

function make_draggable()
{
	var cols = MochiKit.DOM.getElementsByTagAndClassName('div', 'column');
	for (var i=0, size=cols.length; i < size; ++i)
	{
		var col = cols[i];
		DragDrop.makeListContainer( col );
		col.onDragOver = function() { this.style["border"] = "1px dashed #AAA"; clear_main_msg();};
		col.onDragOut = function() {this.style["border"] = "1px solid #e0ecff"; clear_main_msg();};
	}
}

function toggle_acct()
{
	var block = MochiKit.DOM.$('acct');
	if (MochiKit.DOM.hasElementClass(block, 'invisible'))
	{
		var d = MochiKit.Async.doSimpleXMLHttpRequest("/captcha/g/?r=" + rand());
    	d.addCallback(function(block, result)
		{
			var json = MochiKit.Async.evalJSONRequest(result);
			MochiKit.DOM.$('acct_capimg').src = json['captcha_image'];
			MochiKit.DOM.$('acct_cap').value = json['captcha_id'];
			toggle_specialblock(block);
		}, block);
	}
	else
	{
		toggle_specialblock(block);
	}
}


function toggle_specialblock(id)
{
	var block = MochiKit.DOM.$(id);
	if (MochiKit.DOM.hasElementClass(block, 'invisible'))
	{
		var cols = MochiKit.DOM.getElementsByTagAndClassName('div', 'column');
		var col = cols[parseInt(cols.length / 2)];
		if (cols % 2 == 0)
			col = cols[parseInt(cols.length / 2) - 1];
		
		var blocks = MochiKit.DOM.getElementsByTagAndClassName('div', 'block', col);
		block.specialBlock = true;
		block.parentNode.removeChild(block);
		blocks.unshift(block);
		MochiKit.DOM.replaceChildNodes(col, blocks);
		MochiKit.DOM.toggleElementClass('invisible', block);
		DragDrop.makeItemDragable(block, col);
	}
	else
	{
		MochiKit.DOM.toggleElementClass('invisible', block);
		block.parentNode.removeChild(block);
		MochiKit.DOM.$('container').appendChild(block);
	}
}


function append_block(block)
{
	var cols = MochiKit.DOM.getElementsByTagAndClassName('div', 'column');
	cols.reverse();
	var leastcol = null;
	var least = null;
	var leastblocks = null;
	for (var i=0, size=cols.length; i < size; ++i)
	{
		var col = cols[i];
		var blocks = MochiKit.DOM.getElementsByTagAndClassName('div', 'block', col);
		var len = blocks.length;
		if (least == null || len < least)
		{
			least = len;
			leastcol = col;
			leastblocks = blocks;
		}
	}
	leastblocks.unshift(block);
	MochiKit.DOM.replaceChildNodes(leastcol, leastblocks);
	DragDrop.makeItemDragable(block, leastcol);
	
	if (navigator.appVersion.indexOf("MSIE")!=-1)
	{
		correctPNG();
	}
}

function form_to_anchor(form)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var link = MochiKit.DOM.A({'href' : form.action + "?" + qStr}, "");
	return link;
}


function subscribe(form, statusid, on_my_page, calling_link)
{
	if (MochiKit.Base.isUndefinedOrNull(on_my_page))
		on_my_page = false;
		
	if (MochiKit.Base.isUndefinedOrNull(calling_link))
		calling_link = false;
		
	//alert("calling_link: " + calling_link);
	
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var d = sendPOST("/feed/subscribe/?async", qStr);
	var status = MochiKit.DOM.$(statusid);
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Attempting to Subscribe...';
	d.addErrback(function(status, err)
	{	
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 404 )
		{
			set_status(status, 'Error - Unable to add feed. Invalid feed information.');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to add feed.');
		}
	}, status);
	d.addCallback(function(status, contents, on_my_page, calling_link, result)
	{
		var msg = "";
		
		if (result.status && result.status == 200)
		{
			if (result.responseText.length > 0)
			{
				if (on_my_page)
				{
					var div = MochiKit.DOM.DIV();
					div.innerHTML = result.responseText;
					div = div.childNodes[div.childNodes.length - 1];
					div.parentNode.removeChild(div);
					append_block(div);
					setup_entries($(div));
					var user = contents[1][MochiKit.Base.findValue(contents[0], 'user')];
					refresh_tags(user);
				}
				
				msg = 'Subscribed!';
				if(calling_link)				
					toggle_visible(calling_link);
			}
			else
			{
				msg = 'Already Subscribed!';
			}
		}
		else
		{
			msg = 'Error - Unable to subscribe to feed!';
		}
		
		set_main_msg(msg);
		set_status(status, msg);
		eval_after_delay(hideLightbox);
		
	}, status, contents, on_my_page, calling_link);
	return false;
}


//This returns a deferred object and sends a POST request
function sendPOST(url, params)
{
	var req = MochiKit.Async.getXMLHttpRequest();
	req.open('POST', url, true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.setRequestHeader("Content-length", params.length);
	req.setRequestHeader("Connection", "close");
	return MochiKit.Async.sendXMLHttpRequest(req, params);
}


function do_search(query, type, offset, limit, page_user)
{
	if (!query && !type)
	{
		var contents = MochiKit.DOM.formContents('search');
		var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	}
	else
	{
		var qStr = MochiKit.Base.queryString(['query', 'type', 'page_user'], [query, type, page_user]);
	}
	if (MochiKit.Base.isUndefinedOrNull(offset))
		offset = 0;
	if (MochiKit.Base.isUndefinedOrNull(limit))
		limit = 10;
	
	var status = MochiKit.DOM.getElementsByTagAndClassName('div', 'status', 'addsearch_main')[0];
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Searching...';
	
	var d = MochiKit.Async.doSimpleXMLHttpRequest('/feed/search/?' + qStr + '&o=' + offset + '&l=' + limit + '&r=' + rand());
	d.addCallbacks(function(result)
	{
		var elem = MochiKit.DOM.$('searchresults');
		elem.innerHTML = result.responseText;
		MochiKit.DOM.removeElementClass(elem, 'invisible');
		if (navigator.appVersion.indexOf("MSIE")!=-1)
		{
			correctPNG();
		}
		var status = MochiKit.DOM.getElementsByTagAndClassName('div', 'status', 'addsearch_main')[0];
		MochiKit.DOM.addElementClass(status, 'invisible');
		status.innerHTML='';
	});
}


function toggle_block(href, id)
{
	var id = MochiKit.DOM.$(id);
	var href = MochiKit.DOM.$(href);
	
	$(id).toggleClass("invisible");
	//MochiKit.DOM.toggleElementClass('invisible', id);
	var img = href.childNodes[0];
	//firefox
	if (!MochiKit.Base.isUndefinedOrNull(img.src))
	{
		var src = img.src;
		if (MochiKit.DOM.hasElementClass(id, 'invisible'))
			img.src = src.replace(/down/, "right");
		else
			img.src = src.replace(/right/, "down");
	}
	//IE
	else if (!MochiKit.Base.isUndefinedOrNull(img['outerHTML']))
	{
		var src = img.outerHTML;
		if (MochiKit.DOM.hasElementClass(id, 'invisible'))
			img.outerHTML = src.replace(/down/, "right");
		else
			img.outerHTML = src.replace(/right/, "down");
	}
	return false;
}

var REM_NO_PROMPT = ['addsearch'];
function remove_block(id, user)
{
	if (MochiKit.Base.findValue(REM_NO_PROMPT, id) == -1)
	{
		if (confirm("Are you sure you wish to remove this feed?\n (This un-subscribes you from the feed)"))
		{
			var qStr = MochiKit.Base.queryString(['id'], [id]);
			var d = sendPOST("/feed/remove/?async", qStr);
			d.addCallback(function(id, user, result)
			{
				MochiKit.DOM.removeElement('block_' + id);
				MochiKit.DOM.$('main_msg').innerHTML = 'Removed Feed!';
				MochiKit.DOM.removeElementClass('main_msg', 'invisible');
				
				set_main_msg("Removed Feed!");
				refresh_tags(user);
			}, id, user);
			
			d.addErrback(function(err)
			{
				if(err.number == 403)
				{
					set_main_msg('Error - Must be logged in to do that. Redirecting to login page...');
					redirect_after_delay('/');
				}
				else if(err.number == 404 )
				{
					set_main_msg('Error - Invalid feed information.');
				}
				else if(err.number == 500)
				{
					set_main_msg('Error - Unable to remove feed.');
				}
			});
		}
	}
	else
	{
		MochiKit.DOM.addElementClass(id, 'invisible');
	}
	return false;
}

function script_redirect()
{
	MochiKit.DOM.currentWindow().location = '/?script';
}

function clear_main_msg()
{
	MochiKit.DOM.$('main_msg').innerHTML="";
	MochiKit.DOM.addElementClass('main_msg', 'invisible');
}

var main_msg_d = null;
function set_main_msg(msg, clear)
{
	if (MochiKit.Base.isUndefinedOrNull(clear))
		clear = true;
	MochiKit.DOM.$('main_msg').innerHTML=msg;
	MochiKit.DOM.removeElementClass('main_msg', 'invisible');
	//now, let's wait for 5 seconds, then we'll make it disappear
	if (main_msg_d)
		main_msg_d.cancel();
	if (clear){
	 	main_msg_d = MochiKit.Async.wait(5);
		main_msg_d.addCallback(function(res){clear_main_msg();});
	}
}

function refresh_tags(username)
{
	var d = MochiKit.Async.doSimpleXMLHttpRequest('/' + username + '/tags/?r=' + rand());
	d.addCallbacks(function(result)
	{
		var utags = MochiKit.DOM.$('utags');
		var json = MochiKit.Async.evalJSONRequest(result);
		var tags = [];
		for (var i = 0, size=json.length; i < size; ++i)
		{
			var tag = json[i];
			var color = (i % 2 == 0 ? "navy" : "#0065D0");
			var div = MochiKit.DOM.SPAN(null, MochiKit.DOM.A({'style':'color:' + color + ';', 'href' : 'javascript:void(0)', 'onclick':'load_feeds(this, "' + username + '");'}, tag[0] + " (" + tag[1] + ")"));
			tags.push(div);
		}
		var div = MochiKit.DOM.SPAN(null, MochiKit.DOM.A({'href' : 'javascript:void(0)', 'onclick':'load_feeds(this, "' + username + '");'}, "fn:untagged"));
		tags.push(div);
		MochiKit.DOM.replaceChildNodes(utags, tags);
		var html = MochiKit.DOM.$('tagsTab').innerHTML;
		html = html.substring(0, html.indexOf('('));
		MochiKit.DOM.$('tagsTab').innerHTML = html + '(' + json.length + ')';
	});
}


function refresh_buddies(username)
{
	var d = MochiKit.Async.doSimpleXMLHttpRequest('/' + username + '/buddies/?r=' + rand());
	d.addCallbacks(function(result)
	{
		var friend_div = MochiKit.DOM.$('buddies');
		var json = MochiKit.Async.evalJSONRequest(result);
		var friends = [];
		for (var i = 0, size=json.length; i < size; ++i)
		{
			var friend = json[i];
			var color = (i % 2 == 0 ? "navy" : "#0065D0");
			var div = MochiKit.DOM.SPAN(null,
				MochiKit.DOM.A({'style':'color:' + color + ';', 'href' : '/' + friend + '/'}, friend),
				' ',
				MochiKit.DOM.A({'href':'javascript:void(0)', 'onclick':'del_buddy("' + username + '", "' + friend + '");'},
					MochiKit.DOM.IMG({'src':'/static/img/del_small.gif'})));
			friends.push(div);
		}
		MochiKit.DOM.replaceChildNodes(friend_div, friends);
		var html = MochiKit.DOM.$('budtitle').innerHTML;
		html = html.substring(0, html.indexOf('('));
		MochiKit.DOM.$('budtitle').innerHTML = html + '(' + json.length + ')';
	});
}


function tagIt(form)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var d = sendPOST("/feed/tag/?async", qStr);
	var id = contents[1][MochiKit.Base.findValue(contents[0], 'id')];
	var user = contents[1][MochiKit.Base.findValue(contents[0], 'user')];
	var status = MochiKit.DOM.$('tagst_' + id);
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Tagging...';
	d.addCallback(function(id, status, user, result)
	{
		var json = MochiKit.Async.evalJSONRequest(result);
		set_main_msg("Tagged Feed!");
		MochiKit.DOM.$('tags_' + id).value = json;
		status.innerHTML="Tagged Feed!";
		MochiKit.Async.wait(3).addCallback(function(res){
			MochiKit.DOM.addElementClass(status, 'invisible');
			status.innerHTML='';
		});
		refresh_tags(user);
	}, id, status, user);
	d.addErrback(function(status, err)
	{	
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 404 )
		{
			set_status(status, 'Error - Unable to tag feed.');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to tag feed.');
		}
	}, status);
	return false;
}



function add_buddy(user, buddy)
{
	var qStr = MochiKit.Base.queryString(['buddy'], [buddy]);
	var d = sendPOST("/" + user + "/buddies/add/?async", qStr);
	var status = MochiKit.DOM.$('addf_st2');
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Adding Buddy...';
	d.addCallback(add_buddy_cback, user, status);
	d.addErrback(function(status, err){
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 404 )
		{
			set_status(status, 'Error - Invalid buddy username.');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to add buddy.');
		}
	},status);
	return false;
}

function del_buddy(user, buddy)
{
	var qStr = MochiKit.Base.queryString(['buddy'], [buddy]);
	var d = sendPOST("/" + user + "/buddies/del/?async", qStr);
	var status = MochiKit.DOM.$('delf_st');
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Deleting Buddy...';
	d.addCallback(function(status, result)
	{
		var msg = 'Deleted Buddy!';
		set_main_msg(msg);
		status.innerHTML=msg;
		MochiKit.Async.wait(3).addCallback(function(res){
			MochiKit.DOM.addElementClass(status, 'invisible');
			status.innerHTML='';
		});
		refresh_buddies(user);
	}, status);
	d.addErrback(function(status, err){
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to remove buddy.');
		}
	},status);
	return false;
}

function add_buddy_f(form)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var user = contents[1][MochiKit.Base.findValue(contents[0], 'user')];
	var d = sendPOST("/" + user + "/buddies/add/?async", qStr);
	var status = MochiKit.DOM.$('addf_st');
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Adding Buddy...';
	d.addCallback(add_buddy_cback, user, status);
	d.addErrback(function(status, err){
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 404 )
		{
			set_status(status, 'Error - Invalid buddy username.');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to add buddy.');
		}
	},status);
	return false;
}


function add_buddy_cback(user, status, result)
{
	var msg = 'Added Buddy!';
	if (result.status && result.status == 200)
	{
		if (result.responseText.length == 0)
			refresh_buddies(user);
		else
			msg = result.responseText;
	}
	else
	{
		msg = 'Error - Unable to add Buddy';
	}
	set_main_msg(msg);
	status.innerHTML=msg;
	MochiKit.Async.wait(3).addCallback(function(res){
		MochiKit.DOM.addElementClass(status, 'invisible');
		status.innerHTML='';
	});
}


function move_feed(feed_id, dir)
{
	var block = MochiKit.DOM.$('block_' + feed_id);
	move_block(block, dir);
}

function move_block(block, dir)
{
	block = MochiKit.DOM.$(block);
	var col = block.parentNode;
	if (dir == 'down' || dir == 'd')
	{
		var next = DragUtils.nextItem(block);
		if (next)
			DragUtils.swap(next, block);
	}
	else if (dir == 'up' || dir == 'u')
	{
		var prev = DragUtils.previousItem(block);
		if (prev)
			DragUtils.swap(block, prev);
	}
	else if (dir == 'left' || dir == 'l' || dir == 'right' || dir == 'r')
	{
		//figure out the index in this col
		var index = 0;
		var item = block;
		while((item = DragUtils.previousItem(item)))
			index++;
		var newcol;
		if (dir == 'left' || dir == 'l')
			newcol = col.previousContainer;
		else
			newcol = col.nextContainer;
		if (newcol)
		{
			col.removeChild(block);
			var blocks = MochiKit.DOM.getElementsByTagAndClassName('div', 'block', newcol);
			var newblocks = [];
			for (var i = 0, size=blocks.length; i < size; ++i)
			{
				var b = blocks[i];
				if (i == index)
					newblocks.push(block);
				newblocks.push(b);
			}
			if (index >= newblocks.length)
				newblocks.push(block);
			block.container = newcol;
			MochiKit.DOM.replaceChildNodes(newcol, newblocks);
			//block.doSort();
		}
	}
}

function do_login(form, from_lbox)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var d = sendPOST("/login/", qStr);
	
	if (MochiKit.Base.isUndefinedOrNull(from_lbox))
		from_lbox = false;
	
	d.addCallback(function(from_lbox, result)
	{
		var append = '';
		if (from_lbox)
			append = '_lbox';
		var json = MochiKit.Async.evalJSONRequest(result);
		if (json['ok'])
		{
			if(json['next'])
				MochiKit.DOM.currentWindow().location = json['next'];
			else
				MochiKit.DOM.currentWindow().location = '/';
		}
		else
		{
			MochiKit.DOM.removeElementClass('user_lbl' + append, 'error');
			MochiKit.DOM.removeElementClass('pass_lbl' + append, 'error');
			var err = 'Invalid login attempt';
			if (json['bad_user'])
			{
				MochiKit.DOM.addElementClass('user_lbl' + append, 'error');
				err = json['bad_user'];
			}
			else if (json['bad_pass'])
			{
				MochiKit.DOM.addElementClass('pass_lbl' + append, 'error');
				err = json['bad_pass'];
			}
			MochiKit.DOM.replaceChildNodes(MochiKit.DOM.$('login_error' + append), MochiKit.DOM.DIV(err));
		}
	}, from_lbox);
	return false;
}


function register(form)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var d = sendPOST("/register/", qStr);
	$('#newacc_status').html('Registering...').show();
	
	d.addCallback(function(result)
	{
		var json = MochiKit.Async.evalJSONRequest(result);
		if (json['ok'])
		{
			$('#newacc_status').html('Registered! Redirecting...');
			
			if(json['next'])
				MochiKit.DOM.currentWindow().location = json['next'];
			else
				MochiKit.DOM.currentWindow().location = '/';
			
		}
		else
		{
			$('#newacc_status').hide();
			
			MochiKit.DOM.removeElementClass('newuser_lbl', 'error');
			MochiKit.DOM.removeElementClass('newpass_lbl', 'error');
			MochiKit.DOM.removeElementClass('newemail_lbl', 'error');
			MochiKit.DOM.removeElementClass('newcaptcha_lbl', 'error');
			var errs = [];
			if (json['bad_user'])
			{
				MochiKit.DOM.addElementClass('newuser_lbl', 'error');
				errs.push(MochiKit.DOM.DIV(json['bad_user']));
			}
			if (json['bad_pass'])
			{
				MochiKit.DOM.addElementClass('newpass_lbl', 'error');
				errs.push(MochiKit.DOM.DIV(json['bad_pass']));
			}
			if (json['bad_email'])
			{
				MochiKit.DOM.addElementClass('newemail_lbl', 'error');
				errs.push(MochiKit.DOM.DIV(json['bad_email']));
			}
			if (json['bad_captcha'])
			{
				MochiKit.DOM.addElementClass('newcaptcha_lbl', 'error');
				errs.push(MochiKit.DOM.DIV(json['bad_captcha']));
			}
			MochiKit.DOM.replaceChildNodes(MochiKit.DOM.$('newacc_error'), errs);
		}
	});
	
	return false;
}


function reset_tags()
{
	//set all tags to normal
	var tags_node = MochiKit.DOM.getElementsByTagAndClassName('div', 'tags', null)[0];
	var tags = MochiKit.DOM.getElementsByTagAndClassName('span', null, tags_node);
	for (var i = 0, size=tags.length; i < size; ++i)
		MochiKit.DOM.removeElementClass(tags[i], 'bigtag');
}


function less_hdr(div)
{
	if (navigator.appVersion.indexOf("MSIE")!=-1){
		MochiKit.Async.wait(1).addCallback(null);
	} 
	var controls = MochiKit.DOM.getElementsByTagAndClassName('div', 'controls', div);
	for (var i = 0, size = controls.length; i < size; ++i)
		MochiKit.DOM.addElementClass(controls[i], 'invisible');
}
function more_hdr(div)
{
	var controls = MochiKit.DOM.getElementsByTagAndClassName('div', 'controls', div);
	for (var i = 0, size = controls.length; i < size; ++i)
		MochiKit.DOM.removeElementClass(controls[i], 'invisible');
}

function load_feeds(tag_anchor, username)
{
	var tag = MochiKit.DOM.$(tag_anchor).innerHTML.split(" ")[0];
	set_main_msg("Loading '" + tag + "' Feeds", false);
	var d = MochiKit.Async.doSimpleXMLHttpRequest("/" + username + "/tags/" + tag + "/?async&r=" + rand());
	d.addCallback(function(tag, tag_anchor, result)
	{
		//first, hide the 'special' blocks
		if (!MochiKit.DOM.hasElementClass('addsearch', 'invisible'))
			toggle_specialblock('addsearch');
		
		var div = MochiKit.DOM.DIV();
		div.innerHTML = result.responseText;
		div = div.childNodes[div.childNodes.length - 1];
		div.parentNode.removeChild(div);
		MochiKit.DOM.swapDOM('feeds', div);
		
		reset_tags();
		MochiKit.DOM.addElementClass(tag_anchor.parentNode, 'bigtag');
		
		make_draggable();
		setup_entries(null);
		clear_main_msg();
		tag_anchor.blur();
		
		if(NiftyCheck())
    		Rounded("feeds##div.block","all","transparent","#c3d9ff", "small");
    	
		if (navigator.appVersion.indexOf("MSIE")!=-1)
		{
			correctPNG();
		}
	}, tag, tag_anchor);
}

function _read(id)
{
	var sumid = MochiKit.DOM.$('sum_' + id);
	var tid = MochiKit.DOM.$('t_' + id);
	var fid = id.substring(0, id.indexOf('_'));
	var sumdata = MochiKit.DOM.getElementsByTagAndClassName('div', 'sumdata', sumid)[0].innerHTML;
	var link = MochiKit.DOM.getElementsByTagAndClassName('a', null, sumid)[0].href;
	var title = MochiKit.DOM.getElementsByTagAndClassName('a', null, tid)[1].innerHTML;
	var xml_url = MochiKit.DOM.$('url_' + fid).innerHTML;
	var qStr = MochiKit.Base.queryString(['url', 'title', 'summary', 'xml_url'], [link, title, sumdata, xml_url]);
	var d = sendPOST("/feed/read/", qStr);
	d.addBoth(function(result){});
	return true;
}

function _read_later(id)
{
	var sumid = MochiKit.DOM.$('sum_' + id);
	var tid = MochiKit.DOM.$('t_' + id);
	var entry_link = MochiKit.DOM.$('entry_link_' + id);
	var fid = id.substring(0, id.indexOf('_'));
	var sumdata = MochiKit.DOM.getElementsByTagAndClassName('div', 'sumdata', sumid)[0].innerHTML;
	var link = entry_link.href;
	var title = entry_link.innerHTML;
	var xml_url = MochiKit.DOM.$('url_' + fid).innerHTML;
	var qStr = MochiKit.Base.queryString(['url', 'title', 'summary', 'xml_url'], [link, title, sumdata, xml_url]);
	var d = sendPOST("/feed/readlater/?async", qStr);
	var status = MochiKit.DOM.$('entryst_' + id);
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Saving...';
	d.addCallback(function(id, status, result)
	{
		if (result.status && result.status == 200)
		{
			status.innerHTML="Saved for Later!";		
		}
		else
		{
			status.innerHTML = 'Error - Unable to Save';
		}
		
		MochiKit.Async.wait(3).addCallback(function(res){
			MochiKit.DOM.addElementClass(status, 'invisible');
			status.innerHTML='';
		});
	}, id, status);
	d.addErrback(function(status, err)
	{	
		if(err.number == 403)
		{
			set_status(status, 'Error - Must be logged in to do that. Redirecting to login page...');
			redirect_after_delay('/');
		}
		else if(err.number == 404 )
		{
			set_status(status, 'Error - Invalid read later submission.');
		}
		else if(err.number == 500)
		{
			set_status(status, 'Error - Unable to save article for later.');
		}	
	}, status);
	
	return true;
}

function expand_art(id)
{
    $('div.entry_title', $('#' + id)).find('../div.sum').filter('.hidden').removeClass('hidden').show("fast");
}

function collapse_art(id)
{
	$('div.entry_title', $('#' + id)).find('../div.sum').not('.hidden').hide("fast").addClass('hidden');
}

function update_acct(username, form)
{
	var contents = MochiKit.DOM.formContents(form);
	var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
	var d = sendPOST("/" + username + "/update/", qStr);
	d.addCallback(function(result)
	{
		var json = MochiKit.Async.evalJSONRequest(result);
	});
	return false;
}


var panes = new Array();
function setupPanes(containerId, defaultTabId) {
     // go through the DOM, find each tab-container
     // set up the panes array with named panes
     if (!defaultTabId) defaultTabId = "tagsTab";
     panes[containerId] = new Array();
     var container = MochiKit.DOM.$(containerId);
     var paneContainer = MochiKit.DOM.getElementsByTagAndClassName(null, "tab-panes", container)[0];
     var paneList = paneContainer.childNodes;
     for (var i=0; i < paneList.length; i++ ) {
       var pane = paneList[i];
       if (pane.nodeType != 1) continue;
       panes[containerId][pane.id] = pane;
       MochiKit.DOM.addElementClass(pane, 'invisible');
     }
     MochiKit.DOM.getElement(defaultTabId).onclick();
     return;
}

function showPane(paneId, activeTab) {
     // make tab active class
     // hide other panes (siblings)
     // make pane visible
     
     for (var con in panes) {
       activeTab.blur();
       MochiKit.DOM.addElementClass(activeTab.parentNode, 'current');
       if (panes[con][paneId] != null) { // tab and pane are members of this container
         var pane = MochiKit.DOM.$(paneId);
         MochiKit.DOM.removeElementClass(pane, 'invisible');
         var container = MochiKit.DOM.$(con);
         var tabs = container.getElementsByTagName("ul")[0];
         var tabList = tabs.getElementsByTagName("li");
         for (var i=0; i < tabList.length; i++ ) {
           var tab = tabList[i];
           if (tab != activeTab.parentNode)
           {
           	 MochiKit.DOM.removeElementClass(tab, 'current');
           }
         }
         for (var i in panes[con]) {
           var pane = panes[con][i];
           if (pane == undefined) continue;
           if (pane.id == paneId) continue;
           MochiKit.DOM.addElementClass(pane, 'invisible');
         }
       }
     }
     return false;
}

function reload_feed(username, id)
{
	set_main_msg('Reloading Feed', false);
	var status = MochiKit.DOM.$('subsc_' + id);
	MochiKit.DOM.removeElementClass(status, 'invisible');
	status.innerHTML='Reloading Feed...';
	var d = MochiKit.Async.doSimpleXMLHttpRequest("/" + username + "/feed/" + id + "/?a=entries&r=" + rand());
	d.addCallback(function(id, status, result)
	{
		var json = MochiKit.Async.evalJSONRequest(result);
		var entries = json['entries'];
		var entryDivs = [];
		for (var j=0, sizej=entries.length; j < sizej; ++j)
		{
			var entry = entries[j];
			var entryDiv = MochiKit.DOM.DIV();
			entryDiv.innerHTML = entry;
			entryDivs.push(entryDiv);
		}
		var entryDiv = MochiKit.DOM.getElementsByTagAndClassName('div', 'entries', 'block_' + id)[0];
		MochiKit.DOM.replaceChildNodes(entryDiv, entryDivs);
		
		setup_entries($('#' + id));
		
		clear_main_msg();
		set_main_msg('Reloaded Feed!');
		status.innerHTML = 'Reloaded Feed!';
		MochiKit.Async.wait(3).addCallback(function(res){
			MochiKit.DOM.addElementClass(status, 'invisible');
			status.innerHTML='';
		});
		
		if (navigator.appVersion.indexOf("MSIE")!=-1)
		{
			correctPNG();
		}
	}, id, status);
	return false;
}


function forgot_password(form, st)
{
	var link = form_to_anchor(form);
	var d = MochiKit.Async.doSimpleXMLHttpRequest(link);
	var status = MochiKit.DOM.$(st);
	d.addCallback(function(status, result)
	{
		MochiKit.DOM.removeElementClass(status, 'invisible');
		set_status(status, result.responseText, 5);
		eval_after_delay(hideLightbox, 5);
	}, status);
	d.addErrback(function(status)
	{
		MochiKit.DOM.removeElementClass(status, 'invisible');
		set_status(status, "Uh oh! We can't find the specified e-mail in the system. (Or, a serious error occurred.)", 0);
		//eval_after_delay(hideLightbox);
	}, status);
}


var xoff = 220;
var yoff = 58;
function float_msg () {
	if (document.all) {
		document.all.main_msg.style.pixelTop = document.body.scrollTop + yoff + 10;
	}
	else if (document.layers) {
		document.main_msg.top = window.pageYOffset + yoff;
	}
	else if (document.getElementById) {
		MochiKit.DOM.$('main_msg').style.top = (window.pageYOffset + yoff) + 'px';
	}
}

function init_main_msg () {
	if (document.all) {
		document.all.main_msg.style.pixelLeft = document.body.clientWidth - document.all.main_msg.offsetWidth - xoff;
		document.all.main_msg.style.visibility = 'visible';
	}
	else if (document.layers) {
		document.main_msg.left = window.innerWidth - document.main_msg.clip.width - xoff;
		document.main_msg.visibility = 'show';
	}
	else if (document.getElementById) {
		MochiKit.DOM.$('main_msg').style.left = (window.innerWidth - xoff) + 'px';
		MochiKit.DOM.$('main_msg').style.visibility = 'visible';
	}
	float_msg();
}


function update_num_entries(form, username, feed_id)
{
    var contents = MochiKit.DOM.formContents(form);
    var qStr = MochiKit.Base.queryString(contents[0], contents[1]);
    var d = sendPOST(form.action, qStr);
	d.addCallback(function(username, feed_id, result)
	{
	    reload_feed(username, feed_id);
	}, username, feed_id);
}
