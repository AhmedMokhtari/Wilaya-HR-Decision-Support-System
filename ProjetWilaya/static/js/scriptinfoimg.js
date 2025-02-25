$('.ui.dropdown').dropdown({
    forceSelection: false
});
document.getElementById('formsearch').addEventListener('change', e=>{
    let division = document.getElementById("div").value;
    let budget = document.getElementById("budget").value;
    let grade = document.getElementById("grade").value;
    let genre=$('input[name="radioGenre"]:checked').val();
    let ancienneteAdmi = 1;
    let ancienneteAdmiValue=1;
    let idDivision = 1;
    let idDivisionValue=1;
    let idGrade = 1;
    let idGradeValue=1;
    let genreName=1;
    let genreValue=1;
    if(e.target.name=="budget"){
       if(division!=""){
           if(division==-1){
               idDivision = 1;
               idDivisionValue=1;
           }else{
               idDivision = "IdDivision";
               idDivisionValue=division;
           }
       }
        if(grade!=""){
           if(grade==-1){
               idGrade = 1;
               idGradeValue=1;
           }else{
               idGrade = "IdGrade";
               idGradeValue=grade;
           }
       }
       if(genre!=undefined){
           if(genre=="Homme"){
               genreName = "Sexe";
               genreValue="Homme";
           }else{
               genreName = "Sexe";
               genreValue="Femme";
           }
       }
        if(e.target.value==-1){
              ancienneteAdmi = 1;
              ancienneteAdmiValue=1;
       }else{
           ancienneteAdmi="AdministrationApp";
           ancienneteAdmiValue=e.target.value;
       }

   }
    if(e.target.name=="div"){
       if(budget!=""){
           if(budget==-1){
               ancienneteAdmi = 1;
               ancienneteAdmiValue=1;
           }else{
               ancienneteAdmi = "AdministrationApp";
               ancienneteAdmiValue=budget;
           }
       }
        if(grade!=""){
           if(grade==-1){
               idGrade = 1;
               idGradeValue=1;
           }else{
               idGrade = "IdGrade";
               idGradeValue=grade;
           }
       }
       if(genre!=undefined){
           if(genre=="Homme"){
               genreName = "Sexe";
               genreValue="Homme";
           }else{
               genreName = "Sexe";
               genreValue="Femme";
           }
       }
       if(e.target.value==-1){
               idDivision = 1;
               idDivisionValue=1;
       }else{
           idDivision = "IdDivision";
           idDivisionValue=e.target.value;
       }
   }
    if(e.target.name=="grade"){
       if(budget!=""){
           if(budget==-1){
               ancienneteAdmi = 1;
               ancienneteAdmiValue=1;
           }else{
               ancienneteAdmi = "AdministrationApp";
               ancienneteAdmiValue=budget;
           }
       }
        if(division!=""){
           if(division==-1){
               idDivision = 1;
               idDivisionValue=1;
           }else{
               idDivision = "IdDivision";
               idDivisionValue=division;
           }
       }
       if(genre!=undefined){
           if(genre=="Homme"){
               genreName = "Sexe";
               genreValue="Homme";
           }else{
               genreName = "Sexe";
               genreValue="Femme";
           }
       }
       if(e.target.value==-1){
               idGrade = 1;
               idGradeValue=1;
       }else{
           idGrade = "IdGrade";
           idGradeValue=e.target.value;
       }
   }
   if(e.target.name=="radioGenre"){
       if(budget!=""){
           if(budget==-1){
               ancienneteAdmi = 1;
               ancienneteAdmiValue=1;
           }else{
               ancienneteAdmi = "AdministrationApp";
               ancienneteAdmiValue=budget;
           }
       }
        if(division!=""){
           if(division==-1){
               idDivision = 1;
               idDivisionValue=1;
           }else{
               idDivision = "IdDivision";
               idDivisionValue=division;
           }
       }
       if(grade!=""){
           if(grade==-1){
               idGrade = 1;
               idGradeValue=1;
           }else{
               idGrade = "IdGrade";
               idGradeValue=grade;
           }
       }
       if(e.target.value=="Homme"){
           genreName = "Sexe";
               genreValue="Homme";
       }else{
           genreName = "Sexe";
           genreValue="Femme";
       }
   }
   let values=ancienneteAdmi+"-"+ancienneteAdmiValue+"-"+idDivision+"-"+idDivisionValue+"-"+idGrade+"-"+idGradeValue+"-"+genreName+"-"+genreValue;
  console.log(e.target.value)
  console.log(genre)
  ajaxPerso(values)

})
DJANGO_STATIC_URL = "{{ static 'images/steve.jpg' }}";
function ajaxPerso(selectedbudget){
   $.ajax({
       type: 'GET',
       url: `perso-json/${selectedbudget}/`,
       success: function(response){
           const persoData = response.data
           let tb1 = document.querySelector('#imglist');
           tb1.innerHTML=""
           persoData.map(item=>{
               let idp = item.IdPersonnel;
               let personnels;
               personnels=` <div class="col-12 col-sm-8 col-md-6 col-lg-4">
               <div class="card p-2 shadow  " >
                <div class="p-5">              
                     <img class="card-img-top" style="border-radius: 50%" src="http://127.0.0.1:8000/static/images/${item.photo}" alt="${item.PrenomFr} ${item.NomFr}">
                 </div>
                <div class="card-body">
                   <a href="info/${item.IdPersonnel}"><p class="card-title" style="color:#0092ff;font-size:23px">${item.NomFr} ${item.PrenomFr} </p></a>
                   <h4 class="card-subtitle mb-2 text-muted my-2">${item.LibelleServiceFr} </h4
                 </div>
               </div>
              </div>`;
           tb1.innerHTML+=personnels;
           })
       },
       error: function(error){
           console.log(error)
       }
   })
}