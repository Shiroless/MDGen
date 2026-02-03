<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useProjectStore } from '../stores/projectStore'
import ProjectStepper from '../components/project/ProjectStepper.vue'
import CollaborativeChat from '../components/project/CollaborativeChat.vue'
import MarkdownViewer from '../components/project/MarkdownViewer.vue'
import SlidesEditor from '../components/project/SlidesEditor.vue';

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()

// Get project ID from route
const projectId = computed(() => Number(route.params.id))
const project = computed(() => projectStore.getProject(projectId.value))

// Initialize state based on project or fallback
const currentStep = ref(project.value?.stepCurrent || 1)
const markdownContent = ref('') // Ideally also loaded from store if backend existed

// Watch for project changes (in case we navigated from one to another)
watch(project, (newP) => {
  if (newP) {
    currentStep.value = newP.stepCurrent
  }
}, { immediate: true })

const projectTitle = computed(() => {
  return project.value?.title || (route.query.name as string) || 'Proyecto Sin Título'
})

const projectSubtitle = computed(() => {
  return project.value?.description || (route.query.desc as string) || 'Sin descripción'
})

const showUnsavedModal = ref(false)
const hasUnsavedChanges = ref(false)
const showToast = ref(false)

// Init watcher after mount or initial setup to avoid immediate dirty state
watch([currentStep, markdownContent], () => {
  hasUnsavedChanges.value = true
})

const saveChanges = () => {
  // Simulate saving step
  projectStore.updateProject(projectId.value, {
    stepCurrent: currentStep.value
  })
  
  hasUnsavedChanges.value = false
  
  // Show toast
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const goBack = () => {
  if (hasUnsavedChanges.value) {
    showUnsavedModal.value = true
  } else {
    router.push('/')
  }
}

const exitWithoutSaving = () => {
  showUnsavedModal.value = false
  router.push('/')
}

const saveAndExit = () => {
  saveChanges()
  showUnsavedModal.value = false
  router.push('/')
}

const handleNextStep = () => {
  if (currentStep.value < 5) {
    currentStep.value++
  }
}

const handleMarkdownUpdate = (newContent: string) => {
  markdownContent.value = newContent
}
</script>

<template>
  <div class="project-layout">
    <!-- Header -->
    <header class="header">
      <div class="header-left">
        <button class="back-link" @click="goBack">
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
            <path d="M19 12H5" />
            <path d="m12 19-7-7 7-7" />
          </svg>
          Volver
        </button>
        <div class="separator"></div>
        <div class="title-box">
          <h1 class="project-title">{{ projectTitle }}</h1>
          <p class="project-subtitle">{{ projectSubtitle }}</p>
        </div>
      </div>
      <div class="header-right">
        <button class="btn-dark" @click="saveChanges">Guardar Cambios</button>
      </div>
    </header>

    <!-- Stepper -->
    <ProjectStepper :current-step="currentStep" @update:step="(step) => (currentStep = step)" />

    <!-- Step 1 Content -->
    <main v-if="currentStep === 1" class="step-content">
      <div class="step-header">
        <div class="step-icon-box">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <div>
          <h2 class="step-title">Paso 1: Desarrollo Colaborativo con LLM</h2>
          <p class="step-desc">
            Trabaja junto con la IA para desarrollar contenidos detallados. Los contenidos generados
            se guardarán en formato Markdown.
          </p>
        </div>
      </div>

      <div class="workspace-grid">
        <div class="chat-column">
          <CollaborativeChat
            :markdown-content="markdownContent"
            @update:markdown="handleMarkdownUpdate"
          />
        </div>
        <div class="preview-column">
          <MarkdownViewer :content="markdownContent" />
        </div>
      </div>
    </main>

    <!-- Step 2 Content -->
    <main v-else-if="currentStep === 2" class="step-content">
      <SlidesEditor />
    </main>

    <div v-else class="placeholder-step">
      <h2>Paso {{ currentStep }} en construcción</h2>
      <p>Este paso aún no está disponible en esta demostración.</p>
    </div>

    <!-- Footer Navigation (Bottom of page) -->
    <footer class="footer-nav">
      <!-- Left spacer or "Previous Step" button -->
      <div class="nav-left">
        <button v-if="currentStep > 1" class="nav-btn prev" @click="currentStep--">
          ← Paso Anterior
        </button>

        <!-- Specifically for Step 1, user mentioned "Paso Anterior" logic. 
              Prompt: "en este caso solo siguiente paso porque es el paso 1". 
              So I hide Previous button for Step 1. -->
        <button v-else class="nav-btn prev visible-hidden">← Paso Anterior</button>
      </div>

      <button class="nav-btn next" @click="handleNextStep">Siguiente Paso →</button>
    </footer>

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="showToast" class="toast-notification">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <span>Cambios guardados correctamente</span>
      </div>
    </transition>

    <!-- Unsaved Changes Modal -->
    <div v-if="showUnsavedModal" class="modal-overlay">
      <div class="modal-card">
        <h3 class="modal-title">¿Tienes cambios sin guardar?</h3>
        <p class="modal-desc">Si sales ahora, perderás el progreso realizado desde el último guardado.</p>
        <div class="modal-actions">
          <button class="modal-btn cancel" @click="showUnsavedModal = false">Cancelar</button>
          <button class="modal-btn danger" @click="exitWithoutSaving">Salir sin guardar</button>
          <button class="modal-btn confirm" @click="saveAndExit">Guardar y Salir</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.modal-desc {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.modal-btn.cancel {
  background-color: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.modal-btn.cancel:hover {
  background-color: #f3f4f6;
}

.modal-btn.danger {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fee2e2;
}

.modal-btn.danger:hover {
  background-color: #fecaca;
}

.modal-btn.confirm {
  background-color: #000;
  color: white;
}

.modal-btn.confirm:hover {
  opacity: 0.9;
}

/* Toast Styles */
.toast-notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: #10b981; /* Emerald-500 */
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  z-index: 50;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.3s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.project-layout {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #4b5563;
  background: none;
  font-size: 0.875rem;
}

.back-link:hover {
  color: #111827;
}

.separator {
  width: 1px;
  height: 40px;
  background-color: #e5e7eb;
}

.project-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
}

.project-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
}

.header-right {
  display: flex;
  gap: 12px;
}

.btn-outline {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  background-color: white;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.btn-outline:hover {
  background-color: #f9fafb;
}

.btn-dark {
  padding: 8px 16px;
  background-color: #000;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-dark:hover {
  opacity: 0.9;
}

/* Content */
.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.step-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
  background-color: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

.step-icon-box {
  width: 48px;
  height: 48px;
  background-color: #f3e8ff; /* Purple-100 */
  color: #a855f7; /* Purple-600 */
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.step-desc {
  color: #6b7280;
  font-size: 0.9375rem;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  flex: 1;
  min-height: 500px; /* Ensure chat has height */
}

.chat-column,
.preview-column {
  height: 100%;
}

.placeholder-step {
  padding: 48px;
  text-align: center;
  color: #6b7280;
  background-color: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

/* Footer Nav */
.footer-nav {
  margin-top: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.nav-btn.prev {
  background-color: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.nav-btn.prev:hover {
  background-color: #f9fafb;
}

.nav-btn.next {
  background-color: #000;
  color: white;
}

.nav-btn.next:hover {
  opacity: 0.9;
}

.visible-hidden {
  visibility: hidden;
}
</style>
