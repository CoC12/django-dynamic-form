const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                return decodeURIComponent(cookie.trim().substring(name.length + 1));
            }
        });
    }
    return null;
}

const initDynamicForm = () => {
    const dynamicFormNodeList = document.querySelectorAll('.ddf-form-container');
    dynamicFormNodeList.forEach(dynamicFormNode => {
        triggerNodeList = dynamicFormNode.querySelectorAll('[data-ddf-trigger]');
        triggerNodeList.forEach(triggerNode => {
            const trigger = triggerNode.dataset.ddfTrigger;
            triggerNode.addEventListener(trigger, updateForm);
        });
    });
}

const updateForm = (event) => {
    const dynamicFormContainer = event.target.closest('.ddf-form-container');
    const formData = new FormData(dynamicFormContainer.closest('form'));
    formData.append('ddf-form-key', dynamicFormContainer.dataset.formKey);

    const xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.addEventListener('load', _ => {
        if (xmlHttpRequest.status !== 200) {
            return;
        }
        dynamicFormContainer.innerHTML = xmlHttpRequest.responseText;
        document.dispatchEvent(new CustomEvent('ddfFormUpdated'));
    });
    xmlHttpRequest.open('POST', '/ddf-get-form/');
    xmlHttpRequest.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xmlHttpRequest.send(formData);
}

document.addEventListener('DOMContentLoaded', initDynamicForm);
document.addEventListener('ddfFormUpdated', initDynamicForm);
