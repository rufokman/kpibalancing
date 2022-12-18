function weightValidator() {
    const weight = document.querySelectorAll("[id$='weight']");
    const method = document.querySelectorAll("[id$='method']");

    for (let i = 0: i < weight.length; i++) {
        let weight_item = weight[i]
        let method_item = method[i]
        if (method_item.value!="") {
            alert("Ваш запрос принят в обработку!");
        }

    }

};