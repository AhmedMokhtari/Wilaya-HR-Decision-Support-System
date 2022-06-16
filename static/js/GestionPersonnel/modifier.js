 var image = document.getElementById("image");

    // La fonction previewPicture
    var previewPicture  = function (e) {
        // e.files contient un objet FileList
        const [picture] = e.files

        // "picture" est un objet File
        if (picture) {
            // On change l'URL de l'image
            image.src = URL.createObjectURL(picture)
        }
    }

function red (link,val)
{
	var data = link+"/"+val;
	window.open(data,link,'width=620,height=550');
}