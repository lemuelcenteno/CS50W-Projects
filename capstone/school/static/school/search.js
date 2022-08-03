/* search.js */
// If input-search is empty or purely spaces, prevent form-search from submitting

document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#form-search").onsubmit = (event) => {
        const value = document.querySelector('#input-search').value.trim()
        if (value === '' || !value.replace(/\s/g, '').length) {
            event.preventDefault()
        };
    };

});