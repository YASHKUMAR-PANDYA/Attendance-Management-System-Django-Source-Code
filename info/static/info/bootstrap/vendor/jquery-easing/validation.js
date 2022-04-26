function validatepunch(){
    let x = document.forms["punchform"]["reivew"].value;
    if (x == "") {
        alert("Add your work review before punching out");
        return false;
    }
}