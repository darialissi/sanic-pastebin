'use strict';


async function getResponse(url, method, body) {
    const response = await fetch(url, {
        method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`
        },
        body: JSON.stringify(body),
    })
    if (!response.ok) {
        throw new Error(`${response.status}: ${response.statusText}`)
    }
    return await response.json()
};

// Sign In modal logic
const modal = document.getElementById('signinModal');
const btn = document.querySelector('.signin-btn');
const btnSubmit = document.querySelector('.signin-form-btn');
const span = document.getElementsByClassName('close')[0];

btnSubmit.onclick = async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const pattern = /^\w{5,}$/

    if (!pattern.exec(username) || !pattern.exec(password)) {
        alert('Fields can contain only latin characters;\nThe minimal length of fields is 5.');
        return;
    }
    
    // Send API request to '/signin'
    try {
        const data = await getResponse('http://127.0.0.1:8000/api/signin', 'POST', { username, password })
        if (data.token) 
            {
                sessionStorage.setItem('token', data.token);
                alert('Sign in successful!');
                modal.style.display = "none";
            } else {
                alert(`Sign in failed: ${data.message}`);
            }
    } catch(e) {
        console.error('Error:', e);
        alert(`Sign in failed: ${e}`);
    };
  };

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Paste creation
async function createPaste(text) {

    const result = document.getElementById('pasteResult');
    const modal = document.getElementById('pasteResultModal');
        
    // Send API request to '/pastes'
    try {
      const data = await getResponse('http://127.0.0.1:8000/api/pastes', 'POST',  { text })
      if (data.uri) {
          const pasteLink = `http://127.0.0.1:8000/${data.uri}`;
          result.textContent = `Paste created successfully! Link: ${pasteLink}`;
          modal.style.display = 'block';
                
          // Clear the textarea
          document.getElementById('paste-content').value = '';
          } else {
          result.textContent = data.message || 'Failed to create paste. Please try again.';
          modal.style.display = 'block';
          }
      } catch(e) {
          console.error('Error:', error);
          result.textContent = 'An error occurred. Please try again later.';
          modal.style.display = 'block';
      }
};

const p_modal = document.getElementById('pasteResultModal');
const p_btn = document.querySelector('.create-paste-btn');
const p_span = document.getElementsByClassName('close')[1];

p_btn.onclick = async function() {
    const text = document.getElementById('paste-content').value;
    if (!text.trim()) {
        alert('Please enter some content before creating a paste.');
        return;
    };
    await createPaste(text);
  };

p_span.onclick = function() {
  p_modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    p_modal.style.display = "none";
  }
}



