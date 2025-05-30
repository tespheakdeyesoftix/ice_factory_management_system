
import {handleServerMessage} from '@/helper/handle-server-message.js'
import { FrappeApp } from 'frappe-js-sdk';
const frappe = new FrappeApp()
const db = frappe.db()
const call = frappe.call()

export function getDoc(doctype, name){
 
    return  new Promise((resolve, reject)=>{
        db.getDoc(doctype, name)
        .then((doc) => { 
            resolve(doc)
        })
        .catch((error) => {
            const message = handleServerMessage(error)
            reject(message)
        });
    })
}


export function getDocument(doctype, name,show_message=true){
 
    return db.getDoc(doctype, name)
  .then((doc) =>({ data: doc, error: null }))
  .catch((error) => {
    if(show_message){
        handleServerMessage(error)
    }
    
    return { data: null, error }
  });

}

export function getDocList(doctype, option){
 
    return new Promise((resolve, reject)=>{
        db.getDocList(doctype, option)
        .then((doc) => {
            resolve(doc)
        })
        .catch((error) => {
            const message = handleServerMessage(error)
            reject(error)
           
        });
    })
}

export function getDocumentList(doctype, option){
 
    return db.getDocList(doctype, option)
    .then((r) => ({ data: r, error: null }))
    .catch((error) => {
        handleServerMessage(error)
        return { data: null, error }
    });
}
 
export function getSingleValue(doctype, fields){
  
    return db.getSingleValue(doctype, fields)
    .then((r) => ({ data: r, error: null }))
    .catch((error) => {
        handleServerMessage(error)
        return { data: null, error }
    });
}
 
export function getCount(doctype, filters){
 
    return new Promise((resolve, reject)=>{
        db.getCount(doctype, filters,false,false)
        .then((doc) => {
            resolve(doc)
        })
        .catch((error) => {
            reject(error)
            window.postMessage('show_error|' + 'Server Error', '*')
        });
    })
}


export function getDoctypeCount(doctype, filters,orFilters) {
        

        return call.post("edoor.api.utils.get_doctype_count",{doctype_name:doctype,filters:filters,or_filters:orFilters})
        .then((r) => {
            return { data: r.message, error: null };
})
        .catch((error) => {
        return { data: null, error }
    });
}



export function updateDoc(doctype, name, data, message="",show_message=true){
 
    return new Promise((resolve, reject)=>{
        db.updateDoc(doctype, name, data)
        .then((doc) => {
            resolve(doc)
            if(show_message){
            window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
            }
        })
        .catch((error) => {
            
            const message = handleServerMessage(error)
            reject(error) 
        });
    })
}



export function updateData(param){
    //doctype:"", name:"", data:{}, message:"",show_message=true
    return db.updateDoc(param.doctype, param.name, param.data,param.ignores)
        .then((doc) => {
           
            if(!param.hide_message){
            window.postMessage('show_success|' + `${param.message ? param.message : 'Update successful'}`, '*')
            }
            return  { data: doc, error: null }
        })
        .catch((error) => {
            handleServerMessage(error)
            return { data: null, error }
        });
    
}

export function updateDocument(param){
    //doctype:"", name:"", data:{}, message:"",show_message=true
    return db.updateDoc(param.doctype, param.name, param.data,param.ignores)
        .then((doc) => {
           
            if(!param.hide_message){
            window.postMessage('show_success|' + `${param.message ? param.message : 'Update successful'}`, '*')
            }
            return  { data: doc, error: null }
        })
        .catch((error) => {
            handleServerMessage(error)
            return { data: null, error }
        });
    
}


export function createUpdateDoc(doctype, data, message, rename=null,show_error_message=true){ 
 
 
    return new Promise((resolve, reject)=>{
        if(data.name){
      
            db.updateDoc(doctype, data.name, data)
            .then((doc) => {
               
                // rename
                if(rename && (rename.old_name != rename.new_name)){
                    var update_name = {
                        doctype: doctype,
                        old_name: rename.old_name,
                        new_name: rename.new_name
                    }
                    postApi('utils.rename_doc', { data: update_name },'', false).then((r)=>{
                        doc.name = rename.new_name
                        resolve(doc)
                        window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
                    }).catch((err)=>{
                        reject(err)
                    })
                }
                else{
                    resolve(doc) 
                    window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
                }
            })
            .catch((error) => {
              
                if(show_error_message){
                    handleServerMessage(error)
                } 
                reject(error) 
            });
        }
        else{ 
            db.createDoc(doctype, data)
            .then((doc) => {
                resolve(doc)
                window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
                
            })
            .catch((error) => {
                const message = handleServerMessage(error)
                reject(error) 
            });
        }
    })
}

