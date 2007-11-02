var main_msg_d=null;
function set_main_msg(_1,_2){
if(MochiKit.Base.isUndefinedOrNull(_2)){
_2=true;
}
$("main_msg").innerHTML=_1;
MochiKit.DOM.removeElementClass("main_msg","invisible");
if(main_msg_d){
main_msg_d.cancel();
}
if(_2){
main_msg_d=MochiKit.Async.wait(5);
main_msg_d.addCallback(function(_3){
clear_main_msg();
});
}
}
var loadingImage="/static/img/loading1.gif";
function getPageScroll(){
var _4;
if(self.pageYOffset){
_4=self.pageYOffset;
}else{
if(document.documentElement&&document.documentElement.scrollTop){
_4=document.documentElement.scrollTop;
}else{
if(document.body){
_4=document.body.scrollTop;
}
}
}
arrayPageScroll=new Array("",_4);
return arrayPageScroll;
}
function getPageSize(){
var _5,yScroll;
if(window.innerHeight&&window.scrollMaxY){
_5=document.body.scrollWidth;
yScroll=window.innerHeight+window.scrollMaxY;
}else{
if(document.body.scrollHeight>document.body.offsetHeight){
_5=document.body.scrollWidth;
yScroll=document.body.scrollHeight;
}else{
_5=document.body.offsetWidth;
yScroll=document.body.offsetHeight;
}
}
var _6,windowHeight;
if(self.innerHeight){
_6=self.innerWidth;
windowHeight=self.innerHeight;
}else{
if(document.documentElement&&document.documentElement.clientHeight){
_6=document.documentElement.clientWidth;
windowHeight=document.documentElement.clientHeight;
}else{
if(document.body){
_6=document.body.clientWidth;
windowHeight=document.body.clientHeight;
}
}
}
if(yScroll<windowHeight){
pageHeight=windowHeight;
}else{
pageHeight=yScroll;
}
if(_5<_6){
pageWidth=_6;
}else{
pageWidth=_5;
}
arrayPageSize=new Array(pageWidth,pageHeight,_6,windowHeight);
return arrayPageSize;
}
function pause(_7){
var _8=new Date();
var _9=_8.getTime()+_7;
while(true){
_8=new Date();
if(_8.getTime()>_9){
return;
}
}
}
function showLightbox(_10){
var _11=document.getElementById("overlay");
var _12=document.getElementById("lightbox");
var _13=document.getElementById("lightboxCaption");
var _14=document.getElementById("lightboxImage");
var _15=document.getElementById("loadingImage");
var _16=document.getElementById("lightboxDetails");
var _17=getPageSize();
var _18=getPageScroll();
if(_15){
_15.style.top=(_18[1]+((_17[3]-35-_15.height)/2)+"px");
_15.style.left=(((_17[0]-20-_15.width)/2)+"px");
_15.style.display="block";
}
_11.style.height=(_17[1]+"px");
_11.style.display="block";
var d=MochiKit.Async.doSimpleXMLHttpRequest(_10.href);
d.addErrback(function(_20,err){
if(err.number==403){
set_main_msg("Must be logged in to do that. Redirecting to login page...");
redirect_after_delay("/");
}else{
if(err.number==404){
set_main_msg("Error - Invalid information.");
}else{
if(err.number==500){
set_status("Error - Internal Server Error.");
}
}
}
},status);
d.addCallback(function(_22){
_14.innerHTML=_22.responseText;
_12.style.display="block";
var dim=MochiKit.DOM.elementDimensions(_14);
_12.style.display="none";
var _24=_18[1]+((_17[3]-35-dim.h)/4);
var _25=((_17[0]-20-dim.w)/2);
_12.style.top=(_24<0)?"0px":_24+"px";
_12.style.left=(_25<0)?"0px":_25+"px";
_16.style.width=dim.w+"px";
if(_10.getAttribute("title")){
_13.style.display="block";
_13.innerHTML=_10.getAttribute("title");
}else{
_13.style.display="none";
}
if(navigator.appVersion.indexOf("MSIE")!=-1){
pause(250);
}
if(_15){
_15.style.display="none";
}
selects=document.getElementsByTagName("select");
for(i=0;i!=selects.length;i++){
selects[i].style.visibility="hidden";
}
_12.style.display="block";
_17=getPageSize();
_11.style.height=(_17[1]+"px");
});
}
function hideLightbox(){
objOverlay=document.getElementById("overlay");
objLightbox=document.getElementById("lightbox");
objOverlay.style.display="none";
objLightbox.style.display="none";
selects=document.getElementsByTagName("select");
for(i=0;i!=selects.length;i++){
selects[i].style.visibility="visible";
}
}
function initLightbox(){
if(!document.getElementsByTagName){
return;
}
var _26=document.getElementsByTagName("a");
for(var i=0;i<_26.length;i++){
var _28=_26[i];
if(_28.getAttribute("href")&&(_28.getAttribute("rel")=="lightbox")){
_28.onclick=function(){
showLightbox(this);
return false;
};
}
}
var _29=document.getElementsByTagName("body").item(0);
var _30=document.createElement("div");
_30.setAttribute("id","overlay");
_30.onclick=function(){
hideLightbox();
return false;
};
_30.style.display="none";
_30.style.position="absolute";
_30.style.top="0";
_30.style.left="0";
_30.style.zIndex="90";
_30.style.width="100%";
_29.insertBefore(_30,_29.firstChild);
var _31=getPageSize();
var _32=getPageScroll();
var _33=new Image();
_33.onload=function(){
var _34=document.createElement("a");
_34.setAttribute("href","#");
_34.onclick=function(){
hideLightbox();
return false;
};
_30.appendChild(_34);
var _35=document.createElement("img");
_35.src=loadingImage;
_35.setAttribute("id","loadingImage");
_35.style.position="absolute";
_35.style.zIndex="150";
_34.appendChild(_35);
_33.onload=function(){
};
return false;
};
_33.src=loadingImage;
var _36=document.createElement("div");
_36.setAttribute("id","lightbox");
_36.style.display="none";
_36.style.position="absolute";
_36.style.zIndex="100";
_29.insertBefore(_36,_30.nextSibling);
var _37=document.createElement("div");
_37.setAttribute("id","lightboxImage");
_36.appendChild(_37);
var _38=document.createElement("div");
_38.setAttribute("id","lightboxDetails");
_36.appendChild(_38);
var _39=document.createElement("div");
_39.setAttribute("id","lightboxCaption");
_39.style.display="none";
_38.appendChild(_39);
var _40=document.createElement("div");
_40.setAttribute("id","keyboardMsg");
_40.innerHTML="";
_38.appendChild(_40);
}


