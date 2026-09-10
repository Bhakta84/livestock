const CONFIG = {
  SHEET_ID: 'PASTE_GOOGLE_SHEET_ID_HERE',
  DRIVE_FOLDER_ID: 'PASTE_GOOGLE_DRIVE_FOLDER_ID_HERE',
  TOKEN_HOURS: 24
};

const SHEETS = {
  USERS:'Users', TENDERS:'Tenders', DOCUMENTS:'Documents',
  BOQS:'BOQs', BOQ_ITEMS:'BOQ_Items', BIDS:'Bids',
  BID_ITEMS:'Bid_Items', AUDIT:'AuditLog'
};

const HEADERS = {
  Users:['id','email','name','company','phone','password_hash','role','active','created_at'],
  Tenders:['id','tender_id','title','category','location','procurement_method','description','publication_date','submission_deadline','opening_date','emd_type','emd_amount','financial_evaluation_percent','status','created_by','created_at','updated_at'],
  Documents:['id','parent_type','parent_id','name','drive_file_id','drive_url','mime_type','uploaded_at'],
  BOQs:['id','tender_id','name','created_at'],
  BOQ_Items:['id','boq_id','line_no','description','unit','quantity'],
  Bids:['id','tender_id','bidder_email','reference','total_amount','emd_reference','status','submitted_at','created_at'],
  Bid_Items:['id','bid_id','boq_item_id','rate','amount'],
  AuditLog:['id','timestamp','user','action','entity_type','entity_id','details']
};

function setup(){
  const ss=SpreadsheetApp.openById(CONFIG.SHEET_ID);
  Object.keys(HEADERS).forEach(n=>{
    let sh=ss.getSheetByName(n); if(!sh) sh=ss.insertSheet(n);
    if(sh.getLastRow()===0) sh.appendRow(HEADERS[n]);
  });
  return out({ok:true,message:'BLDCL e-Procurement Google Sheets database initialized'});
}

function doGet(e){
  try{
    const a=(e.parameter.action||'').toLowerCase();
    if(a==='setup') return setup();
    if(a==='tenders') return authGet(e,()=>({tenders:listTenders()}));
    if(a==='tender') return authGet(e,()=>({tender:getTender(e.parameter.id)}));
    if(a==='documents') return authGet(e,()=>({documents:documentsFor(e.parameter.parent_id)}));
    if(a==='boq') return authGet(e,()=>({boq:getBOQ(e.parameter.tender_id)}));
    if(a==='bids') return authGet(e,()=>({bids:listBids(e.parameter.email)}));
    return out({ok:false,error:'Unknown action'});
  }catch(err){return out({ok:false,error:String(err)})}
}

function doPost(e){
  const lock=LockService.getScriptLock(); lock.waitLock(30000);
  try{
    const b=JSON.parse(e.postData.contents||'{}'), a=(b.action||'').toLowerCase();
    if(a==='setup') return setup();
    if(a==='register') return register(b);
    if(a==='login') return login(b);
    return authPost(b,a);
  }catch(err){return out({ok:false,error:String(err)})}
  finally{lock.releaseLock()}
}

function authPost(b,a){
  const user=authorize(b.token);
  const map={
    create_tender:()=>needRole(user,['Admin','Procurement Officer'])&&createTender(b,user),
    publish_tender:()=>needRole(user,['Admin','Procurement Officer'])&&setTenderStatus(b.id,'OPEN',user),
    close_tender:()=>needRole(user,['Admin','Procurement Officer'])&&setTenderStatus(b.id,'CLOSED',user),
    create_bid:()=>createBid(b,user),
    save_bid_items:()=>saveBidItems(b,user),
    submit_bid:()=>submitBid(b.id,user),
    upload_document:()=>uploadDocument(b,user),
    create_boq:()=>needRole(user,['Admin','Procurement Officer'])&&createBOQ(b,user)
  };
  if(!map[a]) throw new Error('Unknown action');
  const result=map[a](); return out({ok:true,...(result||{})});
}

function register(b){
  if(!b.email||!b.password||!b.name||!b.company) throw new Error('Name, company, email and password are required');
  const email=String(b.email).trim().toLowerCase();
  if(rows('Users').some(u=>String(u.email).toLowerCase()===email)) throw new Error('Email is already registered');
  const u={id:uid(),email,name:b.name,company:b.company,phone:b.phone||'',password_hash:hash(b.password),role:'Bidder',active:'TRUE',created_at:iso()};
  append('Users',u); audit(email,'REGISTER','User',u.id,u.company);
  return out({ok:true,user:safeUser(u),token:tokenFor(u)});
}
function login(b){
  const email=String(b.email||'').trim().toLowerCase();
  const u=rows('Users').find(x=>String(x.email).toLowerCase()===email);
  if(!u||String(u.active).toUpperCase()!=='TRUE'||u.password_hash!==hash(b.password||'')) throw new Error('Invalid email or password');
  return out({ok:true,user:safeUser(u),token:tokenFor(u)});
}

