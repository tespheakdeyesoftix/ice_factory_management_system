import{E as Z,p as U,B as C,b as x,h as A,G as j,H as _,I as W,J as X,K as b,L as z,M as J,c as p,o as l,F as m,t as E,m as c,d as v,f,g as O,a as I,r as y,N as Y,O as q,P as Q,R as ee,Q as te,S as ne,U as ie,i as L,V as P,k as K,W as re,l as se,e as ae,n as oe,x as G,q as R,w as D,u as le,T as ue,C as de}from"./index-DKIu33wS.js";function ce(){let t=[];const e=(s,u,o=999)=>{const d=a(s,u,o),h=d.value+(d.key===s?0:o)+1;return t.push({key:s,value:h}),h},n=s=>{t=t.filter(u=>u.value!==s)},r=(s,u)=>a(s).value,a=(s,u,o=0)=>[...t].reverse().find(d=>!0)||{key:s,value:o},i=s=>s&&parseInt(s.style.zIndex,10)||0;return{get:i,set:(s,u,o)=>{u&&(u.style.zIndex=String(e(s,!0,o)))},clear:s=>{s&&(n(i(s)),s.style.zIndex="")},getCurrent:s=>r(s)}}var w=ce();function g(t){"@babel/helpers - typeof";return g=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},g(t)}function pe(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function he(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,me(r.key),r)}}function fe(t,e,n){return e&&he(t.prototype,e),Object.defineProperty(t,"prototype",{writable:!1}),t}function me(t){var e=be(t,"string");return g(e)=="symbol"?e:e+""}function be(t,e){if(g(t)!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var r=n.call(t,e);if(g(r)!="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(t)}var ve=function(){function t(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:function(){};pe(this,t),this.element=e,this.listener=n}return fe(t,[{key:"bindScrollListener",value:function(){this.scrollableParents=Z(this.element);for(var n=0;n<this.scrollableParents.length;n++)this.scrollableParents[n].addEventListener("scroll",this.listener)}},{key:"unbindScrollListener",value:function(){if(this.scrollableParents)for(var n=0;n<this.scrollableParents.length;n++)this.scrollableParents[n].removeEventListener("scroll",this.listener)}},{key:"destroy",value:function(){this.unbindScrollListener(),this.element=null,this.listener=null,this.scrollableParents=null}}])}();function B(t,e){if(t){var n=t.props;if(n){var r=e.replace(/([a-z])([A-Z])/g,"$1-$2").toLowerCase(),a=Object.prototype.hasOwnProperty.call(n,r)?r:e;return t.type.extends.props[e].type===Boolean&&n[a]===""?!0:n[a]}}return null}var ye=U`
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
`,ge={root:function(e){var n=e.props;return["p-splitter p-component","p-splitter-"+n.layout]},gutter:"p-splitter-gutter",gutterHandle:"p-splitter-gutter-handle"},Se=C.extend({name:"splitter",style:ye,classes:ge}),ze={name:"BaseSplitter",extends:x,props:{layout:{type:String,default:"horizontal"},gutterSize:{type:Number,default:4},stateKey:{type:String,default:null},stateStorage:{type:String,default:"session"},step:{type:Number,default:5}},style:Se,provide:function(){return{$pcSplitter:this,$parentInstance:this}}};function S(t){"@babel/helpers - typeof";return S=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},S(t)}function F(t,e,n){return(e=Le(e))in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function Le(t){var e=Pe(t,"string");return S(e)=="symbol"?e:e+""}function Pe(t,e){if(S(t)!="object"||!t)return t;var n=t[Symbol.toPrimitive];if(n!==void 0){var r=n.call(t,e);if(S(r)!="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(t)}function H(t){return we(t)||ke(t)||xe(t)||Ie()}function Ie(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function xe(t,e){if(t){if(typeof t=="string")return T(t,e);var n={}.toString.call(t).slice(8,-1);return n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set"?Array.from(t):n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?T(t,e):void 0}}function ke(t){if(typeof Symbol!="undefined"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function we(t){if(Array.isArray(t))return T(t)}function T(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,r=Array(e);n<e;n++)r[n]=t[n];return r}var Ee={name:"Splitter",extends:ze,inheritAttrs:!1,emits:["resizestart","resizeend","resize"],dragging:!1,mouseMoveListener:null,mouseUpListener:null,touchMoveListener:null,touchEndListener:null,size:null,gutterElement:null,startPos:null,prevPanelElement:null,nextPanelElement:null,nextPanelSize:null,prevPanelSize:null,panelSizes:null,prevPanelIndex:null,timer:null,data:function(){return{prevSize:null}},mounted:function(){this.initializePanels()},beforeUnmount:function(){this.clear(),this.unbindMouseListeners()},methods:{isSplitterPanel:function(e){return e.type.name==="SplitterPanel"},initializePanels:function(){var e=this;if(this.panels&&this.panels.length){var n=!1;if(this.isStateful()&&(n=this.restoreState()),!n){var r=H(this.$el.children).filter(function(i){return i.getAttribute("data-pc-name")==="splitterpanel"}),a=[];this.panels.map(function(i,s){var u=i.props&&J(i.props.size)?i.props.size:null,o=u||100/e.panels.length;a[s]=o,r[s].style.flexBasis="calc("+o+"% - "+(e.panels.length-1)*e.gutterSize+"px)"}),this.panelSizes=a,this.prevSize=parseFloat(a[0]).toFixed(4)}}},onResizeStart:function(e,n,r){this.gutterElement=e.currentTarget||e.target.parentElement,this.size=this.horizontal?W(this.$el):X(this.$el),r||(this.dragging=!0,this.startPos=this.layout==="horizontal"?e.pageX||e.changedTouches[0].pageX:e.pageY||e.changedTouches[0].pageY),this.prevPanelElement=this.gutterElement.previousElementSibling,this.nextPanelElement=this.gutterElement.nextElementSibling,r?(this.prevPanelSize=this.horizontal?b(this.prevPanelElement,!0):z(this.prevPanelElement,!0),this.nextPanelSize=this.horizontal?b(this.nextPanelElement,!0):z(this.nextPanelElement,!0)):(this.prevPanelSize=100*(this.horizontal?b(this.prevPanelElement,!0):z(this.prevPanelElement,!0))/this.size,this.nextPanelSize=100*(this.horizontal?b(this.nextPanelElement,!0):z(this.nextPanelElement,!0))/this.size),this.prevPanelIndex=n,this.$emit("resizestart",{originalEvent:e,sizes:this.panelSizes}),this.$refs.gutter[n].setAttribute("data-p-gutter-resizing",!0),this.$el.setAttribute("data-p-resizing",!0)},onResize:function(e,n,r){var a,i,s;r?this.horizontal?(i=100*(this.prevPanelSize+n)/this.size,s=100*(this.nextPanelSize-n)/this.size):(i=100*(this.prevPanelSize-n)/this.size,s=100*(this.nextPanelSize+n)/this.size):(this.horizontal?_(this.$el)?a=(this.startPos-e.pageX)*100/this.size:a=(e.pageX-this.startPos)*100/this.size:a=(e.pageY-this.startPos)*100/this.size,i=this.prevPanelSize+a,s=this.nextPanelSize-a),this.validateResize(i,s)||(i=Math.min(Math.max(this.prevPanelMinSize,i),100-this.nextPanelMinSize),s=Math.min(Math.max(this.nextPanelMinSize,s),100-this.prevPanelMinSize)),this.prevPanelElement.style.flexBasis="calc("+i+"% - "+(this.panels.length-1)*this.gutterSize+"px)",this.nextPanelElement.style.flexBasis="calc("+s+"% - "+(this.panels.length-1)*this.gutterSize+"px)",this.panelSizes[this.prevPanelIndex]=i,this.panelSizes[this.prevPanelIndex+1]=s,this.prevSize=parseFloat(i).toFixed(4),this.$emit("resize",{originalEvent:e,sizes:this.panelSizes})},onResizeEnd:function(e){this.isStateful()&&this.saveState(),this.$emit("resizeend",{originalEvent:e,sizes:this.panelSizes}),this.$refs.gutter.forEach(function(n){return n.setAttribute("data-p-gutter-resizing",!1)}),this.$el.setAttribute("data-p-resizing",!1),this.clear()},repeat:function(e,n,r){this.onResizeStart(e,n,!0),this.onResize(e,r,!0)},setTimer:function(e,n,r){var a=this;this.timer||(this.timer=setInterval(function(){a.repeat(e,n,r)},40))},clearTimer:function(){this.timer&&(clearInterval(this.timer),this.timer=null)},onGutterKeyUp:function(){this.clearTimer(),this.onResizeEnd()},onGutterKeyDown:function(e,n){switch(e.code){case"ArrowLeft":{this.layout==="horizontal"&&this.setTimer(e,n,this.step*-1),e.preventDefault();break}case"ArrowRight":{this.layout==="horizontal"&&this.setTimer(e,n,this.step),e.preventDefault();break}case"ArrowDown":{this.layout==="vertical"&&this.setTimer(e,n,this.step*-1),e.preventDefault();break}case"ArrowUp":{this.layout==="vertical"&&this.setTimer(e,n,this.step),e.preventDefault();break}}},onGutterMouseDown:function(e,n){this.onResizeStart(e,n),this.bindMouseListeners()},onGutterTouchStart:function(e,n){this.onResizeStart(e,n),this.bindTouchListeners(),e.preventDefault()},onGutterTouchMove:function(e){this.onResize(e),e.preventDefault()},onGutterTouchEnd:function(e){this.onResizeEnd(e),this.unbindTouchListeners(),e.preventDefault()},bindMouseListeners:function(){var e=this;this.mouseMoveListener||(this.mouseMoveListener=function(n){return e.onResize(n)},document.addEventListener("mousemove",this.mouseMoveListener)),this.mouseUpListener||(this.mouseUpListener=function(n){e.onResizeEnd(n),e.unbindMouseListeners()},document.addEventListener("mouseup",this.mouseUpListener))},bindTouchListeners:function(){var e=this;this.touchMoveListener||(this.touchMoveListener=function(n){return e.onResize(n.changedTouches[0])},document.addEventListener("touchmove",this.touchMoveListener)),this.touchEndListener||(this.touchEndListener=function(n){e.resizeEnd(n),e.unbindTouchListeners()},document.addEventListener("touchend",this.touchEndListener))},validateResize:function(e,n){return!(e>100||e<0||n>100||n<0||this.prevPanelMinSize>e||this.nextPanelMinSize>n)},unbindMouseListeners:function(){this.mouseMoveListener&&(document.removeEventListener("mousemove",this.mouseMoveListener),this.mouseMoveListener=null),this.mouseUpListener&&(document.removeEventListener("mouseup",this.mouseUpListener),this.mouseUpListener=null)},unbindTouchListeners:function(){this.touchMoveListener&&(document.removeEventListener("touchmove",this.touchMoveListener),this.touchMoveListener=null),this.touchEndListener&&(document.removeEventListener("touchend",this.touchEndListener),this.touchEndListener=null)},clear:function(){this.dragging=!1,this.size=null,this.startPos=null,this.prevPanelElement=null,this.nextPanelElement=null,this.prevPanelSize=null,this.nextPanelSize=null,this.gutterElement=null,this.prevPanelIndex=null},isStateful:function(){return this.stateKey!=null},getStorage:function(){switch(this.stateStorage){case"local":return window.localStorage;case"session":return window.sessionStorage;default:throw new Error(this.stateStorage+' is not a valid value for the state storage, supported values are "local" and "session".')}},saveState:function(){j(this.panelSizes)&&this.getStorage().setItem(this.stateKey,JSON.stringify(this.panelSizes))},restoreState:function(){var e=this,n=this.getStorage(),r=n.getItem(this.stateKey);if(r){this.panelSizes=JSON.parse(r);var a=H(this.$el.children).filter(function(i){return i.getAttribute("data-pc-name")==="splitterpanel"});return a.forEach(function(i,s){i.style.flexBasis="calc("+e.panelSizes[s]+"% - "+(e.panels.length-1)*e.gutterSize+"px)"}),!0}return!1},resetState:function(){this.initializePanels()}},computed:{panels:function(){var e=this,n=[];return this.$slots.default().forEach(function(r){e.isSplitterPanel(r)?n.push(r):r.children instanceof Array&&r.children.forEach(function(a){e.isSplitterPanel(a)&&n.push(a)})}),n},gutterStyle:function(){return this.horizontal?{width:this.gutterSize+"px"}:{height:this.gutterSize+"px"}},horizontal:function(){return this.layout==="horizontal"},getPTOptions:function(){var e;return{context:{nested:(e=this.$parentInstance)===null||e===void 0?void 0:e.nestedState}}},prevPanelMinSize:function(){var e=B(this.panels[this.prevPanelIndex],"minSize");return this.panels[this.prevPanelIndex].props&&e?e:0},nextPanelMinSize:function(){var e=B(this.panels[this.prevPanelIndex+1],"minSize");return this.panels[this.prevPanelIndex+1].props&&e?e:0},dataP:function(){var e;return A(F(F({},this.layout,this.layout),"nested",((e=this.$parentInstance)===null||e===void 0?void 0:e.nestedState)!=null))}}},Oe=["data-p"],Te=["onMousedown","onTouchstart","onTouchmove","onTouchend","data-p"],Me=["aria-orientation","aria-valuenow","onKeydown","data-p"];function Ce(t,e,n,r,a,i){return l(),p("div",c({class:t.cx("root"),"data-p-resizing":!1,"data-p":i.dataP},t.ptmi("root",i.getPTOptions)),[(l(!0),p(m,null,E(i.panels,function(s,u){return l(),p(m,{key:u},[(l(),v(O(s),{tabindex:"-1"})),u!==i.panels.length-1?(l(),p("div",c({key:0,ref_for:!0,ref:"gutter",class:t.cx("gutter"),role:"separator",tabindex:"-1",onMousedown:function(d){return i.onGutterMouseDown(d,u)},onTouchstart:function(d){return i.onGutterTouchStart(d,u)},onTouchmove:function(d){return i.onGutterTouchMove(d,u)},onTouchend:function(d){return i.onGutterTouchEnd(d,u)},"data-p-gutter-resizing":!1,"data-p":i.dataP},t.ptm("gutter")),[I("div",c({class:t.cx("gutterHandle"),tabindex:"0",style:[i.gutterStyle],"aria-orientation":t.layout,"aria-valuenow":a.prevSize,onKeyup:e[0]||(e[0]=function(){return i.onGutterKeyUp&&i.onGutterKeyUp.apply(i,arguments)}),onKeydown:function(d){return i.onGutterKeyDown(d,u)},"data-p":i.dataP,ref_for:!0},t.ptm("gutterHandle")),null,16,Me)],16,Te)):f("",!0)],64)}),128))],16,Oe)}Ee.render=Ce;var Ae={root:function(e){var n=e.instance;return["p-splitterpanel",{"p-splitterpanel-nested":n.isNested}]}},Ke=C.extend({name:"splitterpanel",classes:Ae}),Re={name:"BaseSplitterPanel",extends:x,props:{size:{type:Number,default:null},minSize:{type:Number,default:null}},style:Ke,provide:function(){return{$pcSplitterPanel:this,$parentInstance:this}}},De={name:"SplitterPanel",extends:Re,inheritAttrs:!1,data:function(){return{nestedState:null}},computed:{isNested:function(){var e=this;return this.$slots.default().some(function(n){return e.nestedState=n.type.name==="Splitter"?!0:null,e.nestedState})},getPTOptions:function(){return{context:{nested:this.isNested}}}}};function Be(t,e,n,r,a,i){return l(),p("div",c({ref:"container",class:t.cx("root")},t.ptmi("root",i.getPTOptions)),[y(t.$slots,"default")],16)}De.render=Be;var Fe=Y(),$={name:"Portal",props:{appendTo:{type:[String,Object],default:"body"},disabled:{type:Boolean,default:!1}},data:function(){return{mounted:!1}},mounted:function(){this.mounted=q()},computed:{inline:function(){return this.disabled||this.appendTo==="self"}}};function He(t,e,n,r,a,i){return i.inline?y(t.$slots,"default",{key:0}):a.mounted?(l(),v(Q,{key:1,to:n.appendTo},[y(t.$slots,"default")],8,["to"])):f("",!0)}$.render=He;var Ne=U`
    .p-menu {
        background: dt('menu.background');
        color: dt('menu.color');
        border: 1px solid dt('menu.border.color');
        border-radius: dt('menu.border.radius');
        min-width: 12.5rem;
    }

    .p-menu-list {
        margin: 0;
        padding: dt('menu.list.padding');
        outline: 0 none;
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: dt('menu.list.gap');
    }

    .p-menu-item-content {
        transition:
            background dt('menu.transition.duration'),
            color dt('menu.transition.duration');
        border-radius: dt('menu.item.border.radius');
        color: dt('menu.item.color');
    }

    .p-menu-item-link {
        cursor: pointer;
        display: flex;
        align-items: center;
        text-decoration: none;
        overflow: hidden;
        position: relative;
        color: inherit;
        padding: dt('menu.item.padding');
        gap: dt('menu.item.gap');
        user-select: none;
        outline: 0 none;
    }

    .p-menu-item-label {
        line-height: 1;
    }

    .p-menu-item-icon {
        color: dt('menu.item.icon.color');
    }

    .p-menu-item.p-focus .p-menu-item-content {
        color: dt('menu.item.focus.color');
        background: dt('menu.item.focus.background');
    }

    .p-menu-item.p-focus .p-menu-item-icon {
        color: dt('menu.item.icon.focus.color');
    }

    .p-menu-item:not(.p-disabled) .p-menu-item-content:hover {
        color: dt('menu.item.focus.color');
        background: dt('menu.item.focus.background');
    }

    .p-menu-item:not(.p-disabled) .p-menu-item-content:hover .p-menu-item-icon {
        color: dt('menu.item.icon.focus.color');
    }

    .p-menu-overlay {
        box-shadow: dt('menu.shadow');
    }

    .p-menu-submenu-label {
        background: dt('menu.submenu.label.background');
        padding: dt('menu.submenu.label.padding');
        color: dt('menu.submenu.label.color');
        font-weight: dt('menu.submenu.label.font.weight');
    }

    .p-menu-separator {
        border-block-start: 1px solid dt('menu.separator.border.color');
    }
`,Ue={root:function(e){var n=e.props;return["p-menu p-component",{"p-menu-overlay":n.popup}]},start:"p-menu-start",list:"p-menu-list",submenuLabel:"p-menu-submenu-label",separator:"p-menu-separator",end:"p-menu-end",item:function(e){var n=e.instance;return["p-menu-item",{"p-focus":n.id===n.focusedOptionId,"p-disabled":n.disabled()}]},itemContent:"p-menu-item-content",itemLink:"p-menu-item-link",itemIcon:"p-menu-item-icon",itemLabel:"p-menu-item-label"},Ge=C.extend({name:"menu",style:Ne,classes:Ue}),$e={name:"BaseMenu",extends:x,props:{popup:{type:Boolean,default:!1},model:{type:Array,default:null},appendTo:{type:[String,Object],default:"body"},autoZIndex:{type:Boolean,default:!0},baseZIndex:{type:Number,default:0},tabindex:{type:Number,default:0},ariaLabel:{type:String,default:null},ariaLabelledby:{type:String,default:null}},style:Ge,provide:function(){return{$pcMenu:this,$parentInstance:this}}},V={name:"Menuitem",hostName:"Menu",extends:x,inheritAttrs:!1,emits:["item-click","item-mousemove"],props:{item:null,templates:null,id:null,focusedOptionId:null,index:null},methods:{getItemProp:function(e,n){return e&&e.item?re(e.item[n]):void 0},getPTOptions:function(e){return this.ptm(e,{context:{item:this.item,index:this.index,focused:this.isItemFocused(),disabled:this.disabled()}})},isItemFocused:function(){return this.focusedOptionId===this.id},onItemClick:function(e){var n=this.getItemProp(this.item,"command");n&&n({originalEvent:e,item:this.item.item}),this.$emit("item-click",{originalEvent:e,item:this.item,id:this.id})},onItemMouseMove:function(e){this.$emit("item-mousemove",{originalEvent:e,item:this.item,id:this.id})},visible:function(){return typeof this.item.visible=="function"?this.item.visible():this.item.visible!==!1},disabled:function(){return typeof this.item.disabled=="function"?this.item.disabled():this.item.disabled},label:function(){return typeof this.item.label=="function"?this.item.label():this.item.label},getMenuItemProps:function(e){return{action:c({class:this.cx("itemLink"),tabindex:"-1"},this.getPTOptions("itemLink")),icon:c({class:[this.cx("itemIcon"),e.icon]},this.getPTOptions("itemIcon")),label:c({class:this.cx("itemLabel")},this.getPTOptions("itemLabel"))}}},computed:{dataP:function(){return A({focus:this.isItemFocused(),disabled:this.disabled()})}},directives:{ripple:ee}},Ve=["id","aria-label","aria-disabled","data-p-focused","data-p-disabled","data-p"],Ze=["data-p"],je=["href","target"],_e=["data-p"],We=["data-p"];function Xe(t,e,n,r,a,i){var s=se("ripple");return i.visible()?(l(),p("li",c({key:0,id:n.id,class:[t.cx("item"),n.item.class],role:"menuitem",style:n.item.style,"aria-label":i.label(),"aria-disabled":i.disabled(),"data-p-focused":i.isItemFocused(),"data-p-disabled":i.disabled()||!1,"data-p":i.dataP},i.getPTOptions("item")),[I("div",c({class:t.cx("itemContent"),onClick:e[0]||(e[0]=function(u){return i.onItemClick(u)}),onMousemove:e[1]||(e[1]=function(u){return i.onItemMouseMove(u)}),"data-p":i.dataP},i.getPTOptions("itemContent")),[n.templates.item?n.templates.item?(l(),v(O(n.templates.item),{key:1,item:n.item,label:i.label(),props:i.getMenuItemProps(n.item)},null,8,["item","label","props"])):f("",!0):ae((l(),p("a",c({key:0,href:n.item.url,class:t.cx("itemLink"),target:n.item.target,tabindex:"-1"},i.getPTOptions("itemLink")),[n.templates.itemicon?(l(),v(O(n.templates.itemicon),{key:0,item:n.item,class:oe(t.cx("itemIcon"))},null,8,["item","class"])):n.item.icon?(l(),p("span",c({key:1,class:[t.cx("itemIcon"),n.item.icon],"data-p":i.dataP},i.getPTOptions("itemIcon")),null,16,_e)):f("",!0),I("span",c({class:t.cx("itemLabel"),"data-p":i.dataP},i.getPTOptions("itemLabel")),G(i.label()),17,We)],16,je)),[[s]])],16,Ze)],16,Ve)):f("",!0)}V.render=Xe;function N(t){return Qe(t)||qe(t)||Ye(t)||Je()}function Je(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Ye(t,e){if(t){if(typeof t=="string")return M(t,e);var n={}.toString.call(t).slice(8,-1);return n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set"?Array.from(t):n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?M(t,e):void 0}}function qe(t){if(typeof Symbol!="undefined"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function Qe(t){if(Array.isArray(t))return M(t)}function M(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,r=Array(e);n<e;n++)r[n]=t[n];return r}var et={name:"Menu",extends:$e,inheritAttrs:!1,emits:["show","hide","focus","blur"],data:function(){return{overlayVisible:!1,focused:!1,focusedOptionIndex:-1,selectedOptionIndex:-1}},target:null,outsideClickListener:null,scrollHandler:null,resizeListener:null,container:null,list:null,mounted:function(){this.popup||(this.bindResizeListener(),this.bindOutsideClickListener())},beforeUnmount:function(){this.unbindResizeListener(),this.unbindOutsideClickListener(),this.scrollHandler&&(this.scrollHandler.destroy(),this.scrollHandler=null),this.target=null,this.container&&this.autoZIndex&&w.clear(this.container),this.container=null},methods:{itemClick:function(e){var n=e.item;this.disabled(n)||(n.command&&n.command(e),this.overlayVisible&&this.hide(),!this.popup&&this.focusedOptionIndex!==e.id&&(this.focusedOptionIndex=e.id))},itemMouseMove:function(e){this.focused&&(this.focusedOptionIndex=e.id)},onListFocus:function(e){this.focused=!0,!this.popup&&this.changeFocusedOptionIndex(0),this.$emit("focus",e)},onListBlur:function(e){this.focused=!1,this.focusedOptionIndex=-1,this.$emit("blur",e)},onListKeyDown:function(e){switch(e.code){case"ArrowDown":this.onArrowDownKey(e);break;case"ArrowUp":this.onArrowUpKey(e);break;case"Home":this.onHomeKey(e);break;case"End":this.onEndKey(e);break;case"Enter":case"NumpadEnter":this.onEnterKey(e);break;case"Space":this.onSpaceKey(e);break;case"Escape":this.popup&&(L(this.target),this.hide());case"Tab":this.overlayVisible&&this.hide();break}},onArrowDownKey:function(e){var n=this.findNextOptionIndex(this.focusedOptionIndex);this.changeFocusedOptionIndex(n),e.preventDefault()},onArrowUpKey:function(e){if(e.altKey&&this.popup)L(this.target),this.hide(),e.preventDefault();else{var n=this.findPrevOptionIndex(this.focusedOptionIndex);this.changeFocusedOptionIndex(n),e.preventDefault()}},onHomeKey:function(e){this.changeFocusedOptionIndex(0),e.preventDefault()},onEndKey:function(e){this.changeFocusedOptionIndex(P(this.container,'li[data-pc-section="item"][data-p-disabled="false"]').length-1),e.preventDefault()},onEnterKey:function(e){var n=K(this.list,'li[id="'.concat("".concat(this.focusedOptionIndex),'"]')),r=n&&K(n,'a[data-pc-section="itemlink"]');this.popup&&L(this.target),r?r.click():n&&n.click(),e.preventDefault()},onSpaceKey:function(e){this.onEnterKey(e)},findNextOptionIndex:function(e){var n=P(this.container,'li[data-pc-section="item"][data-p-disabled="false"]'),r=N(n).findIndex(function(a){return a.id===e});return r>-1?r+1:0},findPrevOptionIndex:function(e){var n=P(this.container,'li[data-pc-section="item"][data-p-disabled="false"]'),r=N(n).findIndex(function(a){return a.id===e});return r>-1?r-1:0},changeFocusedOptionIndex:function(e){var n=P(this.container,'li[data-pc-section="item"][data-p-disabled="false"]'),r=e>=n.length?n.length-1:e<0?0:e;r>-1&&(this.focusedOptionIndex=n[r].getAttribute("id"))},toggle:function(e,n){this.overlayVisible?this.hide():this.show(e,n)},show:function(e,n){this.overlayVisible=!0,this.target=n!=null?n:e.currentTarget},hide:function(){this.overlayVisible=!1,this.target=null},onEnter:function(e){ie(e,{position:"absolute",top:"0"}),this.alignOverlay(),this.bindOutsideClickListener(),this.bindResizeListener(),this.bindScrollListener(),this.autoZIndex&&w.set("menu",e,this.baseZIndex+this.$primevue.config.zIndex.menu),this.popup&&L(this.list),this.$emit("show")},onLeave:function(){this.unbindOutsideClickListener(),this.unbindResizeListener(),this.unbindScrollListener(),this.$emit("hide")},onAfterLeave:function(e){this.autoZIndex&&w.clear(e)},alignOverlay:function(){ne(this.container,this.target);var e=b(this.target);e>b(this.container)&&(this.container.style.minWidth=b(this.target)+"px")},bindOutsideClickListener:function(){var e=this;this.outsideClickListener||(this.outsideClickListener=function(n){var r=e.container&&!e.container.contains(n.target),a=!(e.target&&(e.target===n.target||e.target.contains(n.target)));e.overlayVisible&&r&&a?e.hide():!e.popup&&r&&a&&(e.focusedOptionIndex=-1)},document.addEventListener("click",this.outsideClickListener,!0))},unbindOutsideClickListener:function(){this.outsideClickListener&&(document.removeEventListener("click",this.outsideClickListener,!0),this.outsideClickListener=null)},bindScrollListener:function(){var e=this;this.scrollHandler||(this.scrollHandler=new ve(this.target,function(){e.overlayVisible&&e.hide()})),this.scrollHandler.bindScrollListener()},unbindScrollListener:function(){this.scrollHandler&&this.scrollHandler.unbindScrollListener()},bindResizeListener:function(){var e=this;this.resizeListener||(this.resizeListener=function(){e.overlayVisible&&!te()&&e.hide()},window.addEventListener("resize",this.resizeListener))},unbindResizeListener:function(){this.resizeListener&&(window.removeEventListener("resize",this.resizeListener),this.resizeListener=null)},visible:function(e){return typeof e.visible=="function"?e.visible():e.visible!==!1},disabled:function(e){return typeof e.disabled=="function"?e.disabled():e.disabled},label:function(e){return typeof e.label=="function"?e.label():e.label},onOverlayClick:function(e){Fe.emit("overlay-click",{originalEvent:e,target:this.target})},containerRef:function(e){this.container=e},listRef:function(e){this.list=e}},computed:{focusedOptionId:function(){return this.focusedOptionIndex!==-1?this.focusedOptionIndex:null},dataP:function(){return A({popup:this.popup})}},components:{PVMenuitem:V,Portal:$}},tt=["id","data-p"],nt=["id","tabindex","aria-activedescendant","aria-label","aria-labelledby"],it=["id"];function rt(t,e,n,r,a,i){var s=R("PVMenuitem"),u=R("Portal");return l(),v(u,{appendTo:t.appendTo,disabled:!t.popup},{default:D(function(){return[le(ue,c({name:"p-connected-overlay",onEnter:i.onEnter,onLeave:i.onLeave,onAfterLeave:i.onAfterLeave},t.ptm("transition")),{default:D(function(){return[!t.popup||a.overlayVisible?(l(),p("div",c({key:0,ref:i.containerRef,id:t.$id,class:t.cx("root"),onClick:e[3]||(e[3]=function(){return i.onOverlayClick&&i.onOverlayClick.apply(i,arguments)}),"data-p":i.dataP},t.ptmi("root")),[t.$slots.start?(l(),p("div",c({key:0,class:t.cx("start")},t.ptm("start")),[y(t.$slots,"start")],16)):f("",!0),I("ul",c({ref:i.listRef,id:t.$id+"_list",class:t.cx("list"),role:"menu",tabindex:t.tabindex,"aria-activedescendant":a.focused?i.focusedOptionId:void 0,"aria-label":t.ariaLabel,"aria-labelledby":t.ariaLabelledby,onFocus:e[0]||(e[0]=function(){return i.onListFocus&&i.onListFocus.apply(i,arguments)}),onBlur:e[1]||(e[1]=function(){return i.onListBlur&&i.onListBlur.apply(i,arguments)}),onKeydown:e[2]||(e[2]=function(){return i.onListKeyDown&&i.onListKeyDown.apply(i,arguments)})},t.ptm("list")),[(l(!0),p(m,null,E(t.model,function(o,d){return l(),p(m,{key:i.label(o)+d.toString()},[o.items&&i.visible(o)&&!o.separator?(l(),p(m,{key:0},[o.items?(l(),p("li",c({key:0,id:t.$id+"_"+d,class:[t.cx("submenuLabel"),o.class],role:"none",ref_for:!0},t.ptm("submenuLabel")),[y(t.$slots,t.$slots.submenulabel?"submenulabel":"submenuheader",{item:o},function(){return[de(G(i.label(o)),1)]})],16,it)):f("",!0),(l(!0),p(m,null,E(o.items,function(h,k){return l(),p(m,{key:h.label+d+"_"+k},[i.visible(h)&&!h.separator?(l(),v(s,{key:0,id:t.$id+"_"+d+"_"+k,item:h,templates:t.$slots,focusedOptionId:i.focusedOptionId,unstyled:t.unstyled,onItemClick:i.itemClick,onItemMousemove:i.itemMouseMove,pt:t.pt},null,8,["id","item","templates","focusedOptionId","unstyled","onItemClick","onItemMousemove","pt"])):i.visible(h)&&h.separator?(l(),p("li",c({key:"separator"+d+k,class:[t.cx("separator"),o.class],style:h.style,role:"separator",ref_for:!0},t.ptm("separator")),null,16)):f("",!0)],64)}),128))],64)):i.visible(o)&&o.separator?(l(),p("li",c({key:"separator"+d.toString(),class:[t.cx("separator"),o.class],style:o.style,role:"separator",ref_for:!0},t.ptm("separator")),null,16)):(l(),v(s,{key:i.label(o)+d.toString(),id:t.$id+"_"+d,item:o,index:d,templates:t.$slots,focusedOptionId:i.focusedOptionId,unstyled:t.unstyled,onItemClick:i.itemClick,onItemMousemove:i.itemMouseMove,pt:t.pt},null,8,["id","item","index","templates","focusedOptionId","unstyled","onItemClick","onItemMousemove","pt"]))],64)}),128))],16,nt),t.$slots.end?(l(),p("div",c({key:1,class:t.cx("end")},t.ptm("end")),[y(t.$slots,"end")],16)):f("",!0)],16,tt)):f("",!0)]}),_:3},16,["onEnter","onLeave","onAfterLeave"])]}),_:3},8,["appendTo","disabled"])}et.render=rt;export{Ee as a,De as b,et as s};
