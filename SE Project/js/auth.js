document.getElementById('loginForm').addEventListener('submit', async e => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    const remember = e.target.remember.checked;
  
    // TODO: Replace with real API call
    console.log('Signing in:', { email, password, remember });
    // Simulate success
    setTimeout(() => {
      window.location.href = 'dashboard.html';
    }, 500);
  });
  
  function oauth(provider) {
    // TODO: Kick off OAuth flow
    alert(`OAuth with ${provider} (not yet implemented)`);
  }

document.getElementById('signupForm').addEventListener('submit', e => {
    e.preventDefault();
    const username = e.target.username.value;
    const email    = e.target.email.value;
    const password = e.target.password.value;
    const confirm  = e.target.confirmPassword.value;
    const remember = e.target.remember.checked;
  
    if (password !== confirm) {
      return alert("Passwords don't match");
    }
    console.log('Signing up:', { username, email, password, remember });
    // simulate success
    setTimeout(() => window.location.href = 'dashboard.html', 500);
  });
  
  