function listTenders(){
  return rows('Tenders').map(t=>{
    if(t.status==='OPEN'&&new Date(t.submission_deadline)<=new Date()) setTenderStatus(t.id,'CLOSED',{email:'system',role:'Admin'});
    return t;
  });
}
function getTender(id){
  const t=listTenders().find(x=>String(x.id)===String(id)||String(x.tender_id)===String(id));
  if(!t) return null;
  t.documents=documentsFor(t.id); t.boq=getBOQ(t.id); return t;
}
function createTender(b,u){
  const t={id:uid(),tender_id:b.tender_id,title:b.title,category:b.category,location:b.location||'',
    procurement_method:b.procurement_method||'Open Tendering',description:b.description||'',
    publication_date:b.publication_date||iso(),submission_deadline:b.submission_deadline,opening_date:b.opening_date,
    emd_type:b.emd_type||'',emd_amount:b.emd_amount||0,financial_evaluation_percent:b.financial_evaluation_percent||100,
    status:'DRAFT',created_by:u.email,created_at:iso(),updated_at:iso()};
  append('Tenders',t); audit(u.email,'CREATE','Tender',t.id,t.tender_id); return {tender:t};
}
function setTenderStatus(id,status,u){
  const t=getRow('Tenders',id); if(!t) throw new Error('Tender not found');
  if(status==='OPEN'&&new Date(t.submission_deadline)<=new Date()) throw new Error('Submission deadline must be in the future');
  updateRow('Tenders',id,{status,updated_at:iso()}); audit(u.email,status,'Tender',id,t.tender_id);
  return {tender:getTender(id)};
}

function createBOQ(b,u){
  const t=getTender(b.tender_id); if(!t) throw new Error('Tender not found');
  const q={id:uid(),tender_id:t.id,name:b.name||'BOQ',created_at:iso()}; append('BOQs',q);
  (b.items||[]).forEach((x,i)=>append('BOQ_Items',{id:uid(),boq_id:q.id,line_no:x.line_no||i+1,description:x.description,unit:x.unit||'',quantity:x.quantity||0}));
  audit(u.email,'CREATE','BOQ',q.id,t.tender_id); return {boq:getBOQ(t.id)};
}
function getBOQ(tenderId){
  const q=rows('BOQs').find(x=>String(x.tender_id)===String(tenderId));
  if(!q) return null;
  q.items=rows('BOQ_Items').filter(x=>String(x.boq_id)===String(q.id)); return q;
}

function createBid(b,u){
  const t=getTender(b.tender_id); if(!t) throw new Error('Tender not found');
  if(t.status!=='OPEN'||new Date(t.submission_deadline)<=new Date()) throw new Error('Tender is closed');
  const old=rows('Bids').find(x=>String(x.tender_id)===String(t.id)&&String(x.bidder_email).toLowerCase()===u.email.toLowerCase());
  if(old) return {bid:old};
  const bid={id:uid(),tender_id:t.id,bidder_email:u.email,reference:'BID-'+Date.now()+'-'+Math.floor(Math.random()*10000),
    total_amount:b.total_amount||0,emd_reference:b.emd_reference||'',status:'DRAFT',submitted_at:'',created_at:iso()};
  append('Bids',bid); audit(u.email,'CREATE','Bid',bid.id,bid.reference); return {bid};
}
function saveBidItems(b,u){
  const bid=getRow('Bids',b.bid_id); if(!bid||bid.bidder_email.toLowerCase()!==u.email.toLowerCase()) throw new Error('Not permitted');
  if(bid.status!=='DRAFT') throw new Error('Submitted bid cannot be edited');
  rows('Bid_Items').filter(x=>String(x.bid_id)===String(bid.id)).forEach(x=>deleteRow('Bid_Items',x.id));
  let total=0;
  (b.items||[]).forEach(x=>{const amount=Number(x.amount||Number(x.rate||0)*Number(x.quantity||0)); total+=amount;
    append('Bid_Items',{id:uid(),bid_id:bid.id,boq_item_id:x.boq_item_id,rate:x.rate||0,amount});});
  updateRow('Bids',bid.id,{total_amount:total}); return {bid:getRow('Bids',bid.id)};
}
function submitBid(id,u){
  const bid=getRow('Bids',id); if(!bid||bid.bidder_email.toLowerCase()!==u.email.toLowerCase()) throw new Error('Not permitted');
  const t=getTender(bid.tender_id);
  if(!t||t.status!=='OPEN'||new Date(t.submission_deadline)<=new Date()) throw new Error('Tender is closed; bid submission is disabled');
  updateRow('Bids',id,{status:'SUBMITTED',submitted_at:iso()}); audit(u.email,'SUBMIT','Bid',id,bid.reference);
  return {bid:getRow('Bids',id)};
}
function listBids(email){return rows('Bids').filter(x=>!email||String(x.bidder_email).toLowerCase()===String(email).toLowerCase())}

