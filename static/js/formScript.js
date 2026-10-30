function laptopValidateForm() {

    let brand = document.getElementById('brand').value;
    let hdd = document.getElementById('hdd').value;
    let processor = document.getElementById('processor').value;
    let ram_gb = document.getElementById('ram_gb').value;
    let ram_type = document.getElementById('ram_type').value;
    let ssd = document.getElementById('ssd').value;
    let os = document.getElementById('os').value;
    let weight = document.getElementById('weight').value;
    let warranty = document.getElementById('warranty').value;
    let Touchscreen = document.getElementById('Touchscreen').value;
    let graphic_card_gb = document.getElementById('graphic_card_gb').value;

    if (!graphic_card_gb || !processor || !Touchscreen || !warranty || !weight || !hdd || !os || !ssd || !ram_type || !ram_gb || !brand) {
        // Show the modal with the error message
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        //alert("Please fill out all required fields.");
        return false; // Prevent form submission
    }
    window.location.href = 'result.html';
    return true;
}


function cameraValidateForm() {

    let model = document.getElementById('model').value;
    let low_resolution = document.getElementById('low_resolution').value;
    let max_resolution = document.getElementById('max_resolution').value;
    let effective_pixels = document.getElementById('effective_pixels').value;
    let zoom_wide = document.getElementById('zoom_wide').value;
    let zoom_tele = document.getElementById('zoom_tele').value;
    let normal_focus_range = document.getElementById('normal_focus_range').value;
    let macro_focus_range = document.getElementById('macro_focus_range').value;
    let storage_included = document.getElementById('storage_included').value;
    let weight = document.getElementById('weight').value;
    let dimensions = document.getElementById('dimensions').value;

    if (!model || !low_resolution || !weight || !max_resolution || !effective_pixels || !zoom_wide || !zoom_tele || !normal_focus_range || !macro_focus_range || !storage_included || !processor_brand || !dimensions) {
        // Show the modal with the error message
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        //alert("Please fill out all required fields.");
        return false; // Prevent form submission
    }
    window.location.href = 'result.html';
    return true;
}


function refrigeratorValidateForm()
{

    let brand = document.getElementById('brand').value;
    let model = document.getElementById('model').value;
    let capacity = document.getElementById('capacity').value;
    let type = document.getElementById('type').value;
    let material = document.getElementById('material').value;
    let text_feature = document.getElementById('text_feature').value;
    let category = document.getElementById('category').value;
    let random_numeric_features = document.getElementById('random_numeric_features').value;
    let price = document.getElementById('price').value;


    if (!model || !price || !brand || !capacity || !type || !material || !text_feature || !category || !random_numeric_features) {
        // Show the modal with the error message
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        //alert("Please fill out all required fields.");
        return false; // Prevent form submission
    }
    window.location.href = 'result.html';
    return true;
}

function washingMachineValidateForm()
{

    let brand = document.getElementById('brand').value;
    let capacity = document.getElementById('capacity').value;
    let color = document.getElementById('color').value;
    let maximum_spin = document.getElementById('maximum_spin').value;
    let product_name = document.getElementById('product_name').value;
    let speed = document.getElementById('speed').value;
    let fuction_type = document.getElementById('fuction_type').value;
    let washing_method = document.getElementById('washing_method').value;
    


    if (!brand || !capacity || !color || !maximum_spin || !product_name || !speed || !fuction_type||!washing_method||!model) {
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        return false; 
    }
    window.location.href = 'result.html';
    return true;
}

function tabletValidateForm()
{

    let name = document.getElementById('name').value;
    let sim = document.getElementById('sim').value;
    let brand = document.getElementById('processor_brand').value;
    let num = document.getElementById('num_processor').value;
    let memory = document.getElementById('memory_inbuilt').value;
    let battry_capacity = document.getElementById('battry_capacity').value;
    let resolution_height = document.getElementById('resolution_height').value;
    let resolution_width = document.getElementById('resolution_width').value;
    let ppi = document.getElementById('ppi').value;
    let speed = document.getElementById('processor_speed').value;
    let primary_front_camera = document.getElementById('primary_front_camera').value;
    let primary_rear_camera = document.getElementById('primary_rear_camera').value;
    let memory_card_up = document.getElementById('memory_card_up').value;
    let ram = document.getElementById('ram').valur;


    if (!name||!sim||!resolution_width||!primary_rear_camera||!brand || !num || !memory || !battry_capacity || !resolution_height || !ppi || !primary_front_camera || !speed || !memory_card_up||!ram) {
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        return false; 
    }
    window.location.href = 'result.html';
    return true;
}

function cellphoneValidateForm()
{

    let brand = document.getElementById('product_brand').value;
    let model = document.getElementById('model').value;
    let storage = document.getElementById('product_storage').value;
    let battry_capacity = document.getElementById('battry_capacity').value;
    let screen_size = document.getElementById('screen_size').value;
    let primary_front_camera = document.getElementById('primary_front_camera').value;
    let ram = document.getElementById('ram').valur;


    if (!brand || !model || !storage || !battry_capacity || !primary_front_camera || !screen_size||!ram) {
        modalMessage.textContent = "Please fill out all required fields!";
        errorModal.style.display = "block";
        return false; 
    }
    window.location.href = 'result.html';
    return true;
}
const okBtn = document.getElementById("okBtn");
    if (okBtn) {
        okBtn.onclick = function() {
            const errorModal = document.getElementById("errorModal");
            if (errorModal) {
                errorModal.style.display = "none"; // Close the error modal on OK click
            }
        };
    }

// Close the error modal if clicked outside the modal content
window.onclick = function(event) {
    const errorModal = document.getElementById("errorModal");
    if (event.target === errorModal) {
        errorModal.style.display = "none";
    }
};
