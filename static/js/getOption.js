function updateOptions() {
    const selectedBrand = document.getElementById("brand").value;

    if (selectedBrand) {
        fetch("/get-options", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ brand: selectedBrand }),
        })
        .then(response => response.json())
        .then(data => {
            // Update OS dropdown
            const osDropdown = document.getElementById("os");
            osDropdown.innerHTML = "<option value=''>Select OS</option>";
            data.os.forEach(os => {
                osDropdown.innerHTML += `<option value="${os}">${os}</option>`;
            });

            const processorDropdown = document.getElementById("processor");
            processorDropdown.innerHTML = "<option value=''>Select Processor</option>";
            data.processor.forEach(processor => {
                processorDropdown.innerHTML += `<option value="${processor}">${processor}</option>`;
            });
        })
        .catch(error => console.error("Error fetching options:", error));
    }
}
