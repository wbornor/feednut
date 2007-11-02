if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Base");
}
if(typeof (MochiKit)=="undefined"){
MochiKit={};
}
if(typeof (MochiKit.Base)=="undefined"){
MochiKit.Base={};
}
MochiKit.Base.VERSION="1.3.1";
MochiKit.Base.NAME="MochiKit.Base";
MochiKit.Base.update=function(_1,_2){
if(_1===null){
_1={};
}
for(var i=1;i<arguments.length;i++){
var o=arguments[i];
if(typeof (o)!="undefined"&&o!==null){
for(var k in o){
_1[k]=o[k];
}
}
}
return _1;
};
MochiKit.Base.update(MochiKit.Base,{__repr__:function(){
return "["+this.NAME+" "+this.VERSION+"]";
},toString:function(){
return this.__repr__();
},counter:function(n){
if(arguments.length===0){
n=1;
}
return function(){
return n++;
};
},clone:function(_7){
var me=arguments.callee;
if(arguments.length==1){
me.prototype=_7;
return new me();
}
},flattenArguments:function(_9){
var res=[];
var m=MochiKit.Base;
var _12=m.extend(null,arguments);
while(_12.length){
var o=_12.shift();
if(o&&typeof (o)=="object"&&typeof (o.length)=="number"){
for(var i=o.length-1;i>=0;i--){
_12.unshift(o[i]);
}
}else{
res.push(o);
}
}
return res;
},extend:function(_13,obj,_15){
if(!_15){
_15=0;
}
if(obj){
var l=obj.length;
if(typeof (l)!="number"){
if(typeof (MochiKit.Iter)!="undefined"){
obj=MochiKit.Iter.list(obj);
l=obj.length;
}else{
throw new TypeError("Argument not an array-like and MochiKit.Iter not present");
}
}
if(!_13){
_13=[];
}
for(var i=_15;i<l;i++){
_13.push(obj[i]);
}
}
return _13;
},updatetree:function(_17,obj){
if(_17===null){
_17={};
}
for(var i=1;i<arguments.length;i++){
var o=arguments[i];
if(typeof (o)!="undefined"&&o!==null){
for(var k in o){
var v=o[k];
if(typeof (_17[k])=="object"&&typeof (v)=="object"){
arguments.callee(_17[k],v);
}else{
_17[k]=v;
}
}
}
}
return _17;
},setdefault:function(_19,obj){
if(_19===null){
_19={};
}
for(var i=1;i<arguments.length;i++){
var o=arguments[i];
for(var k in o){
if(!(k in _19)){
_19[k]=o[k];
}
}
}
return _19;
},keys:function(obj){
var _20=[];
for(var _21 in obj){
_20.push(_21);
}
return _20;
},items:function(obj){
var _22=[];
var e;
for(var _24 in obj){
var v;
try{
v=obj[_24];
}
catch(e){
continue;
}
_22.push([_24,v]);
}
return _22;
},_newNamedError:function(_25,_26,_27){
_27.prototype=new MochiKit.Base.NamedError(_25.NAME+"."+_26);
_25[_26]=_27;
},operator:{truth:function(a){
return !!a;
},lognot:function(a){
return !a;
},identity:function(a){
return a;
},not:function(a){
return ~a;
},neg:function(a){
return -a;
},add:function(a,b){
return a+b;
},sub:function(a,b){
return a-b;
},div:function(a,b){
return a/b;
},mod:function(a,b){
return a%b;
},mul:function(a,b){
return a*b;
},and:function(a,b){
return a&b;
},or:function(a,b){
return a|b;
},xor:function(a,b){
return a^b;
},lshift:function(a,b){
return a<<b;
},rshift:function(a,b){
return a>>b;
},zrshift:function(a,b){
return a>>>b;
},eq:function(a,b){
return a==b;
},ne:function(a,b){
return a!=b;
},gt:function(a,b){
return a>b;
},ge:function(a,b){
return a>=b;
},lt:function(a,b){
return a<b;
},le:function(a,b){
return a<=b;
},ceq:function(a,b){
return MochiKit.Base.compare(a,b)===0;
},cne:function(a,b){
return MochiKit.Base.compare(a,b)!==0;
},cgt:function(a,b){
return MochiKit.Base.compare(a,b)==1;
},cge:function(a,b){
return MochiKit.Base.compare(a,b)!=-1;
},clt:function(a,b){
return MochiKit.Base.compare(a,b)==-1;
},cle:function(a,b){
return MochiKit.Base.compare(a,b)!=1;
},logand:function(a,b){
return a&&b;
},logor:function(a,b){
return a||b;
},contains:function(a,b){
return b in a;
}},forwardCall:function(_30){
return function(){
return this[_30].apply(this,arguments);
};
},itemgetter:function(_31){
return function(arg){
return arg[_31];
};
},typeMatcher:function(){
var _33={};
for(var i=0;i<arguments.length;i++){
var typ=arguments[i];
_33[typ]=typ;
}
return function(){
for(var i=0;i<arguments.length;i++){
if(!(typeof (arguments[i]) in _33)){
return false;
}
}
return true;
};
},isNull:function(){
for(var i=0;i<arguments.length;i++){
if(arguments[i]!==null){
return false;
}
}
return true;
},isUndefinedOrNull:function(){
for(var i=0;i<arguments.length;i++){
var o=arguments[i];
if(!(typeof (o)=="undefined"||o===null)){
return false;
}
}
return true;
},isEmpty:function(obj){
return !MochiKit.Base.isNotEmpty.apply(this,arguments);
},isNotEmpty:function(obj){
for(var i=0;i<arguments.length;i++){
var o=arguments[i];
if(!(o&&o.length)){
return false;
}
}
return true;
},isArrayLike:function(){
for(var i=0;i<arguments.length;i++){
var o=arguments[i];
var typ=typeof (o);
if((typ!="object"&&!(typ=="function"&&typeof (o.item)=="function"))||o===null||typeof (o.length)!="number"){
return false;
}
}
return true;
},isDateLike:function(){
for(var i=0;i<arguments.length;i++){
var o=arguments[i];
if(typeof (o)!="object"||o===null||typeof (o.getTime)!="function"){
return false;
}
}
return true;
},xmap:function(fn){
if(fn===null){
return MochiKit.Base.extend(null,arguments,1);
}
var _36=[];
for(var i=1;i<arguments.length;i++){
_36.push(fn(arguments[i]));
}
return _36;
},map:function(fn,lst){
var m=MochiKit.Base;
var itr=MochiKit.Iter;
var _39=m.isArrayLike;
if(arguments.length<=2){
if(!_39(lst)){
if(itr){
lst=itr.list(lst);
if(fn===null){
return lst;
}
}else{
throw new TypeError("Argument not an array-like and MochiKit.Iter not present");
}
}
if(fn===null){
return m.extend(null,lst);
}
var _40=[];
for(var i=0;i<lst.length;i++){
_40.push(fn(lst[i]));
}
return _40;
}else{
if(fn===null){
fn=Array;
}
var _41=null;
for(i=1;i<arguments.length;i++){
if(!_39(arguments[i])){
if(itr){
return itr.list(itr.imap.apply(null,arguments));
}else{
throw new TypeError("Argument not an array-like and MochiKit.Iter not present");
}
}
var l=arguments[i].length;
if(_41===null||_41>l){
_41=l;
}
}
_40=[];
for(i=0;i<_41;i++){
var _42=[];
for(var j=1;j<arguments.length;j++){
_42.push(arguments[j][i]);
}
_40.push(fn.apply(this,_42));
}
return _40;
}
},xfilter:function(fn){
var _44=[];
if(fn===null){
fn=MochiKit.Base.operator.truth;
}
for(var i=1;i<arguments.length;i++){
var o=arguments[i];
if(fn(o)){
_44.push(o);
}
}
return _44;
},filter:function(fn,lst,_45){
var _46=[];
var m=MochiKit.Base;
if(!m.isArrayLike(lst)){
if(MochiKit.Iter){
lst=MochiKit.Iter.list(lst);
}else{
throw new TypeError("Argument not an array-like and MochiKit.Iter not present");
}
}
if(fn===null){
fn=m.operator.truth;
}
if(typeof (Array.prototype.filter)=="function"){
return Array.prototype.filter.call(lst,fn,_45);
}else{
if(typeof (_45)=="undefined"||_45===null){
for(var i=0;i<lst.length;i++){
var o=lst[i];
if(fn(o)){
_46.push(o);
}
}
}else{
for(i=0;i<lst.length;i++){
o=lst[i];
if(fn.call(_45,o)){
_46.push(o);
}
}
}
}
return _46;
},_wrapDumbFunction:function(_47){
return function(){
switch(arguments.length){
case 0:
return _47();
case 1:
return _47(arguments[0]);
case 2:
return _47(arguments[0],arguments[1]);
case 3:
return _47(arguments[0],arguments[1],arguments[2]);
}
var _48=[];
for(var i=0;i<arguments.length;i++){
_48.push("arguments["+i+"]");
}
return eval("(func("+_48.join(",")+"))");
};
},method:function(_49,_50){
var m=MochiKit.Base;
return m.bind.apply(this,m.extend([_50,_49],arguments,2));
},bind:function(_51,_52){
if(typeof (_51)=="string"){
_51=_52[_51];
}
var _53=_51.im_func;
var _54=_51.im_preargs;
var _55=_51.im_self;
var m=MochiKit.Base;
if(typeof (_51)=="function"&&typeof (_51.apply)=="undefined"){
_51=m._wrapDumbFunction(_51);
}
if(typeof (_53)!="function"){
_53=_51;
}
if(typeof (_52)!="undefined"){
_55=_52;
}
if(typeof (_54)=="undefined"){
_54=[];
}else{
_54=_54.slice();
}
m.extend(_54,arguments,2);
var _56=function(){
var _57=arguments;
var me=arguments.callee;
if(me.im_preargs.length>0){
_57=m.concat(me.im_preargs,_57);
}
var _52=me.im_self;
if(!_52){
_52=this;
}
return me.im_func.apply(_52,_57);
};
_56.im_self=_55;
_56.im_func=_53;
_56.im_preargs=_54;
return _56;
},bindMethods:function(_58){
var _59=MochiKit.Base.bind;
for(var k in _58){
var _60=_58[k];
if(typeof (_60)=="function"){
_58[k]=_59(_60,_58);
}
}
},registerComparator:function(_61,_62,_63,_64){
MochiKit.Base.comparatorRegistry.register(_61,_62,_63,_64);
},_primitives:{"boolean":true,"string":true,"number":true},compare:function(a,b){
if(a==b){
return 0;
}
var _65=(typeof (a)=="undefined"||a===null);
var _66=(typeof (b)=="undefined"||b===null);
if(_65&&_66){
return 0;
}else{
if(_65){
return -1;
}else{
if(_66){
return 1;
}
}
}
var m=MochiKit.Base;
var _67=m._primitives;
if(!(typeof (a) in _67&&typeof (b) in _67)){
try{
return m.comparatorRegistry.match(a,b);
}
catch(e){
if(e!=m.NotFound){
throw e;
}
}
}
if(a<b){
return -1;
}else{
if(a>b){
return 1;
}
}
var _68=m.repr;
throw new TypeError(_68(a)+" and "+_68(b)+" can not be compared");
},compareDateLike:function(a,b){
return MochiKit.Base.compare(a.getTime(),b.getTime());
},compareArrayLike:function(a,b){
var _69=MochiKit.Base.compare;
var _70=a.length;
var _71=0;
if(_70>b.length){
_71=1;
_70=b.length;
}else{
if(_70<b.length){
_71=-1;
}
}
for(var i=0;i<_70;i++){
var cmp=_69(a[i],b[i]);
if(cmp){
return cmp;
}
}
return _71;
},registerRepr:function(_73,_74,_75,_76){
MochiKit.Base.reprRegistry.register(_73,_74,_75,_76);
},repr:function(o){
if(typeof (o)=="undefined"){
return "undefined";
}else{
if(o===null){
return "null";
}
}
try{
if(typeof (o.__repr__)=="function"){
return o.__repr__();
}else{
if(typeof (o.repr)=="function"&&o.repr!=arguments.callee){
return o.repr();
}
}
return MochiKit.Base.reprRegistry.match(o);
}
catch(e){
if(typeof (o.NAME)=="string"&&(o.toString==Function.prototype.toString||o.toString==Object.prototype.toString)){
return o.NAME;
}
}
try{
var _77=(o+"");
}
catch(e){
return "["+typeof (o)+"]";
}
if(typeof (o)=="function"){
o=_77.replace(/^\s+/,"");
var idx=o.indexOf("{");
if(idx!=-1){
o=o.substr(0,idx)+"{...}";
}
}
return _77;
},reprArrayLike:function(o){
var m=MochiKit.Base;
return "["+m.map(m.repr,o).join(", ")+"]";
},reprString:function(o){
return ("\""+o.replace(/(["\\])/g,"\\$1")+"\"").replace(/[\f]/g,"\\f").replace(/[\b]/g,"\\b").replace(/[\n]/g,"\\n").replace(/[\t]/g,"\\t").replace(/[\r]/g,"\\r");
},reprNumber:function(o){
return o+"";
},registerJSON:function(_79,_80,_81,_82){
MochiKit.Base.jsonRegistry.register(_79,_80,_81,_82);
},evalJSON:function(){
return eval("("+arguments[0]+")");
},serializeJSON:function(o){
var _83=typeof (o);
if(_83=="undefined"){
return "undefined";
}else{
if(_83=="number"||_83=="boolean"){
return o+"";
}else{
if(o===null){
return "null";
}
}
}
var m=MochiKit.Base;
var _84=m.reprString;
if(_83=="string"){
return _84(o);
}
var me=arguments.callee;
var _85;
if(typeof (o.__json__)=="function"){
_85=o.__json__();
if(o!==_85){
return me(_85);
}
}
if(typeof (o.json)=="function"){
_85=o.json();
if(o!==_85){
return me(_85);
}
}
if(_83!="function"&&typeof (o.length)=="number"){
var res=[];
for(var i=0;i<o.length;i++){
var val=me(o[i]);
if(typeof (val)!="string"){
val="undefined";
}
res.push(val);
}
return "["+res.join(", ")+"]";
}
try{
_85=m.jsonRegistry.match(o);
return me(_85);
}
catch(e){
if(e!=m.NotFound){
throw e;
}
}
if(_83=="function"){
return null;
}
res=[];
for(var k in o){
var _87;
if(typeof (k)=="number"){
_87="\""+k+"\"";
}else{
if(typeof (k)=="string"){
_87=_84(k);
}else{
continue;
}
}
val=me(o[k]);
if(typeof (val)!="string"){
continue;
}
res.push(_87+":"+val);
}
return "{"+res.join(", ")+"}";
},objEqual:function(a,b){
return (MochiKit.Base.compare(a,b)===0);
},arrayEqual:function(_88,arr){
if(_88.length!=arr.length){
return false;
}
return (MochiKit.Base.compare(_88,arr)===0);
},concat:function(){
var _90=[];
var _91=MochiKit.Base.extend;
for(var i=0;i<arguments.length;i++){
_91(_90,arguments[i]);
}
return _90;
},keyComparator:function(key){
var m=MochiKit.Base;
var _93=m.compare;
if(arguments.length==1){
return function(a,b){
return _93(a[key],b[key]);
};
}
var _94=m.extend(null,arguments);
return function(a,b){
var _95=0;
for(var i=0;(_95===0)&&(i<_94.length);i++){
var key=_94[i];
_95=_93(a[key],b[key]);
}
return _95;
};
},reverseKeyComparator:function(key){
var _96=MochiKit.Base.keyComparator.apply(this,arguments);
return function(a,b){
return _96(b,a);
};
},partial:function(_97){
var m=MochiKit.Base;
return m.bind.apply(this,m.extend([_97,undefined],arguments,1));
},listMinMax:function(_98,lst){
if(lst.length===0){
return null;
}
var cur=lst[0];
var _100=MochiKit.Base.compare;
for(var i=1;i<lst.length;i++){
var o=lst[i];
if(_100(o,cur)==_98){
cur=o;
}
}
return cur;
},objMax:function(){
return MochiKit.Base.listMinMax(1,arguments);
},objMin:function(){
return MochiKit.Base.listMinMax(-1,arguments);
},findIdentical:function(lst,_101,_102,end){
if(typeof (end)=="undefined"||end===null){
end=lst.length;
}
for(var i=(_102||0);i<end;i++){
if(lst[i]===_101){
return i;
}
}
return -1;
},findValue:function(lst,_104,_105,end){
if(typeof (end)=="undefined"||end===null){
end=lst.length;
}
var cmp=MochiKit.Base.compare;
for(var i=(_105||0);i<end;i++){
if(cmp(lst[i],_104)===0){
return i;
}
}
return -1;
},nodeWalk:function(node,_107){
var _108=[node];
var _109=MochiKit.Base.extend;
while(_108.length){
var res=_107(_108.shift());
if(res){
_109(_108,res);
}
}
},nameFunctions:function(_110){
var base=_110.NAME;
if(typeof (base)=="undefined"){
base="";
}else{
base=base+".";
}
for(var name in _110){
var o=_110[name];
if(typeof (o)=="function"&&typeof (o.NAME)=="undefined"){
try{
o.NAME=base+name;
}
catch(e){
}
}
}
},queryString:function(_113,_114){
if(typeof (MochiKit.DOM)!="undefined"&&arguments.length==1&&(typeof (_113)=="string"||(typeof (_113.nodeType)!="undefined"&&_113.nodeType>0))){
var kv=MochiKit.DOM.formContents(_113);
_113=kv[0];
_114=kv[1];
}else{
if(arguments.length==1){
var o=_113;
_113=[];
_114=[];
for(var k in o){
var v=o[k];
if(typeof (v)!="function"){
_113.push(k);
_114.push(v);
}
}
}
}
var rval=[];
var len=Math.min(_113.length,_114.length);
var _118=MochiKit.Base.urlEncode;
for(var i=0;i<len;i++){
v=_114[i];
if(typeof (v)!="undefined"&&v!==null){
rval.push(_118(_113[i])+"="+_118(v));
}
}
return rval.join("&");
},parseQueryString:function(_119,_120){
var _121=_119.replace(/\+/g,"%20").split("&");
var o={};
var _122;
if(typeof (decodeURIComponent)!="undefined"){
_122=decodeURIComponent;
}else{
_122=unescape;
}
if(_120){
for(var i=0;i<_121.length;i++){
var pair=_121[i].split("=");
var name=_122(pair[0]);
var arr=o[name];
if(!(arr instanceof Array)){
arr=[];
o[name]=arr;
}
arr.push(_122(pair[1]));
}
}else{
for(i=0;i<_121.length;i++){
pair=_121[i].split("=");
o[_122(pair[0])]=_122(pair[1]);
}
}
return o;
}});
MochiKit.Base.AdapterRegistry=function(){
this.pairs=[];
};
MochiKit.Base.AdapterRegistry.prototype={register:function(name,_124,wrap,_126){
if(_126){
this.pairs.unshift([name,_124,wrap]);
}else{
this.pairs.push([name,_124,wrap]);
}
},match:function(){
for(var i=0;i<this.pairs.length;i++){
var pair=this.pairs[i];
if(pair[1].apply(this,arguments)){
return pair[2].apply(this,arguments);
}
}
throw MochiKit.Base.NotFound;
},unregister:function(name){
for(var i=0;i<this.pairs.length;i++){
var pair=this.pairs[i];
if(pair[0]==name){
this.pairs.splice(i,1);
return true;
}
}
return false;
}};
MochiKit.Base.EXPORT=["counter","clone","extend","update","updatetree","setdefault","keys","items","NamedError","operator","forwardCall","itemgetter","typeMatcher","isCallable","isUndefined","isUndefinedOrNull","isNull","isEmpty","isNotEmpty","isArrayLike","isDateLike","xmap","map","xfilter","filter","bind","bindMethods","NotFound","AdapterRegistry","registerComparator","compare","registerRepr","repr","objEqual","arrayEqual","concat","keyComparator","reverseKeyComparator","partial","merge","listMinMax","listMax","listMin","objMax","objMin","nodeWalk","zip","urlEncode","queryString","serializeJSON","registerJSON","evalJSON","parseQueryString","findValue","findIdentical","flattenArguments","method"];
MochiKit.Base.EXPORT_OK=["nameFunctions","comparatorRegistry","reprRegistry","jsonRegistry","compareDateLike","compareArrayLike","reprArrayLike","reprString","reprNumber"];
MochiKit.Base._exportSymbols=function(_127,_128){
if(typeof (MochiKit.__export__)=="undefined"){
MochiKit.__export__=(MochiKit.__compat__||(typeof (JSAN)=="undefined"&&typeof (dojo)=="undefined"));
}
if(!MochiKit.__export__){
return;
}
var all=_128.EXPORT_TAGS[":all"];
for(var i=0;i<all.length;i++){
_127[all[i]]=_128[all[i]];
}
};
MochiKit.Base.__new__=function(){
var m=this;
m.forward=m.forwardCall;
m.find=m.findValue;
if(typeof (encodeURIComponent)!="undefined"){
m.urlEncode=function(_130){
return encodeURIComponent(_130).replace(/\'/g,"%27");
};
}else{
m.urlEncode=function(_131){
return escape(_131).replace(/\+/g,"%2B").replace(/\"/g,"%22").rval.replace(/\'/g,"%27");
};
}
m.NamedError=function(name){
this.message=name;
this.name=name;
};
m.NamedError.prototype=new Error();
m.update(m.NamedError.prototype,{repr:function(){
if(this.message&&this.message!=this.name){
return this.name+"("+m.repr(this.message)+")";
}else{
return this.name+"()";
}
},toString:m.forwardCall("repr")});
m.NotFound=new m.NamedError("MochiKit.Base.NotFound");
m.listMax=m.partial(m.listMinMax,1);
m.listMin=m.partial(m.listMinMax,-1);
m.isCallable=m.typeMatcher("function");
m.isUndefined=m.typeMatcher("undefined");
m.merge=m.partial(m.update,null);
m.zip=m.partial(m.map,null);
m.comparatorRegistry=new m.AdapterRegistry();
m.registerComparator("dateLike",m.isDateLike,m.compareDateLike);
m.registerComparator("arrayLike",m.isArrayLike,m.compareArrayLike);
m.reprRegistry=new m.AdapterRegistry();
m.registerRepr("arrayLike",m.isArrayLike,m.reprArrayLike);
m.registerRepr("string",m.typeMatcher("string"),m.reprString);
m.registerRepr("numbers",m.typeMatcher("number","boolean"),m.reprNumber);
m.jsonRegistry=new m.AdapterRegistry();
var all=m.concat(m.EXPORT,m.EXPORT_OK);
m.EXPORT_TAGS={":common":m.concat(m.EXPORT_OK),":all":all};
m.nameFunctions(this);
};
MochiKit.Base.__new__();
if(!MochiKit.__compat__){
compare=MochiKit.Base.compare;
}
MochiKit.Base._exportSymbols(this,MochiKit.Base);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Iter");
dojo.require("MochiKit.Base");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Iter depends on MochiKit.Base!";
}
if(typeof (MochiKit.Iter)=="undefined"){
MochiKit.Iter={};
}
MochiKit.Iter.NAME="MochiKit.Iter";
MochiKit.Iter.VERSION="1.3.1";
MochiKit.Base.update(MochiKit.Iter,{__repr__:function(){
return "["+this.NAME+" "+this.VERSION+"]";
},toString:function(){
return this.__repr__();
},registerIteratorFactory:function(name,_132,_133,_134){
MochiKit.Iter.iteratorRegistry.register(name,_132,_133,_134);
},iter:function(_135,_136){
var self=MochiKit.Iter;
if(arguments.length==2){
return self.takewhile(function(a){
return a!=_136;
},_135);
}
if(typeof (_135.next)=="function"){
return _135;
}else{
if(typeof (_135.iter)=="function"){
return _135.iter();
}
}
try{
return self.iteratorRegistry.match(_135);
}
catch(e){
var m=MochiKit.Base;
if(e==m.NotFound){
e=new TypeError(typeof (_135)+": "+m.repr(_135)+" is not iterable");
}
throw e;
}
},count:function(n){
if(!n){
n=0;
}
var m=MochiKit.Base;
return {repr:function(){
return "count("+n+")";
},toString:m.forwardCall("repr"),next:m.counter(n)};
},cycle:function(p){
var self=MochiKit.Iter;
var m=MochiKit.Base;
var lst=[];
var _139=self.iter(p);
return {repr:function(){
return "cycle(...)";
},toString:m.forwardCall("repr"),next:function(){
try{
var rval=_139.next();
lst.push(rval);
return rval;
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
if(lst.length===0){
this.next=function(){
throw self.StopIteration;
};
}else{
var i=-1;
this.next=function(){
i=(i+1)%lst.length;
return lst[i];
};
}
return this.next();
}
}};
},repeat:function(elem,n){
var m=MochiKit.Base;
if(typeof (n)=="undefined"){
return {repr:function(){
return "repeat("+m.repr(elem)+")";
},toString:m.forwardCall("repr"),next:function(){
return elem;
}};
}
return {repr:function(){
return "repeat("+m.repr(elem)+", "+n+")";
},toString:m.forwardCall("repr"),next:function(){
if(n<=0){
throw MochiKit.Iter.StopIteration;
}
n-=1;
return elem;
}};
},next:function(_141){
return _141.next();
},izip:function(p,q){
var m=MochiKit.Base;
var next=MochiKit.Iter.next;
var _144=m.map(iter,arguments);
return {repr:function(){
return "izip(...)";
},toString:m.forwardCall("repr"),next:function(){
return m.map(next,_144);
}};
},ifilter:function(pred,seq){
var m=MochiKit.Base;
seq=MochiKit.Iter.iter(seq);
if(pred===null){
pred=m.operator.truth;
}
return {repr:function(){
return "ifilter(...)";
},toString:m.forwardCall("repr"),next:function(){
while(true){
var rval=seq.next();
if(pred(rval)){
return rval;
}
}
return undefined;
}};
},ifilterfalse:function(pred,seq){
var m=MochiKit.Base;
seq=MochiKit.Iter.iter(seq);
if(pred===null){
pred=m.operator.truth;
}
return {repr:function(){
return "ifilterfalse(...)";
},toString:m.forwardCall("repr"),next:function(){
while(true){
var rval=seq.next();
if(!pred(rval)){
return rval;
}
}
return undefined;
}};
},islice:function(seq){
var self=MochiKit.Iter;
var m=MochiKit.Base;
seq=self.iter(seq);
var _147=0;
var stop=0;
var step=1;
var i=-1;
if(arguments.length==2){
stop=arguments[1];
}else{
if(arguments.length==3){
_147=arguments[1];
stop=arguments[2];
}else{
_147=arguments[1];
stop=arguments[2];
step=arguments[3];
}
}
return {repr:function(){
return "islice("+["...",_147,stop,step].join(", ")+")";
},toString:m.forwardCall("repr"),next:function(){
var rval;
while(i<_147){
rval=seq.next();
i++;
}
if(_147>=stop){
throw self.StopIteration;
}
_147+=step;
return rval;
}};
},imap:function(fun,p,q){
var m=MochiKit.Base;
var self=MochiKit.Iter;
var _151=m.map(self.iter,m.extend(null,arguments,1));
var map=m.map;
var next=self.next;
return {repr:function(){
return "imap(...)";
},toString:m.forwardCall("repr"),next:function(){
return fun.apply(this,map(next,_151));
}};
},applymap:function(fun,seq,self){
seq=MochiKit.Iter.iter(seq);
var m=MochiKit.Base;
return {repr:function(){
return "applymap(...)";
},toString:m.forwardCall("repr"),next:function(){
return fun.apply(self,seq.next());
}};
},chain:function(p,q){
var self=MochiKit.Iter;
var m=MochiKit.Base;
if(arguments.length==1){
return self.iter(arguments[0]);
}
var _153=m.map(self.iter,arguments);
return {repr:function(){
return "chain(...)";
},toString:m.forwardCall("repr"),next:function(){
while(_153.length>1){
try{
return _153[0].next();
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
_153.shift();
}
}
if(_153.length==1){
var arg=_153.shift();
this.next=m.bind("next",arg);
return this.next();
}
throw self.StopIteration;
}};
},takewhile:function(pred,seq){
var self=MochiKit.Iter;
seq=self.iter(seq);
return {repr:function(){
return "takewhile(...)";
},toString:MochiKit.Base.forwardCall("repr"),next:function(){
var rval=seq.next();
if(!pred(rval)){
this.next=function(){
throw self.StopIteration;
};
this.next();
}
return rval;
}};
},dropwhile:function(pred,seq){
seq=MochiKit.Iter.iter(seq);
var m=MochiKit.Base;
var bind=m.bind;
return {"repr":function(){
return "dropwhile(...)";
},"toString":m.forwardCall("repr"),"next":function(){
while(true){
var rval=seq.next();
if(!pred(rval)){
break;
}
}
this.next=bind("next",seq);
return rval;
}};
},_tee:function(_155,sync,_157){
sync.pos[_155]=-1;
var m=MochiKit.Base;
var _158=m.listMin;
return {repr:function(){
return "tee("+_155+", ...)";
},toString:m.forwardCall("repr"),next:function(){
var rval;
var i=sync.pos[_155];
if(i==sync.max){
rval=_157.next();
sync.deque.push(rval);
sync.max+=1;
sync.pos[_155]+=1;
}else{
rval=sync.deque[i-sync.min];
sync.pos[_155]+=1;
if(i==sync.min&&_158(sync.pos)!=sync.min){
sync.min+=1;
sync.deque.shift();
}
}
return rval;
}};
},tee:function(_159,n){
var rval=[];
var sync={"pos":[],"deque":[],"max":-1,"min":-1};
if(arguments.length==1){
n=2;
}
var self=MochiKit.Iter;
_159=self.iter(_159);
var _tee=self._tee;
for(var i=0;i<n;i++){
rval.push(_tee(i,sync,_159));
}
return rval;
},list:function(_161){
var m=MochiKit.Base;
if(typeof (_161.slice)=="function"){
return _161.slice();
}else{
if(m.isArrayLike(_161)){
return m.concat(_161);
}
}
var self=MochiKit.Iter;
_161=self.iter(_161);
var rval=[];
try{
while(true){
rval.push(_161.next());
}
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
return rval;
}
return undefined;
},reduce:function(fn,_162,_163){
var i=0;
var x=_163;
var self=MochiKit.Iter;
_162=self.iter(_162);
if(arguments.length<3){
try{
x=_162.next();
}
catch(e){
if(e==self.StopIteration){
e=new TypeError("reduce() of empty sequence with no initial value");
}
throw e;
}
i++;
}
try{
while(true){
x=fn(x,_162.next());
}
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
}
return x;
},range:function(){
var _165=0;
var stop=0;
var step=1;
if(arguments.length==1){
stop=arguments[0];
}else{
if(arguments.length==2){
_165=arguments[0];
stop=arguments[1];
}else{
if(arguments.length==3){
_165=arguments[0];
stop=arguments[1];
step=arguments[2];
}else{
throw new TypeError("range() takes 1, 2, or 3 arguments!");
}
}
}
if(step===0){
throw new TypeError("range() step must not be 0");
}
return {next:function(){
if((step>0&&_165>=stop)||(step<0&&_165<=stop)){
throw MochiKit.Iter.StopIteration;
}
var rval=_165;
_165+=step;
return rval;
},repr:function(){
return "range("+[_165,stop,step].join(", ")+")";
},toString:MochiKit.Base.forwardCall("repr")};
},sum:function(_166,_167){
var x=_167||0;
var self=MochiKit.Iter;
_166=self.iter(_166);
try{
while(true){
x+=_166.next();
}
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
}
return x;
},exhaust:function(_168){
var self=MochiKit.Iter;
_168=self.iter(_168);
try{
while(true){
_168.next();
}
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
}
},forEach:function(_169,func,self){
var m=MochiKit.Base;
if(arguments.length>2){
func=m.bind(func,self);
}
if(m.isArrayLike(_169)){
try{
for(var i=0;i<_169.length;i++){
func(_169[i]);
}
}
catch(e){
if(e!=MochiKit.Iter.StopIteration){
throw e;
}
}
}else{
self=MochiKit.Iter;
self.exhaust(self.imap(func,_169));
}
},every:function(_171,func){
var self=MochiKit.Iter;
try{
self.ifilterfalse(func,_171).next();
return false;
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
return true;
}
},sorted:function(_172,cmp){
var rval=MochiKit.Iter.list(_172);
if(arguments.length==1){
cmp=MochiKit.Base.compare;
}
rval.sort(cmp);
return rval;
},reversed:function(_173){
var rval=MochiKit.Iter.list(_173);
rval.reverse();
return rval;
},some:function(_174,func){
var self=MochiKit.Iter;
try{
self.ifilter(func,_174).next();
return true;
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
return false;
}
},iextend:function(lst,_175){
if(MochiKit.Base.isArrayLike(_175)){
for(var i=0;i<_175.length;i++){
lst.push(_175[i]);
}
}else{
var self=MochiKit.Iter;
_175=self.iter(_175);
try{
while(true){
lst.push(_175.next());
}
}
catch(e){
if(e!=self.StopIteration){
throw e;
}
}
}
return lst;
},groupby:function(_176,_177){
var m=MochiKit.Base;
var self=MochiKit.Iter;
if(arguments.length<2){
_177=m.operator.identity;
}
_176=self.iter(_176);
var pk=undefined;
var k=undefined;
var v;
function fetch(){
v=_176.next();
k=_177(v);
}
function eat(){
var ret=v;
v=undefined;
return ret;
}
var _180=true;
return {repr:function(){
return "groupby(...)";
},next:function(){
while(k==pk){
fetch();
if(_180){
_180=false;
break;
}
}
pk=k;
return [k,{next:function(){
if(v==undefined){
fetch();
}
if(k!=pk){
throw self.StopIteration;
}
return eat();
}}];
}};
},groupby_as_array:function(_181,_182){
var m=MochiKit.Base;
var self=MochiKit.Iter;
if(arguments.length<2){
_182=m.operator.identity;
}
_181=self.iter(_181);
var _183=[];
var _184=true;
var _185;
while(true){
try{
var _186=_181.next();
var key=_182(_186);
}
catch(e){
if(e==self.StopIteration){
break;
}
throw e;
}
if(_184||key!=_185){
var _187=[];
_183.push([key,_187]);
}
_187.push(_186);
_184=false;
_185=key;
}
return _183;
},arrayLikeIter:function(_188){
var i=0;
return {repr:function(){
return "arrayLikeIter(...)";
},toString:MochiKit.Base.forwardCall("repr"),next:function(){
if(i>=_188.length){
throw MochiKit.Iter.StopIteration;
}
return _188[i++];
}};
},hasIterateNext:function(_189){
return (_189&&typeof (_189.iterateNext)=="function");
},iterateNextIter:function(_190){
return {repr:function(){
return "iterateNextIter(...)";
},toString:MochiKit.Base.forwardCall("repr"),next:function(){
var rval=_190.iterateNext();
if(rval===null||rval===undefined){
throw MochiKit.Iter.StopIteration;
}
return rval;
}};
}});
MochiKit.Iter.EXPORT_OK=["iteratorRegistry","arrayLikeIter","hasIterateNext","iterateNextIter",];
MochiKit.Iter.EXPORT=["StopIteration","registerIteratorFactory","iter","count","cycle","repeat","next","izip","ifilter","ifilterfalse","islice","imap","applymap","chain","takewhile","dropwhile","tee","list","reduce","range","sum","exhaust","forEach","every","sorted","reversed","some","iextend","groupby","groupby_as_array"];
MochiKit.Iter.__new__=function(){
var m=MochiKit.Base;
this.StopIteration=new m.NamedError("StopIteration");
this.iteratorRegistry=new m.AdapterRegistry();
this.registerIteratorFactory("arrayLike",m.isArrayLike,this.arrayLikeIter);
this.registerIteratorFactory("iterateNext",this.hasIterateNext,this.iterateNextIter);
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
m.nameFunctions(this);
};
MochiKit.Iter.__new__();
if(!MochiKit.__compat__){
reduce=MochiKit.Iter.reduce;
}
MochiKit.Base._exportSymbols(this,MochiKit.Iter);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Logging");
dojo.require("MochiKit.Base");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Logging depends on MochiKit.Base!";
}
if(typeof (MochiKit.Logging)=="undefined"){
MochiKit.Logging={};
}
MochiKit.Logging.NAME="MochiKit.Logging";
MochiKit.Logging.VERSION="1.3.1";
MochiKit.Logging.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.Logging.toString=function(){
return this.__repr__();
};
MochiKit.Logging.EXPORT=["LogLevel","LogMessage","Logger","alertListener","logger","log","logError","logDebug","logFatal","logWarning"];
MochiKit.Logging.EXPORT_OK=["logLevelAtLeast","isLogMessage","compareLogMessage"];
MochiKit.Logging.LogMessage=function(num,_192,info){
this.num=num;
this.level=_192;
this.info=info;
this.timestamp=new Date();
};
MochiKit.Logging.LogMessage.prototype={repr:function(){
var m=MochiKit.Base;
return "LogMessage("+m.map(m.repr,[this.num,this.level,this.info]).join(", ")+")";
},toString:MochiKit.Base.forwardCall("repr")};
MochiKit.Base.update(MochiKit.Logging,{logLevelAtLeast:function(_194){
var self=MochiKit.Logging;
if(typeof (_194)=="string"){
_194=self.LogLevel[_194];
}
return function(msg){
var _196=msg.level;
if(typeof (_196)=="string"){
_196=self.LogLevel[_196];
}
return _196>=_194;
};
},isLogMessage:function(){
var _197=MochiKit.Logging.LogMessage;
for(var i=0;i<arguments.length;i++){
if(!(arguments[i] instanceof _197)){
return false;
}
}
return true;
},compareLogMessage:function(a,b){
return MochiKit.Base.compare([a.level,a.info],[b.level,b.info]);
},alertListener:function(msg){
alert("num: "+msg.num+"\nlevel: "+msg.level+"\ninfo: "+msg.info.join(" "));
}});
MochiKit.Logging.Logger=function(_198){
this.counter=0;
if(typeof (_198)=="undefined"||_198===null){
_198=-1;
}
this.maxSize=_198;
this._messages=[];
this.listeners={};
this.useNativeConsole=false;
};
MochiKit.Logging.Logger.prototype={clear:function(){
this._messages.splice(0,this._messages.length);
},logToConsole:function(msg){
if(typeof (window)!="undefined"&&window.console&&window.console.log){
window.console.log(msg);
}else{
if(typeof (opera)!="undefined"&&opera.postError){
opera.postError(msg);
}else{
if(typeof (printfire)=="function"){
printfire(msg);
}
}
}
},dispatchListeners:function(msg){
for(var k in this.listeners){
var pair=this.listeners[k];
if(pair.ident!=k||(pair[0]&&!pair[0](msg))){
continue;
}
pair[1](msg);
}
},addListener:function(_199,_200,_201){
if(typeof (_200)=="string"){
_200=MochiKit.Logging.logLevelAtLeast(_200);
}
var _202=[_200,_201];
_202.ident=_199;
this.listeners[_199]=_202;
},removeListener:function(_203){
delete this.listeners[_203];
},baseLog:function(_204,_205){
var msg=new MochiKit.Logging.LogMessage(this.counter,_204,MochiKit.Base.extend(null,arguments,1));
this._messages.push(msg);
this.dispatchListeners(msg);
if(this.useNativeConsole){
this.logToConsole(msg.level+": "+msg.info.join(" "));
}
this.counter+=1;
while(this.maxSize>=0&&this._messages.length>this.maxSize){
this._messages.shift();
}
},getMessages:function(_206){
var _207=0;
if(!(typeof (_206)=="undefined"||_206===null)){
_207=Math.max(0,this._messages.length-_206);
}
return this._messages.slice(_207);
},getMessageText:function(_208){
if(typeof (_208)=="undefined"||_208===null){
_208=30;
}
var _209=this.getMessages(_208);
if(_209.length){
var lst=map(function(m){
return "\n  ["+m.num+"] "+m.level+": "+m.info.join(" ");
},_209);
lst.unshift("LAST "+_209.length+" MESSAGES:");
return lst.join("");
}
return "";
},debuggingBookmarklet:function(_210){
if(typeof (MochiKit.LoggingPane)=="undefined"){
alert(this.getMessageText());
}else{
MochiKit.LoggingPane.createLoggingPane(_210||false);
}
}};
MochiKit.Logging.__new__=function(){
this.LogLevel={ERROR:40,FATAL:50,WARNING:30,INFO:20,DEBUG:10};
var m=MochiKit.Base;
m.registerComparator("LogMessage",this.isLogMessage,this.compareLogMessage);
var _211=m.partial;
var _212=this.Logger;
var _213=_212.prototype.baseLog;
m.update(this.Logger.prototype,{debug:_211(_213,"DEBUG"),log:_211(_213,"INFO"),error:_211(_213,"ERROR"),fatal:_211(_213,"FATAL"),warning:_211(_213,"WARNING")});
var self=this;
var _214=function(name){
return function(){
self.logger[name].apply(self.logger,arguments);
};
};
this.log=_214("log");
this.logError=_214("error");
this.logDebug=_214("debug");
this.logFatal=_214("fatal");
this.logWarning=_214("warning");
this.logger=new _212();
this.logger.useNativeConsole=true;
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
m.nameFunctions(this);
};
if(typeof (printfire)=="undefined"&&typeof (document)!="undefined"&&document.createEvent&&typeof (dispatchEvent)!="undefined"){
printfire=function(){
printfire.args=arguments;
var ev=document.createEvent("Events");
ev.initEvent("printfire",false,true);
dispatchEvent(ev);
};
}
MochiKit.Logging.__new__();
MochiKit.Base._exportSymbols(this,MochiKit.Logging);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.DateTime");
}
if(typeof (MochiKit)=="undefined"){
MochiKit={};
}
if(typeof (MochiKit.DateTime)=="undefined"){
MochiKit.DateTime={};
}
MochiKit.DateTime.NAME="MochiKit.DateTime";
MochiKit.DateTime.VERSION="1.3.1";
MochiKit.DateTime.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.DateTime.toString=function(){
return this.__repr__();
};
MochiKit.DateTime.isoDate=function(str){
str=str+"";
if(typeof (str)!="string"||str.length===0){
return null;
}
var iso=str.split("-");
if(iso.length===0){
return null;
}
return new Date(iso[0],iso[1]-1,iso[2]);
};
MochiKit.DateTime._isoRegexp=/(\d{4,})(?:-(\d{1,2})(?:-(\d{1,2})(?:[T ](\d{1,2}):(\d{1,2})(?::(\d{1,2})(?:\.(\d+))?)?(?:(Z)|([+-])(\d{1,2})(?::(\d{1,2}))?)?)?)?)?/;
MochiKit.DateTime.isoTimestamp=function(str){
str=str+"";
if(typeof (str)!="string"||str.length===0){
return null;
}
var res=str.match(MochiKit.DateTime._isoRegexp);
if(typeof (res)=="undefined"||res===null){
return null;
}
var year,month,day,hour,min,sec,msec;
year=parseInt(res[1],10);
if(typeof (res[2])=="undefined"||res[2]===""){
return new Date(year);
}
month=parseInt(res[2],10)-1;
day=parseInt(res[3],10);
if(typeof (res[4])=="undefined"||res[4]===""){
return new Date(year,month,day);
}
hour=parseInt(res[4],10);
min=parseInt(res[5],10);
sec=(typeof (res[6])!="undefined"&&res[6]!=="")?parseInt(res[6],10):0;
if(typeof (res[7])!="undefined"&&res[7]!==""){
msec=Math.round(1000*parseFloat("0."+res[7]));
}else{
msec=0;
}
if((typeof (res[8])=="undefined"||res[8]==="")&&(typeof (res[9])=="undefined"||res[9]==="")){
return new Date(year,month,day,hour,min,sec,msec);
}
var ofs;
if(typeof (res[9])!="undefined"&&res[9]!==""){
ofs=parseInt(res[10],10)*3600000;
if(typeof (res[11])!="undefined"&&res[11]!==""){
ofs+=parseInt(res[11],10)*60000;
}
if(res[9]=="-"){
ofs=-ofs;
}
}else{
ofs=0;
}
return new Date(Date.UTC(year,month,day,hour,min,sec,msec)-ofs);
};
MochiKit.DateTime.toISOTime=function(date,_221){
if(typeof (date)=="undefined"||date===null){
return null;
}
var hh=date.getHours();
var mm=date.getMinutes();
var ss=date.getSeconds();
var lst=[((_221&&(hh<10))?"0"+hh:hh),((mm<10)?"0"+mm:mm),((ss<10)?"0"+ss:ss)];
return lst.join(":");
};
MochiKit.DateTime.toISOTimestamp=function(date,_225){
if(typeof (date)=="undefined"||date===null){
return null;
}
var sep=_225?"T":" ";
var foot=_225?"Z":"";
if(_225){
date=new Date(date.getTime()+(date.getTimezoneOffset()*60000));
}
return MochiKit.DateTime.toISODate(date)+sep+MochiKit.DateTime.toISOTime(date,_225)+foot;
};
MochiKit.DateTime.toISODate=function(date){
if(typeof (date)=="undefined"||date===null){
return null;
}
var _228=MochiKit.DateTime._padTwo;
return [date.getFullYear(),_228(date.getMonth()+1),_228(date.getDate())].join("-");
};
MochiKit.DateTime.americanDate=function(d){
d=d+"";
if(typeof (d)!="string"||d.length===0){
return null;
}
var a=d.split("/");
return new Date(a[2],a[0]-1,a[1]);
};
MochiKit.DateTime._padTwo=function(n){
return (n>9)?n:"0"+n;
};
MochiKit.DateTime.toPaddedAmericanDate=function(d){
if(typeof (d)=="undefined"||d===null){
return null;
}
var _230=MochiKit.DateTime._padTwo;
return [_230(d.getMonth()+1),_230(d.getDate()),d.getFullYear()].join("/");
};
MochiKit.DateTime.toAmericanDate=function(d){
if(typeof (d)=="undefined"||d===null){
return null;
}
return [d.getMonth()+1,d.getDate(),d.getFullYear()].join("/");
};
MochiKit.DateTime.EXPORT=["isoDate","isoTimestamp","toISOTime","toISOTimestamp","toISODate","americanDate","toPaddedAmericanDate","toAmericanDate"];
MochiKit.DateTime.EXPORT_OK=[];
MochiKit.DateTime.EXPORT_TAGS={":common":MochiKit.DateTime.EXPORT,":all":MochiKit.DateTime.EXPORT};
MochiKit.DateTime.__new__=function(){
var base=this.NAME+".";
for(var k in this){
var o=this[k];
if(typeof (o)=="function"&&typeof (o.NAME)=="undefined"){
try{
o.NAME=base+k;
}
catch(e){
}
}
}
};
MochiKit.DateTime.__new__();
if(typeof (MochiKit.Base)!="undefined"){
MochiKit.Base._exportSymbols(this,MochiKit.DateTime);
}else{
(function(_231,_232){
if((typeof (JSAN)=="undefined"&&typeof (dojo)=="undefined")||(typeof (MochiKit.__compat__)=="boolean"&&MochiKit.__compat__)){
var all=_232.EXPORT_TAGS[":all"];
for(var i=0;i<all.length;i++){
_231[all[i]]=_232[all[i]];
}
}
})(this,MochiKit.DateTime);
}
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Format");
}
if(typeof (MochiKit)=="undefined"){
MochiKit={};
}
if(typeof (MochiKit.Format)=="undefined"){
MochiKit.Format={};
}
MochiKit.Format.NAME="MochiKit.Format";
MochiKit.Format.VERSION="1.3.1";
MochiKit.Format.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.Format.toString=function(){
return this.__repr__();
};
MochiKit.Format._numberFormatter=function(_233,_234,_235,_236,_237,_238,_239,_240,_241){
return function(num){
num=parseFloat(num);
if(typeof (num)=="undefined"||num===null||isNaN(num)){
return _233;
}
var _242=_234;
var _243=_235;
if(num<0){
num=-num;
}else{
_242=_242.replace(/-/,"");
}
var me=arguments.callee;
var fmt=MochiKit.Format.formatLocale(_236);
if(_237){
num=num*100;
_243=fmt.percent+_243;
}
num=MochiKit.Format.roundToFixed(num,_238);
var _245=num.split(/\./);
var _246=_245[0];
var frac=(_245.length==1)?"":_245[1];
var res="";
while(_246.length<_239){
_246="0"+_246;
}
if(_240){
while(_246.length>_240){
var i=_246.length-_240;
res=fmt.separator+_246.substring(i,_246.length)+res;
_246=_246.substring(0,i);
}
}
res=_246+res;
if(_238>0){
while(frac.length<_241){
frac=frac+"0";
}
res=res+fmt.decimal+frac;
}
return _242+res+_243;
};
};
MochiKit.Format.numberFormatter=function(_248,_249,_250){
if(typeof (_249)=="undefined"){
_249="";
}
var _251=_248.match(/((?:[0#]+,)?[0#]+)(?:\.([0#]+))?(%)?/);
if(!_251){
throw TypeError("Invalid pattern");
}
var _252=_248.substr(0,_251.index);
var _253=_248.substr(_251.index+_251[0].length);
if(_252.search(/-/)==-1){
_252=_252+"-";
}
var _254=_251[1];
var frac=(typeof (_251[2])=="string"&&_251[2]!="")?_251[2]:"";
var _255=(typeof (_251[3])=="string"&&_251[3]!="");
var tmp=_254.split(/,/);
var _257;
if(typeof (_250)=="undefined"){
_250="default";
}
if(tmp.length==1){
_257=null;
}else{
_257=tmp[1].length;
}
var _258=_254.length-_254.replace(/0/g,"").length;
var _259=frac.length-frac.replace(/0/g,"").length;
var _260=frac.length;
var rval=MochiKit.Format._numberFormatter(_249,_252,_253,_250,_255,_260,_258,_257,_259);
var m=MochiKit.Base;
if(m){
var fn=arguments.callee;
var args=m.concat(arguments);
rval.repr=function(){
return [self.NAME,"(",map(m.repr,args).join(", "),")"].join("");
};
}
return rval;
};
MochiKit.Format.formatLocale=function(_262){
if(typeof (_262)=="undefined"||_262===null){
_262="default";
}
if(typeof (_262)=="string"){
var rval=MochiKit.Format.LOCALE[_262];
if(typeof (rval)=="string"){
rval=arguments.callee(rval);
MochiKit.Format.LOCALE[_262]=rval;
}
return rval;
}else{
return _262;
}
};
MochiKit.Format.twoDigitAverage=function(_263,_264){
if(_264){
var res=_263/_264;
if(!isNaN(res)){
return MochiKit.Format.twoDigitFloat(_263/_264);
}
}
return "0";
};
MochiKit.Format.twoDigitFloat=function(_265){
var sign=(_265<0?"-":"");
var s=Math.floor(Math.abs(_265)*100).toString();
if(s=="0"){
return s;
}
if(s.length<3){
while(s.charAt(s.length-1)=="0"){
s=s.substring(0,s.length-1);
}
return sign+"0."+s;
}
var head=sign+s.substring(0,s.length-2);
var tail=s.substring(s.length-2,s.length);
if(tail=="00"){
return head;
}else{
if(tail.charAt(1)=="0"){
return head+"."+tail.charAt(0);
}else{
return head+"."+tail;
}
}
};
MochiKit.Format.lstrip=function(str,_270){
str=str+"";
if(typeof (str)!="string"){
return null;
}
if(!_270){
return str.replace(/^\s+/,"");
}else{
return str.replace(new RegExp("^["+_270+"]+"),"");
}
};
MochiKit.Format.rstrip=function(str,_271){
str=str+"";
if(typeof (str)!="string"){
return null;
}
if(!_271){
return str.replace(/\s+$/,"");
}else{
return str.replace(new RegExp("["+_271+"]+$"),"");
}
};
MochiKit.Format.strip=function(str,_272){
var self=MochiKit.Format;
return self.rstrip(self.lstrip(str,_272),_272);
};
MochiKit.Format.truncToFixed=function(_273,_274){
_273=Math.floor(_273*Math.pow(10,_274));
var res=(_273*Math.pow(10,-_274)).toFixed(_274);
if(res.charAt(0)=="."){
res="0"+res;
}
return res;
};
MochiKit.Format.roundToFixed=function(_275,_276){
return MochiKit.Format.truncToFixed(_275+0.5*Math.pow(10,-_276),_276);
};
MochiKit.Format.percentFormat=function(_277){
return MochiKit.Format.twoDigitFloat(100*_277)+"%";
};
MochiKit.Format.EXPORT=["truncToFixed","roundToFixed","numberFormatter","formatLocale","twoDigitAverage","twoDigitFloat","percentFormat","lstrip","rstrip","strip"];
MochiKit.Format.LOCALE={en_US:{separator:",",decimal:".",percent:"%"},de_DE:{separator:".",decimal:",",percent:"%"},fr_FR:{separator:" ",decimal:",",percent:"%"},"default":"en_US"};
MochiKit.Format.EXPORT_OK=[];
MochiKit.Format.EXPORT_TAGS={":all":MochiKit.Format.EXPORT,":common":MochiKit.Format.EXPORT};
MochiKit.Format.__new__=function(){
var base=this.NAME+".";
var k,v,o;
for(k in this.LOCALE){
o=this.LOCALE[k];
if(typeof (o)=="object"){
o.repr=function(){
return this.NAME;
};
o.NAME=base+"LOCALE."+k;
}
}
for(k in this){
o=this[k];
if(typeof (o)=="function"&&typeof (o.NAME)=="undefined"){
try{
o.NAME=base+k;
}
catch(e){
}
}
}
};
MochiKit.Format.__new__();
if(typeof (MochiKit.Base)!="undefined"){
MochiKit.Base._exportSymbols(this,MochiKit.Format);
}else{
(function(_278,_279){
if((typeof (JSAN)=="undefined"&&typeof (dojo)=="undefined")||(typeof (MochiKit.__compat__)=="boolean"&&MochiKit.__compat__)){
var all=_279.EXPORT_TAGS[":all"];
for(var i=0;i<all.length;i++){
_278[all[i]]=_279[all[i]];
}
}
})(this,MochiKit.Format);
}
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Async");
dojo.require("MochiKit.Base");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Async depends on MochiKit.Base!";
}
if(typeof (MochiKit.Async)=="undefined"){
MochiKit.Async={};
}
MochiKit.Async.NAME="MochiKit.Async";
MochiKit.Async.VERSION="1.3.1";
MochiKit.Async.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.Async.toString=function(){
return this.__repr__();
};
MochiKit.Async.Deferred=function(_280){
this.chain=[];
this.id=this._nextId();
this.fired=-1;
this.paused=0;
this.results=[null,null];
this.canceller=_280;
this.silentlyCancelled=false;
this.chained=false;
};
MochiKit.Async.Deferred.prototype={repr:function(){
var _281;
if(this.fired==-1){
_281="unfired";
}else{
if(this.fired===0){
_281="success";
}else{
_281="error";
}
}
return "Deferred("+this.id+", "+_281+")";
},toString:MochiKit.Base.forwardCall("repr"),_nextId:MochiKit.Base.counter(),cancel:function(){
var self=MochiKit.Async;
if(this.fired==-1){
if(this.canceller){
this.canceller(this);
}else{
this.silentlyCancelled=true;
}
if(this.fired==-1){
this.errback(new self.CancelledError(this));
}
}else{
if((this.fired===0)&&(this.results[0] instanceof self.Deferred)){
this.results[0].cancel();
}
}
},_pause:function(){
this.paused++;
},_unpause:function(){
this.paused--;
if((this.paused===0)&&(this.fired>=0)){
this._fire();
}
},_continue:function(res){
this._resback(res);
this._unpause();
},_resback:function(res){
this.fired=((res instanceof Error)?1:0);
this.results[this.fired]=res;
this._fire();
},_check:function(){
if(this.fired!=-1){
if(!this.silentlyCancelled){
throw new MochiKit.Async.AlreadyCalledError(this);
}
this.silentlyCancelled=false;
return;
}
},callback:function(res){
this._check();
if(res instanceof MochiKit.Async.Deferred){
throw new Error("Deferred instances can only be chained if they are the result of a callback");
}
this._resback(res);
},errback:function(res){
this._check();
var self=MochiKit.Async;
if(res instanceof self.Deferred){
throw new Error("Deferred instances can only be chained if they are the result of a callback");
}
if(!(res instanceof Error)){
res=new self.GenericError(res);
}
this._resback(res);
},addBoth:function(fn){
if(arguments.length>1){
fn=MochiKit.Base.partial.apply(null,arguments);
}
return this.addCallbacks(fn,fn);
},addCallback:function(fn){
if(arguments.length>1){
fn=MochiKit.Base.partial.apply(null,arguments);
}
return this.addCallbacks(fn,null);
},addErrback:function(fn){
if(arguments.length>1){
fn=MochiKit.Base.partial.apply(null,arguments);
}
return this.addCallbacks(null,fn);
},addCallbacks:function(cb,eb){
if(this.chained){
throw new Error("Chained Deferreds can not be re-used");
}
this.chain.push([cb,eb]);
if(this.fired>=0){
this._fire();
}
return this;
},_fire:function(){
var _284=this.chain;
var _285=this.fired;
var res=this.results[_285];
var self=this;
var cb=null;
while(_284.length>0&&this.paused===0){
var pair=_284.shift();
var f=pair[_285];
if(f===null){
continue;
}
try{
res=f(res);
_285=((res instanceof Error)?1:0);
if(res instanceof MochiKit.Async.Deferred){
cb=function(res){
self._continue(res);
};
this._pause();
}
}
catch(err){
_285=1;
if(!(err instanceof Error)){
err=new MochiKit.Async.GenericError(err);
}
res=err;
}
}
this.fired=_285;
this.results[_285]=res;
if(cb&&this.paused){
res.addBoth(cb);
res.chained=true;
}
}};
MochiKit.Base.update(MochiKit.Async,{evalJSONRequest:function(){
return eval("("+arguments[0].responseText+")");
},succeed:function(_287){
var d=new MochiKit.Async.Deferred();
d.callback.apply(d,arguments);
return d;
},fail:function(_288){
var d=new MochiKit.Async.Deferred();
d.errback.apply(d,arguments);
return d;
},getXMLHttpRequest:function(){
var self=arguments.callee;
if(!self.XMLHttpRequest){
var _289=[function(){
return new XMLHttpRequest();
},function(){
return new ActiveXObject("Msxml2.XMLHTTP");
},function(){
return new ActiveXObject("Microsoft.XMLHTTP");
},function(){
return new ActiveXObject("Msxml2.XMLHTTP.4.0");
},function(){
throw new MochiKit.Async.BrowserComplianceError("Browser does not support XMLHttpRequest");
}];
for(var i=0;i<_289.length;i++){
var func=_289[i];
try{
self.XMLHttpRequest=func;
return func();
}
catch(e){
}
}
}
return self.XMLHttpRequest();
},_nothing:function(){
},_xhr_onreadystatechange:function(d){
if(this.readyState==4){
try{
this.onreadystatechange=null;
}
catch(e){
try{
this.onreadystatechange=MochiKit.Async._nothing;
}
catch(e){
}
}
var _290=null;
try{
_290=this.status;
if(!_290&&MochiKit.Base.isNotEmpty(this.responseText)){
_290=304;
}
}
catch(e){
}
if(_290==200||_290==304){
d.callback(this);
}else{
var err=new MochiKit.Async.XMLHttpRequestError(this,"Request failed");
if(err.number){
d.errback(err);
}else{
d.errback(err);
}
}
}
},_xhr_canceller:function(req){
try{
req.onreadystatechange=null;
}
catch(e){
try{
req.onreadystatechange=MochiKit.Async._nothing;
}
catch(e){
}
}
req.abort();
},sendXMLHttpRequest:function(req,_293){
if(typeof (_293)=="undefined"||_293===null){
_293="";
}
var m=MochiKit.Base;
var self=MochiKit.Async;
var d=new self.Deferred(m.partial(self._xhr_canceller,req));
try{
req.onreadystatechange=m.bind(self._xhr_onreadystatechange,req,d);
req.send(_293);
}
catch(e){
try{
req.onreadystatechange=null;
}
catch(ignore){
}
d.errback(e);
}
return d;
},doSimpleXMLHttpRequest:function(url){
var self=MochiKit.Async;
var req=self.getXMLHttpRequest();
if(arguments.length>1){
var m=MochiKit.Base;
var qs=m.queryString.apply(null,m.extend(null,arguments,1));
if(qs){
url+="?"+qs;
}
}
req.open("GET",url,true);
return self.sendXMLHttpRequest(req);
},loadJSONDoc:function(url){
var self=MochiKit.Async;
var d=self.doSimpleXMLHttpRequest.apply(self,arguments);
d=d.addCallback(self.evalJSONRequest);
return d;
},wait:function(_296,_297){
var d=new MochiKit.Async.Deferred();
var m=MochiKit.Base;
if(typeof (_297)!="undefined"){
d.addCallback(function(){
return _297;
});
}
var _298=setTimeout(m.bind("callback",d),Math.floor(_296*1000));
d.canceller=function(){
try{
clearTimeout(_298);
}
catch(e){
}
};
return d;
},callLater:function(_299,func){
var m=MochiKit.Base;
var _300=m.partial.apply(m,m.extend(null,arguments,1));
return MochiKit.Async.wait(_299).addCallback(function(res){
return _300();
});
}});
MochiKit.Async.DeferredLock=function(){
this.waiting=[];
this.locked=false;
this.id=this._nextId();
};
MochiKit.Async.DeferredLock.prototype={__class__:MochiKit.Async.DeferredLock,acquire:function(){
d=new MochiKit.Async.Deferred();
if(this.locked){
this.waiting.push(d);
}else{
this.locked=true;
d.callback(this);
}
return d;
},release:function(){
if(!this.locked){
throw TypeError("Tried to release an unlocked DeferredLock");
}
this.locked=false;
if(this.waiting.length>0){
this.locked=true;
this.waiting.shift().callback(this);
}
},_nextId:MochiKit.Base.counter(),repr:function(){
var _301;
if(this.locked){
_301="locked, "+this.waiting.length+" waiting";
}else{
_301="unlocked";
}
return "DeferredLock("+this.id+", "+_301+")";
},toString:MochiKit.Base.forwardCall("repr")};
MochiKit.Async.DeferredList=function(list,_303,_304,_305,_306){
this.list=list;
this.resultList=new Array(this.list.length);
this.chain=[];
this.id=this._nextId();
this.fired=-1;
this.paused=0;
this.results=[null,null];
this.canceller=_306;
this.silentlyCancelled=false;
if(this.list.length===0&&!_303){
this.callback(this.resultList);
}
this.finishedCount=0;
this.fireOnOneCallback=_303;
this.fireOnOneErrback=_304;
this.consumeErrors=_305;
var _307=0;
MochiKit.Base.map(MochiKit.Base.bind(function(d){
d.addCallback(MochiKit.Base.bind(this._cbDeferred,this),_307,true);
d.addErrback(MochiKit.Base.bind(this._cbDeferred,this),_307,false);
_307+=1;
},this),this.list);
};
MochiKit.Base.update(MochiKit.Async.DeferredList.prototype,MochiKit.Async.Deferred.prototype);
MochiKit.Base.update(MochiKit.Async.DeferredList.prototype,{_cbDeferred:function(_308,_309,_310){
this.resultList[_308]=[_309,_310];
this.finishedCount+=1;
if(this.fired!==0){
if(_309&&this.fireOnOneCallback){
this.callback([_308,_310]);
}else{
if(!_309&&this.fireOnOneErrback){
this.errback(_310);
}else{
if(this.finishedCount==this.list.length){
this.callback(this.resultList);
}
}
}
}
if(!_309&&this.consumeErrors){
_310=null;
}
return _310;
}});
MochiKit.Async.gatherResults=function(_311){
var d=new MochiKit.Async.DeferredList(_311,false,true,false);
d.addCallback(function(_312){
var ret=[];
for(var i=0;i<_312.length;i++){
ret.push(_312[i][1]);
}
return ret;
});
return d;
};
MochiKit.Async.maybeDeferred=function(func){
var self=MochiKit.Async;
var _313;
try{
var r=func.apply(null,MochiKit.Base.extend([],arguments,1));
if(r instanceof self.Deferred){
_313=r;
}else{
if(r instanceof Error){
_313=self.fail(r);
}else{
_313=self.succeed(r);
}
}
}
catch(e){
_313=self.fail(e);
}
return _313;
};
MochiKit.Async.EXPORT=["AlreadyCalledError","CancelledError","BrowserComplianceError","GenericError","XMLHttpRequestError","Deferred","succeed","fail","getXMLHttpRequest","doSimpleXMLHttpRequest","loadJSONDoc","wait","callLater","sendXMLHttpRequest","DeferredLock","DeferredList","gatherResults","maybeDeferred"];
MochiKit.Async.EXPORT_OK=["evalJSONRequest"];
MochiKit.Async.__new__=function(){
var m=MochiKit.Base;
var ne=m.partial(m._newNamedError,this);
ne("AlreadyCalledError",function(_316){
this.deferred=_316;
});
ne("CancelledError",function(_317){
this.deferred=_317;
});
ne("BrowserComplianceError",function(msg){
this.message=msg;
});
ne("GenericError",function(msg){
this.message=msg;
});
ne("XMLHttpRequestError",function(req,msg){
this.req=req;
this.message=msg;
try{
this.number=req.status;
}
catch(e){
}
});
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
m.nameFunctions(this);
};
MochiKit.Async.__new__();
MochiKit.Base._exportSymbols(this,MochiKit.Async);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.DOM");
dojo.require("MochiKit.Iter");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Iter",[]);
}
try{
if(typeof (MochiKit.Iter)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.DOM depends on MochiKit.Iter!";
}
if(typeof (MochiKit.DOM)=="undefined"){
MochiKit.DOM={};
}
MochiKit.DOM.NAME="MochiKit.DOM";
MochiKit.DOM.VERSION="1.3.1";
MochiKit.DOM.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.DOM.toString=function(){
return this.__repr__();
};
MochiKit.DOM.EXPORT=["formContents","currentWindow","currentDocument","withWindow","withDocument","registerDOMConverter","coerceToDOM","createDOM","createDOMFunc","getNodeAttribute","setNodeAttribute","updateNodeAttributes","appendChildNodes","replaceChildNodes","removeElement","swapDOM","BUTTON","TT","PRE","H1","H2","H3","BR","CANVAS","HR","LABEL","TEXTAREA","FORM","STRONG","SELECT","OPTION","OPTGROUP","LEGEND","FIELDSET","P","UL","OL","LI","TD","TR","THEAD","TBODY","TFOOT","TABLE","TH","INPUT","SPAN","A","DIV","IMG","getElement","$","computedStyle","getElementsByTagAndClassName","addToCallStack","addLoadEvent","focusOnLoad","setElementClass","toggleElementClass","addElementClass","removeElementClass","swapElementClass","hasElementClass","escapeHTML","toHTML","emitHTML","setDisplayForElement","hideElement","showElement","scrapeText","elementDimensions","elementPosition","setElementDimensions","setElementPosition","getViewportDimensions","setOpacity"];
MochiKit.DOM.EXPORT_OK=["domConverters"];
MochiKit.DOM.Dimensions=function(w,h){
this.w=w;
this.h=h;
};
MochiKit.DOM.Dimensions.prototype.repr=function(){
var repr=MochiKit.Base.repr;
return "{w: "+repr(this.w)+", h: "+repr(this.h)+"}";
};
MochiKit.DOM.Coordinates=function(x,y){
this.x=x;
this.y=y;
};
MochiKit.DOM.Coordinates.prototype.repr=function(){
var repr=MochiKit.Base.repr;
return "{x: "+repr(this.x)+", y: "+repr(this.y)+"}";
};
MochiKit.DOM.Coordinates.prototype.toString=function(){
return this.repr();
};
MochiKit.Base.update(MochiKit.DOM,{setOpacity:function(elem,o){
elem=MochiKit.DOM.getElement(elem);
MochiKit.DOM.updateNodeAttributes(elem,{"style":{"opacity":o,"-moz-opacity":o,"-khtml-opacity":o,"filter":" alpha(opacity="+(o*100)+")"}});
},getViewportDimensions:function(){
var d=new MochiKit.DOM.Dimensions();
var w=MochiKit.DOM._window;
var b=MochiKit.DOM._document.body;
if(w.innerWidth){
d.w=w.innerWidth;
d.h=w.innerHeight;
}else{
if(b.parentElement.clientWidth){
d.w=b.parentElement.clientWidth;
d.h=b.parentElement.clientHeight;
}else{
if(b&&b.clientWidth){
d.w=b.clientWidth;
d.h=b.clientHeight;
}
}
}
return d;
},elementDimensions:function(elem){
var self=MochiKit.DOM;
if(typeof (elem.w)=="number"||typeof (elem.h)=="number"){
return new self.Dimensions(elem.w||0,elem.h||0);
}
elem=self.getElement(elem);
if(!elem){
return undefined;
}
if(self.computedStyle(elem,"display")!="none"){
return new self.Dimensions(elem.offsetWidth||0,elem.offsetHeight||0);
}
var s=elem.style;
var _322=s.visibility;
var _323=s.position;
s.visibility="hidden";
s.position="absolute";
s.display="";
var _324=elem.offsetWidth;
var _325=elem.offsetHeight;
s.display="none";
s.position=_323;
s.visibility=_322;
return new self.Dimensions(_324,_325);
},elementPosition:function(elem,_326){
var self=MochiKit.DOM;
elem=self.getElement(elem);
if(!elem){
return undefined;
}
var c=new self.Coordinates(0,0);
if(elem.x&&elem.y){
c.x+=elem.x||0;
c.y+=elem.y||0;
return c;
}else{
if(elem.parentNode===null||self.computedStyle(elem,"display")=="none"){
return undefined;
}
}
var box=null;
var _329=null;
var d=MochiKit.DOM._document;
var de=d.documentElement;
var b=d.body;
if(elem.getBoundingClientRect){
box=elem.getBoundingClientRect();
c.x+=box.left+(de.scrollLeft||b.scrollLeft)-(de.clientLeft||b.clientLeft);
c.y+=box.top+(de.scrollTop||b.scrollTop)-(de.clientTop||b.clientTop);
}else{
if(d.getBoxObjectFor){
box=d.getBoxObjectFor(elem);
c.x+=box.x;
c.y+=box.y;
}else{
if(elem.offsetParent){
c.x+=elem.offsetLeft;
c.y+=elem.offsetTop;
_329=elem.offsetParent;
if(_329!=elem){
while(_329){
c.x+=_329.offsetLeft;
c.y+=_329.offsetTop;
_329=_329.offsetParent;
}
}
var ua=navigator.userAgent.toLowerCase();
if((typeof (opera)!="undefined"&&parseFloat(opera.version())<9)||(ua.indexOf("safari")!=-1&&self.computedStyle(elem,"position")=="absolute")){
c.x-=b.offsetLeft;
c.y-=b.offsetTop;
}
}
}
}
if(typeof (_326)!="undefined"){
_326=arguments.callee(_326);
if(_326){
c.x-=(_326.x||0);
c.y-=(_326.y||0);
}
}
if(elem.parentNode){
_329=elem.parentNode;
}else{
_329=null;
}
while(_329&&_329.tagName!="BODY"&&_329.tagName!="HTML"){
c.x-=_329.scrollLeft;
c.y-=_329.scrollTop;
if(_329.parentNode){
_329=_329.parentNode;
}else{
_329=null;
}
}
return c;
},setElementDimensions:function(elem,_332,_333){
elem=MochiKit.DOM.getElement(elem);
if(typeof (_333)=="undefined"){
_333="px";
}
MochiKit.DOM.updateNodeAttributes(elem,{"style":{"width":_332.w+_333,"height":_332.h+_333}});
},setElementPosition:function(elem,_334,_335){
elem=MochiKit.DOM.getElement(elem);
if(typeof (_335)=="undefined"){
_335="px";
}
MochiKit.DOM.updateNodeAttributes(elem,{"style":{"left":_334.x+_335,"top":_334.y+_335}});
},currentWindow:function(){
return MochiKit.DOM._window;
},currentDocument:function(){
return MochiKit.DOM._document;
},withWindow:function(win,func){
var self=MochiKit.DOM;
var _337=self._document;
var _338=self._win;
var rval;
try{
self._window=win;
self._document=win.document;
rval=func();
}
catch(e){
self._window=_338;
self._document=_337;
throw e;
}
self._window=_338;
self._document=_337;
return rval;
},formContents:function(elem){
var _339=[];
var _340=[];
var m=MochiKit.Base;
var self=MochiKit.DOM;
if(typeof (elem)=="undefined"||elem===null){
elem=self._document;
}else{
elem=self.getElement(elem);
}
m.nodeWalk(elem,function(elem){
var name=elem.name;
if(m.isNotEmpty(name)){
var _341=elem.nodeName;
if(_341=="INPUT"&&(elem.type=="radio"||elem.type=="checkbox")&&!elem.checked){
return null;
}
if(_341=="SELECT"){
if(elem.selectedIndex>=0){
var opt=elem.options[elem.selectedIndex];
_339.push(name);
_340.push((opt.value)?opt.value:opt.text);
return null;
}
_339.push(name);
_340.push("");
return null;
}
if(_341=="FORM"||_341=="P"||_341=="SPAN"||_341=="DIV"){
return elem.childNodes;
}
_339.push(name);
_340.push(elem.value||"");
return null;
}
return elem.childNodes;
});
return [_339,_340];
},withDocument:function(doc,func){
var self=MochiKit.DOM;
var _344=self._document;
var rval;
try{
self._document=doc;
rval=func();
}
catch(e){
self._document=_344;
throw e;
}
self._document=_344;
return rval;
},registerDOMConverter:function(name,_345,wrap,_346){
MochiKit.DOM.domConverters.register(name,_345,wrap,_346);
},coerceToDOM:function(node,ctx){
var im=MochiKit.Iter;
var self=MochiKit.DOM;
var iter=im.iter;
var _350=im.repeat;
var imap=im.imap;
var _352=self.domConverters;
var _353=self.coerceToDOM;
var _354=MochiKit.Base.NotFound;
while(true){
if(typeof (node)=="undefined"||node===null){
return null;
}
if(typeof (node.nodeType)!="undefined"&&node.nodeType>0){
return node;
}
if(typeof (node)=="number"||typeof (node)=="boolean"){
node=node.toString();
}
if(typeof (node)=="string"){
return self._document.createTextNode(node);
}
if(typeof (node.toDOM)=="function"){
node=node.toDOM(ctx);
continue;
}
if(typeof (node)=="function"){
node=node(ctx);
continue;
}
var _355=null;
try{
_355=iter(node);
}
catch(e){
}
if(_355){
return imap(_353,_355,_350(ctx));
}
try{
node=_352.match(node,ctx);
continue;
}
catch(e){
if(e!=_354){
throw e;
}
}
return self._document.createTextNode(node.toString());
}
return undefined;
},setNodeAttribute:function(node,attr,_357){
var o={};
o[attr]=_357;
try{
return MochiKit.DOM.updateNodeAttributes(node,o);
}
catch(e){
}
return null;
},getNodeAttribute:function(node,attr){
var self=MochiKit.DOM;
var _358=self.attributeArray.renames[attr];
node=self.getElement(node);
try{
if(_358){
return node[_358];
}
return node.getAttribute(attr);
}
catch(e){
}
return null;
},updateNodeAttributes:function(node,_359){
var elem=node;
var self=MochiKit.DOM;
if(typeof (node)=="string"){
elem=self.getElement(node);
}
if(_359){
var _360=MochiKit.Base.updatetree;
if(self.attributeArray.compliant){
for(var k in _359){
var v=_359[k];
if(typeof (v)=="object"&&typeof (elem[k])=="object"){
_360(elem[k],v);
}else{
if(k.substring(0,2)=="on"){
if(typeof (v)=="string"){
v=new Function(v);
}
elem[k]=v;
}else{
elem.setAttribute(k,v);
}
}
}
}else{
var _361=self.attributeArray.renames;
for(k in _359){
v=_359[k];
var _362=_361[k];
if(k=="style"&&typeof (v)=="string"){
elem.style.cssText=v;
}else{
if(typeof (_362)=="string"){
elem[_362]=v;
}else{
if(typeof (elem[k])=="object"&&typeof (v)=="object"){
_360(elem[k],v);
}else{
if(k.substring(0,2)=="on"){
if(typeof (v)=="string"){
v=new Function(v);
}
elem[k]=v;
}else{
elem.setAttribute(k,v);
}
}
}
}
}
}
}
return elem;
},appendChildNodes:function(node){
var elem=node;
var self=MochiKit.DOM;
if(typeof (node)=="string"){
elem=self.getElement(node);
}
var _363=[self.coerceToDOM(MochiKit.Base.extend(null,arguments,1),elem)];
var _364=MochiKit.Base.concat;
while(_363.length){
var n=_363.shift();
if(typeof (n)=="undefined"||n===null){
}else{
if(typeof (n.nodeType)=="number"){
elem.appendChild(n);
}else{
_363=_364(n,_363);
}
}
}
return elem;
},replaceChildNodes:function(node){
var elem=node;
var self=MochiKit.DOM;
if(typeof (node)=="string"){
elem=self.getElement(node);
arguments[0]=elem;
}
var _365;
while((_365=elem.firstChild)){
elem.removeChild(_365);
}
if(arguments.length<2){
return elem;
}else{
return self.appendChildNodes.apply(this,arguments);
}
},createDOM:function(name,_366){
var elem;
var self=MochiKit.DOM;
var m=MochiKit.Base;
if(typeof (_366)=="string"||typeof (_366)=="number"){
var args=m.extend([name,null],arguments,1);
return arguments.callee.apply(this,args);
}
if(typeof (name)=="string"){
if(_366&&"name" in _366&&!self.attributeArray.compliant){
name=("<"+name+" name=\""+self.escapeHTML(_366.name)+"\">");
}
elem=self._document.createElement(name);
}else{
elem=name;
}
if(_366){
self.updateNodeAttributes(elem,_366);
}
if(arguments.length<=2){
return elem;
}else{
var args=m.extend([elem],arguments,2);
return self.appendChildNodes.apply(this,args);
}
},createDOMFunc:function(){
var m=MochiKit.Base;
return m.partial.apply(this,m.extend([MochiKit.DOM.createDOM],arguments));
},swapDOM:function(dest,src){
var self=MochiKit.DOM;
dest=self.getElement(dest);
var _369=dest.parentNode;
if(src){
src=self.getElement(src);
_369.replaceChild(src,dest);
}else{
_369.removeChild(dest);
}
return src;
},getElement:function(id){
var self=MochiKit.DOM;
if(arguments.length==1){
return ((typeof (id)=="string")?self._document.getElementById(id):id);
}else{
return MochiKit.Base.map(self.getElement,arguments);
}
},computedStyle:function(_371,_372,_373){
if(arguments.length==2){
_373=_372;
}
var self=MochiKit.DOM;
var el=self.getElement(_371);
var _375=self._document;
if(!el||el==_375){
return undefined;
}
if(el.currentStyle){
return el.currentStyle[_372];
}
if(typeof (_375.defaultView)=="undefined"){
return undefined;
}
if(_375.defaultView===null){
return undefined;
}
var _376=_375.defaultView.getComputedStyle(el,null);
if(typeof (_376)=="undefined"||_376===null){
return undefined;
}
return _376.getPropertyValue(_373);
},getElementsByTagAndClassName:function(_377,_378,_379){
var self=MochiKit.DOM;
if(typeof (_377)=="undefined"||_377===null){
_377="*";
}
if(typeof (_379)=="undefined"||_379===null){
_379=self._document;
}
_379=self.getElement(_379);
var _380=(_379.getElementsByTagName(_377)||self._document.all);
if(typeof (_378)=="undefined"||_378===null){
return MochiKit.Base.extend(null,_380);
}
var _381=[];
for(var i=0;i<_380.length;i++){
var _382=_380[i];
var _383=_382.className.split(" ");
for(var j=0;j<_383.length;j++){
if(_383[j]==_378){
_381.push(_382);
break;
}
}
}
return _381;
},_newCallStack:function(path,once){
var rval=function(){
var _386=arguments.callee.callStack;
for(var i=0;i<_386.length;i++){
if(_386[i].apply(this,arguments)===false){
break;
}
}
if(once){
try{
this[path]=null;
}
catch(e){
}
}
};
rval.callStack=[];
return rval;
},addToCallStack:function(_387,path,func,once){
var self=MochiKit.DOM;
var _388=_387[path];
var _389=_388;
if(!(typeof (_388)=="function"&&typeof (_388.callStack)=="object"&&_388.callStack!==null)){
_389=self._newCallStack(path,once);
if(typeof (_388)=="function"){
_389.callStack.push(_388);
}
_387[path]=_389;
}
_389.callStack.push(func);
},addLoadEvent:function(func){
var self=MochiKit.DOM;
self.addToCallStack(self._window,"onload",func,true);
},focusOnLoad:function(_390){
var self=MochiKit.DOM;
self.addLoadEvent(function(){
_390=self.getElement(_390);
if(_390){
_390.focus();
}
});
},setElementClass:function(_391,_392){
var self=MochiKit.DOM;
var obj=self.getElement(_391);
if(self.attributeArray.compliant){
obj.setAttribute("class",_392);
}else{
obj.setAttribute("className",_392);
}
},toggleElementClass:function(_393){
var self=MochiKit.DOM;
for(var i=1;i<arguments.length;i++){
var obj=self.getElement(arguments[i]);
if(!self.addElementClass(obj,_393)){
self.removeElementClass(obj,_393);
}
}
},addElementClass:function(_394,_395){
var self=MochiKit.DOM;
var obj=self.getElement(_394);
var cls=obj.className;
if(cls.length===0){
self.setElementClass(obj,_395);
return true;
}
if(cls==_395){
return false;
}
var _397=obj.className.split(" ");
for(var i=0;i<_397.length;i++){
if(_397[i]==_395){
return false;
}
}
self.setElementClass(obj,cls+" "+_395);
return true;
},removeElementClass:function(_398,_399){
var self=MochiKit.DOM;
var obj=self.getElement(_398);
var cls=obj.className;
if(cls.length===0){
return false;
}
if(cls==_399){
self.setElementClass(obj,"");
return true;
}
var _400=obj.className.split(" ");
for(var i=0;i<_400.length;i++){
if(_400[i]==_399){
_400.splice(i,1);
self.setElementClass(obj,_400.join(" "));
return true;
}
}
return false;
},swapElementClass:function(_401,_402,_403){
var obj=MochiKit.DOM.getElement(_401);
var res=MochiKit.DOM.removeElementClass(obj,_402);
if(res){
MochiKit.DOM.addElementClass(obj,_403);
}
return res;
},hasElementClass:function(_404,_405){
var obj=MochiKit.DOM.getElement(_404);
var _406=obj.className.split(" ");
for(var i=1;i<arguments.length;i++){
var good=false;
for(var j=0;j<_406.length;j++){
if(_406[j]==arguments[i]){
good=true;
break;
}
}
if(!good){
return false;
}
}
return true;
},escapeHTML:function(s){
return s.replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
},toHTML:function(dom){
return MochiKit.DOM.emitHTML(dom).join("");
},emitHTML:function(dom,lst){
if(typeof (lst)=="undefined"||lst===null){
lst=[];
}
var _409=[dom];
var self=MochiKit.DOM;
var _410=self.escapeHTML;
var _411=self.attributeArray;
while(_409.length){
dom=_409.pop();
if(typeof (dom)=="string"){
lst.push(dom);
}else{
if(dom.nodeType==1){
lst.push("<"+dom.nodeName.toLowerCase());
var _412=[];
var _413=_411(dom);
for(var i=0;i<_413.length;i++){
var a=_413[i];
_412.push([" ",a.name,"=\"",_410(a.value),"\""]);
}
_412.sort();
for(i=0;i<_412.length;i++){
var _414=_412[i];
for(var j=0;j<_414.length;j++){
lst.push(_414[j]);
}
}
if(dom.hasChildNodes()){
lst.push(">");
_409.push("</"+dom.nodeName.toLowerCase()+">");
var _415=dom.childNodes;
for(i=_415.length-1;i>=0;i--){
_409.push(_415[i]);
}
}else{
lst.push("/>");
}
}else{
if(dom.nodeType==3){
lst.push(_410(dom.nodeValue));
}
}
}
}
return lst;
},setDisplayForElement:function(_416,_417){
var m=MochiKit.Base;
var _418=m.extend(null,arguments,1);
MochiKit.Iter.forEach(m.filter(null,m.map(MochiKit.DOM.getElement,_418)),function(_417){
_417.style.display=_416;
});
},scrapeText:function(node,_419){
var rval=[];
(function(node){
var cn=node.childNodes;
if(cn){
for(var i=0;i<cn.length;i++){
arguments.callee.call(this,cn[i]);
}
}
var _421=node.nodeValue;
if(typeof (_421)=="string"){
rval.push(_421);
}
})(MochiKit.DOM.getElement(node));
if(_419){
return rval;
}else{
return rval.join("");
}
},__new__:function(win){
var m=MochiKit.Base;
this._document=document;
this._window=win;
this.domConverters=new m.AdapterRegistry();
var _422=this._document.createElement("span");
var _423;
if(_422&&_422.attributes&&_422.attributes.length>0){
var _424=m.filter;
_423=function(node){
return _424(_423.ignoreAttrFilter,node.attributes);
};
_423.ignoreAttr={};
MochiKit.Iter.forEach(_422.attributes,function(a){
_423.ignoreAttr[a.name]=a.value;
});
_423.ignoreAttrFilter=function(a){
return (_423.ignoreAttr[a.name]!=a.value);
};
_423.compliant=false;
_423.renames={"class":"className","checked":"defaultChecked","usemap":"useMap","for":"htmlFor"};
}else{
_423=function(node){
return node.attributes;
};
_423.compliant=true;
_423.renames={};
}
this.attributeArray=_423;
var _425=this.createDOMFunc;
this.UL=_425("ul");
this.OL=_425("ol");
this.LI=_425("li");
this.TD=_425("td");
this.TR=_425("tr");
this.TBODY=_425("tbody");
this.THEAD=_425("thead");
this.TFOOT=_425("tfoot");
this.TABLE=_425("table");
this.TH=_425("th");
this.INPUT=_425("input");
this.SPAN=_425("span");
this.A=_425("a");
this.DIV=_425("div");
this.IMG=_425("img");
this.BUTTON=_425("button");
this.TT=_425("tt");
this.PRE=_425("pre");
this.H1=_425("h1");
this.H2=_425("h2");
this.H3=_425("h3");
this.BR=_425("br");
this.HR=_425("hr");
this.LABEL=_425("label");
this.TEXTAREA=_425("textarea");
this.FORM=_425("form");
this.P=_425("p");
this.SELECT=_425("select");
this.OPTION=_425("option");
this.OPTGROUP=_425("optgroup");
this.LEGEND=_425("legend");
this.FIELDSET=_425("fieldset");
this.STRONG=_425("strong");
this.CANVAS=_425("canvas");
this.hideElement=m.partial(this.setDisplayForElement,"none");
this.showElement=m.partial(this.setDisplayForElement,"block");
this.removeElement=this.swapDOM;
this.$=this.getElement;
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
m.nameFunctions(this);
}});
MochiKit.DOM.__new__(((typeof (window)=="undefined")?this:window));
if(!MochiKit.__compat__){
withWindow=MochiKit.DOM.withWindow;
withDocument=MochiKit.DOM.withDocument;
}
MochiKit.Base._exportSymbols(this,MochiKit.DOM);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.LoggingPane");
dojo.require("MochiKit.Logging");
dojo.require("MochiKit.Base");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Logging",[]);
JSAN.use("MochiKit.Base",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"||typeof (MochiKit.Logging)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.LoggingPane depends on MochiKit.Base and MochiKit.Logging!";
}
if(typeof (MochiKit.LoggingPane)=="undefined"){
MochiKit.LoggingPane={};
}
MochiKit.LoggingPane.NAME="MochiKit.LoggingPane";
MochiKit.LoggingPane.VERSION="1.3.1";
MochiKit.LoggingPane.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.LoggingPane.toString=function(){
return this.__repr__();
};
MochiKit.LoggingPane.createLoggingPane=function(_426){
var m=MochiKit.LoggingPane;
_426=!(!_426);
if(m._loggingPane&&m._loggingPane.inline!=_426){
m._loggingPane.closePane();
m._loggingPane=null;
}
if(!m._loggingPane||m._loggingPane.closed){
m._loggingPane=new m.LoggingPane(_426,MochiKit.Logging.logger);
}
return m._loggingPane;
};
MochiKit.LoggingPane.LoggingPane=function(_427,_428){
if(typeof (_428)=="undefined"||_428===null){
_428=MochiKit.Logging.logger;
}
this.logger=_428;
var _429=MochiKit.Base.update;
var _430=MochiKit.Base.updatetree;
var bind=MochiKit.Base.bind;
var _431=MochiKit.Base.clone;
var win=window;
var uid="_MochiKit_LoggingPane";
if(typeof (MochiKit.DOM)!="undefined"){
win=MochiKit.DOM.currentWindow();
}
if(!_427){
var url=win.location.href.split("?")[0].replace(/[:\/.><&]/g,"_");
var name=uid+"_"+url;
var nwin=win.open("",name,"dependent,resizable,height=200");
if(!nwin){
alert("Not able to open debugging window due to pop-up blocking.");
return undefined;
}
nwin.document.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\" "+"\"http://www.w3.org/TR/html4/loose.dtd\">"+"<html><head><title>[MochiKit.LoggingPane]</title></head>"+"<body></body></html>");
nwin.document.close();
nwin.document.title+=" "+win.document.title;
win=nwin;
}
var doc=win.document;
this.doc=doc;
var _434=doc.getElementById(uid);
var _435=!!_434;
if(_434&&typeof (_434.loggingPane)!="undefined"){
_434.loggingPane.logger=this.logger;
_434.loggingPane.buildAndApplyFilter();
return _434.loggingPane;
}
if(_435){
var _436;
while((_436=_434.firstChild)){
_434.removeChild(_436);
}
}else{
_434=doc.createElement("div");
_434.id=uid;
}
_434.loggingPane=this;
var _437=doc.createElement("input");
var _438=doc.createElement("input");
var _439=doc.createElement("button");
var _440=doc.createElement("button");
var _441=doc.createElement("button");
var _442=doc.createElement("button");
var _443=doc.createElement("div");
var _444=doc.createElement("div");
var _445=uid+"_Listener";
this.colorTable=_431(this.colorTable);
var _446=[];
var _447=null;
var _448=function(msg){
var _449=msg.level;
if(typeof (_449)=="number"){
_449=MochiKit.Logging.LogLevel[_449];
}
return _449;
};
var _450=function(msg){
return msg.info.join(" ");
};
var _451=bind(function(msg){
var _452=_448(msg);
var text=_450(msg);
var c=this.colorTable[_452];
var p=doc.createElement("span");
p.className="MochiKit-LogMessage MochiKit-LogLevel-"+_452;
p.style.cssText="margin: 0px; white-space: -moz-pre-wrap; white-space: -o-pre-wrap; white-space: pre-wrap; white-space: pre-line; word-wrap: break-word; wrap-option: emergency; color: "+c;
p.appendChild(doc.createTextNode(_452+": "+text));
_444.appendChild(p);
_444.appendChild(doc.createElement("br"));
if(_443.offsetHeight>_443.scrollHeight){
_443.scrollTop=0;
}else{
_443.scrollTop=_443.scrollHeight;
}
},this);
var _454=function(msg){
_446[_446.length]=msg;
_451(msg);
};
var _455=function(){
var _456,infore;
try{
_456=new RegExp(_437.value);
infore=new RegExp(_438.value);
}
catch(e){
logDebug("Error in filter regex: "+e.message);
return null;
}
return function(msg){
return (_456.test(_448(msg))&&infore.test(_450(msg)));
};
};
var _457=function(){
while(_444.firstChild){
_444.removeChild(_444.firstChild);
}
};
var _458=function(){
_446=[];
_457();
};
var _459=bind(function(){
if(this.closed){
return;
}
this.closed=true;
if(MochiKit.LoggingPane._loggingPane==this){
MochiKit.LoggingPane._loggingPane=null;
}
this.logger.removeListener(_445);
_434.loggingPane=null;
if(_427){
_434.parentNode.removeChild(_434);
}else{
this.win.close();
}
},this);
var _460=function(){
_457();
for(var i=0;i<_446.length;i++){
var msg=_446[i];
if(_447===null||_447(msg)){
_451(msg);
}
}
};
this.buildAndApplyFilter=function(){
_447=_455();
_460();
this.logger.removeListener(_445);
this.logger.addListener(_445,_447,_454);
};
var _461=bind(function(){
_446=this.logger.getMessages();
_460();
},this);
var _462=bind(function(_463){
_463=_463||window.event;
key=_463.which||_463.keyCode;
if(key==13){
this.buildAndApplyFilter();
}
},this);
var _464="display: block; z-index: 1000; left: 0px; bottom: 0px; position: fixed; width: 100%; background-color: white; font: "+this.logFont;
if(_427){
_464+="; height: 10em; border-top: 2px solid black";
}else{
_464+="; height: 100%;";
}
_434.style.cssText=_464;
if(!_435){
doc.body.appendChild(_434);
}
_464={"cssText":"width: 33%; display: inline; font: "+this.logFont};
_430(_437,{"value":"FATAL|ERROR|WARNING|INFO|DEBUG","onkeypress":_462,"style":_464});
_434.appendChild(_437);
_430(_438,{"value":".*","onkeypress":_462,"style":_464});
_434.appendChild(_438);
_464="width: 8%; display:inline; font: "+this.logFont;
_439.appendChild(doc.createTextNode("Filter"));
_439.onclick=bind("buildAndApplyFilter",this);
_439.style.cssText=_464;
_434.appendChild(_439);
_440.appendChild(doc.createTextNode("Load"));
_440.onclick=_461;
_440.style.cssText=_464;
_434.appendChild(_440);
_441.appendChild(doc.createTextNode("Clear"));
_441.onclick=_458;
_441.style.cssText=_464;
_434.appendChild(_441);
_442.appendChild(doc.createTextNode("Close"));
_442.onclick=_459;
_442.style.cssText=_464;
_434.appendChild(_442);
_443.style.cssText="overflow: auto; width: 100%";
_444.style.cssText="width: 100%; height: "+(_427?"8em":"100%");
_443.appendChild(_444);
_434.appendChild(_443);
this.buildAndApplyFilter();
_461();
if(_427){
this.win=undefined;
}else{
this.win=win;
}
this.inline=_427;
this.closePane=_459;
this.closed=false;
return this;
};
MochiKit.LoggingPane.LoggingPane.prototype={"logFont":"8pt Verdana,sans-serif","colorTable":{"ERROR":"red","FATAL":"darkred","WARNING":"blue","INFO":"black","DEBUG":"green"}};
MochiKit.LoggingPane.EXPORT_OK=["LoggingPane"];
MochiKit.LoggingPane.EXPORT=["createLoggingPane"];
MochiKit.LoggingPane.__new__=function(){
this.EXPORT_TAGS={":common":this.EXPORT,":all":MochiKit.Base.concat(this.EXPORT,this.EXPORT_OK)};
MochiKit.Base.nameFunctions(this);
MochiKit.LoggingPane._loggingPane=null;
};
MochiKit.LoggingPane.__new__();
MochiKit.Base._exportSymbols(this,MochiKit.LoggingPane);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Color");
dojo.require("MochiKit.Base");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Color depends on MochiKit.Base";
}
if(typeof (MochiKit.Color)=="undefined"){
MochiKit.Color={};
}
MochiKit.Color.NAME="MochiKit.Color";
MochiKit.Color.VERSION="1.3.1";
MochiKit.Color.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.Color.toString=function(){
return this.__repr__();
};
MochiKit.Color.Color=function(red,_466,blue,_468){
if(typeof (_468)=="undefined"||_468===null){
_468=1;
}
this.rgb={r:red,g:_466,b:blue,a:_468};
};
MochiKit.Color.Color.prototype={__class__:MochiKit.Color.Color,colorWithAlpha:function(_469){
var rgb=this.rgb;
var m=MochiKit.Color;
return m.Color.fromRGB(rgb.r,rgb.g,rgb.b,_469);
},colorWithHue:function(hue){
var hsl=this.asHSL();
hsl.h=hue;
var m=MochiKit.Color;
return m.Color.fromHSL(hsl);
},colorWithSaturation:function(_473){
var hsl=this.asHSL();
hsl.s=_473;
var m=MochiKit.Color;
return m.Color.fromHSL(hsl);
},colorWithLightness:function(_474){
var hsl=this.asHSL();
hsl.l=_474;
var m=MochiKit.Color;
return m.Color.fromHSL(hsl);
},darkerColorWithLevel:function(_475){
var hsl=this.asHSL();
hsl.l=Math.max(hsl.l-_475,0);
var m=MochiKit.Color;
return m.Color.fromHSL(hsl);
},lighterColorWithLevel:function(_476){
var hsl=this.asHSL();
hsl.l=Math.min(hsl.l+_476,1);
var m=MochiKit.Color;
return m.Color.fromHSL(hsl);
},blendedColor:function(_477,_478){
if(typeof (_478)=="undefined"||_478===null){
_478=0.5;
}
var sf=1-_478;
var s=this.rgb;
var d=_477.rgb;
var df=_478;
return MochiKit.Color.Color.fromRGB((s.r*sf)+(d.r*df),(s.g*sf)+(d.g*df),(s.b*sf)+(d.b*df),(s.a*sf)+(d.a*df));
},compareRGB:function(_481){
var a=this.asRGB();
var b=_481.asRGB();
return MochiKit.Base.compare([a.r,a.g,a.b,a.a],[b.r,b.g,b.b,b.a]);
},isLight:function(){
return this.asHSL().b>0.5;
},isDark:function(){
return (!this.isLight());
},toHSLString:function(){
var c=this.asHSL();
var ccc=MochiKit.Color.clampColorComponent;
var rval=this._hslString;
if(!rval){
var mid=(ccc(c.h,360).toFixed(0)+","+ccc(c.s,100).toPrecision(4)+"%"+","+ccc(c.l,100).toPrecision(4)+"%");
var a=c.a;
if(a>=1){
a=1;
rval="hsl("+mid+")";
}else{
if(a<=0){
a=0;
}
rval="hsla("+mid+","+a+")";
}
this._hslString=rval;
}
return rval;
},toRGBString:function(){
var c=this.rgb;
var ccc=MochiKit.Color.clampColorComponent;
var rval=this._rgbString;
if(!rval){
var mid=(ccc(c.r,255).toFixed(0)+","+ccc(c.g,255).toFixed(0)+","+ccc(c.b,255).toFixed(0));
if(c.a!=1){
rval="rgba("+mid+","+c.a+")";
}else{
rval="rgb("+mid+")";
}
this._rgbString=rval;
}
return rval;
},asRGB:function(){
return MochiKit.Base.clone(this.rgb);
},toHexString:function(){
var m=MochiKit.Color;
var c=this.rgb;
var ccc=MochiKit.Color.clampColorComponent;
var rval=this._hexString;
if(!rval){
rval=("#"+m.toColorPart(ccc(c.r,255))+m.toColorPart(ccc(c.g,255))+m.toColorPart(ccc(c.b,255)));
this._hexString=rval;
}
return rval;
},asHSV:function(){
var hsv=this.hsv;
var c=this.rgb;
if(typeof (hsv)=="undefined"||hsv===null){
hsv=MochiKit.Color.rgbToHSV(this.rgb);
this.hsv=hsv;
}
return MochiKit.Base.clone(hsv);
},asHSL:function(){
var hsl=this.hsl;
var c=this.rgb;
if(typeof (hsl)=="undefined"||hsl===null){
hsl=MochiKit.Color.rgbToHSL(this.rgb);
this.hsl=hsl;
}
return MochiKit.Base.clone(hsl);
},toString:function(){
return this.toRGBString();
},repr:function(){
var c=this.rgb;
var col=[c.r,c.g,c.b,c.a];
return this.__class__.NAME+"("+col.join(", ")+")";
}};
MochiKit.Base.update(MochiKit.Color.Color,{fromRGB:function(red,_486,blue,_487){
var _488=MochiKit.Color.Color;
if(arguments.length==1){
var rgb=red;
red=rgb.r;
_486=rgb.g;
blue=rgb.b;
if(typeof (rgb.a)=="undefined"){
_487=undefined;
}else{
_487=rgb.a;
}
}
return new _488(red,_486,blue,_487);
},fromHSL:function(hue,_489,_490,_491){
var m=MochiKit.Color;
return m.Color.fromRGB(m.hslToRGB.apply(m,arguments));
},fromHSV:function(hue,_492,_493,_494){
var m=MochiKit.Color;
return m.Color.fromRGB(m.hsvToRGB.apply(m,arguments));
},fromName:function(name){
var _495=MochiKit.Color.Color;
if(name.charAt(0)=="\""){
name=name.substr(1,name.length-2);
}
var _496=_495._namedColors[name.toLowerCase()];
if(typeof (_496)=="string"){
return _495.fromHexString(_496);
}else{
if(name=="transparent"){
return _495.transparentColor();
}
}
return null;
},fromString:function(_497){
var self=MochiKit.Color.Color;
var _498=_497.substr(0,3);
if(_498=="rgb"){
return self.fromRGBString(_497);
}else{
if(_498=="hsl"){
return self.fromHSLString(_497);
}else{
if(_497.charAt(0)=="#"){
return self.fromHexString(_497);
}
}
}
return self.fromName(_497);
},fromHexString:function(_499){
if(_499.charAt(0)=="#"){
_499=_499.substring(1);
}
var _500=[];
var i,hex;
if(_499.length==3){
for(i=0;i<3;i++){
hex=_499.substr(i,1);
_500.push(parseInt(hex+hex,16)/255);
}
}else{
for(i=0;i<6;i+=2){
hex=_499.substr(i,2);
_500.push(parseInt(hex,16)/255);
}
}
var _501=MochiKit.Color.Color;
return _501.fromRGB.apply(_501,_500);
},_fromColorString:function(pre,_503,_504,_505){
if(_505.indexOf(pre)===0){
_505=_505.substring(_505.indexOf("(",3)+1,_505.length-1);
}
var _506=_505.split(/\s*,\s*/);
var _507=[];
for(var i=0;i<_506.length;i++){
var c=_506[i];
var val;
var _508=c.substring(c.length-3);
if(c.charAt(c.length-1)=="%"){
val=0.01*parseFloat(c.substring(0,c.length-1));
}else{
if(_508=="deg"){
val=parseFloat(c)/360;
}else{
if(_508=="rad"){
val=parseFloat(c)/(Math.PI*2);
}else{
val=_504[i]*parseFloat(c);
}
}
}
_507.push(val);
}
return this[_503].apply(this,_507);
},fromComputedStyle:function(elem,_509,_510){
var d=MochiKit.DOM;
var cls=MochiKit.Color.Color;
for(elem=d.getElement(elem);elem;elem=elem.parentNode){
var _511=d.computedStyle.apply(d,arguments);
if(!_511){
continue;
}
var _512=cls.fromString(_511);
if(!_512){
break;
}
if(_512.asRGB().a>0){
return _512;
}
}
return null;
},fromBackground:function(elem){
var cls=MochiKit.Color.Color;
return cls.fromComputedStyle(elem,"backgroundColor","background-color")||cls.whiteColor();
},fromText:function(elem){
var cls=MochiKit.Color.Color;
return cls.fromComputedStyle(elem,"color","color")||cls.blackColor();
},namedColors:function(){
return MochiKit.Base.clone(MochiKit.Color.Color._namedColors);
}});
MochiKit.Base.update(MochiKit.Color,{clampColorComponent:function(v,_513){
v*=_513;
if(v<0){
return 0;
}else{
if(v>_513){
return _513;
}else{
return v;
}
}
},_hslValue:function(n1,n2,hue){
if(hue>6){
hue-=6;
}else{
if(hue<0){
hue+=6;
}
}
var val;
if(hue<1){
val=n1+(n2-n1)*hue;
}else{
if(hue<3){
val=n2;
}else{
if(hue<4){
val=n1+(n2-n1)*(4-hue);
}else{
val=n1;
}
}
}
return val;
},hsvToRGB:function(hue,_516,_517,_518){
if(arguments.length==1){
var hsv=hue;
hue=hsv.h;
_516=hsv.s;
_517=hsv.v;
_518=hsv.a;
}
var red;
var _519;
var blue;
if(_516===0){
red=0;
_519=0;
blue=0;
}else{
var i=Math.floor(hue*6);
var f=(hue*6)-i;
var p=_517*(1-_516);
var q=_517*(1-(_516*f));
var t=_517*(1-(_516*(1-f)));
switch(i){
case 1:
red=q;
_519=_517;
blue=p;
break;
case 2:
red=p;
_519=_517;
blue=t;
break;
case 3:
red=p;
_519=q;
blue=_517;
break;
case 4:
red=t;
_519=p;
blue=_517;
break;
case 5:
red=_517;
_519=p;
blue=q;
break;
case 6:
case 0:
red=_517;
_519=t;
blue=p;
break;
}
}
return {r:red,g:_519,b:blue,a:_518};
},hslToRGB:function(hue,_521,_522,_523){
if(arguments.length==1){
var hsl=hue;
hue=hsl.h;
_521=hsl.s;
_522=hsl.l;
_523=hsl.a;
}
var red;
var _524;
var blue;
if(_521===0){
red=_522;
_524=_522;
blue=_522;
}else{
var m2;
if(_522<=0.5){
m2=_522*(1+_521);
}else{
m2=_522+_521-(_522*_521);
}
var m1=(2*_522)-m2;
var f=MochiKit.Color._hslValue;
var h6=hue*6;
red=f(m1,m2,h6+2);
_524=f(m1,m2,h6);
blue=f(m1,m2,h6-2);
}
return {r:red,g:_524,b:blue,a:_523};
},rgbToHSV:function(red,_528,blue,_529){
if(arguments.length==1){
var rgb=red;
red=rgb.r;
_528=rgb.g;
blue=rgb.b;
_529=rgb.a;
}
var max=Math.max(Math.max(red,_528),blue);
var min=Math.min(Math.min(red,_528),blue);
var hue;
var _532;
var _533=max;
if(min==max){
hue=0;
_532=0;
}else{
var _534=(max-min);
_532=_534/max;
if(red==max){
hue=(_528-blue)/_534;
}else{
if(_528==max){
hue=2+((blue-red)/_534);
}else{
hue=4+((red-_528)/_534);
}
}
hue/=6;
if(hue<0){
hue+=1;
}
if(hue>1){
hue-=1;
}
}
return {h:hue,s:_532,v:_533,a:_529};
},rgbToHSL:function(red,_535,blue,_536){
if(arguments.length==1){
var rgb=red;
red=rgb.r;
_535=rgb.g;
blue=rgb.b;
_536=rgb.a;
}
var max=Math.max(red,Math.max(_535,blue));
var min=Math.min(red,Math.min(_535,blue));
var hue;
var _537;
var _538=(max+min)/2;
var _539=max-min;
if(_539===0){
hue=0;
_537=0;
}else{
if(_538<=0.5){
_537=_539/(max+min);
}else{
_537=_539/(2-max-min);
}
if(red==max){
hue=(_535-blue)/_539;
}else{
if(_535==max){
hue=2+((blue-red)/_539);
}else{
hue=4+((red-_535)/_539);
}
}
hue/=6;
if(hue<0){
hue+=1;
}
if(hue>1){
hue-=1;
}
}
return {h:hue,s:_537,l:_538,a:_536};
},toColorPart:function(num){
num=Math.round(num);
var _540=num.toString(16);
if(num<16){
return "0"+_540;
}
return _540;
},__new__:function(){
var m=MochiKit.Base;
this.Color.fromRGBString=m.bind(this.Color._fromColorString,this.Color,"rgb","fromRGB",[1/255,1/255,1/255,1]);
this.Color.fromHSLString=m.bind(this.Color._fromColorString,this.Color,"hsl","fromHSL",[1/360,0.01,0.01,1]);
var _541=1/3;
var _542={black:[0,0,0],blue:[0,0,1],brown:[0.6,0.4,0.2],cyan:[0,1,1],darkGray:[_541,_541,_541],gray:[0.5,0.5,0.5],green:[0,1,0],lightGray:[2*_541,2*_541,2*_541],magenta:[1,0,1],orange:[1,0.5,0],purple:[0.5,0,0.5],red:[1,0,0],transparent:[0,0,0,0],white:[1,1,1],yellow:[1,1,0]};
var _543=function(name,r,g,b,a){
var rval=this.fromRGB(r,g,b,a);
this[name]=function(){
return rval;
};
return rval;
};
for(var k in _542){
var name=k+"Color";
var _545=m.concat([_543,this.Color,name],_542[k]);
this.Color[name]=m.bind.apply(null,_545);
}
var _546=function(){
for(var i=0;i<arguments.length;i++){
if(!(arguments[i] instanceof Color)){
return false;
}
}
return true;
};
var _547=function(a,b){
return a.compareRGB(b);
};
m.nameFunctions(this);
m.registerComparator(this.Color.NAME,_546,_547);
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
}});
MochiKit.Color.EXPORT=["Color"];
MochiKit.Color.EXPORT_OK=["clampColorComponent","rgbToHSL","hslToRGB","rgbToHSV","hsvToRGB","toColorPart"];
MochiKit.Color.__new__();
MochiKit.Base._exportSymbols(this,MochiKit.Color);
MochiKit.Color.Color._namedColors={aliceblue:"#f0f8ff",antiquewhite:"#faebd7",aqua:"#00ffff",aquamarine:"#7fffd4",azure:"#f0ffff",beige:"#f5f5dc",bisque:"#ffe4c4",black:"#000000",blanchedalmond:"#ffebcd",blue:"#0000ff",blueviolet:"#8a2be2",brown:"#a52a2a",burlywood:"#deb887",cadetblue:"#5f9ea0",chartreuse:"#7fff00",chocolate:"#d2691e",coral:"#ff7f50",cornflowerblue:"#6495ed",cornsilk:"#fff8dc",crimson:"#dc143c",cyan:"#00ffff",darkblue:"#00008b",darkcyan:"#008b8b",darkgoldenrod:"#b8860b",darkgray:"#a9a9a9",darkgreen:"#006400",darkgrey:"#a9a9a9",darkkhaki:"#bdb76b",darkmagenta:"#8b008b",darkolivegreen:"#556b2f",darkorange:"#ff8c00",darkorchid:"#9932cc",darkred:"#8b0000",darksalmon:"#e9967a",darkseagreen:"#8fbc8f",darkslateblue:"#483d8b",darkslategray:"#2f4f4f",darkslategrey:"#2f4f4f",darkturquoise:"#00ced1",darkviolet:"#9400d3",deeppink:"#ff1493",deepskyblue:"#00bfff",dimgray:"#696969",dimgrey:"#696969",dodgerblue:"#1e90ff",firebrick:"#b22222",floralwhite:"#fffaf0",forestgreen:"#228b22",fuchsia:"#ff00ff",gainsboro:"#dcdcdc",ghostwhite:"#f8f8ff",gold:"#ffd700",goldenrod:"#daa520",gray:"#808080",green:"#008000",greenyellow:"#adff2f",grey:"#808080",honeydew:"#f0fff0",hotpink:"#ff69b4",indianred:"#cd5c5c",indigo:"#4b0082",ivory:"#fffff0",khaki:"#f0e68c",lavender:"#e6e6fa",lavenderblush:"#fff0f5",lawngreen:"#7cfc00",lemonchiffon:"#fffacd",lightblue:"#add8e6",lightcoral:"#f08080",lightcyan:"#e0ffff",lightgoldenrodyellow:"#fafad2",lightgray:"#d3d3d3",lightgreen:"#90ee90",lightgrey:"#d3d3d3",lightpink:"#ffb6c1",lightsalmon:"#ffa07a",lightseagreen:"#20b2aa",lightskyblue:"#87cefa",lightslategray:"#778899",lightslategrey:"#778899",lightsteelblue:"#b0c4de",lightyellow:"#ffffe0",lime:"#00ff00",limegreen:"#32cd32",linen:"#faf0e6",magenta:"#ff00ff",maroon:"#800000",mediumaquamarine:"#66cdaa",mediumblue:"#0000cd",mediumorchid:"#ba55d3",mediumpurple:"#9370db",mediumseagreen:"#3cb371",mediumslateblue:"#7b68ee",mediumspringgreen:"#00fa9a",mediumturquoise:"#48d1cc",mediumvioletred:"#c71585",midnightblue:"#191970",mintcream:"#f5fffa",mistyrose:"#ffe4e1",moccasin:"#ffe4b5",navajowhite:"#ffdead",navy:"#000080",oldlace:"#fdf5e6",olive:"#808000",olivedrab:"#6b8e23",orange:"#ffa500",orangered:"#ff4500",orchid:"#da70d6",palegoldenrod:"#eee8aa",palegreen:"#98fb98",paleturquoise:"#afeeee",palevioletred:"#db7093",papayawhip:"#ffefd5",peachpuff:"#ffdab9",peru:"#cd853f",pink:"#ffc0cb",plum:"#dda0dd",powderblue:"#b0e0e6",purple:"#800080",red:"#ff0000",rosybrown:"#bc8f8f",royalblue:"#4169e1",saddlebrown:"#8b4513",salmon:"#fa8072",sandybrown:"#f4a460",seagreen:"#2e8b57",seashell:"#fff5ee",sienna:"#a0522d",silver:"#c0c0c0",skyblue:"#87ceeb",slateblue:"#6a5acd",slategray:"#708090",slategrey:"#708090",snow:"#fffafa",springgreen:"#00ff7f",steelblue:"#4682b4",tan:"#d2b48c",teal:"#008080",thistle:"#d8bfd8",tomato:"#ff6347",turquoise:"#40e0d0",violet:"#ee82ee",wheat:"#f5deb3",white:"#ffffff",whitesmoke:"#f5f5f5",yellow:"#ffff00",yellowgreen:"#9acd32"};
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Signal");
dojo.require("MochiKit.Base");
dojo.require("MochiKit.DOM");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
JSAN.use("MochiKit.DOM",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Signal depends on MochiKit.Base!";
}
try{
if(typeof (MochiKit.DOM)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Signal depends on MochiKit.DOM!";
}
if(typeof (MochiKit.Signal)=="undefined"){
MochiKit.Signal={};
}
MochiKit.Signal.NAME="MochiKit.Signal";
MochiKit.Signal.VERSION="1.3.1";
MochiKit.Signal._observers=[];
MochiKit.Signal.Event=function(src,e){
this._event=e||window.event;
this._src=src;
};
MochiKit.Base.update(MochiKit.Signal.Event.prototype,{__repr__:function(){
var repr=MochiKit.Base.repr;
var str="{event(): "+repr(this.event())+", src(): "+repr(this.src())+", type(): "+repr(this.type())+", target(): "+repr(this.target())+", modifier(): "+"{alt: "+repr(this.modifier().alt)+", ctrl: "+repr(this.modifier().ctrl)+", meta: "+repr(this.modifier().meta)+", shift: "+repr(this.modifier().shift)+", any: "+repr(this.modifier().any)+"}";
if(this.type()&&this.type().indexOf("key")===0){
str+=", key(): {code: "+repr(this.key().code)+", string: "+repr(this.key().string)+"}";
}
if(this.type()&&(this.type().indexOf("mouse")===0||this.type().indexOf("click")!=-1||this.type()=="contextmenu")){
str+=", mouse(): {page: "+repr(this.mouse().page)+", client: "+repr(this.mouse().client);
if(this.type()!="mousemove"){
str+=", button: {left: "+repr(this.mouse().button.left)+", middle: "+repr(this.mouse().button.middle)+", right: "+repr(this.mouse().button.right)+"}}";
}else{
str+="}";
}
}
if(this.type()=="mouseover"||this.type()=="mouseout"){
str+=", relatedTarget(): "+repr(this.relatedTarget());
}
str+="}";
return str;
},toString:function(){
return this.__repr__();
},src:function(){
return this._src;
},event:function(){
return this._event;
},type:function(){
return this._event.type||undefined;
},target:function(){
return this._event.target||this._event.srcElement;
},relatedTarget:function(){
if(this.type()=="mouseover"){
return (this._event.relatedTarget||this._event.fromElement);
}else{
if(this.type()=="mouseout"){
return (this._event.relatedTarget||this._event.toElement);
}
}
return undefined;
},modifier:function(){
var m={};
m.alt=this._event.altKey;
m.ctrl=this._event.ctrlKey;
m.meta=this._event.metaKey||false;
m.shift=this._event.shiftKey;
m.any=m.alt||m.ctrl||m.shift||m.meta;
return m;
},key:function(){
var k={};
if(this.type()&&this.type().indexOf("key")===0){
if(this.type()=="keydown"||this.type()=="keyup"){
k.code=this._event.keyCode;
k.string=(MochiKit.Signal._specialKeys[k.code]||"KEY_UNKNOWN");
return k;
}else{
if(this.type()=="keypress"){
k.code=0;
k.string="";
if(typeof (this._event.charCode)!="undefined"&&this._event.charCode!==0&&!MochiKit.Signal._specialMacKeys[this._event.charCode]){
k.code=this._event.charCode;
k.string=String.fromCharCode(k.code);
}else{
if(this._event.keyCode&&typeof (this._event.charCode)=="undefined"){
k.code=this._event.keyCode;
k.string=String.fromCharCode(k.code);
}
}
return k;
}
}
}
return undefined;
},mouse:function(){
var m={};
var e=this._event;
if(this.type()&&(this.type().indexOf("mouse")===0||this.type().indexOf("click")!=-1||this.type()=="contextmenu")){
m.client=new MochiKit.DOM.Coordinates(0,0);
if(e.clientX||e.clientY){
m.client.x=(!e.clientX||e.clientX<0)?0:e.clientX;
m.client.y=(!e.clientY||e.clientY<0)?0:e.clientY;
}
m.page=new MochiKit.DOM.Coordinates(0,0);
if(e.pageX||e.pageY){
m.page.x=(!e.pageX||e.pageX<0)?0:e.pageX;
m.page.y=(!e.pageY||e.pageY<0)?0:e.pageY;
}else{
var de=MochiKit.DOM._document.documentElement;
var b=MochiKit.DOM._document.body;
m.page.x=e.clientX+(de.scrollLeft||b.scrollLeft)-(de.clientLeft||b.clientLeft);
m.page.y=e.clientY+(de.scrollTop||b.scrollTop)-(de.clientTop||b.clientTop);
}
if(this.type()!="mousemove"){
m.button={};
m.button.left=false;
m.button.right=false;
m.button.middle=false;
if(e.which){
m.button.left=(e.which==1);
m.button.middle=(e.which==2);
m.button.right=(e.which==3);
}else{
m.button.left=!!(e.button&1);
m.button.right=!!(e.button&2);
m.button.middle=!!(e.button&4);
}
}
return m;
}
return undefined;
},stop:function(){
this.stopPropagation();
this.preventDefault();
},stopPropagation:function(){
if(this._event.stopPropagation){
this._event.stopPropagation();
}else{
this._event.cancelBubble=true;
}
},preventDefault:function(){
if(this._event.preventDefault){
this._event.preventDefault();
}else{
this._event.returnValue=false;
}
}});
MochiKit.Signal._specialMacKeys={3:"KEY_ENTER",63289:"KEY_NUM_PAD_CLEAR",63276:"KEY_PAGE_UP",63277:"KEY_PAGE_DOWN",63275:"KEY_END",63273:"KEY_HOME",63234:"KEY_ARROW_LEFT",63232:"KEY_ARROW_UP",63235:"KEY_ARROW_RIGHT",63233:"KEY_ARROW_DOWN",63302:"KEY_INSERT",63272:"KEY_DELETE"};
for(i=63236;i<=63242;i++){
MochiKit.Signal._specialMacKeys[i]="KEY_F"+(i-63236+1);
}
MochiKit.Signal._specialKeys={8:"KEY_BACKSPACE",9:"KEY_TAB",12:"KEY_NUM_PAD_CLEAR",13:"KEY_ENTER",16:"KEY_SHIFT",17:"KEY_CTRL",18:"KEY_ALT",19:"KEY_PAUSE",20:"KEY_CAPS_LOCK",27:"KEY_ESCAPE",32:"KEY_SPACEBAR",33:"KEY_PAGE_UP",34:"KEY_PAGE_DOWN",35:"KEY_END",36:"KEY_HOME",37:"KEY_ARROW_LEFT",38:"KEY_ARROW_UP",39:"KEY_ARROW_RIGHT",40:"KEY_ARROW_DOWN",44:"KEY_PRINT_SCREEN",45:"KEY_INSERT",46:"KEY_DELETE",59:"KEY_SEMICOLON",91:"KEY_WINDOWS_LEFT",92:"KEY_WINDOWS_RIGHT",93:"KEY_SELECT",106:"KEY_NUM_PAD_ASTERISK",107:"KEY_NUM_PAD_PLUS_SIGN",109:"KEY_NUM_PAD_HYPHEN-MINUS",110:"KEY_NUM_PAD_FULL_STOP",111:"KEY_NUM_PAD_SOLIDUS",144:"KEY_NUM_LOCK",145:"KEY_SCROLL_LOCK",186:"KEY_SEMICOLON",187:"KEY_EQUALS_SIGN",188:"KEY_COMMA",189:"KEY_HYPHEN-MINUS",190:"KEY_FULL_STOP",191:"KEY_SOLIDUS",192:"KEY_GRAVE_ACCENT",219:"KEY_LEFT_SQUARE_BRACKET",220:"KEY_REVERSE_SOLIDUS",221:"KEY_RIGHT_SQUARE_BRACKET",222:"KEY_APOSTROPHE"};
for(var i=48;i<=57;i++){
MochiKit.Signal._specialKeys[i]="KEY_"+(i-48);
}
for(i=65;i<=90;i++){
MochiKit.Signal._specialKeys[i]="KEY_"+String.fromCharCode(i);
}
for(i=96;i<=105;i++){
MochiKit.Signal._specialKeys[i]="KEY_NUM_PAD_"+(i-96);
}
for(i=112;i<=123;i++){
MochiKit.Signal._specialKeys[i]="KEY_F"+(i-112+1);
}
MochiKit.Base.update(MochiKit.Signal,{__repr__:function(){
return "["+this.NAME+" "+this.VERSION+"]";
},toString:function(){
return this.__repr__();
},_unloadCache:function(){
var self=MochiKit.Signal;
var _548=self._observers;
for(var i=0;i<_548.length;i++){
self._disconnect(_548[i]);
}
delete self._observers;
try{
window.onload=undefined;
}
catch(e){
}
try{
window.onunload=undefined;
}
catch(e){
}
},_listener:function(src,func,obj,_549){
var E=MochiKit.Signal.Event;
if(!_549){
return MochiKit.Base.bind(func,obj);
}
obj=obj||src;
if(typeof (func)=="string"){
return function(_551){
obj[func].apply(obj,[new E(src,_551)]);
};
}else{
return function(_552){
func.apply(obj,[new E(src,_552)]);
};
}
},connect:function(src,sig,_554,_555){
src=MochiKit.DOM.getElement(src);
var self=MochiKit.Signal;
if(typeof (sig)!="string"){
throw new Error("'sig' must be a string");
}
var obj=null;
var func=null;
if(typeof (_555)!="undefined"){
obj=_554;
func=_555;
if(typeof (_555)=="string"){
if(typeof (_554[_555])!="function"){
throw new Error("'funcOrStr' must be a function on 'objOrFunc'");
}
}else{
if(typeof (_555)!="function"){
throw new Error("'funcOrStr' must be a function or string");
}
}
}else{
if(typeof (_554)!="function"){
throw new Error("'objOrFunc' must be a function if 'funcOrStr' is not given");
}else{
func=_554;
}
}
if(typeof (obj)=="undefined"||obj===null){
obj=src;
}
var _556=!!(src.addEventListener||src.attachEvent);
var _557=self._listener(src,func,obj,_556);
if(src.addEventListener){
src.addEventListener(sig.substr(2),_557,false);
}else{
if(src.attachEvent){
src.attachEvent(sig,_557);
}
}
var _558=[src,sig,_557,_556,_554,_555];
self._observers.push(_558);
return _558;
},_disconnect:function(_559){
if(!_559[3]){
return;
}
var src=_559[0];
var sig=_559[1];
var _560=_559[2];
if(src.removeEventListener){
src.removeEventListener(sig.substr(2),_560,false);
}else{
if(src.detachEvent){
src.detachEvent(sig,_560);
}else{
throw new Error("'src' must be a DOM element");
}
}
},disconnect:function(_561){
var self=MochiKit.Signal;
var _562=self._observers;
var m=MochiKit.Base;
if(arguments.length>1){
var src=MochiKit.DOM.getElement(arguments[0]);
var sig=arguments[1];
var obj=arguments[2];
var func=arguments[3];
for(var i=_562.length-1;i>=0;i--){
var o=_562[i];
if(o[0]===src&&o[1]===sig&&o[4]===obj&&o[5]===func){
self._disconnect(o);
_562.splice(i,1);
return true;
}
}
}else{
var idx=m.findIdentical(_562,_561);
if(idx>=0){
self._disconnect(_561);
_562.splice(idx,1);
return true;
}
}
return false;
},disconnectAll:function(src,sig){
src=MochiKit.DOM.getElement(src);
var m=MochiKit.Base;
var _563=m.flattenArguments(m.extend(null,arguments,1));
var self=MochiKit.Signal;
var _564=self._disconnect;
var _565=self._observers;
if(_563.length===0){
for(var i=_565.length-1;i>=0;i--){
var _566=_565[i];
if(_566[0]===src){
_564(_566);
_565.splice(i,1);
}
}
}else{
var sigs={};
for(var i=0;i<_563.length;i++){
sigs[_563[i]]=true;
}
for(var i=_565.length-1;i>=0;i--){
var _566=_565[i];
if(_566[0]===src&&_566[1] in sigs){
_564(_566);
_565.splice(i,1);
}
}
}
},signal:function(src,sig){
var _568=MochiKit.Signal._observers;
src=MochiKit.DOM.getElement(src);
var args=MochiKit.Base.extend(null,arguments,2);
var _569=[];
for(var i=0;i<_568.length;i++){
var _570=_568[i];
if(_570[0]===src&&_570[1]===sig){
try{
_570[2].apply(src,args);
}
catch(e){
_569.push(e);
}
}
}
if(_569.length==1){
throw _569[0];
}else{
if(_569.length>1){
var e=new Error("Multiple errors thrown in handling 'sig', see errors property");
e.errors=_569;
throw e;
}
}
}});
MochiKit.Signal.EXPORT_OK=[];
MochiKit.Signal.EXPORT=["connect","disconnect","signal","disconnectAll"];
MochiKit.Signal.__new__=function(win){
var m=MochiKit.Base;
this._document=document;
this._window=win;
try{
this.connect(window,"onunload",this._unloadCache);
}
catch(e){
}
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
m.nameFunctions(this);
};
MochiKit.Signal.__new__(this);
if(!MochiKit.__compat__){
connect=MochiKit.Signal.connect;
disconnect=MochiKit.Signal.disconnect;
disconnectAll=MochiKit.Signal.disconnectAll;
signal=MochiKit.Signal.signal;
}
MochiKit.Base._exportSymbols(this,MochiKit.Signal);
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.Visual");
dojo.require("MochiKit.Base");
dojo.require("MochiKit.DOM");
dojo.require("MochiKit.Color");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
JSAN.use("MochiKit.DOM",[]);
JSAN.use("MochiKit.Color",[]);
}
try{
if(typeof (MochiKit.Base)=="undefined"||typeof (MochiKit.DOM)=="undefined"||typeof (MochiKit.Color)=="undefined"){
throw "";
}
}
catch(e){
throw "MochiKit.Visual depends on MochiKit.Base, MochiKit.DOM and MochiKit.Color!";
}
if(typeof (MochiKit.Visual)=="undefined"){
MochiKit.Visual={};
}
MochiKit.Visual.NAME="MochiKit.Visual";
MochiKit.Visual.VERSION="1.3.1";
MochiKit.Visual.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.Visual.toString=function(){
return this.__repr__();
};
MochiKit.Visual._RoundCorners=function(e,_571){
e=MochiKit.DOM.getElement(e);
this._setOptions(_571);
if(this.options.__unstable__wrapElement){
e=this._doWrap(e);
}
var _572=this.options.color;
var C=MochiKit.Color.Color;
if(this.options.color=="fromElement"){
_572=C.fromBackground(e);
}else{
if(!(_572 instanceof C)){
_572=C.fromString(_572);
}
}
this.isTransparent=(_572.asRGB().a<=0);
var _574=this.options.bgColor;
if(this.options.bgColor=="fromParent"){
_574=C.fromBackground(e.offsetParent);
}else{
if(!(_574 instanceof C)){
_574=C.fromString(_574);
}
}
this._roundCornersImpl(e,_572,_574);
};
MochiKit.Visual._RoundCorners.prototype={_doWrap:function(e){
var _575=e.parentNode;
var doc=MochiKit.DOM.currentDocument();
if(typeof (doc.defaultView)=="undefined"||doc.defaultView===null){
return e;
}
var _576=doc.defaultView.getComputedStyle(e,null);
if(typeof (_576)=="undefined"||_576===null){
return e;
}
var _577=MochiKit.DOM.DIV({"style":{display:"block",marginTop:_576.getPropertyValue("padding-top"),marginRight:_576.getPropertyValue("padding-right"),marginBottom:_576.getPropertyValue("padding-bottom"),marginLeft:_576.getPropertyValue("padding-left"),padding:"0px"}});
_577.innerHTML=e.innerHTML;
e.innerHTML="";
e.appendChild(_577);
return e;
},_roundCornersImpl:function(e,_578,_579){
if(this.options.border){
this._renderBorder(e,_579);
}
if(this._isTopRounded()){
this._roundTopCorners(e,_578,_579);
}
if(this._isBottomRounded()){
this._roundBottomCorners(e,_578,_579);
}
},_renderBorder:function(el,_580){
var _581="1px solid "+this._borderColor(_580);
var _582="border-left: "+_581;
var _583="border-right: "+_581;
var _584="style='"+_582+";"+_583+"'";
el.innerHTML="<div "+_584+">"+el.innerHTML+"</div>";
},_roundTopCorners:function(el,_585,_586){
var _587=this._createCorner(_586);
for(var i=0;i<this.options.numSlices;i++){
_587.appendChild(this._createCornerSlice(_585,_586,i,"top"));
}
el.style.paddingTop=0;
el.insertBefore(_587,el.firstChild);
},_roundBottomCorners:function(el,_588,_589){
var _590=this._createCorner(_589);
for(var i=(this.options.numSlices-1);i>=0;i--){
_590.appendChild(this._createCornerSlice(_588,_589,i,"bottom"));
}
el.style.paddingBottom=0;
el.appendChild(_590);
},_createCorner:function(_591){
var dom=MochiKit.DOM;
return dom.DIV({style:{backgroundColor:_591.toString()}});
},_createCornerSlice:function(_592,_593,n,_594){
var _595=MochiKit.DOM.SPAN();
var _596=_595.style;
_596.backgroundColor=_592.toString();
_596.display="block";
_596.height="1px";
_596.overflow="hidden";
_596.fontSize="1px";
var _597=this._borderColor(_592,_593);
if(this.options.border&&n===0){
_596.borderTopStyle="solid";
_596.borderTopWidth="1px";
_596.borderLeftWidth="0px";
_596.borderRightWidth="0px";
_596.borderBottomWidth="0px";
_596.height="0px";
_596.borderColor=_597.toString();
}else{
if(_597){
_596.borderColor=_597.toString();
_596.borderStyle="solid";
_596.borderWidth="0px 1px";
}
}
if(!this.options.compact&&(n==(this.options.numSlices-1))){
_596.height="2px";
}
this._setMargin(_595,n,_594);
this._setBorder(_595,n,_594);
return _595;
},_setOptions:function(_598){
this.options={corners:"all",color:"fromElement",bgColor:"fromParent",blend:true,border:false,compact:false,__unstable__wrapElement:false};
MochiKit.Base.update(this.options,_598);
this.options.numSlices=(this.options.compact?2:4);
},_whichSideTop:function(){
var _599=this.options.corners;
if(this._hasString(_599,"all","top")){
return "";
}
var _600=(_599.indexOf("tl")!=-1);
var _601=(_599.indexOf("tr")!=-1);
if(_600&&_601){
return "";
}
if(_600){
return "left";
}
if(_601){
return "right";
}
return "";
},_whichSideBottom:function(){
var _602=this.options.corners;
if(this._hasString(_602,"all","bottom")){
return "";
}
var _603=(_602.indexOf("bl")!=-1);
var _604=(_602.indexOf("br")!=-1);
if(_603&&_604){
return "";
}
if(_603){
return "left";
}
if(_604){
return "right";
}
return "";
},_borderColor:function(_605,_606){
if(_605=="transparent"){
return _606;
}else{
if(this.options.border){
return this.options.border;
}else{
if(this.options.blend){
return _606.blendedColor(_605);
}
}
}
return "";
},_setMargin:function(el,n,_607){
var _608=this._marginSize(n)+"px";
var _609=(_607=="top"?this._whichSideTop():this._whichSideBottom());
var _610=el.style;
if(_609=="left"){
_610.marginLeft=_608;
_610.marginRight="0px";
}else{
if(_609=="right"){
_610.marginRight=_608;
_610.marginLeft="0px";
}else{
_610.marginLeft=_608;
_610.marginRight=_608;
}
}
},_setBorder:function(el,n,_611){
var _612=this._borderSize(n)+"px";
var _613=(_611=="top"?this._whichSideTop():this._whichSideBottom());
var _614=el.style;
if(_613=="left"){
_614.borderLeftWidth=_612;
_614.borderRightWidth="0px";
}else{
if(_613=="right"){
_614.borderRightWidth=_612;
_614.borderLeftWidth="0px";
}else{
_614.borderLeftWidth=_612;
_614.borderRightWidth=_612;
}
}
},_marginSize:function(n){
if(this.isTransparent){
return 0;
}
var o=this.options;
if(o.compact&&o.blend){
var _615=[1,0];
return _615[n];
}else{
if(o.compact){
var _616=[2,1];
return _616[n];
}else{
if(o.blend){
var _617=[3,2,1,0];
return _617[n];
}else{
var _618=[5,3,2,1];
return _618[n];
}
}
}
},_borderSize:function(n){
var o=this.options;
var _619;
if(o.compact&&(o.blend||this.isTransparent)){
return 1;
}else{
if(o.compact){
_619=[1,0];
}else{
if(o.blend){
_619=[2,1,1,1];
}else{
if(o.border){
_619=[0,2,0,0];
}else{
if(this.isTransparent){
_619=[5,3,2,1];
}else{
return 0;
}
}
}
}
}
return _619[n];
},_hasString:function(str){
for(var i=1;i<arguments.length;i++){
if(str.indexOf(arguments[i])!=-1){
return true;
}
}
return false;
},_isTopRounded:function(){
return this._hasString(this.options.corners,"all","top","tl","tr");
},_isBottomRounded:function(){
return this._hasString(this.options.corners,"all","bottom","bl","br");
},_hasSingleTextChild:function(el){
return (el.childNodes.length==1&&el.childNodes[0].nodeType==3);
}};
MochiKit.Visual.roundElement=function(e,_620){
new MochiKit.Visual._RoundCorners(e,_620);
};
MochiKit.Visual.roundClass=function(_621,_622,_623){
var _624=MochiKit.DOM.getElementsByTagAndClassName(_621,_622);
for(var i=0;i<_624.length;i++){
MochiKit.Visual.roundElement(_624[i],_623);
}
};
MochiKit.Visual.Color=MochiKit.Color.Color;
MochiKit.Visual.getElementsComputedStyle=MochiKit.DOM.computedStyle;
MochiKit.Visual.__new__=function(){
var m=MochiKit.Base;
m.nameFunctions(this);
this.EXPORT_TAGS={":common":this.EXPORT,":all":m.concat(this.EXPORT,this.EXPORT_OK)};
};
MochiKit.Visual.EXPORT=["roundElement","roundClass"];
MochiKit.Visual.EXPORT_OK=[];
MochiKit.Visual.__new__();
MochiKit.Base._exportSymbols(this,MochiKit.Visual);
if(typeof (MochiKit)=="undefined"){
MochiKit={};
}
if(typeof (MochiKit.MochiKit)=="undefined"){
MochiKit.MochiKit={};
}
MochiKit.MochiKit.NAME="MochiKit.MochiKit";
MochiKit.MochiKit.VERSION="1.3.1";
MochiKit.MochiKit.__repr__=function(){
return "["+this.NAME+" "+this.VERSION+"]";
};
MochiKit.MochiKit.toString=function(){
return this.__repr__();
};
MochiKit.MochiKit.SUBMODULES=["Base","Iter","Logging","DateTime","Format","Async","DOM","LoggingPane","Color","Signal","Visual"];
if(typeof (JSAN)!="undefined"||typeof (dojo)!="undefined"){
if(typeof (dojo)!="undefined"){
dojo.provide("MochiKit.MochiKit");
dojo.require("MochiKit.*");
}
if(typeof (JSAN)!="undefined"){
JSAN.use("MochiKit.Base",[]);
JSAN.use("MochiKit.Iter",[]);
JSAN.use("MochiKit.Logging",[]);
JSAN.use("MochiKit.DateTime",[]);
JSAN.use("MochiKit.Format",[]);
JSAN.use("MochiKit.Async",[]);
JSAN.use("MochiKit.DOM",[]);
JSAN.use("MochiKit.LoggingPane",[]);
JSAN.use("MochiKit.Color",[]);
JSAN.use("MochiKit.Signal",[]);
JSAN.use("MochiKit.Visual",[]);
}
(function(){
var _625=MochiKit.Base.extend;
var self=MochiKit.MochiKit;
var _626=self.SUBMODULES;
var _627=[];
var _628=[];
var _629={};
var i,k,m,all;
for(i=0;i<_626.length;i++){
m=MochiKit[_626[i]];
_625(_627,m.EXPORT);
_625(_628,m.EXPORT_OK);
for(k in m.EXPORT_TAGS){
_629[k]=_625(_629[k],m.EXPORT_TAGS[k]);
}
all=m.EXPORT_TAGS[":all"];
if(!all){
all=_625(null,m.EXPORT,m.EXPORT_OK);
}
var j;
for(j=0;j<all.length;j++){
k=all[j];
self[k]=m[k];
}
}
self.EXPORT=_627;
self.EXPORT_OK=_628;
self.EXPORT_TAGS=_629;
}());
}else{
if(typeof (MochiKit.__compat__)=="undefined"){
MochiKit.__compat__=true;
}
(function(){
var _630=document.getElementsByTagName("script");
var _631="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul";
var base=null;
var _632=null;
var _633={};
var i;
for(i=0;i<_630.length;i++){
var src=_630[i].getAttribute("src");
if(!src){
continue;
}
_633[src]=true;
if(src.match(/MochiKit.js$/)){
base=src.substring(0,src.lastIndexOf("MochiKit.js"));
_632=_630[i];
}
}
if(base===null){
return;
}
var _634=MochiKit.MochiKit.SUBMODULES;
for(var i=0;i<_634.length;i++){
if(MochiKit[_634[i]]){
continue;
}
var uri=base+_634[i]+".js";
if(uri in _633){
continue;
}
if(document.documentElement&&document.documentElement.namespaceURI==_631){
var s=document.createElementNS(_631,"script");
s.setAttribute("id","MochiKit_"+base+_634[i]);
s.setAttribute("src",uri);
s.setAttribute("type","application/x-javascript");
_632.parentNode.appendChild(s);
}else{
document.write("<script src=\""+uri+"\" type=\"text/javascript\"></script>");
}
}
})();
}


