const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = "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"; // Replace with your actual API key
const inputInitHeight = chatInput.scrollHeight;
let selectionTimeout; // Timeout variable for text selection

// Function to get selected text
function getSelectedText() {
  if (window.getSelection) {
    return window.getSelection().toString();
  } else if (document.selection && document.selection.type != "Control") {
    return document.selection.createRange().text;
  }
  return '';
}

// Function to create chat <li> elements
const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", `${className}`);
  let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
}

// Function to generate chatbot response
const generateResponse = (chatElement, messVar) => {
  // console.log(usrMsg);
  const messageElement = chatElement.querySelector("p");
  const usrMsg = encodeURIComponent(messVar); // Make sure you define yourMessageVariable
  fetch(`/get?usrMsg=${usrMsg}`).then(res => res.text()).then(data => {
    messageElement.textContent = data;
  }).finally(() => {
    chatbox.scrollTo(0, chatbox.scrollHeight);
  });
  // .get("/get", { msg: usrMsg }).done(function (data) {
  //   console.log(rawText);
  //   console.log(data);
  //   // const msgText = data;
  //   messageElement.textContent = data;
  // });

  // fetch("/get", usrMsg)

  // const API_URL = "https://api.openai.com/v1/chat/completions";
  // const messageElement = chatElement.querySelector("p");
  // const requestOptions = {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //     "Authorization": `Bearer ${API_KEY}`
  //   },
  //   body: JSON.stringify({
  //     model: "gpt-3.5-turbo",
  //     messages: [{role: "user", content: userMessage}],
  //   })
  // }
  // fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
  //   messageElement.textContent = data.choices[0].message.content.trim();
  // }).catch(() => {
  //   messageElement.classList.add("error");
  //   messageElement.textContent = "Oops! Something went wrong. Please try again.";
  // }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

// Main function to handle chat
const handleChat = (messageContent = null) => {
  userMessage = messageContent || chatInput.value.trim();
  if (!userMessage) return;
  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);
  setTimeout(() => {
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi, userMessage);
  }, 600);
}

// Adjust the height of the input textarea based on its content
chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Handle chat when Enter is pressed
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

// Send button click handler
sendChatBtn.addEventListener("click", handleChat);

// Close and toggle chatbot listeners
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

// Event listeners for text selection to handle chat
document.onmouseup = document.onkeyup = document.onselectionchange = () => {
  clearTimeout(selectionTimeout);
  selectionTimeout = setTimeout(() => {
    const selectedText = getSelectedText();
    if (selectedText.length > 0) {
      handleChat(selectedText);
      // Optionally clear the selection here
      window.getSelection().removeAllRanges();
    }
  }, 500); // Delay to ensure user has finished selecting text
};
