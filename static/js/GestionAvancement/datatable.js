$(document).ready(datatb);
function datatb() {
     datatbl= $('#table').DataTable(
	    {
            "lengthMenu": [[5, 25, 50,75,100, -1],[5, 25, 50,75,100, "الكل"]],
	        dom: '',
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
          retrieve: true,

	    });
     $('#table_filter input').attr("placeholder", "بحث ......");
     $('#table_filter input').addClass(" form-control-lg")
	};