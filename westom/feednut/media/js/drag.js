var NO_DRAG_TAGS=["INPUT","A","IMG"];
var Drag={BIG_Z_INDEX:10000,group:null,isDragging:false,makeDraggable:function(_1){
_1.handle=_1;
_1.handle.group=_1;
_1.minX=null;
_1.minY=null;
_1.maxX=null;
_1.maxY=null;
_1.threshold=0;
_1.thresholdY=0;
_1.thresholdX=0;
_1.onDragStart=new Function();
_1.onDragEnd=new Function();
_1.onDrag=new Function();
_1.setDragHandle=Drag.setDragHandle;
_1.setDragThreshold=Drag.setDragThreshold;
_1.setDragThresholdX=Drag.setDragThresholdX;
_1.setDragThresholdY=Drag.setDragThresholdY;
_1.constrain=Drag.constrain;
_1.constrainVertical=Drag.constrainVertical;
_1.constrainHorizontal=Drag.constrainHorizontal;
_1.onmousedown=Drag.onMouseDown;
},constrainVertical:function(){
var _2=Coordinates.northwestOffset(this,true);
this.minX=_2.x;
this.maxX=_2.x;
},constrainHorizontal:function(){
var _3=Coordinates.northwestOffset(this,true);
this.minY=_3.y;
this.maxY=_3.y;
},constrain:function(_4,_5){
this.minX=_4.x;
this.minY=_4.y;
this.maxX=_5.x;
this.maxY=_5.y;
},setDragHandle:function(_6){
if(_6&&_6!=null){
this.handle=_6;
}else{
this.handle=this;
}
this.handle.group=this;
this.onmousedown=null;
this.handle.onmousedown=Drag.onMouseDown;
},setDragThreshold:function(_7){
if(isNaN(parseInt(_7))){
return;
}
this.threshold=_7;
},setDragThresholdX:function(_8){
if(isNaN(parseInt(_8))){
return;
}
this.thresholdX=_8;
},setDragThresholdY:function(_9){
if(isNaN(parseInt(_9))){
return;
}
this.thresholdY=_9;
},onMouseDown:function(_10){
_10=Drag.fixEvent(_10);
var _11=null;
var _12=null;
if(_10.target){
_11=_10.target.tagName;
_12=_10.target;
}else{
if(_10.srcElement){
_11=_10.srcElement.tagName;
_12=_10.srcElement;
}
}
if(!(_12.parentNode.className=="blockhdr"||_12.parentNode.parentNode.parentNode.parentNode.className=="blockhdr"||_12.parentNode.parentNode.parentNode.parentNode.parentNode.className=="blockhdr")){
return true;
}
if(MochiKit.Base.findValue(NO_DRAG_TAGS,_11)!=-1){
return true;
}
Drag.group=this.group;
var _13=this.group;
var _14=_10.windowCoordinate;
var _15=Coordinates.northwestOffset(_13,true);
var _16=Coordinates.northwestPosition(_13);
var _17=Coordinates.southeastPosition(_13);
var _18=Coordinates.southeastOffset(_13,true);
_13.originalOpacity=_13.style.opacity;
_13.originalZIndex=_13.style.zIndex;
_13.initialWindowCoordinate=_14;
_13.dragCoordinate=_14;
_13.onDragStart(_16,_17,_15,_18);
if(_13.minX!=null){
_13.minMouseX=_14.x-_16.x+_13.minX-_15.x;
}
if(_13.maxX!=null){
_13.maxMouseX=_13.minMouseX+_13.maxX-_13.minX;
}
if(_13.minY!=null){
_13.minMouseY=_14.y-_16.y+_13.minY-_15.y;
}
if(_13.maxY!=null){
_13.maxMouseY=_13.minMouseY+_13.maxY-_13.minY;
}
_13.mouseMin=new Coordinate(_13.minMouseX,_13.minMouseY);
_13.mouseMax=new Coordinate(_13.maxMouseX,_13.maxMouseY);
document.onmousemove=Drag.onMouseMove;
document.onmouseup=Drag.onMouseUp;
return false;
},showStatus:function(_19,_20,_21,_22,_23){
window.status="mouse: "+_19.toString()+"    "+"NW pos: "+_20.toString()+"    "+"SE pos: "+_21.toString()+"    "+"NW offset: "+_22.toString()+"    "+"SE offset: "+_23.toString();
},onMouseMove:function(_24){
_24=Drag.fixEvent(_24);
var _25=Drag.group;
var _26=_24.windowCoordinate;
var _27=Coordinates.northwestOffset(_25,true);
var _28=Coordinates.northwestPosition(_25);
var _29=Coordinates.southeastPosition(_25);
var _30=Coordinates.southeastOffset(_25,true);
if(!Drag.isDragging){
if(_25.threshold>0){
var _31=_25.initialWindowCoordinate.distance(_26);
if(_31<_25.threshold){
return true;
}
}else{
if(_25.thresholdY>0){
var _32=Math.abs(_25.initialWindowCoordinate.y-_26.y);
if(_32<_25.thresholdY){
return true;
}
}else{
if(_25.thresholdX>0){
var _33=Math.abs(_25.initialWindowCoordinate.x-_26.x);
if(_33<_25.thresholdX){
return true;
}
}
}
}
Drag.isDragging=true;
_25.style["zIndex"]=Drag.BIG_Z_INDEX;
_25.style["opacity"]=0.75;
}
var _34=_26.constrain(_25.mouseMin,_25.mouseMax);
_28=_28.plus(_34.minus(_25.dragCoordinate));
_28.reposition(_25);
_25.dragCoordinate=_34;
var _35=Coordinates.northwestOffset(_25,true);
_25.onDrag(_28,_29,_27,_30);
var _36=Coordinates.northwestOffset(_25,true);
if(!_35.equals(_36)){
var _37=_35.minus(_36);
_28=Coordinates.northwestPosition(_25).plus(_37);
_28.reposition(_25);
}
return false;
},onMouseUp:function(_38){
_38=Drag.fixEvent(_38);
var _39=Drag.group;
var _40=_38.windowCoordinate;
var _41=Coordinates.northwestOffset(_39,true);
var _42=Coordinates.northwestPosition(_39);
var _43=Coordinates.southeastPosition(_39);
var _44=Coordinates.southeastOffset(_39,true);
document.onmousemove=null;
document.onmouseup=null;
_39.onDragEnd(_42,_43,_41,_44);
if(Drag.isDragging){
_39.style["zIndex"]=_39.originalZIndex;
_39.style["opacity"]=_39.originalOpacity;
}
Drag.group=null;
Drag.isDragging=false;
return false;
},fixEvent:function(_45){
if(typeof _45=="undefined"){
_45=window.event;
}
Coordinates.fixEvent(_45);
return _45;
}};


