<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  content: string
}>()

// Simple Markdown pseudo-renderer since I can't pull in new dependencies easily without user input.
// Will render as plain text or simple HTML replacement for now.
const renderedContent = computed(() => {
  if (!props.content) return ''

  // Very basic replacements
  let html = props.content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\n\n/gim, '<br><br>')
    .replace(/\* (.*)/gim, '<li>$1</li>')

  return html
})

const downloadMarkdown = () => {
  if (!props.content) return
  const blob = new Blob([props.content], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'generated_content.md'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="md-container">
    <div class="md-header">
      <span class="md-title">Contenido Generado (Markdown)</span>
      <button class="download-btn" @click="downloadMarkdown" :disabled="!content">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
        Descargar MD
      </button>
    </div>

    <div class="md-content">
      <div v-if="!content" class="empty-placeholder">
        <p>El contenido aparecerá aquí...</p>
      </div>
      <div v-else class="markdown-body" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<style scoped>
.md-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background-color: white;
  overflow: hidden;
}

.md-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.md-title {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: white;
  border: 1px solid #e5e7eb;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
}

.download-btn:hover:not(:disabled) {
  background-color: #f9fafb;
  border-color: #d1d5db;
}

.download-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.md-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  font-family: 'Inter', sans-serif; /* Maintain UI font but structured */
}

.empty-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

/* Simple Markdown Styles */
:deep(.markdown-body h1) {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #111827;
}
:deep(.markdown-body h2) {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 24px;
  margin-bottom: 12px;
  color: #1f2937;
}
:deep(.markdown-body p) {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #4b5563;
}
:deep(.markdown-body li) {
  margin-left: 20px;
  list-style-type: disc;
  margin-bottom: 4px;
  color: #4b5563;
}
</style>
