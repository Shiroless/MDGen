<script setup lang="ts">
import { ref, nextTick } from 'vue'

const props = defineProps<{
  markdownContent: string
}>()

const emit = defineEmits(['update:markdown'])

const messages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])
const userMessage = ref('')
const isTyping = ref(false)

const sendMessage = async () => {
  if (!userMessage.value.trim()) return

  // Add user message
  messages.value.push({ role: 'user', content: userMessage.value })
  const prompt = userMessage.value
  userMessage.value = ''
  isTyping.value = true

  // Simulate LLM delay and streaming
  setTimeout(() => {
    isTyping.value = false
    const response = `Excelente. Voy a ayudarte a estructurar un módulo completo sobre ${prompt}. Comencemos con los temas principales:

**Contenidos Propuestos**
1. **Conceptos Fundamentales**
   * ¿Qué es ${prompt}?
   * Diferencia entre AI, ML y Deep Learning
   * Tipos de aprendizaje: supervisado, no supervisado, refuerzo

2. **Algoritmos Básicos**
   * Regresión lineal y logística
   * Árboles de decisión

3. **Evaluación de Modelos**
   * Metrics: Accuracy, Precision, Recall
   * Overfitting vs Underfitting
`

    messages.value.push({ role: 'assistant', content: response })

    // Update Markdown Content (Append)
    const newMarkdown = props.markdownContent + '\n\n' + `## ${prompt}\n` + response
    emit('update:markdown', newMarkdown)
  }, 1500)
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-header">
      <span class="chat-title">Chat con Asistente IA</span>
      <span class="status-badge">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="12"
          height="12"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
          <path d="M12 2v10l4.24-4.24" />
          <circle cx="12" cy="12" r="10" />
        </svg>
        Conectado
      </span>
    </div>

    <div class="messages-area">
      <div v-for="(msg, index) in messages" :key="index" class="message-bubble" :class="msg.role">
        <div v-if="msg.role === 'assistant'" class="message-content">{{ msg.content }}</div>
        <div v-else class="message-content">{{ msg.content }}</div>
      </div>

      <div v-if="isTyping" class="typing-indicator"><span></span><span></span><span></span></div>

      <div v-if="messages.length === 0" class="empty-state">
        <p>Escribe tu idea para comenzar...</p>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="userMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Escribe tu mensaje..."
        class="chat-input"
      />
      <button @click="sendMessage" class="send-btn">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="22" y1="2" x2="11" y2="13" />
          <polygon points="22 2 15 22 11 13 2 9 22 2" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background-color: white;
  overflow: hidden;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #059669; /* Green-600 */
  background-color: #d1fae5; /* Green-100 */
  padding: 4px 12px;
  border-radius: 999px;
}

.messages-area {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-bubble {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 0.875rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-bubble.user {
  align-self: flex-end;
  background-color: #2563eb;
  color: white;
  border-bottom-right-radius: 2px;
}

.message-bubble.assistant {
  align-self: flex-start;
  background-color: #f3f4f6;
  color: #1f2937;
  border-bottom-left-radius: 2px;
}

.typing-indicator {
  align-self: flex-start;
  background-color: #f3f4f6;
  padding: 12px 16px;
  border-radius: 12px;
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: #9ca3af;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}
.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

.input-area {
  padding: 12px;
  background-color: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  font-family: inherit;
  font-size: 0.875rem;
  background-color: #f9fafb;
  transition: border-color 0.2s;
}

.chat-input:focus {
  border-color: #2563eb;
  background-color: white;
}

.send-btn {
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #111827;
  color: white;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: #000;
}
</style>
