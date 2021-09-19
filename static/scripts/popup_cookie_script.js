$ (document).ready(function() {   
    if ($.cookie("Etherfinder_Popup") == null) {
        $("#myModal").modal('show');
    $.cookie("Etherfinder_Popup", "2", { expires: 365 });
}
});