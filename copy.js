function copyText() {
    var text = document.getElementById("textToCopy").innerText;
  
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
  
    textArea.select();
    document.execCommand("copy");
  
    document.body.removeChild(textArea);
  
    alert("Text copied!");
  }