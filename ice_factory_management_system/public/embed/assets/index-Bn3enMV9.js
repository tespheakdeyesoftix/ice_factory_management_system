import{a5 as x,b as L,B as P,d as E,f as w,a6 as T,a7 as M,j as $,k as A,a0 as f,a8 as m,v as I,c as p,o as h,F as y,p as _,m as v,J as k,n as R,P as G,a as O,r as K}from"./index-DTb4ZBxB.js";function c(t){"@babel/helpers - typeof";return c=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(t)}function U(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function D(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,N(r.key),r)}}function B(t,e,n){return e&&D(t.prototype,e),Object.defineProperty(t,"prototype",{writable:!1}),t}function N(t){var e=j(t,"string");return c(e)=="symbol"?e:e+""}function j(t,e){if(c(t)!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var r=n.call(t,e);if(c(r)!="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(t)}var he=function(){function t(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:function(){};U(this,t),this.element=e,this.listener=n}return B(t,[{key:"bindScrollListener",value:function(){this.scrollableParents=x(this.element);for(var n=0;n<this.scrollableParents.length;n++)this.scrollableParents[n].addEventListener("scroll",this.listener)}},{key:"unbindScrollListener",value:function(){if(this.scrollableParents)for(var n=0;n<this.scrollableParents.length;n++)this.scrollableParents[n].removeEventListener("scroll",this.listener)}},{key:"destroy",value:function(){this.unbindScrollListener(),this.element=null,this.listener=null,this.scrollableParents=null}}])}();function S(t,e){if(t){var n=t.props;if(n){var r=e.replace(/([a-z])([A-Z])/g,"$1-$2").toLowerCase(),s=Object.prototype.hasOwnProperty.call(n,r)?r:e;return t.type.extends.props[e].type===Boolean&&n[s]===""?!0:n[s]}}return null}var C=L`
    .p-splitter {
        display: flex;
        flex-wrap: nowrap;
        border: 1px solid dt('splitter.border.color');
        background: dt('splitter.background');
        border-radius: dt('border.radius.md');
        color: dt('splitter.color');
    }

    .p-splitter-vertical {
        flex-direction: column;
    }

    .p-splitter-gutter {
        flex-grow: 0;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1;
        background: dt('splitter.gutter.background');
    }

    .p-splitter-gutter-handle {
        border-radius: dt('splitter.handle.border.radius');
        background: dt('splitter.handle.background');
        transition:
            outline-color dt('splitter.transition.duration'),
            box-shadow dt('splitter.transition.duration');
        outline-color: transparent;
    }

    .p-splitter-gutter-handle:focus-visible {
        box-shadow: dt('splitter.handle.focus.ring.shadow');
        outline: dt('splitter.handle.focus.ring.width') dt('splitter.handle.focus.ring.style') dt('splitter.handle.focus.ring.color');
        outline-offset: dt('splitter.handle.focus.ring.offset');
    }

    .p-splitter-horizontal.p-splitter-resizing {
        cursor: col-resize;
        user-select: none;
    }

    .p-splitter-vertical.p-splitter-resizing {
        cursor: row-resize;
        user-select: none;
    }

    .p-splitter-horizontal > .p-splitter-gutter > .p-splitter-gutter-handle {
        height: dt('splitter.handle.size');
        width: 100%;
    }

    .p-splitter-vertical > .p-splitter-gutter > .p-splitter-gutter-handle {
        width: dt('splitter.handle.size');
        height: 100%;
    }

    .p-splitter-horizontal > .p-splitter-gutter {
        cursor: col-resize;
    }

    .p-splitter-vertical > .p-splitter-gutter {
        cursor: row-resize;
    }

    .p-splitterpanel {
        flex-grow: 1;
        overflow: hidden;
    }

    .p-splitterpanel-nested {
        display: flex;
    }

    .p-splitterpanel .p-splitter {
        flex-grow: 1;
        border: 0 none;
    }
`,H={root:function(e){var n=e.props;return["p-splitter p-component","p-splitter-"+n.layout]},gutter:"p-splitter-gutter",gutterHandle:"p-splitter-gutter-handle"},F=P.extend({name:"splitter",style:C,classes:H}),X={name:"BaseSplitter",extends:E,props:{layout:{type:String,default:"horizontal"},gutterSize:{type:Number,default:4},stateKey:{type:String,default:null},stateStorage:{type:String,default:"session"},step:{type:Number,default:5}},style:F,provide:function(){return{$pcSplitter:this,$parentInstance:this}}};function d(t){"@babel/helpers - typeof";return d=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},d(t)}function z(t,e,n){return(e=J(e))in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function J(t){var e=V(t,"string");return d(e)=="symbol"?e:e+""}function V(t,e){if(d(t)!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var r=n.call(t,e);if(d(r)!="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(t)}function b(t){return q(t)||Z(t)||Y(t)||W()}function W(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Y(t,e){if(t){if(typeof t=="string")return g(t,e);var n={}.toString.call(t).slice(8,-1);return n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set"?Array.from(t):n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?g(t,e):void 0}}function Z(t){if(typeof Symbol!="undefined"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function q(t){if(Array.isArray(t))return g(t)}function g(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,r=Array(e);n<e;n++)r[n]=t[n];return r}var Q={name:"Splitter",extends:X,inheritAttrs:!1,emits:["resizestart","resizeend","resize"],dragging:!1,mouseMoveListener:null,mouseUpListener:null,touchMoveListener:null,touchEndListener:null,size:null,gutterElement:null,startPos:null,prevPanelElement:null,nextPanelElement:null,nextPanelSize:null,prevPanelSize:null,panelSizes:null,prevPanelIndex:null,timer:null,data:function(){return{prevSize:null}},mounted:function(){this.initializePanels()},beforeUnmount:function(){this.clear(),this.unbindMouseListeners()},methods:{isSplitterPanel:function(e){return e.type.name==="SplitterPanel"},initializePanels:function(){var e=this;if(this.panels&&this.panels.length){var n=!1;if(this.isStateful()&&(n=this.restoreState()),!n){var r=b(this.$el.children).filter(function(i){return i.getAttribute("data-pc-name")==="splitterpanel"}),s=[];this.panels.map(function(i,a){var o=i.props&&I(i.props.size)?i.props.size:null,u=o||100/e.panels.length;s[a]=u,r[a].style.flexBasis="calc("+u+"% - "+(e.panels.length-1)*e.gutterSize+"px)"}),this.panelSizes=s,this.prevSize=parseFloat(s[0]).toFixed(4)}}},onResizeStart:function(e,n,r){this.gutterElement=e.currentTarget||e.target.parentElement,this.size=this.horizontal?$(this.$el):A(this.$el),r||(this.dragging=!0,this.startPos=this.layout==="horizontal"?e.pageX||e.changedTouches[0].pageX:e.pageY||e.changedTouches[0].pageY),this.prevPanelElement=this.gutterElement.previousElementSibling,this.nextPanelElement=this.gutterElement.nextElementSibling,r?(this.prevPanelSize=this.horizontal?f(this.prevPanelElement,!0):m(this.prevPanelElement,!0),this.nextPanelSize=this.horizontal?f(this.nextPanelElement,!0):m(this.nextPanelElement,!0)):(this.prevPanelSize=100*(this.horizontal?f(this.prevPanelElement,!0):m(this.prevPanelElement,!0))/this.size,this.nextPanelSize=100*(this.horizontal?f(this.nextPanelElement,!0):m(this.nextPanelElement,!0))/this.size),this.prevPanelIndex=n,this.$emit("resizestart",{originalEvent:e,sizes:this.panelSizes}),this.$refs.gutter[n].setAttribute("data-p-gutter-resizing",!0),this.$el.setAttribute("data-p-resizing",!0)},onResize:function(e,n,r){var s,i,a;r?this.horizontal?(i=100*(this.prevPanelSize+n)/this.size,a=100*(this.nextPanelSize-n)/this.size):(i=100*(this.prevPanelSize-n)/this.size,a=100*(this.nextPanelSize+n)/this.size):(this.horizontal?M(this.$el)?s=(this.startPos-e.pageX)*100/this.size:s=(e.pageX-this.startPos)*100/this.size:s=(e.pageY-this.startPos)*100/this.size,i=this.prevPanelSize+s,a=this.nextPanelSize-s),this.validateResize(i,a)||(i=Math.min(Math.max(this.prevPanelMinSize,i),100-this.nextPanelMinSize),a=Math.min(Math.max(this.nextPanelMinSize,a),100-this.prevPanelMinSize)),this.prevPanelElement.style.flexBasis="calc("+i+"% - "+(this.panels.length-1)*this.gutterSize+"px)",this.nextPanelElement.style.flexBasis="calc("+a+"% - "+(this.panels.length-1)*this.gutterSize+"px)",this.panelSizes[this.prevPanelIndex]=i,this.panelSizes[this.prevPanelIndex+1]=a,this.prevSize=parseFloat(i).toFixed(4),this.$emit("resize",{originalEvent:e,sizes:this.panelSizes})},onResizeEnd:function(e){this.isStateful()&&this.saveState(),this.$emit("resizeend",{originalEvent:e,sizes:this.panelSizes}),this.$refs.gutter.forEach(function(n){return n.setAttribute("data-p-gutter-resizing",!1)}),this.$el.setAttribute("data-p-resizing",!1),this.clear()},repeat:function(e,n,r){this.onResizeStart(e,n,!0),this.onResize(e,r,!0)},setTimer:function(e,n,r){var s=this;this.timer||(this.timer=setInterval(function(){s.repeat(e,n,r)},40))},clearTimer:function(){this.timer&&(clearInterval(this.timer),this.timer=null)},onGutterKeyUp:function(){this.clearTimer(),this.onResizeEnd()},onGutterKeyDown:function(e,n){switch(e.code){case"ArrowLeft":{this.layout==="horizontal"&&this.setTimer(e,n,this.step*-1),e.preventDefault();break}case"ArrowRight":{this.layout==="horizontal"&&this.setTimer(e,n,this.step),e.preventDefault();break}case"ArrowDown":{this.layout==="vertical"&&this.setTimer(e,n,this.step*-1),e.preventDefault();break}case"ArrowUp":{this.layout==="vertical"&&this.setTimer(e,n,this.step),e.preventDefault();break}}},onGutterMouseDown:function(e,n){this.onResizeStart(e,n),this.bindMouseListeners()},onGutterTouchStart:function(e,n){this.onResizeStart(e,n),this.bindTouchListeners(),e.preventDefault()},onGutterTouchMove:function(e){this.onResize(e),e.preventDefault()},onGutterTouchEnd:function(e){this.onResizeEnd(e),this.unbindTouchListeners(),e.preventDefault()},bindMouseListeners:function(){var e=this;this.mouseMoveListener||(this.mouseMoveListener=function(n){return e.onResize(n)},document.addEventListener("mousemove",this.mouseMoveListener)),this.mouseUpListener||(this.mouseUpListener=function(n){e.onResizeEnd(n),e.unbindMouseListeners()},document.addEventListener("mouseup",this.mouseUpListener))},bindTouchListeners:function(){var e=this;this.touchMoveListener||(this.touchMoveListener=function(n){return e.onResize(n.changedTouches[0])},document.addEventListener("touchmove",this.touchMoveListener)),this.touchEndListener||(this.touchEndListener=function(n){e.resizeEnd(n),e.unbindTouchListeners()},document.addEventListener("touchend",this.touchEndListener))},validateResize:function(e,n){return!(e>100||e<0||n>100||n<0||this.prevPanelMinSize>e||this.nextPanelMinSize>n)},unbindMouseListeners:function(){this.mouseMoveListener&&(document.removeEventListener("mousemove",this.mouseMoveListener),this.mouseMoveListener=null),this.mouseUpListener&&(document.removeEventListener("mouseup",this.mouseUpListener),this.mouseUpListener=null)},unbindTouchListeners:function(){this.touchMoveListener&&(document.removeEventListener("touchmove",this.touchMoveListener),this.touchMoveListener=null),this.touchEndListener&&(document.removeEventListener("touchend",this.touchEndListener),this.touchEndListener=null)},clear:function(){this.dragging=!1,this.size=null,this.startPos=null,this.prevPanelElement=null,this.nextPanelElement=null,this.prevPanelSize=null,this.nextPanelSize=null,this.gutterElement=null,this.prevPanelIndex=null},isStateful:function(){return this.stateKey!=null},getStorage:function(){switch(this.stateStorage){case"local":return window.localStorage;case"session":return window.sessionStorage;default:throw new Error(this.stateStorage+' is not a valid value for the state storage, supported values are "local" and "session".')}},saveState:function(){T(this.panelSizes)&&this.getStorage().setItem(this.stateKey,JSON.stringify(this.panelSizes))},restoreState:function(){var e=this,n=this.getStorage(),r=n.getItem(this.stateKey);if(r){this.panelSizes=JSON.parse(r);var s=b(this.$el.children).filter(function(i){return i.getAttribute("data-pc-name")==="splitterpanel"});return s.forEach(function(i,a){i.style.flexBasis="calc("+e.panelSizes[a]+"% - "+(e.panels.length-1)*e.gutterSize+"px)"}),!0}return!1},resetState:function(){this.initializePanels()}},computed:{panels:function(){var e=this,n=[];return this.$slots.default().forEach(function(r){e.isSplitterPanel(r)?n.push(r):r.children instanceof Array&&r.children.forEach(function(s){e.isSplitterPanel(s)&&n.push(s)})}),n},gutterStyle:function(){return this.horizontal?{width:this.gutterSize+"px"}:{height:this.gutterSize+"px"}},horizontal:function(){return this.layout==="horizontal"},getPTOptions:function(){var e;return{context:{nested:(e=this.$parentInstance)===null||e===void 0?void 0:e.nestedState}}},prevPanelMinSize:function(){var e=S(this.panels[this.prevPanelIndex],"minSize");return this.panels[this.prevPanelIndex].props&&e?e:0},nextPanelMinSize:function(){var e=S(this.panels[this.prevPanelIndex+1],"minSize");return this.panels[this.prevPanelIndex+1].props&&e?e:0},dataP:function(){var e;return w(z(z({},this.layout,this.layout),"nested",((e=this.$parentInstance)===null||e===void 0?void 0:e.nestedState)!=null))}}},ee=["data-p"],te=["onMousedown","onTouchstart","onTouchmove","onTouchend","data-p"],ne=["aria-orientation","aria-valuenow","onKeydown","data-p"];function re(t,e,n,r,s,i){return h(),p("div",v({class:t.cx("root"),"data-p-resizing":!1,"data-p":i.dataP},t.ptmi("root",i.getPTOptions)),[(h(!0),p(y,null,_(i.panels,function(a,o){return h(),p(y,{key:o},[(h(),k(G(a),{tabindex:"-1"})),o!==i.panels.length-1?(h(),p("div",v({key:0,ref_for:!0,ref:"gutter",class:t.cx("gutter"),role:"separator",tabindex:"-1",onMousedown:function(l){return i.onGutterMouseDown(l,o)},onTouchstart:function(l){return i.onGutterTouchStart(l,o)},onTouchmove:function(l){return i.onGutterTouchMove(l,o)},onTouchend:function(l){return i.onGutterTouchEnd(l,o)},"data-p-gutter-resizing":!1,"data-p":i.dataP},t.ptm("gutter")),[O("div",v({class:t.cx("gutterHandle"),tabindex:"0",style:[i.gutterStyle],"aria-orientation":t.layout,"aria-valuenow":s.prevSize,onKeyup:e[0]||(e[0]=function(){return i.onGutterKeyUp&&i.onGutterKeyUp.apply(i,arguments)}),onKeydown:function(l){return i.onGutterKeyDown(l,o)},"data-p":i.dataP,ref_for:!0},t.ptm("gutterHandle")),null,16,ne)],16,te)):R("",!0)],64)}),128))],16,ee)}Q.render=re;var ie={root:function(e){var n=e.instance;return["p-splitterpanel",{"p-splitterpanel-nested":n.isNested}]}},se=P.extend({name:"splitterpanel",classes:ie}),ae={name:"BaseSplitterPanel",extends:E,props:{size:{type:Number,default:null},minSize:{type:Number,default:null}},style:se,provide:function(){return{$pcSplitterPanel:this,$parentInstance:this}}},oe={name:"SplitterPanel",extends:ae,inheritAttrs:!1,data:function(){return{nestedState:null}},computed:{isNested:function(){var e=this;return this.$slots.default().some(function(n){return e.nestedState=n.type.name==="Splitter"?!0:null,e.nestedState})},getPTOptions:function(){return{context:{nested:this.isNested}}}}};function le(t,e,n,r,s,i){return h(),p("div",v({ref:"container",class:t.cx("root")},t.ptmi("root",i.getPTOptions)),[K(t.$slots,"default")],16)}oe.render=le;export{he as C,oe as a,Q as s};
