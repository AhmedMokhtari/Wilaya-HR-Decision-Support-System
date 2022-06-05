$('.ui.dropdown').dropdown({
    forceSelection: false
});
$(document).ready(datatb);
function datatb() {
     datatbl= $('#table').DataTable(
	    {
            "lengthMenu": [[5, 25, 50,75,100, -1],[5, 25, 50,75,100, "الكل"]],
	        dom: 'Blfrtip',
            language:{
                "decimal":        "",
                "emptyTable":     "لا يوجد معلومات",
                "info":           "<span class='btn btn-danger' style='color: white;font-size: 16px;'> <span class='' >العدد الإجمالي :</span> _TOTAL_</span>",
                "infoEmpty":      "إضهار 0 من 0 ",
                "infoFiltered":   "",
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