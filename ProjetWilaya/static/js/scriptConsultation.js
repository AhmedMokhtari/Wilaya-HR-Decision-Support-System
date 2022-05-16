$('.ui.dropdown').dropdown({
    forceSelection: false
});
$(document).ready(datatb);
function datatb() {
     datatbl= $('#table').DataTable(
	    {
            "lengthMenu": [[10, 25, 50,75,100, -1], [10, 25, 50,75,100, "الكل"]],
	        dom: 'Blfrtip',
            language:{
                "decimal":        "",
                "emptyTable":     "لا يوجد معلومات",
                "info":           "<span class='btn btn-danger' style='color: white;font-size: 16px;'> <span class='' >العدد الإجمالي :</span> _TOTAL_</span>",
                "infoEmpty":      "إضهار 0 من 0 ",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     " _MENU_      ",
                "loadingRecords": "جار التحميل ...",
                "processing":     "",
                "search":         "",
                "zeroRecords":    "لا يوجد معلومات",
                "paginate": {
                    "first":      "الأخير",
                    "last":       "الاول",
                    "next":       "التالي",
                    "previous":   "السابق"
                },
                "aria": {
                    "sortAscending":  ": activate to sort column ascending",
                    "sortDescending": ": activate to sort column descending"
                }
            },
            buttons: [
                {
                    extend: 'excelHtml5',
                    title: 'Personnel List',
                    className: 'btn_excel',
                    text:''
                },
                {
                    extend: 'print',
                    title: 'Personnel List',
                    className: 'btn_print',
                    text: ''
                },
                {
                    extend: 'pdfHtml5',
                    title: 'Personnel List',
                    className: 'btn_pdf',
                    text: ''
                },
	       ],
          retrieve: true,

	    });
     $('.btn_excel').html(`<i style="color: green" class="fa-solid fa-file-excel fa-2xl" ></i>`);
     $('.btn_pdf').html(`<i style="color: orange" class="fa-solid fa-file-pdf fa-2xl "></i>`);
     $('.btn_print').html(`<i class="fa-solid fa-print fa-2xl"></i>`);
     $('.btn_excel').removeClass("btn-secondary ");
     $('.btn_pdf').removeClass("btn-secondary ");
     $('.btn_print').removeClass("btn-secondary ");
     //console.log(document.querySelector("#table_filter label").textContent);
     $('#table_filter input').attr("placeholder", "بحث ......");
     $('#table_filter input').addClass(" form-control-lg")
	};
 document.getElementById('formsearch').addEventListener('change', e=>{
     let division = document.getElementById("div").value;
     let budget = document.getElementById("budget").value;
     let grade = document.getElementById("grade").value;
     let ancienneteAdmi = 1;
     let ancienneteAdmiValue=1;
     let idDivision = 1;
     let idDivisionValue=1;
     let idGrade = 1;
     let idGradeValue=1;
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
        if(e.target.value==-1){
                idGrade = 1;
                idGradeValue=1;
        }else{
            idGrade = "IdGrade";
            idGradeValue=e.target.value;
        }
    }
    let values=ancienneteAdmi+"-"+ancienneteAdmiValue+"-"+idDivision+"-"+idDivisionValue+"-"+idGrade+"-"+idGradeValue;
    ajaxPerso(values)
     let table=$('#table').DataTable()
    table.clear().destroy();
    datatb();
   // $('#table').row().invalidate().draw();
   // $('#table').rows().fnInvalidateRow();
   // let a= $('#table tbody tr:eq(0)')
   // $('#table').rows().invalidate().draw();
     //datatbl1.DataTable().draw();

})
 function ajaxPerso(selectedbudget){
    $.ajax({
        type: 'GET',
        url: `perso-json/${selectedbudget}/`,
        success: function(response){
            const persoData = response.data
            let tb1 = document.querySelector('#tbody');
           // tb1.innerHTML=""
            persoData.map(item=>{
                let table =$('#table').DataTable();
                let idp = item.IdPersonnel;
                 table.row.add([
                    item.Cin ,
                    item.NomFr,
                    item.AdministrationApp,
                    item.LibelleDivisionFr,
                    item.GradeFr,
                   `<a href="info/${idp}" class="btn btn-success m-1"><i class="fa-solid fa-arrow-up-right-from-square fa-lg " ></i></a><a href="modifier/${idp}"class="btn btn-warning btn-icon  mx-1"><i class="fa-solid fa-pen-to-square fa-lg"></i></a>`
                ]).draw();
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}