export function deleteDoc(doctype, name, message){

    return new Promise((resolve, reject)=>{
        db.deleteDoc(doctype, name)
        .then((doc) => {
           
            resolve(doc.message)
            window.postMessage('show_success|' + `${message ? message : 'Deleted successful'}`, '*')
        })
        .catch((error) => {
     
            const message = handleServerMessage(error)
            reject(message) 
        });
    })
}


export function deleteDocument(doctype, name, option={show_error_message:true,show_message:true}){

    return  db.deleteDoc(doctype, name)
        .then((doc) => {
            if(!option.show_message){
                window.postMessage('show_success|' + `${message ? message : 'Deleted successful'}`, '*')
            }
            
            return {data:true, error:null}

        })
        .catch((error) => {
            
            if(option?.show_error_message){
                const message = handleServerMessage(error)
            }
           
            return {data:null, error:error}
            
        });
    
}
export function getApi(api, params = Object,base_url="ice_factory_management_system.api."){


    return new Promise((resolve, reject)=>{
        call.get(`${base_url}${api}`, params).then((result) => {
            resolve(result)
        }).catch((error) =>{
          
            handleServerMessage(error)
            reject(error)
        })
    })
}

// new api constract data and error to avoid callback hell like .then().then ....

export function getData(api_url, params=null,base_url="ice_factory_management_system.api.") {
      return call.get(`${base_url}${api_url}`, params)
      .then((r) => {
        if(r.message){
            return { data: r.message, error: null }
        }else {
            return { data: r, error: null }
        }
      })
      .catch((error) => {
        handleServerMessage(error)
        return { data: null, error }
    });
}

export function postApi(api, params = Object, message,show_message=true,base_url="edoor.api."){
    return new Promise((resolve, reject)=>{
        call.post(`${base_url}${api}`, params).then((result) => {
            if(show_message == true){
                if(show_message && !result.hasOwnProperty("_server_messages")){
                    window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
                }else{
                    if(result.hasOwnProperty("_server_messages")){
                        const _server_messages = JSON.parse(result._server_messages)
                        _server_messages.forEach(r => {
                            window.postMessage('show_success|' + JSON.parse(r).message, '*')
                        });
                    }
                   
                }
            }
            resolve(result)
        }).catch((error) =>{
            handleServerMessage(error)
            reject(error)
        })
    })
}

 

export function postData(api, params = Object, message="",show_message=true,base_url="edoor.api."){
      return call.post(`${base_url}${api}`, params)
      .then((result) => {
        if(show_message == true){
            if(show_message && !result.hasOwnProperty("_server_messages")){
                window.postMessage('show_success|' + `${message ? message : 'Update successful'}`, '*')
            }else{
                if(result.hasOwnProperty("_server_messages")){
                    const _server_messages = JSON.parse(result._server_messages)
                    _server_messages.forEach(r => {
                        window.postMessage('show_success|' + JSON.parse(r).message, '*')
                    });
                }
               
            }
        }
       return  { data: result.message, error: null }
    
      })
      .catch((error) => {
        handleServerMessage(error)
        return { data: null, error }
    });
}

export function createDocument(doctype, params = Object){
      return db.createDoc(doctype,params)
        .then((doc) =>{
            window.postMessage('show_success|Save successfully', '*')
            return   { data: doc, error: null }
        }
            
        )
        .catch((error) => 
        {
            handleServerMessage(error)
            return   { data: null, error: error }
        });
}


export function deleteApi(api, params = Object, message){
 
    return new Promise((resolve, reject)=>{
        call.delete(`edoor.api.${api}`, params).then((result) => {
            window.postMessage('show_success|' + `${message ? message : 'Deleted successful'}`, '*')
            resolve(result)
        }).catch((error) =>{
            handleServerMessage(error)
            reject(error)
        })
    })
}
export function renameDoc(doctype, old_name,new_name){
    let doc = {
        doctype: doctype,
        old_name: old_name,
        new_name: new_name
    }

    return new Promise((resolve, reject)=>{
        if(doc.old_name != doc.new_name){
            postApi('utils.rename_doc', { data: doc }).then((r)=>{
                resolve(r.message)
            }).catch((err)=>{
                reject(err)
            }) 
        }
    })
}

export function uploadFiles(files, fileArgs = Object){

 
    const file = frappe.file();
    return new Promise((resolve, reject)=>{
        let countFile = 0
        files.forEach((r)=>{
            fileArgs.otherData={custom_title: r.custom_title || "",custom_description:r.custom_description || ""}
            file.uploadFile(
                r,
                fileArgs,
                undefined,
                "edoor.api.upload.upload_file"
            )
            .then((r) => {
                if(r.data && r.data.message){
                    countFile++
                    if(countFile == files.length){
                        window.postMessage('show_success|' + 'Upload files successfull.', '*')
                        resolve(true)
                    }
                }
                
            })
            .catch((error) =>{
                handleServerMessage(error)
                reject(error)
            })
        })
    })
    
}

