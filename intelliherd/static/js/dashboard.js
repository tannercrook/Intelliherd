/* 
Hide and show the sidebar 
============================
*/
function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var main = document.getElementById("main");
    if (window.innerWidth >= 768) {
        if (sidebar.classList.contains("d-none") && !sidebar.classList.contains("d-md-block")) {
            // Show the sidebar
            //sidebar.classList.remove("d-none");
            sidebar.classList.add("d-md-block");
            main.classList.remove("col-md-12");
            main.classList.add("col-10");
        } else if(sidebar.classList.contains('d-md-block')) {
            // Hide the sidebar
            sidebar.classList.remove("d-md-block");
            //sidebar.classList.add("d-none");
            main.classList.remove("col-md-10");
            main.classList.add("col-md-12"); 
        }
    } else {
        if (sidebar.classList.contains("d-none") && (!sidebar.classList.contains("d-md-block") || !sidebar.classList.contains('d-block'))) {
            // Show the sidebar
            sidebar.classList.remove("d-none");
            sidebar.classList.remove("d-md-block");
            sidebar.classList.add("col-12");
            sidebar.classList.add("d-block");
        } else if(sidebar.classList.contains('d-md-block') || sidebar.classList.contains('d-block')) {
            // Hide the sidebar
            sidebar.classList.remove('d-block');
            sidebar.classList.add("d-none");
            sidebar.classList.remove("col-12");
        }
    }
    
}
// ========================== 