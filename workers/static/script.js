setInterval( async () => {
  const conversionOutput = document.getElementById('nohup-output');

  try {
    const response = await fetch('/api/log');
    const responseText = await response.json();
    conversionOutput.textContent = responseText;
  } catch (err) {
    console.error(err);
  }
}, 5000);