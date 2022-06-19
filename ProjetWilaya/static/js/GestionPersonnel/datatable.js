$(document).ready(datatb);
//<span class='btn btn-danger' style='color: white;font-size: 16px;'> <span class='' >العدد الإجمالي :</span> _TOTAL_</span>
function datatb() {
     datatbl= $('#datatables-dashboard-projects2').DataTable(
	    {
            "lengthMenu": [[10, 25, 50,75,100, -1],[10, 25, 50,75,100, "الكل"]],
	        dom: 'lfrtip',
            language:{
                "decimal":        "",
                "emptyTable":     "لا يوجد معلومات",
                "info":           "",
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
          retrieve: true,

	    });
     $('#datatables-dashboard-projects2_filter input').attr("placeholder", "بحث ......");
	};