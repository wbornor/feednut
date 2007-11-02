window.undefined=window.undefined;
function jQuery(a,c){
if(a&&a.constructor==Function&&jQuery.fn.ready){
return jQuery(document).ready(a);
}
a=a||jQuery.context||document;
if(a.jquery){
return a;
}
if(c&&c.jquery){
return jQuery(c.get()).find(a);
}
if(window==this){
return new jQuery(a,c);
}
var m=/^[^<]*(<.+>)[^>]*$/.exec(a);
if(m){
a=jQuery.clean([m[1]]);
}
this.get(a.constructor==Array||a.length&&a[0]!=undefined&&a[0].nodeType?jQuery.merge(a,[]):jQuery.find(a,c));
var fn=arguments[arguments.length-1];
if(fn&&fn.constructor==Function){
this.each(fn);
}
}
if($){
jQuery._$=$;
}
var $=jQuery;
jQuery.fn=jQuery.prototype={jquery:"$Rev: 158 $",size:function(){
return this.length;
},get:function(_5){
if(_5&&_5.constructor==Array){
this.length=0;
[].push.apply(this,_5);
return this;
}else{
return _5==undefined?jQuery.map(this,function(a){
return a;
}):this[_5];
}
},each:function(fn,_6){
for(var i=0;i<this.length;i++){
fn.apply(this[i],_6||[i]);
}
return this;
},attr:function(_8,_9,_10){
return _8.constructor!=String||_9?this.each(function(){
if(_9==undefined){
for(var _11 in _8){
jQuery.attr(_10?this.style:this,_11,_8[_11]);
}
}else{
jQuery.attr(_10?this.style:this,_8,_9);
}
}):jQuery[_10||"attr"](this[0],_8);
},css:function(key,_13){
return this.attr(key,_13,"curCSS");
},text:function(e){
e=e||this;
var t="";
for(var j=0;j<e.length;j++){
var r=e[j].childNodes;
for(var i=0;i<r.length;i++){
t+=r[i].nodeType!=1?r[i].nodeValue:jQuery.fn.text([r[i]]);
}
}
return t;
},wrap:function(){
var a=jQuery.clean(arguments);
return this.each(function(){
var b=a[0].cloneNode(true);
this.parentNode.insertBefore(b,this);
while(b.firstChild){
b=b.firstChild;
}
b.appendChild(this);
});
},append:function(){
return this.domManip(arguments,true,1,function(a){
this.appendChild(a);
});
},prepend:function(){
return this.domManip(arguments,true,-1,function(a){
this.insertBefore(a,this.firstChild);
});
},before:function(){
return this.domManip(arguments,false,1,function(a){
this.parentNode.insertBefore(a,this);
});
},after:function(){
return this.domManip(arguments,false,-1,function(a){
this.parentNode.insertBefore(a,this.nextSibling);
});
},end:function(){
return this.get(this.stack.pop());
},find:function(t){
return this.pushStack(jQuery.map(this,function(a){
return jQuery.find(t,a);
}),arguments);
},filter:function(t){
return this.pushStack(t.constructor==Array&&jQuery.map(this,function(a){
for(var i=0;i<t.length;i++){
if(jQuery.filter(t[i],[a]).r.length){
return a;
}
}
})||t.constructor==Boolean&&(t?this.get():[])||t.constructor==Function&&jQuery.grep(this,t)||jQuery.filter(t,this).r,arguments);
},not:function(t){
return this.pushStack(t.constructor==String?jQuery.filter(t,this,false).r:jQuery.grep(this,function(a){
return a!=t;
}),arguments);
},add:function(t){
return this.pushStack(jQuery.merge(this,t.constructor==String?jQuery.find(t):t.constructor==Array?t:[t]),arguments);
},is:function(_19){
return _19?jQuery.filter(_19,this).r.length>0:this.length>0;
},domManip:function(_20,_21,dir,fn){
var _23=this.size()>1;
var a=jQuery.clean(_20);
return this.each(function(){
var obj=this;
if(_21&&this.nodeName=="TABLE"){
var _25=this.getElementsByTagName("tbody");
if(!_25.length){
obj=document.createElement("tbody");
this.appendChild(obj);
}else{
obj=_25[0];
}
}
for(var i=(dir<0?a.length-1:0);i!=(dir<0?dir:a.length);i+=dir){
fn.apply(obj,[_23?a[i].cloneNode(true):a[i]]);
}
});
},pushStack:function(a,_26){
var fn=_26&&_26[_26.length-1];
if(!fn||fn.constructor!=Function){
if(!this.stack){
this.stack=[];
}
this.stack.push(this.get());
this.get(a);
}else{
var old=this.get();
this.get(a);
if(fn.constructor==Function){
return this.each(fn);
}
this.get(old);
}
return this;
},extend:function(obj,_28){
if(!_28){
_28=obj;
obj=this;
}
for(var i in _28){
obj[i]=_28[i];
}
return obj;
}};
jQuery.extend=jQuery.fn.extend;
new function(){
var b=navigator.userAgent.toLowerCase();
jQuery.browser={safari:/webkit/.test(b),opera:/opera/.test(b),msie:/msie/.test(b)&&!/opera/.test(b),mozilla:/mozilla/.test(b)&&!/compatible/.test(b)};
jQuery.boxModel=!jQuery.browser.msie||document.compatMode=="CSS1Compat";
var _29={parent:"a.parentNode",ancestors:jQuery.parents,parents:jQuery.parents,next:"jQuery.sibling(a).next",prev:"jQuery.sibling(a).prev",siblings:jQuery.sibling};
for(var i in _29){
new function(){
var t=_29[i];
jQuery.fn[i]=function(a){
var ret=jQuery.map(this,t);
if(a&&a.constructor==String){
ret=jQuery.filter(a,ret).r;
}
return this.pushStack(ret,arguments);
};
};
}
var to=["append","prepend","before","after"];
for(var i=0;i<to.length;i++){
new function(){
var n=to[i];
jQuery.fn[n+"To"]=function(){
var a=arguments;
return this.each(function(){
for(var i=0;i<a.length;i++){
$(a[i])[n](this);
}
});
};
};
}
var _33={show:function(){
this.style.display=this.oldblock?this.oldblock:"";
if(jQuery.css(this,"display")=="none"){
this.style.display="block";
}
},hide:function(){
this.oldblock=jQuery.css(this,"display");
if(this.oldblock=="none"){
this.oldblock="block";
}
this.style.display="none";
},toggle:function(){
var d=jQuery.css(this,"display");
$(this)[!d||d=="none"?"show":"hide"]();
},addClass:function(c){
jQuery.className.add(this,c);
},removeClass:function(c){
jQuery.className.remove(this,c);
},toggleClass:function(c){
jQuery.className[jQuery.className.has(this,c)?"remove":"add"](this,c);
},remove:function(a){
if(!a||jQuery.filter([this],a).r){
this.parentNode.removeChild(this);
}
},empty:function(){
while(this.firstChild){
this.removeChild(this.firstChild);
}
},bind:function(_35,fn){
if(fn.constructor==String){
fn=new Function("e",(!fn.indexOf(".")?"$(this)":"return ")+fn);
}
jQuery.event.add(this,_35,fn);
},unbind:function(_36,fn){
jQuery.event.remove(this,_36,fn);
},trigger:function(_37,_38){
jQuery.event.trigger(_37,_38,this);
}};
for(var i in _33){
new function(){
var n=_33[i];
jQuery.fn[i]=function(){
return this.each(n,arguments);
};
};
}
var _39={val:"value",html:"innerHTML",value:null,id:null,title:null,name:null,href:null,src:null,rel:null};
for(var i in _39){
new function(){
var n=_39[i]||i;
jQuery.fn[i]=function(h){
return h==undefined?this.length?this[0][n]:null:this.attr(n,h);
};
};
}
var css="width,height,top,left,position,float,overflow,color,background".split(",");
for(var i in css){
new function(){
var n=css[i];
jQuery.fn[i]=function(h){
return h==undefined?(this.length?jQuery.css(this[0],n):null):this.css(n,h);
};
};
}
};
jQuery.extend({className:{add:function(o,c){
if(jQuery.className.has(o,c)){
return;
}
o.className+=(o.className?" ":"")+c;
},remove:function(o,c){
o.className=!c?"":o.className.replace(new RegExp("(^|\\s*\\b[^-])"+c+"($|\\b(?=[^-]))","g"),"");
},has:function(e,a){
if(e.className){
e=e.className;
}
return new RegExp("(^|\\s)"+a+"(\\s|$)").test(e);
}},swap:function(e,o,f){
for(var i in o){
e.style["old"+i]=e.style[i];
e.style[i]=o[i];
}
f.apply(e,[]);
for(var i in o){
e.style[i]=e.style["old"+i];
}
},css:function(e,p){
if(p=="height"||p=="width"){
var old={},oHeight,oWidth,d=["Top","Bottom","Right","Left"];
for(var i in d){
old["padding"+d[i]]=0;
old["border"+d[i]+"Width"]=0;
}
jQuery.swap(e,old,function(){
if(jQuery.css(e,"display")!="none"){
oHeight=e.offsetHeight;
oWidth=e.offsetWidth;
}else{
jQuery.swap(e,{visibility:"hidden",position:"absolute",display:""},function(){
oHeight=e.clientHeight;
oWidth=e.clientWidth;
});
}
});
return p=="height"?oHeight:oWidth;
}else{
if(p=="opacity"&&jQuery.browser.msie){
return parseFloat(jQuery.curCSS(e,"filter").replace(/[^0-9.]/,""))||1;
}
}
return jQuery.curCSS(e,p);
},curCSS:function(e,p,_45){
var r;
if(!_45&&e.style[p]){
r=e.style[p];
}else{
if(e.currentStyle){
p=p.replace(/\-(\w)/g,function(m,c){
return c.toUpperCase();
});
r=e.currentStyle[p];
}else{
if(document.defaultView&&document.defaultView.getComputedStyle){
p=p.replace(/([A-Z])/g,"-$1").toLowerCase();
var s=document.defaultView.getComputedStyle(e,"");
r=s?s.getPropertyValue(p):null;
}
}
}
return r;
},clean:function(a){
var r=[];
for(var i=0;i<a.length;i++){
if(a[i].constructor==String){
if(!a[i].indexOf("<tr")){
var tr=true;
a[i]="<table>"+a[i]+"</table>";
}else{
if(!a[i].indexOf("<td")||!a[i].indexOf("<th")){
var td=true;
a[i]="<table><tbody><tr>"+a[i]+"</tr></tbody></table>";
}
}
var div=document.createElement("div");
div.innerHTML=a[i];
if(tr||td){
div=div.firstChild.firstChild;
if(td){
div=div.firstChild;
}
}
for(var j=0;j<div.childNodes.length;j++){
r.push(div.childNodes[j]);
}
}else{
if(a[i].jquery||a[i].length&&!a[i].nodeType){
for(var k=0;k<a[i].length;k++){
r.push(a[i][k]);
}
}else{
if(a[i]!==null){
r.push(a[i].nodeType?a[i]:document.createTextNode(a[i].toString()));
}
}
}
}
return r;
},expr:{"":"m[2]== '*'||a.nodeName.toUpperCase()==m[2].toUpperCase()","#":"a.getAttribute('id')&&a.getAttribute('id')==m[2]",":":{lt:"i<m[3]-0",gt:"i>m[3]-0",nth:"m[3]-0==i",eq:"m[3]-0==i",first:"i==0",last:"i==r.length-1",even:"i%2==0",odd:"i%2","first-child":"jQuery.sibling(a,0).cur","last-child":"jQuery.sibling(a,0).last","only-child":"jQuery.sibling(a).length==1",parent:"a.childNodes.length",empty:"!a.childNodes.length",contains:"(a.innerText||a.innerHTML).indexOf(m[3])>=0",visible:"a.type!='hidden'&&jQuery.css(a,'display')!='none'&&jQuery.css(a,'visibility')!='hidden'",hidden:"a.type=='hidden'||jQuery.css(a,'display')=='none'||jQuery.css(a,'visibility')=='hidden'",enabled:"!a.disabled",disabled:"a.disabled",checked:"a.checked"},".":"jQuery.className.has(a,m[2])","@":{"=":"z==m[4]","!=":"z!=m[4]","^=":"!z.indexOf(m[4])","$=":"z.substr(z.length - m[4].length,m[4].length)==m[4]","*=":"z.indexOf(m[4])>=0","":"z"},"[":"jQuery.find(m[2],a).length"},token:["\\.\\.|/\\.\\.","a.parentNode",">|/","jQuery.sibling(a.firstChild)","\\+","jQuery.sibling(a).next","~",function(a){
var r=[];
var s=jQuery.sibling(a);
if(s.n>0){
for(var i=s.n;i<s.length;i++){
r.push(s[i]);
}
}
return r;
}],find:function(t,_51){
if(_51&&_51.nodeType==undefined){
_51=null;
}
_51=_51||jQuery.context||document;
if(t.constructor!=String){
return [t];
}
if(!t.indexOf("//")){
_51=_51.documentElement;
t=t.substr(2,t.length);
}else{
if(!t.indexOf("/")){
_51=_51.documentElement;
t=t.substr(1,t.length);
if(t.indexOf("/")>=1){
t=t.substr(t.indexOf("/"),t.length);
}
}
}
var ret=[_51];
var _52=[];
var _53=null;
while(t.length>0&&_53!=t){
var r=[];
_53=t;
t=jQuery.trim(t).replace(/^\/\//i,"");
var _54=false;
for(var i=0;i<jQuery.token.length;i+=2){
var re=new RegExp("^("+jQuery.token[i]+")");
var m=re.exec(t);
if(m){
r=ret=jQuery.map(ret,jQuery.token[i+1]);
t=jQuery.trim(t.replace(re,""));
_54=true;
}
}
if(!_54){
if(!t.indexOf(",")||!t.indexOf("|")){
if(ret[0]==_51){
ret.shift();
}
_52=jQuery.merge(_52,ret);
r=ret=[_51];
t=" "+t.substr(1,t.length);
}else{
var re2=/^([#.]?)([a-z0-9\\*_-]*)/i;
var m=re2.exec(t);
if(m[1]=="#"){
var oid=document.getElementById(m[2]);
r=ret=oid?[oid]:[];
t=t.replace(re2,"");
}else{
if(!m[2]||m[1]=="."){
m[2]="*";
}
for(var i=0;i<ret.length;i++){
r=jQuery.merge(r,m[2]=="*"?jQuery.getAll(ret[i]):ret[i].getElementsByTagName(m[2]));
}
}
}
}
if(t){
var val=jQuery.filter(t,r);
ret=r=val.r;
t=jQuery.trim(val.t);
}
}
if(ret&&ret[0]==_51){
ret.shift();
}
_52=jQuery.merge(_52,ret);
return _52;
},getAll:function(o,r){
r=r||[];
var s=o.childNodes;
for(var i=0;i<s.length;i++){
if(s[i].nodeType==1){
r.push(s[i]);
jQuery.getAll(s[i],r);
}
}
return r;
},attr:function(o,a,v){
if(a&&a.constructor==String){
var fix={"for":"htmlFor","class":"className","float":"cssFloat"};
a=(fix[a]&&fix[a].replace&&fix[a]||a).replace(/-([a-z])/ig,function(z,b){
return b.toUpperCase();
});
if(v!=undefined){
o[a]=v;
if(o.setAttribute&&a!="disabled"){
o.setAttribute(a,v);
}
}
return o[a]||o.getAttribute&&o.getAttribute(a)||"";
}else{
return "";
}
},parse:[["\\[ *(@)S *([!*$^=]*) *Q\\]",1],["(\\[)Q\\]",0],["(:)S\\(Q\\)",0],["([:.#]*)S",0]],filter:function(t,r,not){
var g=not!==false?jQuery.grep:function(a,f){
return jQuery.grep(a,f,true);
};
while(t&&/^[a-z[({<*:.#]/i.test(t)){
var p=jQuery.parse;
for(var i=0;i<p.length;i++){
var re=new RegExp("^"+p[i][0].replace("S","([a-z*_-][a-z0-9_-]*)").replace("Q"," *'?\"?([^'\"]*)'?\"? *"),"i");
var m=re.exec(t);
if(m){
if(p[i][1]){
m=["",m[1],m[3],m[2],m[4]];
}
t=t.replace(re,"");
break;
}
}
if(m[1]==":"&&m[2]=="not"){
r=jQuery.filter(m[3],r,false).r;
}else{
var f=jQuery.expr[m[1]];
if(f.constructor!=String){
f=jQuery.expr[m[1]][m[2]];
}
eval("f = function(a,i){"+(m[1]=="@"?"z=jQuery.attr(a,m[3]);":"")+"return "+f+"}");
r=g(r,f);
}
}
return {r:r,t:t};
},trim:function(t){
return t.replace(/^\s+|\s+$/g,"");
},parents:function(a){
var b=[];
var c=a.parentNode;
while(c&&c!=document){
b.push(c);
c=c.parentNode;
}
return b;
},sibling:function(a,n){
var _64=[];
var tmp=a.parentNode.childNodes;
for(var i=0;i<tmp.length;i++){
if(tmp[i].nodeType==1){
_64.push(tmp[i]);
}
if(tmp[i]==a){
_64.n=_64.length-1;
}
}
_64.last=_64.n==_64.length-1;
_64.cur=n=="even"&&_64.n%2==0||n=="odd"&&_64.n%2||_64[n]==a;
_64.prev=_64[_64.n-1];
_64.next=_64[_64.n+1];
return _64;
},merge:function(a,b){
var d=[];
for(var k=0;k<b.length;k++){
d[k]=b[k];
}
for(var i=0;i<a.length;i++){
var c=true;
for(var j=0;j<b.length;j++){
if(a[i]==b[j]){
c=false;
}
}
if(c){
d.push(a[i]);
}
}
return d;
},grep:function(a,f,s){
if(f.constructor==String){
f=new Function("a","i","return "+f);
}
var r=[];
for(var i=0;i<a.length;i++){
if(!s&&f(a[i],i)||s&&!f(a[i],i)){
r.push(a[i]);
}
}
return r;
},map:function(a,f){
if(f.constructor==String){
f=new Function("a","return "+f);
}
var r=[];
for(var i=0;i<a.length;i++){
var t=f(a[i],i);
if(t!==null&&t!=undefined){
if(t.constructor!=Array){
t=[t];
}
r=jQuery.merge(t,r);
}
}
return r;
},event:{add:function(_66,_67,_68){
if(jQuery.browser.msie&&_66.setInterval!=undefined){
_66=window;
}
if(!_68.guid){
_68.guid=this.guid++;
}
if(!_66.events){
_66.events={};
}
var _69=_66.events[_67];
if(!_69){
_69=_66.events[_67]={};
if(_66["on"+_67]){
_69[0]=_66["on"+_67];
}
}
_69[_68.guid]=_68;
_66["on"+_67]=this.handle;
if(!this.global[_67]){
this.global[_67]=[];
}
this.global[_67].push(_66);
},guid:1,global:{},remove:function(_70,_71,_72){
if(_70.events){
if(_71&&_70.events[_71]){
if(_72){
delete _70.events[_71][_72.guid];
}else{
for(var i in _70.events[_71]){
delete _70.events[_71][i];
}
}
}else{
for(var j in _70.events){
this.remove(_70,j);
}
}
}
},trigger:function(_73,_74,_75){
_74=_74||[];
if(!_75){
var g=this.global[_73];
if(g){
for(var i=0;i<g.length;i++){
this.trigger(_73,_74,g[i]);
}
}
}else{
if(_75["on"+_73]){
_74.unshift(this.fix({type:_73,target:_75}));
_75["on"+_73].apply(_75,_74);
}
}
},handle:function(_76){
_76=_76||jQuery.event.fix(window.event);
if(!_76){
return;
}
var _77=true;
var c=this.events[_76.type];
for(var j in c){
if(c[j].apply(this,[_76])===false){
_76.preventDefault();
_76.stopPropagation();
_77=false;
}
}
return _77;
},fix:function(_78){
if(_78){
_78.preventDefault=function(){
this.returnValue=false;
};
_78.stopPropagation=function(){
this.cancelBubble=true;
};
}
return _78;
}}});
jQuery.fn.extend({_show:jQuery.fn.show,show:function(_79,_80){
return _79?this.animate({height:"show",width:"show",opacity:"show"},_79,_80):this._show();
},_hide:jQuery.fn.hide,hide:function(_81,_82){
return _81?this.animate({height:"hide",width:"hide",opacity:"hide"},_81,_82):this._hide();
},slideDown:function(_83,_84){
return this.animate({height:"show"},_83,_84);
},slideUp:function(_85,_86){
return this.animate({height:"hide"},_85,_86);
},fadeIn:function(_87,_88){
return this.animate({opacity:"show"},_87,_88);
},fadeOut:function(_89,_90){
return this.animate({opacity:"hide"},_89,_90);
},fadeTo:function(_91,to,_92){
return this.animate({opacity:to},_91,_92);
},animate:function(_93,_94,_95){
return this.queue(function(){
var i=0;
for(var p in _93){
var e=new jQuery.fx(this,jQuery.speed(_94,_95,i++),p);
if(_93[p].constructor==Number){
e.custom(e.cur(),_93[p]);
}else{
e[_93[p]](_93);
}
}
});
},queue:function(_96,fn){
if(!fn){
fn=_96;
_96="fx";
}
return this.each(function(){
if(!this.queue){
this.queue={};
}
if(!this.queue[_96]){
this.queue[_96]=[];
}
this.queue[_96].push(fn);
if(this.queue[_96].length==1){
fn.apply(this);
}
});
}});
jQuery.extend({setAuto:function(e,p){
if(e.notAuto){
return;
}
if(p=="height"&&e.scrollHeight!=parseInt(jQuery.curCSS(e,p))){
return;
}
if(p=="width"&&e.scrollWidth!=parseInt(jQuery.curCSS(e,p))){
return;
}
var a=e.style[p];
var o=jQuery.curCSS(e,p,1);
if(p=="height"&&e.scrollHeight!=o||p=="width"&&e.scrollWidth!=o){
return;
}
e.style[p]=e.currentStyle?"":"auto";
var n=jQuery.curCSS(e,p,1);
if(o!=n&&n!="auto"){
e.style[p]=a;
e.notAuto=true;
}
},speed:function(s,o,i){
o=o||{};
if(o.constructor==Function){
o={complete:o};
}
var ss={slow:600,fast:200};
o.duration=(s&&s.constructor==Number?s:ss[s])||400;
o.oldComplete=o.complete;
o.complete=function(){
jQuery.dequeue(this,"fx");
if(o.oldComplete&&o.oldComplete.constructor==Function){
o.oldComplete.apply(this);
}
};
if(i>0){
o.complete=null;
}
return o;
},queue:{},dequeue:function(_98,_99){
_99=_99||"fx";
if(_98.queue&&_98.queue[_99]){
_98.queue[_99].shift();
var f=_98.queue[_99][0];
if(f){
f.apply(_98);
}
}
},fx:function(elem,_101,prop){
var z=this;
z.o={duration:_101.duration||400,complete:_101.complete};
z.el=elem;
var y=z.el.style;
z.a=function(){
if(prop=="opacity"){
if(z.now==1){
z.now=0.9999;
}
if(window.ActiveXObject){
y.filter="alpha(opacity="+z.now*100+")";
}else{
y.opacity=z.now;
}
}else{
if(parseInt(z.now)){
y[prop]=parseInt(z.now)+"px";
}
}
y.display="block";
};
z.max=function(){
return parseFloat(jQuery.css(z.el,prop));
};
z.cur=function(){
return parseFloat(jQuery.curCSS(z.el,prop))||z.max();
};
z.custom=function(from,to){
z.startTime=(new Date()).getTime();
z.now=from;
z.a();
z.timer=setInterval(function(){
z.step(from,to);
},13);
};
z.show=function(p){
if(!z.el.orig){
z.el.orig={};
}
z.el.orig[prop]=this.cur();
z.custom(0,z.el.orig[prop]);
if(prop!="opacity"){
y[prop]="1px";
}
};
z.hide=function(){
if(!z.el.orig){
z.el.orig={};
}
z.el.orig[prop]=this.cur();
z.o.hide=true;
z.custom(z.cur(),0);
};
if(jQuery.browser.msie&&!z.el.currentStyle.hasLayout){
y.zoom="1";
}
if(!z.el.oldOverlay){
z.el.oldOverflow=jQuery.css(z.el,"overflow");
}
if(z.el.oldOverlay=="visible"){
y.overflow="hidden";
}
z.step=function(_105,_106){
var t=(new Date()).getTime();
if(t>z.o.duration+z.startTime){
clearInterval(z.timer);
z.timer=null;
z.now=_106;
z.a();
if(z.o.hide){
y.display="none";
}
y.overflow=z.el.oldOverflow;
if(z.o.complete&&z.o.complete.constructor==Function){
z.o.complete.apply(z.el);
}
if(z.o.hide){
y[prop]=z.el.orig[prop].constructor==Number&&prop!="opacity"?z.el.orig[prop]+"px":z.el.orig[prop];
}
jQuery.setAuto(z.el,prop);
}else{
var p=(t-this.startTime)/z.o.duration;
z.now=((-Math.cos(p*Math.PI)/2)+0.5)*(_106-_105)+_105;
z.a();
}
};
}});
jQuery.fn.extend({_toggle:jQuery.fn.toggle,toggle:function(a,b){
return a&&b?this.click(function(e){
this.last=this.last==a?b:a;
e.preventDefault();
return this.last.apply(this,[e])||false;
}):this._toggle();
},hover:function(f,g){
function handleHover(e){
var p=(e.type=="mouseover"?e.fromElement:e.toElement)||e.relatedTarget;
while(p&&p!=this){
p=p.parentNode;
}
if(p==this){
return false;
}
return (e.type=="mouseover"?f:g).apply(this,[e]);
}
return this.mouseover(handleHover).mouseout(handleHover);
},ready:function(f){
if(jQuery.isReady){
f.apply(document);
}else{
jQuery.readyList.push(f);
}
return this;
}});
jQuery.extend({isReady:false,readyList:[],ready:function(){
if(!jQuery.isReady){
jQuery.isReady=true;
if(jQuery.readyList){
for(var i=0;i<jQuery.readyList.length;i++){
jQuery.readyList[i].apply(document);
}
jQuery.readyList=null;
}
}
}});
new function(){
var e=("blur,focus,load,resize,scroll,unload,click,dblclick,"+"mousedown,mouseup,mousemove,mouseover,mouseout,change,reset,select,"+"submit,keydown,keypress,keyup,error").split(",");
for(var i=0;i<e.length;i++){
new function(){
var o=e[i];
jQuery.fn[o]=function(f){
return f?this.bind(o,f):this.trigger(o);
};
jQuery.fn["un"+o]=function(f){
return this.unbind(o,f);
};
jQuery.fn["one"+o]=function(f){
return this.each(function(){
var _107=0;
jQuery.event.add(this,o,function(e){
if(_107++){
return;
}
return f.apply(this,[e]);
});
});
};
};
}
if(jQuery.browser.mozilla||jQuery.browser.opera){
document.addEventListener("DOMContentLoaded",jQuery.ready,false);
}else{
if(jQuery.browser.msie){
document.write("<scr"+"ipt id=__ie_init defer=true "+"src=//:></script>");
var _108=document.getElementById("__ie_init");
_108.onreadystatechange=function(){
if(this.readyState=="complete"){
jQuery.ready();
}
};
_108=null;
}else{
if(jQuery.browser.safari){
jQuery.safariTimer=setInterval(function(){
if(document.readyState=="loaded"||document.readyState=="complete"){
clearInterval(jQuery.safariTimer);
jQuery.safariTimer=null;
jQuery.ready();
}
},10);
}
}
}
jQuery.event.add(window,"load",jQuery.ready);
};
jQuery.fn.load=function(url,_110,_111){
if(url&&url.constructor==Function){
return this.bind("load",url);
}
var type="GET";
if(_110){
if(_110.constructor==Function){
_111=_110;
_110=null;
}else{
_110=jQuery.param(_110);
type="POST";
}
}
var self=this;
jQuery.ajax(type,url,_110,function(res){
self.html(res.responseText).each(function(){
if(_111&&_111.constructor==Function){
_111.apply(self,[res.responseText]);
}
});
$("script",self).each(function(){
eval(this.text||this.textContent||this.innerHTML||"");
});
});
return this;
};
if(jQuery.browser.msie){
XMLHttpRequest=function(){
return new ActiveXObject(navigator.userAgent.indexOf("MSIE 5")>=0?"Microsoft.XMLHTTP":"Msxml2.XMLHTTP");
};
}
new function(){
var e="ajaxStart,ajaxStop,ajaxComplete,ajaxError,ajaxSuccess".split(",");
for(var i=0;i<e.length;i++){
new function(){
var o=e[i];
jQuery.fn[o]=function(f){
return this.bind(o,f);
};
};
}
};
jQuery.extend({get:function(url,data,_116,type){
if(data.constructor==Function){
_116=data;
data=null;
}
if(data){
url+="?"+jQuery.param(data);
}
jQuery.ajax("GET",url,null,function(r){
if(_116){
_116(jQuery.httpData(r,type));
}
});
},post:function(url,data,_117,type){
jQuery.ajax("POST",url,jQuery.param(data),function(r){
if(_117){
_117(jQuery.httpData(r,type));
}
});
},ajax:function(type,url,data,ret){
if(!url){
ret=type.complete;
var _118=type.success;
var _119=type.error;
data=type.data;
url=type.url;
type=type.type;
}
if(!jQuery.active++){
jQuery.event.trigger("ajaxStart");
}
var xml=new XMLHttpRequest();
xml.open(type||"GET",url,true);
if(data){
xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
}
xml.setRequestHeader("X-Requested-With","XMLHttpRequest");
if(xml.overrideMimeType){
xml.setRequestHeader("Connection","close");
}
xml.onreadystatechange=function(){
if(xml.readyState==4){
if(jQuery.httpSuccess(xml)){
if(_118){
_118(xml);
}
jQuery.event.trigger("ajaxSuccess");
}else{
if(_119){
_119(xml);
}
jQuery.event.trigger("ajaxError");
}
jQuery.event.trigger("ajaxComplete");
if(!--jQuery.active){
jQuery.event.trigger("ajaxStop");
}
if(ret){
ret(xml);
}
xml.onreadystatechange=function(){
};
xml=null;
}
};
xml.send(data);
},active:0,httpSuccess:function(r){
try{
return r.status?(r.status>=200&&r.status<300)||r.status==304:location.protocol=="file:";
}
catch(e){
}
return false;
},httpData:function(r,type){
var ct=r.getResponseHeader("content-type");
var xml=(!type||type=="xml")&&ct&&ct.indexOf("xml")>=0;
return xml?r.responseXML:r.responseText;
},param:function(a){
var s=[];
if(a.constructor==Array){
for(var i=0;i<a.length;i++){
s.push(a[i].name+"="+encodeURIComponent(a[i].value));
}
}else{
for(var j in a){
s.push(j+"="+encodeURIComponent(a[j]));
}
}
return s.join("&");
}});
$.fn.ajaxSubmit=function(_122,_123,_124,url,mth){
if(!this.vars){
this.serialize();
}
if(_124&&_124.constructor==Function){
if(_124(this.vars)===false){
return;
}
}
var f=this.get(0);
var url=url||f.action||"";
var mth=mth||f.method||"POST";
if(_122&&_122.constructor==Function){
$.ajax(mth,url,$.param(this.vars),_122);
}else{
if(_122&&_122.constructor==String){
$(_122).load(url,this.vars,_123);
}else{
this.vars.push({name:"evaljs",value:1});
$.ajax(mth,url,$.param(this.vars),function(r){
eval(r.responseText);
});
}
}
return this;
};
$.fn.ajaxForm=function(_126,_127,_128){
return this.each(function(){
$("input[@type=\"submit\"],input[@type=\"image\"]",this).click(function(ev){
this.form.clicked=this;
if(ev.offsetX!=undefined){
this.form.clicked_x=ev.offsetX;
this.form.clicked_y=ev.offsetY;
}else{
this.form.clicked_x=ev.pageX-this.offsetLeft;
this.form.clicked_y=ev.pageY-this.offsetTop;
}
});
}).submit(function(e){
e.preventDefault();
$(this).ajaxSubmit(_126,_127,_128);
return false;
});
};
$.fn.formdata=function(){
this.serialize();
return this.vars;
};
$.fn.serialize=function(){
var a=[];
var ok={INPUT:true,TEXTAREA:true,OPTION:true};
$("*",this).each(function(){
if(this.disabled||this.type=="reset"||(this.type=="checkbox"&&!this.checked)||(this.type=="radio"&&!this.checked)){
return;
}
if(this.type=="submit"||this.type=="image"){
if(this.form.clicked!=this){
return;
}
if(this.type=="image"){
if(this.form.clicked_x){
a.push({name:this.name+"_x",value:this.form.clicked_x});
a.push({name:this.name+"_y",value:this.form.clicked_y});
return;
}
}
}
if(!ok[this.nodeName.toUpperCase()]){
return;
}
var par=this.parentNode;
var p=par.nodeName.toUpperCase();
if((p=="SELECT"||p=="OPTGROUP")&&!this.selected){
return;
}
var n=this.name;
if(!n){
n=(p=="OPTGROUP")?par.parentNode.name:(p=="SELECT")?par.name:this.name;
}
if(n==undefined){
return;
}
a.push({name:n,value:this.value});
});
this.vars=a;
return this;
};
$.drug=null;
$.dragstart=function(e){
this.dragElement.deltaX=e.clientX-this.dragElement.offsetLeft;
this.dragElement.deltaY=e.clientY-this.dragElement.offsetTop;
this.dragElement.oldPos=$.css(this.dragElement,"position");
this.dragElement.oldCursor=$.css(this.dragElement,"cursor");
this.dragElement.oldUserSelect=$.css(this.dragElement,"user-select");
$(this.dragElement).css("position","absolute").css("cursor","move").css("user-select","none");
$.drug=this.dragElement;
};
$.dragstop=function(e){
$.drug=null;
$(this).css("cursor",this.oldCursor).css("user-select",this.oldUserSelect);
};
$.drag=function(e){
if($.drug==null){
return;
}
var nx=(e.clientX-$.drug.deltaX);
var ny=(e.clientY-$.drug.deltaY);
nx=(nx<0)?0:nx;
nx=(nx+$.drug.offsetWidth)>document.width?document.width-$.drug.offsetWidth:nx;
ny=(ny<window.scrollY)?window.scrollY:ny;
ny=(ny+$.drug.offsetHeight)>window.innerHeight+window.scrollY?window.innerHeight+window.scrollY-$.drug.offsetHeight:ny;
$($.drug).css("left",nx+"px").css("top",ny+"px");
};
$.draginit=false;
$.fn.Draggable=function(_134){
if(!$.draginit){
$(document).bind("mousemove",$.drag);
}
return this.each(function(){
var dhe=_134?$(this).find(_134):$(this);
dhe.get(0).dragElement=this;
dhe.bind("mousedown",$.dragstart).bind("mouseup",$.dragstop);
});
};