function uploadDocument(b,u){
  if(!b.parent_id||!b.name||!b.base64) throw new Error('parent_id, name and base64 are required');
  const folder=DriveApp.getFolderById(CONFIG.DRIVE_FOLDER_ID);
  const file=folder.createFile(Utilities.newBlob(Utilities.base64Decode(b.base64),b.mimeType||'application/octet-stream',b.name));
  const d={id:uid(),parent_type:b.parent_type||'Bid',parent_id:b.parent_id,name:b.name,drive_file_id:file.getId(),drive_url:file.getUrl(),mime_type:b.mimeType||'',uploaded_at:iso()};
  append('Documents',d); audit(u.email,'UPLOAD','Document',d.id,d.name); return {document:d};
}
function documentsFor(parent){return rows('Documents').filter(x=>String(x.parent_id)===String(parent))}

function authorize(t){
  if(!t) throw new Error('Authentication token required');
  const parts=String(t).split('|'); if(parts.length!==3) throw new Error('Invalid token');
  const email=parts[0], exp=Number(parts[1]), sig=parts[2];
  if(exp<Date.now()||sig!==Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(email+'|'+exp,CONFIG.SHEET_ID))) throw new Error('Session expired');
  const u=rows('Users').find(x=>x.email===email); if(!u) throw new Error('User not found'); return u;
}
function tokenFor(u){const exp=Date.now()+CONFIG.TOKEN_HOURS*3600000; const sig=Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(u.email+'|'+exp,CONFIG.SHEET_ID)); return u.email+'|'+exp+'|'+sig}
function needRole(u,roles){if(roles.indexOf(u.role)<0)throw new Error('Insufficient permission');return true}
function safeUser(u){return {id:u.id,email:u.email,name:u.name,company:u.company,phone:u.phone,role:u.role}}
function hash(s){return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,String(s),Utilities.Charset.UTF_8))}
function uid(){return Utilities.getUuid()} function iso(){return new Date().toISOString()}
function sheet(n){return SpreadsheetApp.openById(CONFIG.SHEET_ID).getSheetByName(n)}
function rows(n){const sh=sheet(n),v=sh.getDataRange().getValues();if(v.length<2)return[];return v.slice(1).map(r=>Object.fromEntries(v[0].map((h,i)=>[h,r[i]])))}
function append(n,o){const sh=sheet(n),h=sh.getRange(1,1,1,sh.getLastColumn()).getValues()[0];sh.appendRow(h.map(k=>o[k]===undefined?'':o[k]))}
function getRow(n,id){return rows(n).find(x=>String(x.id)===String(id))}
function updateRow(n,id,c){const sh=sheet(n),v=sh.getDataRange().getValues(),h=v[0],ix=h.indexOf('id');for(let r=1;r<v.length;r++)if(String(v[r][ix])===String(id)){Object.keys(c).forEach(k=>{const j=h.indexOf(k);if(j>=0)v[r][j]=c[k]});sh.getRange(r+1,1,1,h.length).setValues([v[r]]);return}throw new Error('Record not found')}
function deleteRow(n,id){const sh=sheet(n),v=sh.getDataRange().getValues(),ix=v[0].indexOf('id');for(let r=v.length-1;r>0;r--)if(String(v[r][ix])===String(id)){sh.deleteRow(r+1);return}}
function audit(user,a,t,id,d){append('AuditLog',{id:uid(),timestamp:iso(),user:user||'',action:a,entity_type:t,entity_id:id,details:d||''})}
function out(x){return ContentService.createTextOutput(JSON.stringify(x)).setMimeType(ContentService.MimeType.JSON)}
function authGet(e,fn){authorize(e.parameter.token);return out({ok:true,...fn()})}
