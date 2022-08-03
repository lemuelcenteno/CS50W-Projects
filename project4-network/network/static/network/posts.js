document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = Cookies.get('csrftoken');

    document.querySelectorAll('.btn-like-toggle').forEach(button => {

        button.onclick = function() {
            const request = new Request(
                `/post/${this.dataset.post}`,
                { headers: {'X-CSRFToken': csrftoken} }
            );
            
            like = (button.className === "btn-like-toggle far fa-heart");
            // update likes (server)
            fetch(request, {
                method: "PUT",
                body: JSON.stringify({
                    liked: like
                })
            })
            .then(response => {
                // update number of likes (client)
                fetch(`/post/${this.dataset.post}`, {
                    method: "GET"
                })
                .then(response => response.json())
                .then(data => {
                    document.querySelector(`#post-${this.dataset.post}-likes`).innerHTML = data.likes
                })
                .catch(error => {
                    if (error) {
                        console.log(error)
                    }
                });

                // toggle like/unlike
                button.className = like? "btn-like-toggle fas fa-heart" : "btn-like-toggle far fa-heart"
            })
            .catch(error => {
                if (error) {
                    console.log(error)
                }
            });

        };

    });

    document.querySelectorAll('.btn-edit').forEach(button => {

        button.onclick = function() {

            // hide edit button after clicking
            button.style.display = 'none';

            // get and hide like container
            const like_container = document.querySelector(`#like-container-post-${button.dataset.post}`)
            like_container.style.display = 'none';

            // get content_div and clear it's contents
            const content_div = document.querySelector(`#post-${this.dataset.post}-content`);
            content_div.innerHTML = '';

            // create text area and add it inside content_div
            const textarea = document.createElement('textarea');
            textarea.style.display = 'block';
            content_div.append(textarea);

            fetch(`/post/${this.dataset.post}`, {
                method: "GET"
            })
            .then(response => response.json())
            .then(data => {
                textarea.value = data.text
            })
            .catch(error => {
                if (error) {
                    console.log(error)
                };
            });

            const btn_save = document.createElement('button');
            btn_save.className = 'btn-save btn btn-primary btn-sm';
            btn_save.innerHTML = 'Save';
            content_div.append(btn_save);

            btn_save.onclick = () => {
                if (textarea.value !== '') {
                    const request = new Request(
                        `/post/${button.dataset.post}`,
                        { headers: {'X-CSRFToken': csrftoken} }
                    );

                    fetch(request, {
                        method: "PUT",
                        body: JSON.stringify({
                            text: textarea.value
                        })
                    })
                    .then(response => {
                        // update number of likes (client)
                        fetch(`/post/${this.dataset.post}`, {
                            method: "GET"
                        })
                        .then(response => response.json())
                        .then(data => {
                            content_div.innerHTML = data.text
        
                            // toggle edit button and like container visibility
                            button.style.display = 'inline';
                            like_container.style.display = 'block';
                        })
                        .catch(error => {
                            if (error) {
                                console.log(error)
                            }
                        });
                    })
                    .catch(error => {
                        if (error) {
                            console.log(error)
                        }
                    });
                }
            };

        };

    });

});