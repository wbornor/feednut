$(document).ready(TB_init);
function TB_init(){
$("a.thickbox").click(function(){
var t=this.title||this.name||null;
var g=this.rel||false;
TB_show(t,this.href,g);
this.blur();
return false;
});
}
function TB_show(_3,_4,_5){
try{
if(document.getElementById("TB_HideSelect")==null){
$("body").append("<iframe id='TB_HideSelect'></iframe><div id='TB_overlay'></div><div id='TB_window'></div>");
$("#TB_overlay").click(TB_remove);
}
if(_3==null){
_3="";
}
$(window).scroll(TB_position);
TB_overlaySize();
$("body").append("<div id='TB_load'><img src='/static/img/loadingAnimation.gif' /></div>");
TB_load_position();
var _6=/\.jpg|\.jpeg|\.png|\.gif|\.html|\.htm|\.php|\.cfm|\.asp|\.aspx|\.jsp|\.jst|\.rb|\.txt|\.bmp/g;
var _7=_4.toLowerCase().match(_6);
if(_7==".jpg"||_7==".jpeg"||_7==".png"||_7==".gif"||_7==".bmp"){
TB_PrevCaption="";
TB_PrevURL="";
TB_PrevHTML="";
TB_NextCaption="";
TB_NextURL="";
TB_NextHTML="";
TB_imageCount="";
TB_FoundURL=false;
if(_5){
TB_TempArray=$("a[@rel="+_5+"]").get();
for(TB_Counter=0;((TB_Counter<TB_TempArray.length)&&(TB_NextHTML==""));TB_Counter++){
var _8=TB_TempArray[TB_Counter].href.toLowerCase().match(_6);
if(!(TB_TempArray[TB_Counter].href==_4)){
if(TB_FoundURL){
TB_NextCaption=TB_TempArray[TB_Counter].title;
TB_NextURL=TB_TempArray[TB_Counter].href;
TB_NextHTML="<span id='TB_next'>&nbsp;&nbsp;<a href='#'>Next &gt;</a></span>";
}else{
TB_PrevCaption=TB_TempArray[TB_Counter].title;
TB_PrevURL=TB_TempArray[TB_Counter].href;
TB_PrevHTML="<span id='TB_prev'>&nbsp;&nbsp;<a href='#'>&lt; Prev</a></span>";
}
}else{
TB_FoundURL=true;
TB_imageCount="Image "+(TB_Counter+1)+" of "+(TB_TempArray.length);
}
}
}
imgPreloader=new Image();
imgPreloader.onload=function(){
imgPreloader.onload=null;
var _9=TB_getPageSize();
var x=_9[0]-150;
var y=_9[1]-150;
var _12=imgPreloader.width;
var _13=imgPreloader.height;
if(_12>x){
_13=_13*(x/_12);
_12=x;
if(_13>y){
_12=_12*(y/_13);
_13=y;
}
}else{
if(_13>y){
_12=_12*(y/_13);
_13=y;
if(_12>x){
_13=_13*(x/_12);
_12=x;
}
}
}
TB_WIDTH=_12+30;
TB_HEIGHT=_13+60;
$("#TB_window").append("<a href='' id='TB_ImageOff' title='Close'><img id='TB_Image' src='"+_4+"' width='"+_12+"' height='"+_13+"' alt='"+_3+"'/></a>"+"<div id='TB_caption'>"+_3+"<div id='TB_secondLine'>"+TB_imageCount+TB_PrevHTML+TB_NextHTML+"</div></div><div id='TB_closeWindow'><a href='#' id='TB_closeWindowButton' title='Close or Escape Button'>close</a></div>");
$("#TB_closeWindowButton").click(TB_remove);
if(!(TB_PrevHTML=="")){
function goPrev(){
if($(document).unclick(goPrev)){
$(document).unclick(goPrev);
}
$("#TB_window").remove();
$("body").append("<div id='TB_window'></div>");
$(document).unkeyup();
TB_show(TB_PrevCaption,TB_PrevURL,_5);
return false;
}
$("#TB_prev").click(goPrev);
$(document).keyup(function(e){
var key=e.keyCode;
if(key==37){
goPrev();
}
});
}
if(!(TB_NextHTML=="")){
function goNext(){
$("#TB_window").remove();
$("body").append("<div id='TB_window'></div>");
$(document).unkeyup();
TB_show(TB_NextCaption,TB_NextURL,_5);
return false;
}
$("#TB_next").click(goNext);
$(document).keyup(function(e){
var key=e.keyCode;
if(key==39){
goNext();
}
});
}
TB_position();
$("#TB_load").remove();
$("#TB_ImageOff").click(TB_remove);
$("#TB_window").css({display:"block"});
};
imgPreloader.src=_4;
}
if(_7==".htm"||_7==".html"||_7==".php"||_7==".asp"||_7==".aspx"||_7==".jsp"||_7==".jst"||_7==".rb"||_7==".txt"||_7==".cfm"||(_4.indexOf("TB_inline")!=-1)||(_4.indexOf("TB_iframe")!=-1)){
var _16=_4.replace(/^[^\?]+\??/,"");
var _17=TB_parseQuery(_16);
TB_WIDTH=(_17["width"]*1)+30;
TB_HEIGHT=(_17["height"]*1)+40;
ajaxContentW=TB_WIDTH-30;
ajaxContentH=TB_HEIGHT-45;
if(_4.indexOf("TB_iframe")!=-1){
urlNoQuery=_4.substr(0,TB_strpos(_4,"?"));
$("#TB_window").append("<div id='TB_title'><div id='TB_ajaxWindowTitle'>"+_3+"</div><div id='TB_closeAjaxWindow'><a href='#' id='TB_closeWindowButton'>close</a></div></div><iframe src='"+urlNoQuery+"' id='TB_iframeContent' style='width:"+(ajaxContentW+30)+"px;height:"+(ajaxContentH+18)+"px;'></iframe>");
}else{
$("#TB_window").append("<div id='TB_title'><div id='TB_ajaxWindowTitle'>"+_3+"</div><div id='TB_closeAjaxWindow'><a href='#' id='TB_closeWindowButton'>close</a></div></div><div id='TB_ajaxContent' style='width:"+ajaxContentW+"px;height:"+ajaxContentH+"px;'></div>");
}
$("#TB_closeWindowButton").click(TB_remove);
if(_4.indexOf("TB_inline")!=-1){
$("#TB_ajaxContent").html($("#"+_17["inlineId"]).html());
TB_position();
$("#TB_load").remove();
$("#TB_window").css({display:"block"});
}else{
if(_4.indexOf("TB_iframe")!=-1){
TB_position();
$("#TB_load").remove();
$("#TB_window").css({display:"block"});
}else{
$("#TB_ajaxContent").load(_4,function(){
TB_position();
$("#TB_load").remove();
$("#TB_window").css({display:"block"});
});
}
}
}
$(window).resize(TB_position);
}
catch(e){
alert(e);
}
}
function TB_remove(){
$("#TB_window").fadeOut("fast",function(){
$("#TB_window,#TB_overlay,#TB_HideSelect").remove();
});
$("#TB_load").remove();
$(document).unkeyup();
return false;
}
function TB_position(){
var _18=TB_getPageSize();
var _19=TB_getPageScrollTop();
$("#TB_window").css({width:TB_WIDTH+"px",left:((_18[0]-TB_WIDTH)/2)+"px",top:(_19[1]+((_18[1]-TB_HEIGHT)/2))+"px"});
TB_overlaySize();
}
function TB_overlaySize(){
if(window.innerHeight&&window.scrollMaxY){
yScroll=window.innerHeight+window.scrollMaxY;
}else{
if(document.body.scrollHeight>document.body.offsetHeight){
yScroll=document.body.scrollHeight;
}else{
yScroll=document.body.offsetHeight;
}
}
$("#TB_overlay").css("height",yScroll+"px");
}
function TB_load_position(){
var _20=TB_getPageSize();
var _21=TB_getPageScrollTop();
$("#TB_load").css({left:((_20[0]-100)/2)+"px",top:(_21[1]+((_20[1]-100)/2))+"px"}).css({display:"block"});
}
function TB_parseQuery(_22){
var _23=new Object();
if(!_22){
return _23;
}
var _24=_22.split(/[;&]/);
for(var i=0;i<_24.length;i++){
var _26=_24[i].split("=");
if(!_26||_26.length!=2){
continue;
}
var key=unescape(_26[0]);
var val=unescape(_26[1]);
val=val.replace(/\+/g," ");
_23[key]=val;
}
return _23;
}
function TB_getPageScrollTop(){
var _28;
if(self.pageYOffset){
_28=self.pageYOffset;
}else{
if(document.documentElement&&document.documentElement.scrollTop){
_28=document.documentElement.scrollTop;
}else{
if(document.body){
_28=document.body.scrollTop;
}
}
}
arrayPageScroll=new Array("",_28);
return arrayPageScroll;
}
function TB_getPageSize(){
var de=document.documentElement;
var w=window.innerWidth||self.innerWidth||(de&&de.clientWidth)||document.body.clientWidth;
var h=window.innerHeight||self.innerHeight||(de&&de.clientHeight)||document.body.clientHeight;
arrayPageSize=new Array(w,h);
return arrayPageSize;
}
function TB_strpos(str,ch){
for(var i=0;i<str.length;i++){
if(str.substring(i,i+1)==ch){
return i;
}
}
return -1;
}


