var DragDrop={firstContainer:null,lastContainer:null,makeListContainer:function(_1){
if(this.firstContainer==null){
this.firstContainer=this.lastContainer=_1;
_1.previousContainer=null;
_1.nextContainer=null;
}else{
_1.previousContainer=this.lastContainer;
_1.nextContainer=null;
this.lastContainer.nextContainer=_1;
this.lastContainer=_1;
}
_1.onDragOver=new Function();
_1.onDragOut=new Function();
var _2=_1.getElementsByTagName("div");
for(var i=0;i<_2.length;i++){
DragDrop.makeItemDragable(_2[i],_1);
}
},makeItemDragable:function(_4,_5){
Drag.makeDraggable(_4);
_4.setDragThreshold(5);
_4.isOutside=false;
_4.onDragStart=DragDrop.onDragStart;
_4.onDrag=DragDrop.onDrag;
_4.onDragEnd=DragDrop.onDragEnd;
_4.doSort=DragDrop.doSort;
_4.container=_5;
},onDragStart:function(_6,_7,_8,_9){
var _10=DragDrop.firstContainer;
while(_10!=null){
_10.northwest=Coordinates.northwestOffset(_10,true);
_10.southeast=Coordinates.southeastOffset(_10,true);
_10=_10.nextContainer;
}
if(this.parentNode.onDragOver){
this.parentNode.onDragOver();
}
},onDrag:function(_11,_12,_13,_14){
if(this.isOutside){
var _15=DragDrop.firstContainer;
while(_15!=null){
if(_13.inside(_15.northwest,_15.southeast)||_14.inside(_15.northwest,_15.southeast)){
_15.onDragOver();
this.isOutside=false;
var _16=this.parentNode;
_16.removeChild(this);
MochiKit.DOM.updateNodeAttributes(this,{"style":{"width":null,"height":null}});
_15.appendChild(this);
_16.parentNode.removeChild(_16);
break;
}
_15=_15.nextContainer;
}
if(this.isOutside){
return;
}
}else{
if(!(_13.inside(this.parentNode.northwest,this.parentNode.southeast)||_14.inside(this.parentNode.northwest,this.parentNode.southeast))){
this.parentNode.onDragOut();
this.isOutside=true;
var _15=DragDrop.firstContainer;
while(_15!=null){
if(_13.inside(_15.northwest,_15.southeast)||_14.inside(_15.northwest,_15.southeast)){
_15.onDragOver();
this.isOutside=false;
this.parentNode.removeChild(this);
_15.appendChild(this);
break;
}
_15=_15.nextContainer;
}
if(this.isOutside){
var _16=this.parentNode.cloneNode(false);
var dim=MochiKit.DOM.elementDimensions(this);
this.parentNode.removeChild(this);
_16.appendChild(this);
document.getElementsByTagName("body").item(0).appendChild(_16);
MochiKit.DOM.setElementDimensions(this,dim);
return;
}
}
}
this.container=this.parentNode;
this.doSort();
},doSort:function(){
var _18=this.parentNode;
var _19=this;
var _20=DragUtils.nextItem(_19);
while(_20!=null&&this.offsetTop>=_20.offsetTop-2){
var _19=_20;
var _20=DragUtils.nextItem(_19);
}
if(this!=_19){
DragUtils.swap(this,_20);
return;
}
var _19=this;
var _21=DragUtils.previousItem(_19);
while(_21!=null&&this.offsetTop<=_21.offsetTop+2){
var _19=_21;
var _21=DragUtils.previousItem(_19);
}
if(this!=_19){
DragUtils.swap(this,_19);
return;
}
},onDragEnd:function(_22,_23,_24,_25){
if(this.isOutside){
var _26=this.parentNode;
this.parentNode.removeChild(this);
_26.parentNode.removeChild(_26);
MochiKit.DOM.updateNodeAttributes(this,{"style":{"width":null,"height":null}});
this.isOutside=false;
this.container.appendChild(this);
this.doSort();
this.style["top"]=this.style["left"]="0px";
return;
}
this.parentNode.onDragOut();
this.style["top"]="0px";
this.style["left"]="0px";
}};
var DragUtils={swap:function(_27,_28){
var _29=_27.parentNode;
_29.removeChild(_27);
_29.insertBefore(_27,_28);
_27.style["top"]=_27.style["left"]="0px";
},nextItem:function(_30){
var _31=_30.nextSibling;
while(_31!=null){
if(_31.nodeName==_30.nodeName){
return _31;
}
_31=_31.nextSibling;
}
return null;
},previousItem:function(_32){
var _33=_32.previousSibling;
while(_33!=null){
if(_33.nodeName==_32.nodeName){
return _33;
}
_33=_33.previousSibling;
}
return null;
}};


