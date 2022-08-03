/* course_detail_student.js */
// Handles the enrolling and unenrolling of students

document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = Cookies.get('csrftoken');
    const btn_enroll_toggle = document.querySelector('#btn-enroll-toggle')
    const btn_enroll_modal = document.querySelector('#btn-enroll-modal')

    if (btn_enroll_modal.innerHTML !== 'Enroll') {
        document.querySelector("#student-grade-container").style.display = 'block';
    }

    btn_enroll_toggle.onclick = function() {

        const request = new Request(
            `/course/${this.dataset.code}/student-api/`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        const enroll = btn_enroll_modal.innerHTML === 'Enroll'
        
        fetch(request, {
            method: 'PUT',
            mode: 'same-origin',  // Do not send CSRF token to another domain.
            body: JSON.stringify({
                enroll: enroll
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.success_message) {

                // Update student count
                console.log(`/course/${btn_enroll_toggle.dataset.code}/student-api/`)
                fetch(request, {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#student-count').innerHTML = data.student_count
                    if (enroll) {
                        document.querySelector('#student-grade-score').innerHTML = data.grade? data.grade : '*Ungraded*'
                    }
                })
                .catch(error => {
                    if (error) {
                        console.log(error);
                    };
                });

                // After modal animation finishes, toggle Enroll/Unenroll 
                Promise.all(
                    document.querySelector("#modal-confirm").getAnimations().map(
                      function(animation) {
                        return animation.finished
                      }
                    )
                  ).then(
                    function() {
                        const word = enroll? "Unenroll" : "Enroll";
                        const word_lower = word.toLowerCase()
                        // Toggle Enroll Button
                        btn_enroll_toggle.innerHTML = `Yes, ${word_lower} me.`
                        // Confirmation Modal
                        btn_enroll_modal.className = enroll? "btn btn-danger" : "btn btn-primary";
                        btn_enroll_modal.innerHTML = word;
                        document.querySelector("#modalConfirmLabel").innerHTML = `${word}ment Confirmation`;
                        document.querySelector(".modal-body").innerHTML = `Are you sure you want to ${word_lower}?`
                        // Show/Hide Grades
                        document.querySelector("#student-grade-container").style.display = enroll? "block" : "none";
                    }
                  );

            };

        });

    };

});