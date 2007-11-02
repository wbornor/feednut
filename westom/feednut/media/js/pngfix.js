function correctPNG(){
if(navigator.appVersion.indexOf("MSIE")!=-1){
var _1=navigator.appVersion.split("MSIE");
var _2=parseFloat(_1[1]);
if((_2>=5.5)&&(document.body.filters)){
fix_imgs(document);
}
}
}
function fix_imgs(_3){
if(navigator.appVersion.indexOf("MSIE")!=-1){
var _4=MochiKit.DOM.getElementsByTagAndClassName("img",null,_3);
for(var i=0,size=_4.length;i<size;i++){
var _6=_4[i];
var _7=_6.src.toUpperCase();
if(_7.substring(_7.length-3,_7.length)=="PNG"&&!MochiKit.DOM.hasElementClass(_6,"skip")){
fix_img(_6);
}
}
}
}
function fix_img(_8){
var _9=(_8.id)?"id='"+_8.id+"' ":"";
var _10=(_8.className)?"class='"+_8.className+"' ":"";
var _11=(_8.title)?"title='"+_8.title+"' ":"title='"+_8.alt+"' ";
var _12="display:inline-block;"+_8.style.cssText;
if(_8.align=="left"){
_12="float:left;"+_12;
}
if(_8.align=="right"){
_12="float:right;"+_12;
}
if(_8.parentElement.href){
_12="cursor:hand;"+_12;
}
var _13="<span "+_9+_10+_11+" style=\""+"width:"+_8.width+"px; height:"+_8.height+"px;"+_12+";"+"filter:progid:DXImageTransform.Microsoft.AlphaImageLoader"+"(src='"+_8.src+"', sizingMethod='scale');\"></span>";
_8.outerHTML=_13;
}


