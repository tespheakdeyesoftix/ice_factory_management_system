
import {getDocument,createDocument,getData,getDocumentList ,postData,getSingleValue } from "@/api-services/api.js";
import {getServerReportDefaultFilter} from "@/helper/utils.js";
 

globalThis.app = globalThis.app || {};


// api url 
globalThis.app.getDoc =  async function (DocType,DocName) {
  return await getDocument(DocType,DocName)
}

globalThis.app.createDoc =  async function (DocType,params) {
  return await createDocument(DocType,params)
}

globalThis.app.updateDoc =  async function (DocType,name,params) {
  return await updateDocument(DocType,name,params)
}

 
globalThis.app.getApi =  async function (api_url,param) {
  return await getData(api_url,param)
}

 
globalThis.app.postApi =  async function (api_url,param) {
  return await postData(api_url,param)
}

globalThis.app.getDocList =  async function (DocType,param) {
  return await getDocumentList(DocType,param)
}
globalThis.app.getSingleValue =  async function (DocType,fields) {
  return await getSingleValue(DocType,fields)
}

globalThis.app.getServerReportDefaultFilter =    function (filter) {
  return getServerReportDefaultFilter(filter);
}

 
globalThis.app.setting = null ;
globalThis.app.user = null ;

 