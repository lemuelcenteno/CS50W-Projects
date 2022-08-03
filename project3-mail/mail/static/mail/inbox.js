document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Event listener for sending emails
  document.querySelector("#compose-form").onsubmit = function(event) {
    event.preventDefault();

    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })
    .catch(error => {
      // Print error
      console.log(error)
    });

    load_mailbox('sent')
  };

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-focus-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  const emails_view = document.querySelector('#emails-view');
  emails_view.style.display = 'block';
  document.querySelector('#email-focus-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  let div;
  fetch(`/emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(emails => {

    for (i = 0; i < emails.length; i++) {

      // Create email div
      div = document.createElement('div');
      div.setAttribute('data-emailid', `${emails[i].id}`)
      div.setAttribute('data-mailbox', `${mailbox}`)
      div.className = 'email-listview';
      div.innerHTML = `<strong>${emails[i].sender}</strong><span class="listview-subject">${emails[i].subject}</span><span class="listview-timestamp">${emails[i].timestamp}</span>`;
      
      // Add click event listener to each email div for detail view
      div.onclick = function() {

        // Update email as 'read'
        fetch(`/emails/${this.dataset.emailid}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error));

        // Show email focus view
        show_email(this.dataset.emailid, this.dataset.mailbox);

      };

      // Background color depending on read/unread
      if (emails[i].read) {
        div.style.backgroundColor = 'lightgray';
      } else {
        div.style.backgroundColor = 'white';
      };

      // Append div
      emails_view.append(div);

    };

  })
  .then(error => {
    return error ? `Error: ${error}` : null;
  });

};

// Email focus view
function show_email(email_id, mailbox) {
  const btn_toggle_archive = document.querySelector('#btn-toggle-archive')
  if (mailbox === 'sent') {
    btn_toggle_archive.style.display = 'none';
  } else {
    btn_toggle_archive.style.display = 'inline';
  }
  
  // Show the email-focus-view and hide other views
  const emails_view = document.querySelector('#emails-view');
  const email_focus_view = document.querySelector('#email-focus-view');
  const compose_view = document.querySelector('#compose-view');

  emails_view.style.display = 'none';
  email_focus_view.style.display = 'block';
  compose_view.style.display = 'none';

  fetch(`/emails/${email_id}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(email => {

    if (email.archived) {
      btn_toggle_archive.innerHTML = 'Unarchive'
    } else {
      btn_toggle_archive.innerHTML = 'Archive'
    }

    // Create comma-separated string of recipients
    let recipients = email["recipients"][0];
    for (i = 1; i < email.recipients.length; i++) {
      recipients += ', ' + email.recipient[i];
    }

    // Display email details
    document.querySelector('#email-sender').innerHTML = `<span class='detail-label'>From:</span> ${email.sender}`;
    document.querySelector('#email-recipients').innerHTML = `<span class='detail-label'>To:</span> ${recipients}`;
    document.querySelector('#email-subject').innerHTML = `<span class='detail-label'>Subject: </span> ${email.subject}`;
    document.querySelector('#email-timestamp').innerHTML = `<span class='detail-label'>Timestamp: </span> ${email.timestamp}`;

    // Display email body
    document.querySelector('#email-body').innerHTML = `${email.body}`;

    // Add event listener for the toggle archive button
    btn_toggle_archive.onclick = () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      load_mailbox('inbox');
    };

    // Add event listener for the reply button
    document.querySelector("#btn-reply").onclick = () => {

      // Show compose view and hide other views
      emails_view.style.display = 'none';
      email_focus_view.style.display = 'none';
      compose_view.style.display = 'block';

      // Pre-populate composition fields
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      if (email.subject.startsWith('Re: ')) {
        document.querySelector('#compose-subject').value = email.subject;
      } else {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      document.querySelector('#compose-body').value = `<div class="reply">"On ${email.timestamp} ${email.sender} wrote: ${email.body}"</div><br>\n\n`;

    };

  })
  .catch(error => console.log('Error: ', error));

};