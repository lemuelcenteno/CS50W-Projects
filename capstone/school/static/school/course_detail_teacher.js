// course_detail_teacher.js
// Handles submission of grades for teachers

document.addEventListener('DOMContentLoaded', () => {

/*     // If any input is empty, prevent form-grades from submitting
    document.querySelector("#form-grades").onsubmit = (event) => {
        document.querySelectorAll('input').forEach(input => {
            if (input.value === '') {
                event.preventDefault()
            };
        })
    }; */

    const btn_submit_grades = document.querySelector("#btn-submit-grades");
    const btn_edit_grades = document.querySelector("#btn-edit-grades");

    // If Submit Grades button exists, set functionality
    if (btn_submit_grades) {
        btn_submit_grades.onclick = function() {
            this.style.display ='none';

            // replace grade field text with input field
            document.querySelectorAll('.no-grade').forEach(td => {
                td.innerHTML = `<input required name="gradebook_${td.dataset.gradebook}" class="grade-input" type="number" min="0" max="100" step="0.01">`;
            });
            
            document.querySelector('#btn-save-grades').style.display = 'inline';
        };
    };
    
    // If Edit Grades button exists, set functionality
    if (btn_edit_grades) {
        btn_edit_grades.onclick = function() {
            this.style.display ='none';

            // replace grade field text with input field
            document.querySelectorAll('.with-grade').forEach(td => {
                const value = parseFloat(td.innerHTML)
                td.innerHTML = `<input required name="gradebook_${td.dataset.gradebook}" value="${value}" class="grade-input" type="number" min="0" max="100" step="0.01">`;
            });

            document.querySelector('#btn-save-edits').style.display = 'inline';
        };
    };

});