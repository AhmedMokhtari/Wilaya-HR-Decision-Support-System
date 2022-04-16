window.onload=function(){
    if (localStorage.getItem("lang") === null) {
        langAR();
    } 
    if (localStorage.getItem("lang") === "fr") {
        langFr();
    } 
    if (localStorage.getItem("lang") === "ar") {
        langAR();
    } 
} 
let ar = document.getElementById("ar");
let fr = document.getElementById("fr");
let myModalLabel = document.getElementById("myModalLabel");
let modalbody = document.getElementById("modalbody");
let cancel_delete = document.getElementById("cancel-delete");
let confirm_delete = document.getElementById("confirm-delete");

// let sitename = document.getElementById("sitename");
// let acc = document.getElementById("acc");
// let emp = document.getElementById("emp");
// let hol = document.getElementById("hol");
// let avan = document.getElementById("avan");
// let formation = document.getElementById("for");
// let pri = document.getElementById("pri");

let empl = document.getElementById("empl");
let newemp = document.getElementById("newemp");
let deleteall = document.getElementById("deleteall");
let exportEx = document.getElementById("export");
let searchby =document.getElementById("searchby");
let cin =document.getElementById("cin");
let nom =document.getElementById("nom");
let prenom =document.getElementById("prenom");
let action =document.getElementById("action");
let next =document.getElementById("next");
let prec =document.getElementById("prec");
function langAR(){
    localStorage.setItem('lang', 'ar');
    document.dir="rtl";
    myModalLabel.textContent=lang["atten"][1];
    modalbody.textContent=lang["modalb"][1];
    cancel_delete.textContent=lang["cancel"][1];
    confirm_delete.textContent=lang["confirm"][1];
    // sitename.textContent=lang["wilaya"][1];
    // acc.textContent=lang["homepage"][1];
    // emp.textContent=lang["employ"][1];
    // hol.textContent=lang["holiday"][1];
    // avan.textContent=lang["upgrade"][1];
    // formation.textContent=lang["training"][1];
    // pri.textContent=lang["print"][1];
    empl.textContent=lang["employ"][1];
    // newemp.textContent=lang["new_employer"][1];
    // deleteall.textContent=lang["delete_all"][1];
    // exportEx.textContent=lang["export"][1];
    searchby.setAttribute("placeholder",lang["serch_by_cin"][1]);
    cin.textContent=lang["cin"][1];
    nom.textContent=lang["last_name"][1];
    prenom.textContent=lang["first_name"][1];
    action.textContent=lang["action"][1];
    next.innerHTML=lang["next"][1];
    prec.innerHTML=lang["previous"][1];
}
function langFr(){
    localStorage.setItem('lang', 'fr');
    document.dir="ltr";
    myModalLabel.textContent=lang["atten"][0];
    modalbody.textContent=lang["modalb"][0];
    cancel_delete.textContent=lang["cancel"][0];
    confirm_delete.textContent=lang["confirm"][0];
    // sitename.textContent=lang["wilaya"][0];
    // acc.textContent=lang["homepage"][0];
    // emp.textContent=lang["employ"][0];
    // hol.textContent=lang["holiday"][0];
    // avan.textContent=lang["upgrade"][0];
    // formation.textContent=lang["training"][0];
    // pri.textContent=lang["print"][0];
    empl.textContent=lang["employ"][0];
    // newemp.textContent=lang["new_employer"][0];
    // deleteall.textContent=lang["delete_all"][0];
    // exportEx.textContent=lang["export"][0];
    searchby.setAttribute("placeholder",lang["serch_by_cin"][0]);
    cin.innerHTML=lang["cin"][0];
    nom.textContent=lang["last_name"][0];
    prenom.textContent=lang["first_name"][0];
    action.textContent=lang["action"][0];
    next.innerHTML=lang["next"][0];
    prec.innerHTML=lang["previous"][0];


}
ar.onclick=langAR;
fr. onclick=langFr;
let lang={
    wilaya:["Wilaya","ولاية"],
    homepage:["Accueil","الرئيسية"],
    employ:["Personnel","الموضفين"],
    holiday:["Congé","العطل"],
    upgrade:["Avancement","الترقية"],
    training:["Formation","التكوينات"],
    print:["Imprimer","الطباعة"],
    serch_by_cin:["Serch By Cin","البحث بالبطاقة"],
    // new_employer:["Add Employer","موضف جديد"],
    // delete_all:["Delete All","مسح الكل"],
    // export:["Export Excel","إخراج اكسل"],
    cin:["CNIE","ب.ت.و"],
    last_name:["Nom","اللقب"],
    first_name:["Prenom","الإسم"],
    action:["Action","فعل"],
    show:["More","إضهار"],
    delete:["Supprimer","مسح"],
    edit:["Modifer","تعديل"],
    next:["Suivant","التالي"],
    previous:["Precedent","السابق"],
    atten:["Supprimer","مسح"],
    confirm:["Supprimer","مسح"],
    cancel:["Quiter","لإلغاء"],
    modalb:["avez-vous sûr","هل انت متاكد"]
};
  