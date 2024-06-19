<template>
  <div class="chatbot-modal" v-if="isChatOpen">
    <div class="chat-header">
      <h1>Chatbot</h1>
    </div>
    <div class="chat-window" ref="chatWindow">
      <div v-for="(message, index) in messages" :key="index" class="message" :class="{'user-message': message.sender === 'User', 'bot-message': message.sender === 'Bot'}">
        <strong>{{ message.sender }}:</strong>
        <span v-if="message.type === 'text'">{{ message.text }}</span>
        <a v-else-if="message.type === 'button'" :href="message.url" target="_blank" class="button-link">{{ message.text }}</a>
        <div v-else-if="message.type === 'form'">
          <EmailForm @emailSent="handleEmailSent" />
        </div>
      </div>
    </div>
    <button @click="toggleFaq" class="faq-button">자주하는 질문</button>
    <FaqForm :sendFAQMessage="sendFAQMessage" v-if="showFaq" @showEmailForm="showEmailForm" />
    <div class="input-container">
      <input v-model="newMessage" placeholder="메시지를 입력하세요" />
      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script>
import FaqForm from '../components/FaqForm.vue';
import EmailForm from '../components/EmailForm.vue';

export default {
  components: {
    FaqForm,
    EmailForm
  },
  data() {
    return {
      isChatOpen: true,
      messages: [
        { sender: 'Bot', text: '안녕하세요, healthy food 챗봇입니다. 무엇을 도와드릴까요?', type: 'text' }
      ],
      newMessage: '',
      showFaq: false,
    };
  },
  methods: {
    closeChat() {
      this.isChatOpen = false;
    },
    toggleFaq() {
      this.showFaq = !this.showFaq;
    },
    async sendMessage() {
      if (this.newMessage.trim() === '') return;
      const userMessage = { sender: 'User', text: this.newMessage, type: 'text' };
      this.messages.push(userMessage);
      this.newMessage = '';
      this.scrollToBottom();

      const response = await fetch('http://127.0.0.1:8000/api/chatbot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage.text })
      });

      const data = await response.json();
      const botMessage = { sender: 'Bot', text: data.reply, type: 'text' };
      this.messages.push(botMessage);
      this.scrollToBottom();
    },
    async sendFAQMessage(question) {
      const userMessage = { sender: 'User', text: question, type: 'text' };
      this.messages.push(userMessage);
      this.scrollToBottom();

      if (question === '나의 주문 내역') {
        const orderHistoryButton = {
          sender: 'Bot',
          text: '나의 주문 내역 확인하기',
          url: 'http://localhost:5173/orderhistory',
          type: 'button'
        };
        this.messages.push(orderHistoryButton);
        this.scrollToBottom();
      }
      if (question === '일반상품 배송조회') {
        const orderHistoryButton = {
          sender: 'Bot',
          text: '배송 조회',
          url: 'http://localhost:5173/#',
          type: 'button'
        };
        this.messages.push(orderHistoryButton);
        this.scrollToBottom();
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/chatbot/faq/');
        const faqData = await response.json();
        const answer = this.findAnswerInFAQ(faqData, question);
        if (answer) {
          const botMessage = { sender: 'Bot', text: answer, type: 'text' };
          this.messages.push(botMessage);
          this.scrollToBottom();
        } 
      } catch (error) {
        console.error('Error fetching or processing FAQ data:', error);
      }
    },
    findAnswerInFAQ(faqData, question) {
      for (const item of faqData) {
        if (item.question === question) {
          return item.answer;
        }
      }
      return null; 
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow;
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    },
    showEmailForm() {
      const botMessage = { sender: 'Bot', type: 'form' };
      this.messages.push(botMessage);
      this.scrollToBottom();
    },
    handleEmailSent(message) {
      this.messages = this.messages.filter(m => m.type !== 'form');
      this.messages.push({ sender: 'Bot', text: message || '문의사항이 접수되었습니다.', type: 'text' });
      this.scrollToBottom();
    }
  },
  updated() {
    this.scrollToBottom();
  }
};
</script>

<style>
.chatbot-modal {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  height: 100%;
  max-height: 600px;
  border: 1px solid #ddd;
  border-radius: 10px;
  position: relative;
}

.chat-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1000;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.2em;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
}

.chat-window {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
  position: relative;
}

.message {
  margin: 5px 0;
  padding: 10px;
  border-radius: 10px;
  word-break: break-word;
}

.user-message {
  background-color: #d1e7dd;
  align-self: flex-end;
  text-align: right;
}

.bot-message {
  background-color: #f8d7da;
  align-self: flex-start;
  text-align: left;
}

.button-link {
  display: inline-block;
  margin-top: 5px;
  padding: 8px 12px;
  background-color: #007BFF;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-link:hover {
  background-color: #0056b3;
}

.faq-button {
  width: 100%;
  padding: 10px;
  background-color: #d6d5e1;
  border: 1px solid #040404;
  border-radius: 5px;
  cursor: pointer;
  box-sizing: border-box;
  position: sticky;
  bottom: 0;
  z-index: 1000;
}

.faq-button:hover {
  background-color: #020101;
  color: white;
}

.input-container {
  display: flex;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border-top: 1px solid #ddd;
  background: white;
  z-index: 1000;
  position: sticky;
  bottom: 0;
}

.input-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px 0 0 5px;
}

.input-container button {
  padding: 10px 20px;
  border: none;
  background-color: #007BFF;
  color: #fff;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.input-container button:hover {
  background-color: #0056b3;
}
</style>
