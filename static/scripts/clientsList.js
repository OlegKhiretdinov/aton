window.onload = () => {
    buttons = document.querySelectorAll('td div.edit')
    buttons.forEach(element => element.addEventListener("click", editClickHandler))

    fields = document.querySelectorAll('td .editable_field')
    fields.forEach(element => {
        element.addEventListener("change", changeHandler)}
    )
}

const editClickHandler = (event) => {
    const button = event.target
    const editableField = event.target.closest('td').querySelector('.editable_field')
    const isDisable = editableField.getAttribute("disabled") === "disabled"

    // Изменения отправлены но ответ пока не получен
    if ([...button.classList].includes('block')){
        return
    }

    if (isDisable) {
        editableField.removeAttribute("disabled")
        button.innerHTML = "отмена"
    } else {
        editableField.setAttribute("disabled", "disabled")
        button.innerHTML = "изменить"
    }
}

const changeHandler = (event) => {
    const editableField = event.target
    const button = editableField.closest('td').querySelector('div.edit')
    button.classList.add("block")

    const id = editableField.dataset.clientId
    console.log(editableField.name)
    console.log(editableField.value)

    fetch(`/clients/${id}`,{
        method: "PUT",
        body: JSON.stringify({field: editableField.name, value: editableField.value})
    })
    .then(res => res.json())
    .then(data => {
        editableField.setAttribute("disabled", "disabled")
        button.innerHTML = "изменить"
    })
    .catch(error => console.error('Ошибка:', error))
    .finally(() => button.classList.remove("block"))
}