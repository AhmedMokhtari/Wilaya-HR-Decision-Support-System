defaultCheck=document.getElementById("defaultCheck");
checkboxes = document.getElementsByName('check');
defaultCheck.onclick=function(){
    for(var i=0, n=checkboxes.length;i<n;i++) {
      checkboxes[i].checked = defaultCheck.checked;
    }   
}
for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].onclick = function(){
        defaultCheck.checked=false;
    };
  } 
$((function(){
    let modal = `
<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
             <div class="modal-header">
                <h4 class="modal-title " id="myModalLabel"></h4>
              </div>
              <div class="modal-body delete-modal-body" id="modalbody">
              </div>
              <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal" id="cancel-delete"></button>
                     <button type="button" class="btn btn-danger" id="confirm-delete"></button>
               </div>
        </div>
    </div>
</div>`
            $('body').append(modal);
            //Delete Action
            $(".delete").on('click',(e)=>{
              
                $("#deleteModal").modal('show');
            });
            $("#confirm-delete").on('click',()=>{
                $("#deleteModal").modal('hide');
            });
            $("#cancel-delete").on('click',()=>{
                $("#deleteModal").modal('hide');
            });
            
        }()));
