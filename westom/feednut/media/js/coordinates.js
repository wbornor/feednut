var Coordinates={ORIGIN:new Coordinate(0,0),northwestPosition:function(_1){
var x=parseInt(_1.style.left);
var y=parseInt(_1.style.top);
return new Coordinate(isNaN(x)?0:x,isNaN(y)?0:y);
},southeastPosition:function(_4){
return Coordinates.northwestPosition(_4).plus(new Coordinate(_4.offsetWidth,_4.offsetHeight));
},northwestOffset:function(_5,_6){
var _7=new Coordinate(_5.offsetLeft,_5.offsetTop);
if(!_6){
return _7;
}
var _8=_5.offsetParent;
while(_8){
_7=_7.plus(new Coordinate(_8.offsetLeft,_8.offsetTop));
_8=_8.offsetParent;
}
return _7;
},southeastOffset:function(_9,_10){
return Coordinates.northwestOffset(_9,_10).plus(new Coordinate(_9.offsetWidth,_9.offsetHeight));
},fixEvent:function(_11){
_11.windowCoordinate=new Coordinate(_11.clientX,_11.clientY);
}};
function Coordinate(x,y){
this.x=x;
this.y=y;
}
Coordinate.prototype.toString=function(){
return "("+this.x+","+this.y+")";
};
Coordinate.prototype.plus=function(_12){
return new Coordinate(this.x+_12.x,this.y+_12.y);
};
Coordinate.prototype.minus=function(_13){
return new Coordinate(this.x-_13.x,this.y-_13.y);
};
Coordinate.prototype.distance=function(_14){
var _15=this.x-_14.x;
var _16=this.y-_14.y;
return Math.sqrt(Math.pow(_15,2)+Math.pow(_16,2));
};
Coordinate.prototype.max=function(_17){
var x=Math.max(this.x,_17.x);
var y=Math.max(this.y,_17.y);
return new Coordinate(x,y);
};
Coordinate.prototype.constrain=function(min,max){
if(min.x>max.x||min.y>max.y){
return this;
}
var x=this.x;
var y=this.y;
if(min.x!=null){
x=Math.max(x,min.x);
}
if(max.x!=null){
x=Math.min(x,max.x);
}
if(min.y!=null){
y=Math.max(y,min.y);
}
if(max.y!=null){
y=Math.min(y,max.y);
}
return new Coordinate(x,y);
};
Coordinate.prototype.reposition=function(_20){
_20.style["top"]=this.y+"px";
_20.style["left"]=this.x+"px";
};
Coordinate.prototype.equals=function(_21){
if(this==_21){
return true;
}
if(!_21||_21==null){
return false;
}
return this.x==_21.x&&this.y==_21.y;
};
Coordinate.prototype.inside=function(_22,_23){
if((this.x>=_22.x)&&(this.x<=_23.x)&&(this.y>=_22.y)&&(this.y<=_23.y)){
return true;
}
return false;
};


