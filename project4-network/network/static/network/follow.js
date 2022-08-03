document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = Cookies.get('csrftoken');
    const btn_toggle_follow = document.querySelector('.btn-follow-toggle')

    btn_toggle_follow.onclick = function() {

        const request = new Request(
            `/profile/${this.dataset.followuser}/follow`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        follow = this.innerHTML === 'Follow'

        fetch(request, {
            method: 'PUT',
            mode: 'same-origin',  // Do not send CSRF token to another domain.
            body: JSON.stringify({
                follow: follow
            })
        }).then(response => {
            // Update follower/following count (client)
            fetch(request, {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('#profile-user-followers').innerHTML = data.followers
                document.querySelector('#profile-user-following').innerHTML = data.following
            })
            .catch(error => {
                if (error) {
                    console.log(error);
                };
            });

            // toggle follow/unfollow
            btn_toggle_follow.innerHTML = follow? "Unfollow" : "Follow"

        });

    };

});