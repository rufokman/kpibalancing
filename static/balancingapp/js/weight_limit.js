function date_comapare() {

    var d1 = document.getElementById("weight").value; // start date
    print d1
    if (new d1 < 10) {
        alert("Endate date should be greater than start date"); // handle  your error validation here
        return false;
    }
    return true;
}
