const key = 'proj-puyqETaxKWFGJeG1TnHIT3BlbkFJvKLHCNIe7aw2465EtNUQ';
const form = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const userInput = document.getElementById('user-input').value;
  const userMessageElement = document.createElement('div');
  userMessageElement.textContent = `You: ${userInput}`;
  chatBox.appendChild(userMessageElement);
  try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
              'Authorization': `Bearer sk-${key}`,
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              model: 'gpt-3.5-turbo',
              messages: [
                {
                  role: 'system',
                  content: 'Ты офис регистратора офиса SDU.обращайся ко всем вопросам как к студенту или преподователю,сначала представься и скажи в чем можешь помочь в студенческой жизни или в вопросах касательно университета. Если вопросы касательно других вещей скажи не могу ответить на этот вопрос,Можешь отвечать только вопросы про университет и расписание студенческой жизни и проблемы студента'
                  
                },
                {
                  role: 'user',
                  content: userInput
                }
              ]
          }),
      });
      
      const data = await response.json();
      
      const botResponseElement = document.createElement('div');
      botResponseElement.textContent = `Chatbot: ${data["choices"][0]["message"]["content"]}`;
      chatBox.appendChild(botResponseElement);
  } catch (error) {
      console.error('Error:', error);
      const errorElement = document.createElement('div');
      errorElement.textContent = 'Error occurred while fetching the chatbot response.';
      chatBox.appendChild(errorElement);
  }
  
  document.getElementById('user-input').value = '';
});
